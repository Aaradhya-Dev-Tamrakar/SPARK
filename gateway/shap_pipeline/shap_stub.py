#!/usr/bin/env python3
"""
shap_stub.py

SHAP explainability scaffold for SPARK's gateway (Layer 2), per
tracker SPARK_TRACKER.md sec:2.1 item 2 ("Runs full SHAP analysis
(device-side) for feature importance visualization") and sec:2.4
Stage 4 ("Gateway SHAP -- Code: TBD, implementation TBD during WP 2.0").

SCOPE: interface + dummy-value stub only. Real SHAP values require a
trained CNN (training/train_cnn.py output, gated behind WP 2.0's
Sensitivity/Specificity >= 90% benchmark, tracker sec:6.1 -- not yet
run). This file must not attempt to load a real model or compute real
attributions; it exists so the report-generation and storage stubs
have a stable shape to build against.

Reference from proposal main.md sec:shap (superseded transport/DB
details aside, the *attribution content* is still the right shape):
  - Six input features = peak IMU channel values over the 2s event
    window (matches wire_format.IMU_CHANNELS).
  - KernelExplainer or GradientExplainer against the trained CNN
    (loaded as TFLite interpreter on gateway) -- library choice not
    re-confirmed against the current tracker design, kept as the only
    documented reference.
  - Output: per-feature attribution value + a "top contributing
    feature" summary, both surfaced in the PDF report and (per
    tracker) local JSON, not a Streamlit/PostgreSQL dashboard (that
    was the superseded v35 design).

`shap` is not installed in this environment (verified this session)
and is not imported here -- this stub has zero dependency on the
real library so it runs anywhere, including before WP 2.0 delivers a
trained model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from gateway.receiver.wire_format import IMU_CHANNELS, EventPayload


@dataclass
class ShapAttribution:
    """
    Gateway-side SHAP result for one event.

    values: {channel_name: attribution_value} -- one entry per
        wire_format.IMU_CHANNELS. Sign/magnitude convention (does
        positive mean "pushed toward FALL"?) TBD with real model;
        stub values carry no such meaning.
    top_feature: channel name with largest |attribution|.
    base_value: model's expected-value baseline (SHAP convention).
        Stub uses 0.0; real value comes from the trained explainer.
    """

    values: Dict[str, float]
    top_feature: str
    base_value: float = 0.0


class ShapExplainer:
    """
    Interface every SHAP backend (real or stub) implements.

    explain(event) -> ShapAttribution. Kept synchronous and single-
    event to match tracker sec:2.4's "triggered only on confirmed
    fall events, not continuously" framing -- no batching/streaming
    concerns belong in this interface.
    """

    def explain(self, event: EventPayload) -> ShapAttribution:
        raise NotImplementedError


class StubShapExplainer(ShapExplainer):
    """
    Deterministic dummy explainer. No model, no `shap` import, no
    randomness -- same event always produces the same fake
    attribution, so downstream report/storage code can be tested
    reproducibly.

    Dummy rule (arbitrary, clearly not real): attribution per channel
    = that channel's peak_features value, normalized so |values| sum
    to 1.0. This is NOT a real SHAP computation -- Shapley values
    satisfy efficiency/symmetry/dummy axioms this rule makes no
    attempt to honor. Replace entirely, don't extend, once WP 2.0
    delivers a trained model (see module docstring gate).
    """

    def explain(self, event: EventPayload) -> ShapAttribution:
        peaks = {ch: float(event.peak_features.get(ch, 0.0)) for ch in IMU_CHANNELS}
        total = sum(abs(v) for v in peaks.values())

        if total == 0.0:
            # No peak data on the event -- distribute attribution
            # uniformly rather than divide by zero. Dummy behavior,
            # not a modeling decision.
            values = {ch: 1.0 / len(IMU_CHANNELS) for ch in IMU_CHANNELS}
        else:
            values = {ch: v / total for ch, v in peaks.items()}

        top_feature = max(values, key=lambda ch: abs(values[ch]))

        return ShapAttribution(values=values, top_feature=top_feature, base_value=0.0)


def get_explainer() -> ShapExplainer:
    """
    Factory. Returns the stub today. Once a trained/quantized model
    exists (WP 2.0 gate, tracker sec:6.1), swap this to return a real
    explainer backend -- callers should depend on get_explainer(),
    never on StubShapExplainer directly, so that swap is one-line.
    """
    return StubShapExplainer()
