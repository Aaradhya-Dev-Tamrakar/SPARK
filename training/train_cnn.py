#!/usr/bin/env python3
"""
train_cnn.py

Trains SPARK's Layer-2 1D CNN on SisFall-derived windows, per proposal
main.md sec:cnn_arch / "1D CNN Training".

Architecture (proposal, verbatim):
    Conv1D(32, k=5) -> ReLU -> MaxPool1D(2) ->
    Conv1D(64, k=3) -> ReLU -> GlobalAveragePooling1D ->
    Dense(32, ReLU) -> Dense(2, Softmax)

Output is fixed at 2 classes (Dense(2, Softmax) is stated explicitly,
not inferred) -- this is binary FALL-vs-ADL regardless of the
label-granularity question left open in prepare_sisfall.py. That
script correctly deferred the choice; this architecture spec makes
it. F01-F15 -> class 1 (FALL), D01-D19 -> class 0 (NON_FALL).

NOTE -- known spec inconsistency, not resolved silently: the
proposal's Figure 5.3 caption states the two Conv1D+MaxPool blocks
compress the 200-sample window to a "12-step feature map". Computing
the stated layer sequence with Keras' default 'valid' padding on a
200-sample input actually gives 48 steps, not 12 (196->98->96->48).
GlobalAveragePooling1D right after makes this inconsequential for
correctness -- it collapses whatever length remains to one value per
channel, and Keras infers all shapes automatically -- so this script
runs correctly either way. Flagged here because the proposal text and
its own figure disagree, and that's worth knowing about, not because
it changes what this script does.

Training protocol (proposal, verbatim):
    Adam, lr=1e-3, batch=64, 50 epochs, early stopping (patience=10
    on val_loss), 80/10/10 train/val/test, stratified by subject,
    class weighting for fall/ADL imbalance.

Proposal names subject-stratification for the self-collected KEC
fine-tuning stage specifically. Applied here too, on this SisFall
pretraining stage: prepare_sisfall.py's meta.csv already carries a
real subject ID per window (SA01-23, SE01-15), and the same leakage
concern -- windows from one subject appearing in both train and test
-- applies equally to any subject-labeled dataset. This is this
script's own extension of the stated principle to the earlier stage,
not something the proposal states outright for SisFall.

Evaluation (proposal, verbatim): Sensitivity (Recall, FALL),
Specificity (Recall, NON_FALL), F1, AUC-ROC. Targets: Sensitivity
>= 90%, Specificity >= 90%.

Usage:
    python train_cnn.py --data /path/to/output_dir_from_prepare_sisfall

Where <output_dir> contains windows.npy, labels.npy, meta.csv as
produced by prepare_sisfall.py.

Output:
    <data>/model/spark_cnn.keras   trained Keras model
    <data>/model/history.csv        per-epoch train/val metrics
    <data>/model/test_report.txt    final held-out test metrics
"""

import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    f1_score,
    roc_auc_score,
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
TEST_FRAC = 0.1  # implied by 1 - TRAIN_FRAC - VAL_FRAC, kept explicit for clarity


def load_data(data_dir: Path):
    windows = np.load(data_dir / "windows.npy")  # (N, 200, 6) float32
    labels_raw = np.load(data_dir / "labels.npy")  # (N,) strings e.g. "F03", "D11"

    with open(data_dir / "meta.csv") as fh:
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
    labels_bin = np.where(np.char.startswith(labels_raw, "F"), 1, 0).astype(
        np.int32
    )

    return windows, labels_bin, subjects, labels_raw


def subject_stratified_split(subjects: np.ndarray, labels: np.ndarray, seed: int):
    """
    80/10/10 split with no subject appearing in more than one split
    (GroupShuffleSplit groups by subject). "Stratified by subject"
    per proposal wording is interpreted as grouped-by-subject
    (no-leakage) rather than class-proportion-per-subject, since the
    proposal doesn't further specify and grouping is the standard
    reading of that phrase in this context.
    """
    gss1 = GroupShuffleSplit(
        n_splits=1, train_size=TRAIN_FRAC, random_state=seed
    )
    trainval_idx, test_idx = next(gss1.split(subjects, labels, groups=subjects))

    # Split remaining 20% into 10/10 (i.e. half of the remainder each)
    remaining_subjects = subjects[trainval_idx]
    remaining_labels = labels[trainval_idx]
    val_frac_of_remaining = VAL_FRAC / (TRAIN_FRAC + VAL_FRAC) if (TRAIN_FRAC + VAL_FRAC) else 0
    gss2 = GroupShuffleSplit(
        n_splits=1, train_size=1 - (VAL_FRAC / (1 - TEST_FRAC)), random_state=seed
    )
    train_sub_idx, val_sub_idx = next(
        gss2.split(remaining_subjects, remaining_labels, groups=remaining_subjects)
    )
    train_idx = trainval_idx[train_sub_idx]
    val_idx = trainval_idx[val_sub_idx]

    # Verify no subject leakage across splits -- assert, don't assume.
    train_subj_set = set(subjects[train_idx])
    val_subj_set = set(subjects[val_idx])
    test_subj_set = set(subjects[test_idx])
    assert not (train_subj_set & val_subj_set), "Subject leakage: train/val"
    assert not (train_subj_set & test_subj_set), "Subject leakage: train/test"
    assert not (val_subj_set & test_subj_set), "Subject leakage: val/test"

    return train_idx, val_idx, test_idx


def build_model(input_shape) -> tf.keras.Model:
    """
    Exact architecture per proposal main.md sec:cnn_arch:
    Conv1D(32,k5) -> ReLU -> MaxPool1D(2) -> Conv1D(64,k3) -> ReLU ->
    GlobalAveragePooling1D -> Dense(32,ReLU) -> Dense(2,Softmax).
    """
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=input_shape),
            tf.keras.layers.Conv1D(32, kernel_size=5, activation="relu"),
            tf.keras.layers.MaxPool1D(pool_size=2),
            tf.keras.layers.Conv1D(64, kernel_size=3, activation="relu"),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(2, activation="softmax"),
        ]
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def evaluate(model, X_test, y_test) -> dict:
    y_prob = model.predict(X_test, verbose=0)  # (N, 2)
    y_pred = np.argmax(y_prob, axis=1)
    y_prob_fall = y_prob[:, 1]

    fall_mask = y_test == 1
    nonfall_mask = y_test == 0

    sensitivity = (
        (y_pred[fall_mask] == 1).sum() / fall_mask.sum() if fall_mask.sum() else float("nan")
    )
    specificity = (
        (y_pred[nonfall_mask] == 0).sum() / nonfall_mask.sum()
        if nonfall_mask.sum()
        else float("nan")
    )
    f1 = f1_score(y_test, y_pred)
    try:
        auc_roc = roc_auc_score(y_test, y_prob_fall)
    except ValueError as e:
        # Can happen if a split ends up single-class -- surface it,
        # don't silently report a fabricated AUC.
        auc_roc = float("nan")
        print(f"WARNING: AUC-ROC undefined ({e})", file=sys.stderr)

    return {
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
    args = ap.parse_args()

    for required_file in ("windows.npy", "labels.npy", "meta.csv"):
        if not (args.data / required_file).exists():
            print(
                f"ERROR: {required_file} not found in {args.data} -- "
                f"run prepare_sisfall.py first",
                file=sys.stderr,
            )
            sys.exit(1)

    tf.keras.utils.set_random_seed(args.seed)

    print("Loading data...")
    windows, labels_bin, subjects, labels_raw = load_data(args.data)
    print(f"  {windows.shape[0]} windows, shape {windows.shape[1:]}")
    print(f"  {int(labels_bin.sum())} FALL, {int((1 - labels_bin).sum())} NON_FALL")
    print(f"  {len(set(subjects))} unique subjects")

    print("Splitting (80/10/10, grouped by subject, no leakage)...")
    train_idx, val_idx, test_idx = subject_stratified_split(
        subjects, labels_bin, args.seed
    )
    print(f"  train: {len(train_idx)} windows, {len(set(subjects[train_idx]))} subjects")
    print(f"  val:   {len(val_idx)} windows, {len(set(subjects[val_idx]))} subjects")
    print(f"  test:  {len(test_idx)} windows, {len(set(subjects[test_idx]))} subjects")

    X_train, y_train = windows[train_idx], labels_bin[train_idx]
    X_val, y_val = windows[val_idx], labels_bin[val_idx]
    X_test, y_test = windows[test_idx], labels_bin[test_idx]

    class_weights_arr = compute_class_weight(
        class_weight="balanced", classes=np.array([0, 1]), y=y_train
    )
    class_weight = {0: class_weights_arr[0], 1: class_weights_arr[1]}
    print(f"Class weights (imbalance correction): {class_weight}")

    model = build_model(input_shape=windows.shape[1:])
    model.summary()

    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=EARLY_STOP_PATIENCE, restore_best_weights=True
    )

    print(f"Training (Adam lr={LEARNING_RATE}, batch={BATCH_SIZE}, max {EPOCHS} epochs)...")
    history = model.fit(
        X_train,
        y_train,
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

    with open(model_dir / "history.csv", "w", newline="") as fh:
        fieldnames = list(history.history.keys())
        writer = csv.writer(fh)
        writer.writerow(["epoch"] + fieldnames)
        for epoch_idx in range(len(history.history[fieldnames[0]])):
            writer.writerow(
                [epoch_idx] + [history.history[k][epoch_idx] for k in fieldnames]
            )

    print("Evaluating on held-out test set...")
    metrics = evaluate(model, X_test, y_test)

    report_lines = [
        f"SPARK 1D CNN -- held-out test set evaluation",
        f"Test windows: {len(test_idx)} ({int(y_test.sum())} FALL, {int((1 - y_test).sum())} NON_FALL)",
        f"Test subjects: {len(set(subjects[test_idx]))}",
        "",
        f"Sensitivity (Recall, FALL):     {metrics['sensitivity']:.4f}  (target >= 0.90)",
        f"Specificity (Recall, NON_FALL): {metrics['specificity']:.4f}  (target >= 0.90)",
        f"F1-score:                       {metrics['f1']:.4f}",
        f"AUC-ROC:                        {metrics['auc_roc']:.4f}",
    ]
    report = "\n".join(report_lines)
    print(report)
    (model_dir / "test_report.txt").write_text(report + "\n")

    print(f"\nModel and reports written to {model_dir}")


if __name__ == "__main__":
    main()
