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
    AsymmetricFocalLoss,
    augment_windows,
    build_model,
    evaluate,
    find_optimal_threshold,
    find_safety_constrained_threshold,
    mixup_augment_windows,
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


class TestAsymmetricFocalLoss:
    """Tests for AsymmetricFocalLoss numerical properties."""

    def test_focal_loss_computes_finite_tensor(self):
        loss_fn = AsymmetricFocalLoss(gamma=2.0, alpha=0.75)
        y_true = tf.constant([0, 1, 1, 0], dtype=tf.int32)
        y_pred = tf.constant([[0.9, 0.1], [0.2, 0.8], [0.8, 0.2], [0.95, 0.05]], dtype=tf.float32)
        val = loss_fn(y_true, y_pred)
        assert np.isfinite(val.numpy())
        assert val.numpy() > 0.0

    def test_focal_loss_penalizes_false_negatives_heavier(self):
        loss_fn = AsymmetricFocalLoss(gamma=2.0, alpha=0.75)
        # Missed fall: true=1, pred=[0.9, 0.1]
        loss_fn_miss = loss_fn(tf.constant([1]), tf.constant([[0.9, 0.1]]))
        # False alarm: true=0, pred=[0.1, 0.9]
        loss_fp_alarm = loss_fn(tf.constant([0]), tf.constant([[0.1, 0.9]]))

        # Because alpha=0.75 (3x weighting on positive class), missed fall has much higher loss
        assert loss_fn_miss.numpy() > loss_fp_alarm.numpy()

    def test_focal_loss_config_serialization(self):
        loss_fn = AsymmetricFocalLoss(gamma=2.5, alpha=0.80)
        cfg = loss_fn.get_config()
        assert cfg["gamma"] == 2.5
        assert cfg["alpha"] == 0.80


class TestMixupAugmentation:
    """Tests for kinematics-safe same-label Mixup."""

    def test_mixup_shape_and_dtype(self):
        rng = np.random.default_rng(42)
        X = rng.standard_normal((10, WINDOW_SAMPLES, CHANNELS)).astype(np.float32)
        y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

        X_mix, y_mix = mixup_augment_windows(X, y, rng, alpha=0.2)
        assert X_mix.shape == X.shape
        assert X_mix.dtype == np.float32
        assert (y_mix == y).all()

    def test_mixup_creates_interpolated_values(self):
        rng = np.random.default_rng(42)
        X = np.zeros((6, WINDOW_SAMPLES, CHANNELS), dtype=np.float32)
        # Give distinct values within class 0 so linear combination yields new numbers
        X[0] = 1.0
        X[1] = 2.0
        X[2] = 3.0
        X[3] = 4.0
        X[4] = 5.0
        X[5] = 6.0
        y = np.array([0, 0, 0, 1, 1, 1])

        X_mix, _ = mixup_augment_windows(X, y, rng, alpha=0.5)
        # Should contain values distinct from original identical steps
        assert not np.array_equal(X_mix, X)


class TestSafetyConstrainedThreshold:
    """Tests for safety-constrained operating thresholding."""

    def test_reaches_target_sensitivity(self):
        y_true = np.array([0] * 20 + [1] * 20)
        # Probabilities with overlap
        rng = np.random.default_rng(42)
        y_prob = np.concatenate([rng.uniform(0.05, 0.60, 20), rng.uniform(0.40, 0.95, 20)])

        thresh = find_safety_constrained_threshold(y_true, y_prob, target_sensitivity=0.85)
        assert 0.10 <= thresh <= 0.90
        sens = ((y_prob >= thresh) & (y_true == 1)).sum() / 20.0
        assert sens >= 0.85

    def test_fallback_on_unreachable_target(self):
        y_true = np.array([0, 1])
        y_prob = np.array([0.9, 0.1])  # inverted probabilities
        thresh = find_safety_constrained_threshold(y_true, y_prob, target_sensitivity=0.99)
        assert 0.10 <= thresh <= 0.90


class TestModelWithFocalAndCosine:
    """Tests for model construction with Focal Loss and Cosine learning rate scheduler."""

    def test_build_model_with_focal_loss(self):
        model = build_model(
            input_shape=(WINDOW_SAMPLES, CHANNELS),
            loss_type="focal",
            focal_gamma=2.0,
            focal_alpha=0.75,
        )
        assert isinstance(model.loss, AsymmetricFocalLoss)
        assert model.loss.gamma == 2.0
        assert model.loss.alpha == 0.75

    def test_build_model_with_cosine_schedule(self):
        model = build_model(
            input_shape=(WINDOW_SAMPLES, CHANNELS),
            lr_schedule_type="cosine",
            steps_per_epoch=50,
        )
        # In Keras 3, _learning_rate stores the schedule instance
        lr_obj = getattr(model.optimizer, "_learning_rate", model.optimizer.learning_rate)
        assert isinstance(
            lr_obj,
            tf.keras.optimizers.schedules.CosineDecayRestarts,
        )
