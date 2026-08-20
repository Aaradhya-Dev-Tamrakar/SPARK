"""
test_train_cnn.py

Unit tests for train_cnn.py utilities:
    1. Data augmentation (temporal shift, sensor scaling, noise jitter)
    2. Model architecture construction (with/without dropout and batchnorm)
    3. Decision threshold tuning (Youden's Index)
    4. Subject-stratified data splitting (no leakage)
    5. Evaluation metric calculation with custom thresholds
"""

import numpy as np
import tensorflow as tf

from training.train_cnn import (
    augment_windows,
    build_model,
    evaluate,
    find_optimal_threshold,
    subject_stratified_split,
)

WINDOW_SAMPLES = 200
CHANNELS = 6


class TestDataAugmentation:
    """Tests for on-the-fly time series data augmentation."""

    def test_augmented_shape_and_dtype(self):
        rng = np.random.default_rng(42)
        windows = rng.standard_normal((10, WINDOW_SAMPLES, CHANNELS)).astype(np.float32)
        aug = augment_windows(windows, rng, max_shift=5, scale_range=0.05, noise_std=0.01)

        assert aug.shape == windows.shape
        assert aug.dtype == np.float32

    def test_augmentation_varies_values(self):
        rng = np.random.default_rng(42)
        windows = np.ones((5, WINDOW_SAMPLES, CHANNELS), dtype=np.float32)
        aug = augment_windows(windows, rng, max_shift=3, scale_range=0.05, noise_std=0.01)

        # Augmented values should not be strictly identical to originals
        assert not np.allclose(aug, windows)


class TestOptimalThresholdTuning:
    """Tests for Youden's J statistic threshold finding."""

    def test_find_optimal_threshold_separable(self):
        y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1])
        # Separable with threshold around 0.40
        y_prob = np.array([0.1, 0.15, 0.2, 0.25, 0.7, 0.8, 0.85, 0.9])
        threshold = find_optimal_threshold(y_true, y_prob)

        assert 0.10 <= threshold <= 0.90
        # Optimal threshold should separate classes
        preds = (y_prob >= threshold).astype(int)
        assert (preds == y_true).all()

    def test_find_optimal_threshold_single_class_fallback(self):
        y_true = np.array([0, 0, 0])
        y_prob = np.array([0.1, 0.2, 0.3])
        threshold = find_optimal_threshold(y_true, y_prob)
        assert threshold == 0.50


class TestModelArchitecture:
    """Tests for CNN construction and regularization layers."""

    def test_build_model_default(self):
        model = build_model(input_shape=(WINDOW_SAMPLES, CHANNELS))
        assert isinstance(model, tf.keras.Model)
        assert model.input_shape == (None, WINDOW_SAMPLES, CHANNELS)
        assert model.output_shape == (None, 2)

    def test_build_model_with_batch_norm(self):
        model = build_model(
            input_shape=(WINDOW_SAMPLES, CHANNELS),
            dropout_rate=0.3,
            use_batch_norm=True,
        )
        layer_names = [layer.name for layer in model.layers]
        assert any("batch_normalization" in name for name in layer_names)
        assert any("dropout" in name for name in layer_names)


class TestSubjectSplit:
    """Tests for leakage-free subject splitting."""

    def test_subject_split_no_leakage(self):
        subjects = np.array([f"S{i:02d}" for i in range(20) for _ in range(5)])
        labels = np.random.randint(0, 2, size=len(subjects))

        train_idx, val_idx, test_idx = subject_stratified_split(subjects, labels, seed=42)

        s_train = set(subjects[train_idx])
        s_val = set(subjects[val_idx])
        s_test = set(subjects[test_idx])

        assert not (s_train & s_val)
        assert not (s_train & s_test)
        assert not (s_val & s_test)
        assert len(train_idx) + len(val_idx) + len(test_idx) == len(subjects)


class TestEvaluationThresholds:
    """Tests for threshold-aware evaluation."""

    def test_evaluate_custom_threshold(self):
        inputs = tf.keras.Input(shape=(WINDOW_SAMPLES, CHANNELS))
        x = tf.keras.layers.GlobalAveragePooling1D()(inputs)
        outputs = tf.keras.layers.Dense(2, activation="softmax")(x)
        model = tf.keras.Model(inputs, outputs)

        X = np.random.standard_normal((20, WINDOW_SAMPLES, CHANNELS)).astype(np.float32)
        y = np.array([0] * 10 + [1] * 10)

        metrics_default = evaluate(model, X, y, threshold=0.50)
        metrics_low = evaluate(model, X, y, threshold=0.10)

        assert metrics_default["threshold"] == 0.50
        assert metrics_low["threshold"] == 0.10
        for m in (metrics_default, metrics_low):
            for k in ("sensitivity", "specificity", "f1", "auc_roc"):
                assert k in m
