"""
test_shap_pipeline.py

Unit tests for the SHAP explainability engine in SPARK Gateway.
Tests verify:
    1. PeakFeatureExplainer computes normalized channel attributions and identifies top feature.
    2. CnnShapExplainer computes gradient-based attribution on raw 200x6 waveforms.
    3. Explainer factory selects appropriate backend based on model presence.
"""

import numpy as np
import pytest
import tensorflow as tf

from gateway.receiver.wire_format import IMU_CHANNELS, EventPayload
from gateway.shap_pipeline.explainer import (
    CnnShapExplainer,
    PeakFeatureExplainer,
    ShapAttribution,
    get_explainer,
)


@pytest.fixture
def dummy_event() -> EventPayload:
    return EventPayload(
        event_id="TEST-EVT-01",
        device_id="TEST-DEV-01",
        firmware_version="v1.0.0",
        timestamp_ms=1724160000000,
        confidence=0.92,
        peak_features={
            "a_x": 0.5,
            "a_y": 0.8,
            "a_z": 4.2,  # Dominant vertical spike
            "w_x": 1.0,
            "w_y": 1.5,
            "w_z": 0.7,
        },
    )


class TestPeakFeatureExplainer:
    def test_attribution_keys_and_top_feature(self, dummy_event: EventPayload):
        explainer = PeakFeatureExplainer()
        result = explainer.explain(dummy_event)

        assert isinstance(result, ShapAttribution)
        assert set(result.values.keys()) == set(IMU_CHANNELS)
        assert result.top_feature == "a_z"
        assert abs(sum(result.values.values()) - 1.0) < 1e-5
        assert result.values["a_z"] > result.values["a_x"]
        assert len(result.clinical_summary) > 0

    def test_zero_peak_features_graceful_handling(self):
        event = EventPayload(
            event_id="ZERO-EVT",
            device_id="TEST-DEV",
            firmware_version="v1.0.0",
            timestamp_ms=1000,
            confidence=0.5,
            peak_features=dict.fromkeys(IMU_CHANNELS, 0.0),
        )
        explainer = PeakFeatureExplainer()
        result = explainer.explain(event)

        assert abs(sum(result.values.values()) - 1.0) < 1e-5
        for ch in IMU_CHANNELS:
            assert abs(result.values[ch] - 1.0 / len(IMU_CHANNELS)) < 1e-5


class TestCnnShapExplainer:
    def test_cnn_gradient_saliency_attribution(self, dummy_event: EventPayload, tmp_path):
        # Build a minimal test Keras model
        inputs = tf.keras.Input(shape=(200, 6))
        x = tf.keras.layers.GlobalAveragePooling1D()(inputs)
        outputs = tf.keras.layers.Dense(2, activation="softmax")(x)
        model = tf.keras.Model(inputs, outputs)

        model_path = tmp_path / "test_model.keras"
        model.save(model_path)

        # Attach raw window
        rng = np.random.default_rng(42)
        raw_window = rng.standard_normal((200, 6)).astype(np.float32)
        # Add large vertical impact spike in a_z (channel 2) during impact phase
        raw_window[90:110, 2] += 5.0
        dummy_event.raw_window = raw_window.tolist()

        explainer = CnnShapExplainer(model_path=model_path)
        result = explainer.explain(dummy_event)

        assert isinstance(result, ShapAttribution)
        assert set(result.values.keys()) == set(IMU_CHANNELS)
        assert abs(sum(result.values.values()) - 1.0) < 1e-5
        assert "pre_impact_dynamics" in result.temporal_attributions
        assert "impact_spike" in result.temporal_attributions

    def test_cnn_fallback_when_raw_window_absent(self, dummy_event: EventPayload):
        explainer = CnnShapExplainer(model_path=None)
        result = explainer.explain(dummy_event)

        assert isinstance(result, ShapAttribution)
        assert result.top_feature == "a_z"


class TestExplainerFactory:
    def test_get_explainer_fallback(self):
        explainer = get_explainer(model_path="non_existent_path.keras")
        assert isinstance(explainer, PeakFeatureExplainer)
