"""train_transfer.py -- Partial-Freeze Transfer Learning on Nepal Cohort Dataset.

Freezes pre-trained SisFall Conv1D feature extraction layers and fine-tunes
the dense classification head on the dorsal-wrist Nepal cohort data.
"""

import argparse
import json
import os
import sys

import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    f1_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import GroupShuffleSplit


def create_base_or_load_model(
    base_model_path: str | None = None,
    freeze_conv: bool = True,
) -> tf.keras.Model:
    """Loads a pre-trained Keras model or builds the standard SPARK 1D CNN baseline."""
    if base_model_path and os.path.exists(base_model_path):
        print(f"[TRANSFER] Loading pre-trained model from {base_model_path}")
        model = tf.keras.models.load_model(base_model_path)
    else:
        print("[TRANSFER] Initializing new 1D CNN baseline architecture...")
        inputs = tf.keras.Input(shape=(200, 6), name="imu_input")
        x = tf.keras.layers.Conv1D(32, kernel_size=5, activation="relu", name="conv1d_1")(inputs)
        x = tf.keras.layers.MaxPooling1D(pool_size=2, name="maxpool_1")(x)
        x = tf.keras.layers.Conv1D(64, kernel_size=3, activation="relu", name="conv1d_2")(x)
        x = tf.keras.layers.GlobalAveragePooling1D(name="gap")(x)
        x = tf.keras.layers.Dropout(0.20, name="dropout")(x)
        x = tf.keras.layers.Dense(32, activation="relu", name="dense_head")(x)
        outputs = tf.keras.layers.Dense(2, activation="softmax", name="output_softmax")(x)
        model = tf.keras.Model(inputs=inputs, outputs=outputs, name="spark_1d_cnn")

    if freeze_conv:
        print("[TRANSFER] Freezing Conv1D feature extraction layers...")
        for layer in model.layers:
            if "conv1d" in layer.name.lower():
                layer.trainable = False
                print(f"  - Frozen: {layer.name}")
            else:
                layer.trainable = True
                print(f"  - Trainable: {layer.name}")

    return model


def calibrate_threshold(y_true: np.ndarray, y_probs: np.ndarray) -> tuple[float, float, float]:
    """Finds optimal decision threshold using Youden's J statistic (Sensitivity + Specificity - 1)."""
    fpr, tpr, thresholds = roc_curve(y_true, y_probs)
    j_scores = tpr - fpr
    best_idx = int(np.argmax(j_scores))
    best_thresh = float(thresholds[best_idx])
    best_sens = float(tpr[best_idx])
    best_spec = float(1.0 - fpr[best_idx])
    return best_thresh, best_sens, best_spec


def run_transfer_training(
    data_dir: str,
    base_model_path: str | None = None,
    out_dir: str = "data/processed_nepal/model",
    epochs: int = 30,
    batch_size: int = 32,
    lr: float = 1e-3,
    freeze_conv: bool = True,
) -> dict[str, object]:
    """Executes the transfer learning pipeline on the processed Nepal cohort dataset."""
    os.makedirs(out_dir, exist_ok=True)

    X_path = os.path.join(data_dir, "nepal_windows.npy")
    y_path = os.path.join(data_dir, "nepal_labels.npy")
    s_path = os.path.join(data_dir, "nepal_subjects.npy")

    if not (os.path.exists(X_path) and os.path.exists(y_path)):
        raise FileNotFoundError(
            f"Processed arrays missing in {data_dir}. Run prepare_nepal_cohort.py first."
        )

    X = np.load(X_path)
    y = np.load(y_path)
    subjects = np.load(s_path, allow_pickle=True) if os.path.exists(s_path) else np.arange(len(y))

    print(f"[DATA] Loaded {len(X)} windows from {data_dir}. Fall ratio: {np.mean(y == 1):.2%}")

    # Subject-grouped split if multiple subjects, else stratified random split
    unique_subjs = np.unique(subjects)
    if len(unique_subjs) >= 3:
        gss = GroupShuffleSplit(n_splits=1, train_size=0.75, random_state=42)
        train_idx, val_idx = next(gss.split(X, y, groups=subjects))
    else:
        indices = np.arange(len(X))
        np.random.seed(42)
        np.random.shuffle(indices)
        split_pt = int(0.75 * len(X))
        train_idx, val_idx = indices[:split_pt], indices[split_pt:]

    X_train, y_train = X[train_idx], y[train_idx]
    X_val, y_val = X[val_idx], y[val_idx]

    model = create_base_or_load_model(base_model_path, freeze_conv=freeze_conv)
    optimizer = tf.keras.optimizers.Adam(learning_rate=lr)
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy()

    model.compile(
        optimizer=optimizer,
        loss=loss_fn,
        metrics=["accuracy"],
    )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=8,
            restore_best_weights=True,
        )
    ]

    _ = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1,
    )

    # Evaluate validation metrics and calibrate threshold
    val_preds = model.predict(X_val)
    fall_probs = val_preds[:, 1]
    best_thresh, best_sens, best_spec = calibrate_threshold(y_val, fall_probs)
    auc_roc = float(roc_auc_score(y_val, fall_probs)) if len(np.unique(y_val)) > 1 else 1.0

    y_pred_tuned = (fall_probs >= best_thresh).astype(int)
    f1 = float(f1_score(y_val, y_pred_tuned, zero_division=0))

    saved_model_path = os.path.join(out_dir, "spark_cnn_transfer.keras")
    model.save(saved_model_path)

    config_data = {
        "model_type": "SPARK_1D_CNN_TRANSFER",
        "frozen_conv": freeze_conv,
        "optimal_threshold": round(best_thresh, 4),
        "validation_sensitivity": round(best_sens, 4),
        "validation_specificity": round(best_spec, 4),
        "validation_f1": round(f1, 4),
        "validation_auc_roc": round(auc_roc, 4),
        "train_windows": len(X_train),
        "val_windows": len(X_val),
    }

    with open(os.path.join(out_dir, "model_config_transfer.json"), "w") as f:
        json.dump(config_data, f, indent=2)

    print("\n" + "=" * 70)
    print("TRANSFER LEARNING EVALUATION SUMMARY")
    print(f"Optimal Threshold (Youden's J): {best_thresh:.4f}")
    print(f"Validation Sensitivity:        {best_sens:.2%}")
    print(f"Validation Specificity:        {best_spec:.2%}")
    print(f"Validation F1-Score:           {f1:.4f}")
    print(f"Validation AUC-ROC:            {auc_roc:.4f}")
    print(f"Saved Fine-Tuned Model:        {saved_model_path}")
    print("=" * 70)

    return config_data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SPARK Nepal Cohort Transfer Learning")
    parser.add_argument(
        "--data-dir", type=str, default="data/processed_nepal", help="Processed data directory"
    )
    parser.add_argument(
        "--base-model", type=str, default=None, help="Path to pre-trained base model"
    )
    parser.add_argument(
        "--out-dir", type=str, default="data/processed_nepal/model", help="Output directory"
    )
    parser.add_argument("--epochs", type=int, default=25, help="Max training epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument(
        "--unfreeze-conv", action="store_true", help="Unfreeze Conv1D layers during fine-tuning"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_transfer_training(
        data_dir=args.data_dir,
        base_model_path=args.base_model,
        out_dir=args.out_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        freeze_conv=not args.unfreeze_conv,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
