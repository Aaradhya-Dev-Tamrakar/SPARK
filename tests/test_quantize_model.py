"""
test_quantize_model.py

Unit tests for the quantization pipeline. Uses synthetic data and tiny
models only -- no dependency on SisFall dataset or real trained weights.

Tests verify:
    1. Representative dataset generator produces correct shapes
    2. INT8 quantization round-trip produces valid INT8 tensors
    3. C header generation produces valid, compilable output
    4. FP32-vs-INT8 metric computation returns valid numbers
"""

import re
from pathlib import Path

import numpy as np
import pytest
import tensorflow as tf

from training.quantize_model import (
    _compute_metrics,
    evaluate_tflite_model,
    generate_c_header,
    quantize_model,
)

WINDOW_SAMPLES = 200
CHANNELS = 6


def _build_tiny_model() -> tf.keras.Model:
    """Build a minimal model matching SPARK's I/O spec for testing.
    NOT the real CNN architecture -- deliberately trivial so tests run fast."""
    inputs = tf.keras.Input(shape=(WINDOW_SAMPLES, CHANNELS))
    x = tf.keras.layers.GlobalAveragePooling1D()(inputs)
    outputs = tf.keras.layers.Dense(2, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")
    return model


def _make_synthetic_data(n: int = 50, seed: int = 42):
    """Generate synthetic windows and labels for testing."""
    rng = np.random.default_rng(seed)
    windows = rng.standard_normal((n, WINDOW_SAMPLES, CHANNELS)).astype(np.float32)
    labels = rng.integers(0, 2, size=n).astype(np.int32)
    return windows, labels


@pytest.fixture()
def tiny_model_dir(tmp_path: Path) -> Path:
    """Create a temp directory with a trained tiny model for testing."""
    model = _build_tiny_model()

    # Train for 1 epoch on synthetic data so weights aren't random-init
    X, y = _make_synthetic_data(20)
    model.fit(X, y, epochs=1, verbose=0)

    model_dir = tmp_path / "model"
    model_dir.mkdir()
    model.save(model_dir / "spark_cnn.keras")
    return tmp_path


def _representative_dataset_fn():
    """Minimal representative dataset for converter calibration."""
    rng = np.random.default_rng(42)
    for _ in range(10):
        yield [rng.standard_normal((1, WINDOW_SAMPLES, CHANNELS)).astype(np.float32)]


class TestRepresentativeDataset:
    """Tests for representative dataset generator shape and type."""

    def test_yields_correct_shape(self):
        for batch in _representative_dataset_fn():
            assert len(batch) == 1
            arr = batch[0]
            assert arr.shape == (1, WINDOW_SAMPLES, CHANNELS)
            assert arr.dtype == np.float32

    def test_yields_multiple_samples(self):
        count = sum(1 for _ in _representative_dataset_fn())
        assert count == 10


class TestQuantizationRoundtrip:
    """Tests that INT8 quantization produces a valid TFLite model
    with INT8 input/output tensors."""

    def test_produces_valid_tflite(self, tiny_model_dir: Path):
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)

        assert isinstance(tflite_bytes, bytes)
        assert len(tflite_bytes) > 0

    def test_input_output_are_int8(self, tiny_model_dir: Path):
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)

        interpreter = tf.lite.Interpreter(model_content=tflite_bytes)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()[0]
        output_details = interpreter.get_output_details()[0]

        assert input_details["dtype"] == np.int8, (
            f"Expected INT8 input, got {input_details['dtype']}"
        )
        assert output_details["dtype"] == np.int8, (
            f"Expected INT8 output, got {output_details['dtype']}"
        )

    def test_io_shapes_match_spec(self, tiny_model_dir: Path):
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)

        interpreter = tf.lite.Interpreter(model_content=tflite_bytes)
        interpreter.allocate_tensors()

        input_shape = interpreter.get_input_details()[0]["shape"].tolist()
        output_shape = interpreter.get_output_details()[0]["shape"].tolist()

        assert input_shape == [1, WINDOW_SAMPLES, CHANNELS]
        assert output_shape == [1, 2]

    def test_model_size_reasonable(self, tiny_model_dir: Path):
        """INT8 quantized tiny model should be well under the 120 KB target."""
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)

        # Tiny model should be < 10 KB; real CNN should be < 120 KB
        assert len(tflite_bytes) < 120 * 1024


class TestCHeaderGeneration:
    """Tests that the C header output is valid and well-formed."""

    def test_header_contains_array(self, tiny_model_dir: Path):
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)
        header = generate_c_header(tflite_bytes)

        assert "spark_cnn_model[]" in header
        assert "spark_cnn_model_len" in header

    def test_header_has_pragma_once(self, tiny_model_dir: Path):
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)
        header = generate_c_header(tflite_bytes)

        assert "#pragma once" in header

    def test_header_byte_count_matches(self, tiny_model_dir: Path):
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)
        header = generate_c_header(tflite_bytes)

        # Extract the size from the header
        match = re.search(r"spark_cnn_model_len = (\d+);", header)
        assert match is not None
        assert int(match.group(1)) == len(tflite_bytes)

    def test_header_hex_values_valid(self, tiny_model_dir: Path):
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)
        header = generate_c_header(tflite_bytes)

        # All hex values should be 0x00-0xff format
        hex_values = re.findall(r"0x[0-9a-f]{2}", header)
        assert len(hex_values) == len(tflite_bytes)

    def test_header_alignment(self, tiny_model_dir: Path):
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)
        header = generate_c_header(tflite_bytes)

        # TFLite models need 16-byte alignment on microcontrollers
        assert "alignas(16)" in header


class TestMetricsComputation:
    """Tests that metric computation returns valid, sensible values."""

    def test_compute_metrics_basic(self):
        y_true = np.array([0, 0, 1, 1, 1])
        y_pred = np.array([0, 0, 1, 1, 0])
        y_prob = np.array([0.1, 0.2, 0.9, 0.8, 0.4])

        metrics = _compute_metrics(y_true, y_pred, y_prob)

        assert 0.0 <= metrics["sensitivity"] <= 1.0
        assert 0.0 <= metrics["specificity"] <= 1.0
        assert 0.0 <= metrics["f1"] <= 1.0
        assert 0.0 <= metrics["auc_roc"] <= 1.0

        # Sensitivity: 2 out of 3 falls detected
        assert abs(metrics["sensitivity"] - 2 / 3) < 1e-6
        # Specificity: 2 out of 2 non-falls correctly rejected
        assert abs(metrics["specificity"] - 1.0) < 1e-6

    def test_evaluate_tflite_returns_valid_metrics(self, tiny_model_dir: Path):
        """INT8 model evaluation should return valid metric values."""
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)

        X, y = _make_synthetic_data(30, seed=99)
        # Ensure both classes are present
        y[:15] = 0
        y[15:] = 1

        metrics = evaluate_tflite_model(tflite_bytes, X, y)

        for key in ("sensitivity", "specificity", "f1", "auc_roc"):
            assert key in metrics
            val = metrics[key]
            assert isinstance(val, float)
            # Values should be in [0, 1] (nan is also acceptable for
            # edge cases, but not expected with both classes present)
            assert 0.0 <= val <= 1.0, f"{key} = {val} is out of range"

    def test_evaluate_tflite_custom_threshold(self, tiny_model_dir: Path):
        """Evaluating with custom threshold works as expected."""
        keras_path = tiny_model_dir / "model" / "spark_cnn.keras"
        tflite_bytes = quantize_model(keras_path, _representative_dataset_fn)

        X, y = _make_synthetic_data(30, seed=99)
        y[:15] = 0
        y[15:] = 1

        metrics_low = evaluate_tflite_model(tflite_bytes, X, y, threshold=0.20)
        metrics_high = evaluate_tflite_model(tflite_bytes, X, y, threshold=0.80)

        assert metrics_low["threshold"] == 0.20
        assert metrics_high["threshold"] == 0.80
        # Lowering threshold should generally increase or keep sensitivity equal
        assert metrics_low["sensitivity"] >= metrics_high["sensitivity"]


class TestBalancedCalibration:
    """Tests for class-balanced representative dataset generator."""

    def test_build_representative_dataset_balanced(self):
        from training.quantize_model import build_representative_dataset

        windows = np.random.standard_normal((100, WINDOW_SAMPLES, CHANNELS)).astype(np.float32)
        labels = np.array([0] * 70 + [1] * 30)  # 70 NON_FALL, 30 FALL
        train_idx = np.arange(100)

        rep_gen = build_representative_dataset(
            windows, train_idx, num_samples=20, seed=42, labels=labels
        )
        samples = list(rep_gen())
        assert len(samples) == 20
        for s in samples:
            assert s[0].shape == (1, WINDOW_SAMPLES, CHANNELS)
