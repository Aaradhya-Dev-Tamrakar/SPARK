#!/usr/bin/env python3
"""
make_placeholder_model.py

Generates a placeholder .tflite for compile/interface testing of
tflite/inference.h against a real FlatBuffer -- NOT a trained model.
Untrained random weights, tiny single-Dense architecture. Only exists to
give the TFLite Micro stub something real to load-check against; it is
not the Stage 3 CNN (train_cnn.py owns that) and produces meaningless
predictions.

I/O shape matches the locked spec (train_cnn.py Stage 3 / §2.4):
    Input:  (1, 200, 6) float32 -- 200-sample window, 6 channels
    Output: (1, 2) float32 Softmax -- [P(NON_FALL), P(FALL)]

Output .tflite is gitignored by repo convention (*.tflite, except
training/models/) -- run this locally to regenerate, don't commit the
binary. Placed at firmware/main/models/spark_placeholder.tflite.

Usage:
    python tools/make_placeholder_model.py
"""

from pathlib import Path

import numpy as np
import tensorflow as tf

WINDOW_SAMPLES = 200
CHANNELS = 6
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "main" / "models" / "spark_placeholder.tflite"


def build_placeholder_model() -> tf.keras.Model:
    """Minimal model with the locked I/O shape. Architecture is NOT
    train_cnn.py's Conv1D/Conv1D/Dense stack -- deliberately trivial
    (Flatten -> Dense(2, softmax)) since this only needs to be a valid,
    loadable FlatBuffer for the stub, not a fall detector."""
    inputs = tf.keras.Input(shape=(WINDOW_SAMPLES, CHANNELS), name="imu_window")
    x = tf.keras.layers.Flatten()(inputs)
    outputs = tf.keras.layers.Dense(2, activation="softmax", name="fall_prob")(x)
    return tf.keras.Model(inputs, outputs, name="spark_placeholder")


def representative_dataset():
    rng = np.random.default_rng(seed=42)
    for _ in range(10):
        yield [rng.uniform(-2.0, 2.0, size=(1, WINDOW_SAMPLES, CHANNELS)).astype(np.float32)]


def main() -> None:
    model = build_placeholder_model()

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    # Float32 (not INT8) -- placeholder is for interface/load testing only;
    # real quantization recipe is Action #3 (open, TBD) and belongs to the
    # actual trained model from train_cnn.py, not this stub.
    tflite_model = converter.convert()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(tflite_model)
    print(f"Wrote placeholder model: {OUTPUT_PATH} ({len(tflite_model)} bytes)")


if __name__ == "__main__":
    main()
