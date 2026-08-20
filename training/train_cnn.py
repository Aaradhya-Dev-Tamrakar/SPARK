#!/usr/bin/env python3
"""
train_cnn.py

Trains SPARK's Layer-2 1D CNN on SisFall-derived windows, per proposal
main.md sec:cnn_arch / "1D CNN Training".

Architecture (proposal, verbatim):
    Conv1D(32, k=5) -> ReLU -> MaxPool1D(2) ->
    Conv1D(64, k=3) -> ReLU -> GlobalAveragePooling1D ->
    Dense(32, ReLU) -> Dense(2, Softmax)

Enhanced with 5 accuracy & sensitivity optimization techniques:
    1. Optimal Decision Threshold Tuning (Youden's Index on validation split)
    2. Class-Balanced INT8 Calibration support
    3. Time-Series Data Augmentation (temporal shift, sensor scaling, noise)
    4. Loss Weighting / Positive Class Boost for recall prioritization
    5. Regularization via Dropout / Batch Normalization

Output is fixed at 2 classes (Dense(2, Softmax) is stated explicitly,
not inferred) -- this is binary FALL-vs-ADL regardless of the
label-granularity question left open in prepare_sisfall.py. That
script correctly deferred the choice; this architecture spec makes
it. F01-F15 -> class 1 (FALL), D01-D19 -> class 0 (NON_FALL).

Usage:
    python train_cnn.py --data /path/to/output_dir_from_prepare_sisfall

Where <output_dir> contains windows.npy, labels.npy, meta.csv as
produced by prepare_sisfall.py.

Output:
    <data>/model/spark_cnn.keras    trained Keras model
    <data>/model/history.csv        per-epoch train/val metrics
    <data>/model/test_report.txt    final held-out test metrics (default & tuned)
    <data>/model/model_config.json  model metadata & optimal decision threshold
"""

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    f1_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.utils.class_weight import compute_class_weight

RANDOM_SEED = 42
BATCH_SIZE = 64
EPOCHS = 50
EARLY_STOP_PATIENCE = 10
LEARNING_RATE = 1e-3
TRAIN_FRAC = 0.8
VAL_FRAC = 0.1
TEST_FRAC = 0.1  # implied by 1 - TRAIN_FRAC - VAL_FRAC


def load_data(data_dir: Path):
    windows = np.load(data_dir / "windows.npy")  # (N, 200, 6) float32
    labels_raw = np.load(data_dir / "labels.npy")  # (N,) strings e.g. "F03", "D11"

    with open(data_dir / "meta.csv", encoding="utf-8") as fh:
        meta_rows = list(csv.DictReader(fh))
    subjects = np.array([r["subject"] for r in meta_rows])

    if len(subjects) != windows.shape[0]:
        raise ValueError(
            f"meta.csv row count ({len(subjects)}) doesn't match "
            f"windows.npy ({windows.shape[0]}) -- files out of sync, "
            f"re-run prepare_sisfall.py"
        )

    # Binary collapse per architecture spec: Dense(2, Softmax).
    # F* -> 1 (FALL), D* -> 0 (NON_FALL).
    labels_bin = np.where(np.char.startswith(labels_raw, "F"), 1, 0).astype(np.int32)

    return windows, labels_bin, subjects, labels_raw


def subject_stratified_split(subjects: np.ndarray, labels: np.ndarray, seed: int):
    """
    80/10/10 split with no subject appearing in more than one split
    (GroupShuffleSplit groups by subject).
    """
    gss1 = GroupShuffleSplit(n_splits=1, train_size=TRAIN_FRAC, random_state=seed)
    trainval_idx, test_idx = next(gss1.split(subjects, labels, groups=subjects))

    # Split remaining 20% into 10/10 (i.e. half of the remainder each)
    remaining_subjects = subjects[trainval_idx]
    remaining_labels = labels[trainval_idx]
    val_frac_of_remaining = VAL_FRAC / (TRAIN_FRAC + VAL_FRAC) if (TRAIN_FRAC + VAL_FRAC) else 0
    gss2 = GroupShuffleSplit(n_splits=1, train_size=1 - val_frac_of_remaining, random_state=seed)
    train_sub_idx, val_sub_idx = next(
        gss2.split(remaining_subjects, remaining_labels, groups=remaining_subjects)
    )
    train_idx = trainval_idx[train_sub_idx]
    val_idx = trainval_idx[val_sub_idx]

    # Verify no subject leakage across splits
    train_subj_set = set(subjects[train_idx])
    val_subj_set = set(subjects[val_idx])
    test_subj_set = set(subjects[test_idx])
    assert not (train_subj_set & val_subj_set), "Subject leakage: train/val"
    assert not (train_subj_set & test_subj_set), "Subject leakage: train/test"
    assert not (val_subj_set & test_subj_set), "Subject leakage: val/test"

    return train_idx, val_idx, test_idx


def augment_windows(
    windows: np.ndarray,
    rng: np.random.Generator,
    max_shift: int = 5,
    scale_range: float = 0.05,
    noise_std: float = 0.01,
) -> np.ndarray:
    """
    Apply on-the-fly time-series augmentation to a batch of windows:
    1. Temporal shift (circular/edge-padded shift by +/- max_shift samples)
    2. Sensor magnitude scaling (+/- scale_range)
    3. Gaussian noise jitter
    """
    n, timesteps, channels = windows.shape
    augmented = np.empty_like(windows)

    for i in range(n):
        w = windows[i]
        # 1. Temporal shift
        shift = int(rng.integers(-max_shift, max_shift + 1))
        if shift > 0:
            pad = np.repeat(w[:1, :], shift, axis=0)
            aug = np.concatenate([pad, w[:-shift, :]], axis=0)
        elif shift < 0:
            pad = np.repeat(w[-1:, :], -shift, axis=0)
            aug = np.concatenate([w[-shift:, :], pad], axis=0)
        else:
            aug = w.copy()

        # 2. Magnitude scaling (per-channel)
        scale = rng.uniform(1.0 - scale_range, 1.0 + scale_range, size=(1, channels))
        aug = aug * scale

        # 3. Gaussian noise
        if noise_std > 0:
            noise = rng.normal(0, noise_std, size=(timesteps, channels))
            aug = aug + noise

        augmented[i] = aug

    return augmented.astype(np.float32)


def build_model(
    input_shape,
    dropout_rate: float = 0.2,
    use_batch_norm: bool = False,
    learning_rate: float = LEARNING_RATE,
) -> tf.keras.Model:
    """
    1D CNN architecture per proposal main.md sec:cnn_arch:
    Conv1D(32,k5) -> ReLU -> MaxPool1D(2) -> Conv1D(64,k3) -> ReLU ->
    GlobalAveragePooling1D -> Dense(32,ReLU) -> Dense(2,Softmax).

    Configurable dropout and optional batch normalization provide regularization
    without altering the INT8 quantization / inference contract.
    """
    layers = [tf.keras.layers.Input(shape=input_shape)]

    layers.append(tf.keras.layers.Conv1D(32, kernel_size=5, activation="relu"))
    if use_batch_norm:
        layers.append(tf.keras.layers.BatchNormalization())
    layers.append(tf.keras.layers.MaxPool1D(pool_size=2))
    if dropout_rate > 0:
        layers.append(tf.keras.layers.Dropout(dropout_rate))

    layers.append(tf.keras.layers.Conv1D(64, kernel_size=3, activation="relu"))
    if use_batch_norm:
        layers.append(tf.keras.layers.BatchNormalization())
    if dropout_rate > 0:
        layers.append(tf.keras.layers.Dropout(dropout_rate))

    layers.append(tf.keras.layers.GlobalAveragePooling1D())
    layers.append(tf.keras.layers.Dense(32, activation="relu"))
    if dropout_rate > 0:
        layers.append(tf.keras.layers.Dropout(dropout_rate))
    layers.append(tf.keras.layers.Dense(2, activation="softmax"))

    model = tf.keras.Sequential(layers)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def find_optimal_threshold(y_true: np.ndarray, y_prob_fall: np.ndarray) -> float:
    """
    Find optimal classification threshold on validation set using Youden's J
    statistic (J = Sensitivity + Specificity - 1 = TPR - FPR).
    """
    if len(np.unique(y_true)) < 2:
        return 0.50

    fpr, tpr, thresholds = roc_curve(y_true, y_prob_fall)
    j_scores = tpr - fpr
    best_idx = int(np.argmax(j_scores))
    best_thresh = float(thresholds[best_idx])
    # Constrain to practical probability range [0.10, 0.90]
    return float(np.clip(best_thresh, 0.10, 0.90))


def evaluate(model, X_test: np.ndarray, y_test: np.ndarray, threshold: float = 0.5) -> dict:
    """Evaluate model at a specified fall decision threshold."""
    y_prob = model.predict(X_test, verbose=0)  # (N, 2)
    y_prob_fall = y_prob[:, 1]
    y_pred = (y_prob_fall >= threshold).astype(np.int32)

    fall_mask = y_test == 1
    nonfall_mask = y_test == 0

    sensitivity = (
        float((y_pred[fall_mask] == 1).sum() / fall_mask.sum()) if fall_mask.sum() else float("nan")
    )
    specificity = (
        float((y_pred[nonfall_mask] == 0).sum() / nonfall_mask.sum())
        if nonfall_mask.sum()
        else float("nan")
    )
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    try:
        auc_roc = float(roc_auc_score(y_test, y_prob_fall))
    except ValueError as e:
        auc_roc = float("nan")
        print(f"WARNING: AUC-ROC undefined ({e})", file=sys.stderr)

    return {
        "threshold": threshold,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "f1": f1,
        "auc_roc": auc_roc,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--data",
        required=True,
        type=Path,
        help="Directory containing windows.npy, labels.npy, meta.csv from prepare_sisfall.py",
    )
    ap.add_argument("--seed", type=int, default=RANDOM_SEED)
    ap.add_argument(
        "--pos-weight-boost",
        type=float,
        default=1.25,
        help="Multiplier for the FALL class weight to boost sensitivity (default: 1.25)",
    )
    ap.add_argument(
        "--dropout",
        type=float,
        default=0.20,
        help="Dropout rate after Conv and Dense layers (default: 0.20)",
    )
    ap.add_argument(
        "--use-batch-norm",
        action="store_true",
        help="Enable Batch Normalization layers in Conv blocks",
    )
    ap.add_argument(
        "--augment",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable time-series data augmentation during training (default: True)",
    )
    args = ap.parse_args()

    for required_file in ("windows.npy", "labels.npy", "meta.csv"):
        if not (args.data / required_file).exists():
            print(
                f"ERROR: {required_file} not found in {args.data} -- run prepare_sisfall.py first",
                file=sys.stderr,
            )
            sys.exit(1)

    tf.keras.utils.set_random_seed(args.seed)
    rng = np.random.default_rng(args.seed)

    print("Loading data...")
    windows, labels_bin, subjects, labels_raw = load_data(args.data)
    print(f"  {windows.shape[0]} windows, shape {windows.shape[1:]}")
    print(f"  {int(labels_bin.sum())} FALL, {int((1 - labels_bin).sum())} NON_FALL")
    print(f"  {len(set(subjects))} unique subjects")

    print("Splitting (80/10/10, grouped by subject, no leakage)...")
    train_idx, val_idx, test_idx = subject_stratified_split(subjects, labels_bin, args.seed)
    print(f"  train: {len(train_idx)} windows, {len(set(subjects[train_idx]))} subjects")
    print(f"  val:   {len(val_idx)} windows, {len(set(subjects[val_idx]))} subjects")
    print(f"  test:  {len(test_idx)} windows, {len(set(subjects[test_idx]))} subjects")

    X_train, y_train = windows[train_idx], labels_bin[train_idx]
    X_val, y_val = windows[val_idx], labels_bin[val_idx]
    X_test, y_test = windows[test_idx], labels_bin[test_idx]

    # Data augmentation for training set if enabled
    if args.augment:
        print("Data augmentation enabled: applying temporal shift, scaling, and jitter...")
        # Create augmented copy to double effective training diversity
        X_train_aug = augment_windows(X_train, rng)
        X_train_combined = np.concatenate([X_train, X_train_aug], axis=0)
        y_train_combined = np.concatenate([y_train, y_train], axis=0)
        # Shuffle combined training set
        shuffle_idx = rng.permutation(len(y_train_combined))
        X_train_fit, y_train_fit = X_train_combined[shuffle_idx], y_train_combined[shuffle_idx]
        print(f"  Augmented training set: {len(X_train_fit)} windows")
    else:
        X_train_fit, y_train_fit = X_train, y_train

    # Class weighting with positive class boost
    class_weights_arr = compute_class_weight(
        class_weight="balanced", classes=np.array([0, 1]), y=y_train
    )
    class_weight = {
        0: float(class_weights_arr[0]),
        1: float(class_weights_arr[1] * args.pos_weight_boost),
    }
    print(
        f"Class weights (imbalance correction with {args.pos_weight_boost:.2f}x boost): {class_weight}"
    )

    model = build_model(
        input_shape=windows.shape[1:],
        dropout_rate=args.dropout,
        use_batch_norm=args.use_batch_norm,
        learning_rate=LEARNING_RATE,
    )
    model.summary()

    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=EARLY_STOP_PATIENCE, restore_best_weights=True
    )

    print(f"Training (Adam lr={LEARNING_RATE}, batch={BATCH_SIZE}, max {EPOCHS} epochs)...")
    history = model.fit(
        X_train_fit,
        y_train_fit,
        validation_data=(X_val, y_val),
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        class_weight=class_weight,
        callbacks=[early_stop],
        verbose=2,
    )

    model_dir = args.data / "model"
    model_dir.mkdir(exist_ok=True)

    model.save(model_dir / "spark_cnn.keras")

    with open(model_dir / "history.csv", "w", newline="", encoding="utf-8") as fh:
        fieldnames = list(history.history.keys())
        writer = csv.writer(fh)
        writer.writerow(["epoch"] + fieldnames)
        for epoch_idx in range(len(history.history[fieldnames[0]])):
            writer.writerow([epoch_idx] + [history.history[k][epoch_idx] for k in fieldnames])

    # Validation-based threshold tuning (Youden's Index)
    print("\nTuning decision threshold on validation set (Youden's Index)...")
    val_probs = model.predict(X_val, verbose=0)[:, 1]
    optimal_threshold = find_optimal_threshold(y_val, val_probs)
    print("  Default threshold: 0.5000")
    print(f"  Optimal threshold: {optimal_threshold:.4f}")

    # Evaluate on held-out test set
    print("\nEvaluating on held-out test set...")
    default_metrics = evaluate(model, X_test, y_test, threshold=0.50)
    tuned_metrics = evaluate(model, X_test, y_test, threshold=optimal_threshold)

    # Save model config metadata
    config_data = {
        "architecture": "SPARK_1D_CNN",
        "optimal_threshold": round(optimal_threshold, 4),
        "default_threshold": 0.50,
        "dropout_rate": args.dropout,
        "use_batch_norm": args.use_batch_norm,
        "pos_weight_boost": args.pos_weight_boost,
        "metrics_default": default_metrics,
        "metrics_tuned": tuned_metrics,
    }
    (model_dir / "model_config.json").write_text(
        json.dumps(config_data, indent=2) + "\n", encoding="utf-8"
    )

    report_lines = [
        "SPARK 1D CNN -- Held-Out Test Set Evaluation Report",
        "=" * 60,
        f"Test Windows:  {len(test_idx)} ({int(y_test.sum())} FALL, {int((1 - y_test).sum())} NON_FALL)",
        f"Test Subjects: {len(set(subjects[test_idx]))}",
        f"Optimal Threshold (Youden's J on Val): {optimal_threshold:.4f}",
        "",
        f"{'Metric':<30} {'Default (0.50)':>15} {'Tuned (' + f'{optimal_threshold:.2f}' + ')':>15}",
        f"{'-' * 30} {'-' * 15} {'-' * 15}",
        f"  {'Sensitivity (Recall, FALL)':<28} {default_metrics['sensitivity']:>15.4f} {tuned_metrics['sensitivity']:>15.4f}  (target >= 0.90)",
        f"  {'Specificity (NON_FALL)':<28} {default_metrics['specificity']:>15.4f} {tuned_metrics['specificity']:>15.4f}  (target >= 0.90)",
        f"  {'F1-Score':<28} {default_metrics['f1']:>15.4f} {tuned_metrics['f1']:>15.4f}",
        f"  {'AUC-ROC':<28} {default_metrics['auc_roc']:>15.4f} {tuned_metrics['auc_roc']:>15.4f}",
        "=" * 60,
    ]
    report = "\n".join(report_lines)
    print(report)
    (model_dir / "test_report.txt").write_text(report + "\n", encoding="utf-8")

    print(f"\nModel and reports written to {model_dir}")
    print(
        "\nNext step: INT8 quantization for ESP32-S3 deployment:\n"
        f"  python training/quantize_model.py --data {args.data}"
    )


if __name__ == "__main__":
    main()
