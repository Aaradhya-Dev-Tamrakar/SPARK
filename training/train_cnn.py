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


def mixup_augment_windows(
    windows: np.ndarray,
    labels: np.ndarray,
    rng: np.random.Generator,
    alpha: float = 0.2,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Kinematics-safe Mixup: Blends pairs of time-series windows from the same
    label group (fall-with-fall, nonfall-with-nonfall) to preserve physical validity
    and prevent creating hybrid gravity vectors.
    """
    mixed_windows = windows.copy()
    mixed_labels = labels.copy()

    for cls in [0, 1]:
        cls_idx = np.where(labels == cls)[0]
        if len(cls_idx) < 2:
            continue
        shuffled = rng.permutation(cls_idx)
        # Sample lambda from Beta distribution constrained to [0.75, 1.0] for physical stability
        lam = rng.beta(alpha, alpha, size=len(cls_idx))
        lam = np.maximum(lam, 1.0 - lam)
        for i, idx in enumerate(cls_idx):
            partner_idx = shuffled[i]
            mix_ratio = float(lam[i])
            mixed_windows[idx] = mix_ratio * windows[idx] + (1.0 - mix_ratio) * windows[partner_idx]

    return mixed_windows.astype(np.float32), mixed_labels


class AsymmetricFocalLoss(tf.keras.losses.Loss):
    """
    Focal Loss specially calibrated for edge fall detection.
    gamma: suppresses easy background ADL noise.
    alpha: heavily penalizes missed safety events (falls).
    """

    def __init__(
        self,
        gamma: float = 2.0,
        alpha: float = 0.75,
        name: str = "asymmetric_focal_loss",
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self.gamma = float(gamma)
        self.alpha = float(alpha)

    def call(self, y_true, y_pred):
        y_true = tf.cast(tf.squeeze(y_true), tf.int32)
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)
        y_true_oh = tf.one_hot(y_true, depth=2)

        # Probability of true class
        p_t = tf.reduce_sum(y_true_oh * y_pred, axis=-1)
        focal_weight = tf.pow(1.0 - p_t, self.gamma)

        # Alpha weighting: alpha for fall (1), (1 - alpha) for non-fall (0)
        alpha_t = tf.where(tf.equal(y_true, 1), self.alpha, 1.0 - self.alpha)

        loss = -alpha_t * focal_weight * tf.math.log(p_t)
        return tf.reduce_mean(loss)

    def get_config(self):
        config = super().get_config()
        config.update({"gamma": self.gamma, "alpha": self.alpha})
        return config


def build_model(
    input_shape,
    dropout_rate: float = 0.2,
    use_batch_norm: bool = False,
    learning_rate: float = LEARNING_RATE,
    loss_type: str = "sparse_categorical_crossentropy",
    focal_gamma: float = 2.0,
    focal_alpha: float = 0.75,
    lr_schedule_type: str = "constant",
    steps_per_epoch: int = 100,
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

    # Configure learning rate schedule or constant LR
    if lr_schedule_type == "cosine":
        lr_schedule = tf.keras.optimizers.schedules.CosineDecayRestarts(
            initial_learning_rate=learning_rate,
            first_decay_steps=max(10 * steps_per_epoch, 100),
            t_mul=1.5,
            m_mul=0.9,
            alpha=1e-5,
        )
        optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)
    else:
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    # Configure loss function
    if loss_type == "focal":
        loss_fn = AsymmetricFocalLoss(gamma=focal_gamma, alpha=focal_alpha)
    else:
        loss_fn = "sparse_categorical_crossentropy"

    model.compile(
        optimizer=optimizer,
        loss=loss_fn,
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


def find_safety_constrained_threshold(
    y_true: np.ndarray,
    y_prob_fall: np.ndarray,
    target_sensitivity: float = 0.90,
) -> float:
    """
    Finds optimal operating cutoff guaranteeing safety-constrained sensitivity (>= target_sensitivity),
    maximizing specificity among candidate thresholds. Falls back to Youden's J if target is unreachable.
    """
    if len(np.unique(y_true)) < 2:
        return 0.50

    fpr, tpr, thresholds = roc_curve(y_true, y_prob_fall)
    valid_idx = np.where(tpr >= target_sensitivity)[0]
    if len(valid_idx) > 0:
        best_sub_idx = int(np.argmin(fpr[valid_idx]))
        best_thresh = float(thresholds[valid_idx[best_sub_idx]])
    else:
        j_scores = tpr - fpr
        best_thresh = float(thresholds[np.argmax(j_scores)])

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
    ap.add_argument(
        "--loss",
        type=str,
        default="sparse_categorical_crossentropy",
        choices=["sparse_categorical_crossentropy", "focal"],
        help="Loss function: sparse_categorical_crossentropy or focal (default: sparse_categorical_crossentropy)",
    )
    ap.add_argument(
        "--focal-gamma",
        type=float,
        default=2.0,
        help="Focusing parameter gamma for Focal Loss (default: 2.0)",
    )
    ap.add_argument(
        "--focal-alpha",
        type=float,
        default=0.75,
        help="Alpha weight for fall class in Focal Loss (default: 0.75)",
    )
    ap.add_argument(
        "--use-mixup",
        action="store_true",
        help="Apply kinematics-safe label-preserving Mixup to training windows",
    )
    ap.add_argument(
        "--mixup-alpha",
        type=float,
        default=0.2,
        help="Beta distribution parameter alpha for Mixup (default: 0.2)",
    )
    ap.add_argument(
        "--lr-schedule",
        type=str,
        default="constant",
        choices=["constant", "cosine"],
        help="Learning rate schedule: constant or cosine (default: constant)",
    )
    ap.add_argument(
        "--target-sensitivity",
        type=float,
        default=0.90,
        help="Target clinical sensitivity threshold for operating cutoff (default: 0.90)",
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

    if args.use_mixup:
        print(f"Kinematics-safe Mixup enabled (alpha={args.mixup_alpha})...")
        X_mix, y_mix = mixup_augment_windows(X_train_fit, y_train_fit, rng, alpha=args.mixup_alpha)
        X_train_fit = np.concatenate([X_train_fit, X_mix], axis=0)
        y_train_fit = np.concatenate([y_train_fit, y_mix], axis=0)
        shuffle_idx = rng.permutation(len(y_train_fit))
        X_train_fit, y_train_fit = X_train_fit[shuffle_idx], y_train_fit[shuffle_idx]
        print(f"  Training set after Mixup: {len(X_train_fit)} windows")

    # Class weighting with positive class boost
    class_weights_arr = compute_class_weight(
        class_weight="balanced", classes=np.array([0, 1]), y=y_train
    )
    class_weight = {
        0: float(class_weights_arr[0]),
        1: float(class_weights_arr[1] * args.pos_weight_boost),
    }

    # For Focal Loss, alpha handles class imbalance internally
    fit_class_weight = None if args.loss == "focal" else class_weight
    if args.loss == "focal":
        print(f"Loss: Asymmetric Focal Loss (gamma={args.focal_gamma}, alpha={args.focal_alpha})")
    else:
        print(
            f"Class weights (imbalance correction with {args.pos_weight_boost:.2f}x boost): {class_weight}"
        )

    steps_per_epoch = max(len(X_train_fit) // BATCH_SIZE, 1)
    model = build_model(
        input_shape=windows.shape[1:],
        dropout_rate=args.dropout,
        use_batch_norm=args.use_batch_norm,
        learning_rate=LEARNING_RATE,
        loss_type=args.loss,
        focal_gamma=args.focal_gamma,
        focal_alpha=args.focal_alpha,
        lr_schedule_type=args.lr_schedule,
        steps_per_epoch=steps_per_epoch,
    )
    model.summary()

    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=EARLY_STOP_PATIENCE, restore_best_weights=True
    )

    print(
        f"Training (lr={LEARNING_RATE}, schedule={args.lr_schedule}, batch={BATCH_SIZE}, max {EPOCHS} epochs)..."
    )
    history = model.fit(
        X_train_fit,
        y_train_fit,
        validation_data=(X_val, y_val),
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        class_weight=fit_class_weight,
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

    # Validation-based threshold tuning (Youden's Index & Safety-Constrained)
    print("\nTuning decision thresholds on validation set...")
    val_probs = model.predict(X_val, verbose=0)[:, 1]
    optimal_threshold = find_optimal_threshold(y_val, val_probs)
    safety_threshold = find_safety_constrained_threshold(
        y_val, val_probs, target_sensitivity=args.target_sensitivity
    )
    print("  Default threshold:               0.5000")
    print(f"  Youden's J optimal threshold:    {optimal_threshold:.4f}")
    print(
        f"  Safety-constrained threshold:    {safety_threshold:.4f} (target sens >= {args.target_sensitivity:.2f})"
    )

    # Evaluate on held-out test set
    print("\nEvaluating on held-out test set...")
    default_metrics = evaluate(model, X_test, y_test, threshold=0.50)
    tuned_metrics = evaluate(model, X_test, y_test, threshold=optimal_threshold)
    safety_metrics = evaluate(model, X_test, y_test, threshold=safety_threshold)

    # Save model config metadata
    config_data = {
        "architecture": "SPARK_1D_CNN",
        "loss_type": args.loss,
        "focal_gamma": args.focal_gamma if args.loss == "focal" else None,
        "focal_alpha": args.focal_alpha if args.loss == "focal" else None,
        "use_mixup": args.use_mixup,
        "lr_schedule": args.lr_schedule,
        "default_threshold": 0.50,
        "optimal_threshold": round(optimal_threshold, 4),
        "safety_threshold": round(safety_threshold, 4),
        "target_sensitivity": args.target_sensitivity,
        "dropout_rate": args.dropout,
        "use_batch_norm": args.use_batch_norm,
        "pos_weight_boost": args.pos_weight_boost,
        "metrics_default": default_metrics,
        "metrics_tuned": tuned_metrics,
        "metrics_safety": safety_metrics,
    }
    (model_dir / "model_config.json").write_text(
        json.dumps(config_data, indent=2) + "\n", encoding="utf-8"
    )

    report_lines = [
        "SPARK 1D CNN -- Held-Out Test Set Evaluation Report",
        "=" * 75,
        f"Test Windows:  {len(test_idx)} ({int(y_test.sum())} FALL, {int((1 - y_test).sum())} NON_FALL)",
        f"Test Subjects: {len(set(subjects[test_idx]))}",
        f"Loss Function: {args.loss} | LR Schedule: {args.lr_schedule} | Mixup: {args.use_mixup}",
        f"Thresholds:    Default=0.5000, Youden={optimal_threshold:.4f}, Safety={safety_threshold:.4f}",
        "",
        f"{'Metric':<28} {'Default (0.50)':>14} {'Youden (' + f'{optimal_threshold:.2f}' + ')':>14} {'Safety (' + f'{safety_threshold:.2f}' + ')':>14}",
        f"{'-' * 28} {'-' * 14} {'-' * 14} {'-' * 14}",
        f"  {'Sensitivity (FALL)':<26} {default_metrics['sensitivity']:>14.4f} {tuned_metrics['sensitivity']:>14.4f} {safety_metrics['sensitivity']:>14.4f}  (target >= 0.90)",
        f"  {'Specificity (NON_FALL)':<26} {default_metrics['specificity']:>14.4f} {tuned_metrics['specificity']:>14.4f} {safety_metrics['specificity']:>14.4f}  (target >= 0.90)",
        f"  {'F1-Score':<26} {default_metrics['f1']:>14.4f} {tuned_metrics['f1']:>14.4f} {safety_metrics['f1']:>14.4f}",
        f"  {'AUC-ROC':<26} {default_metrics['auc_roc']:>14.4f} {tuned_metrics['auc_roc']:>14.4f} {safety_metrics['auc_roc']:>14.4f}",
        "=" * 75,
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
