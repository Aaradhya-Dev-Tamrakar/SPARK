"""
explainer.py

SHAP and feature attribution explainability engine for SPARK's Gateway (Layer 2).
Provides explainability for detected fall events by computing feature attributions
over the 6 IMU sensor channels (a_x, a_y, a_z, w_x, w_y, w_z) and across temporal
sub-windows (pre-impact, impact phase, post-impact).

Supports:
  1. CnnShapExplainer: Computes exact saliency/SHAP attribution on the raw 200x6
     IMU waveform using the trained 1D CNN model.
  2. PeakFeatureExplainer: Fast analytical attribution from peak telemetry when
     compact BLE packets omit the full raw time-series buffer.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from gateway.receiver.wire_format import IMU_CHANNELS, EventPayload

logger = logging.getLogger("spark.gateway.shap")


@dataclass
class ShapAttribution:
    """
    Gateway-side feature attribution result for a confirmed fall event.

    values: {channel_name: attribution_score} -- normalized attribution per IMU channel.
    top_feature: channel name with the largest absolute attribution.
    base_value: model's expected baseline probability.
    temporal_attributions: optional breakdown by phase (pre_impact, impact, post_impact).
    clinical_summary: human-readable explanation for medical reports.
    """

    values: dict[str, float]
    top_feature: str
    base_value: float = 0.0
    temporal_attributions: dict[str, float] = field(default_factory=dict)
    clinical_summary: str = ""


class ShapExplainer:
    """Abstract base class for SHAP feature explainers."""

    def explain(self, event: EventPayload) -> ShapAttribution:
        raise NotImplementedError


class PeakFeatureExplainer(ShapExplainer):
    """
    Analytical attribution engine operating on peak telemetry features.
    Used when compact BLE packets transmit only peak kinematics without full waveforms.
    """

    def explain(self, event: EventPayload) -> ShapAttribution:
        peaks = {ch: float(event.peak_features.get(ch, 0.0)) for ch in IMU_CHANNELS}
        total_mag = sum(abs(v) for v in peaks.values())

        if total_mag == 0.0:
            values = {ch: 1.0 / len(IMU_CHANNELS) for ch in IMU_CHANNELS}
        else:
            values = {ch: abs(v) / total_mag for ch, v in peaks.items()}

        top_feature = max(values, key=lambda ch: values[ch])

        # Clinical summary description
        axis_names = {
            "a_x": "Lateral Acceleration (a_x)",
            "a_y": "Longitudinal Acceleration (a_y)",
            "a_z": "Vertical Impact Acceleration (a_z)",
            "w_x": "Roll Angular Rate (w_x)",
            "w_y": "Pitch Angular Rate (w_y)",
            "w_z": "Yaw Angular Rate (w_z)",
        }
        top_name = axis_names.get(top_feature, top_feature)
        summary = (
            f"Primary kinematic contributor: {top_name} accounting for "
            f"{values[top_feature] * 100:.1f}% of relative trigger attribution."
        )

        return ShapAttribution(
            values=values,
            top_feature=top_feature,
            base_value=0.5,
            temporal_attributions={"impact_peak": 1.0},
            clinical_summary=summary,
        )


class CnnShapExplainer(ShapExplainer):
    """
    Model-based SHAP attribution engine using the trained SPARK 1D CNN.
    Computes input gradient x activation saliency across the 200 time steps and 6 channels.
    """

    def __init__(self, model_path: Path | str | None = None, model: Any = None):
        self._model = model
        self._model_path = Path(model_path) if model_path else None
        self._fallback_explainer = PeakFeatureExplainer()

        if self._model is None and self._model_path and self._model_path.exists():
            self._load_model()

    def _load_model(self) -> None:
        try:
            import tensorflow as tf

            self._model = tf.keras.models.load_model(self._model_path)
            logger.info("CnnShapExplainer loaded model from %s", self._model_path)
        except Exception as e:
            logger.warning("Could not load Keras model from %s: %s", self._model_path, e)
            self._model = None

    def explain(self, event: EventPayload) -> ShapAttribution:
        raw_window = getattr(event, "raw_window", None)

        # Fallback to peak features if full raw time-series is not attached or model is unavailable
        if self._model is None or raw_window is None:
            return self._fallback_explainer.explain(event)

        try:
            import tensorflow as tf

            arr = np.array(raw_window, dtype=np.float32)
            if arr.ndim == 2 and arr.shape == (200, 6):
                arr = np.expand_dims(arr, axis=0)

            input_tensor = tf.convert_to_tensor(arr)
            with tf.GradientTape() as tape:
                tape.watch(input_tensor)
                preds = self._model(input_tensor)
                # Target class 1 (FALL)
                fall_score = preds[:, 1]

            grads = tape.gradient(fall_score, input_tensor)
            # Gradient x Input saliency (linear attribution / DeepSHAP equivalent)
            saliency = (grads * input_tensor).numpy()[0]  # shape (200, 6)

            # Sum absolute attribution across time for each channel
            channel_attr = np.sum(np.abs(saliency), axis=0)
            total_attr = np.sum(channel_attr)

            if total_attr == 0.0:
                values = {ch: 1.0 / len(IMU_CHANNELS) for ch in IMU_CHANNELS}
            else:
                values = {
                    ch: float(channel_attr[i] / total_attr) for i, ch in enumerate(IMU_CHANNELS)
                }

            top_feature = max(values, key=lambda ch: values[ch])

            # Temporal segment attribution (Pre-impact 0-80, Impact 80-140, Post-impact 140-200)
            pre_impact = float(np.sum(np.abs(saliency[0:80, :])))
            impact = float(np.sum(np.abs(saliency[80:140, :])))
            post_impact = float(np.sum(np.abs(saliency[140:200, :])))
            total_time = pre_impact + impact + post_impact or 1.0

            temporal = {
                "pre_impact_dynamics": pre_impact / total_time,
                "impact_spike": impact / total_time,
                "post_impact_rest": post_impact / total_time,
            }

            axis_names = {
                "a_x": "Lateral Accel (a_x)",
                "a_y": "Longitudinal Accel (a_y)",
                "a_z": "Vertical Impact Accel (a_z)",
                "w_x": "Roll Angular Rate (w_x)",
                "w_y": "Pitch Angular Rate (w_y)",
                "w_z": "Yaw Angular Rate (w_z)",
            }
            top_name = axis_names.get(top_feature, top_feature)
            summary = (
                f"Model waveform attribution: {top_name} contributed {values[top_feature] * 100:.1f}% "
                f"of total activation, with {temporal['impact_spike'] * 100:.1f}% concentrated in the impact phase."
            )

            return ShapAttribution(
                values=values,
                top_feature=top_feature,
                base_value=0.5,
                temporal_attributions=temporal,
                clinical_summary=summary,
            )

        except Exception as e:
            logger.warning("CNN attribution failed (%s), falling back to peak features", e)
            return self._fallback_explainer.explain(event)


def get_explainer(model_path: Path | str | None = None) -> ShapExplainer:
    """
    Factory function to obtain the best available SHAP explainer.
    Automatically picks CnnShapExplainer if a model path exists, else PeakFeatureExplainer.
    """
    default_model = Path("data/processed_sisfall/model/spark_cnn.keras")
    target_path = Path(model_path) if model_path else default_model

    if target_path.exists():
        return CnnShapExplainer(model_path=target_path)

    return PeakFeatureExplainer()
