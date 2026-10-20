"""Unit tests for SPARK Kinetics Adversarial Stress Harness."""

from tools.spark_kinetics_stress_harness import SparkKineticsStressHarness


def test_generate_borderline_jerk_stream():
    harness = SparkKineticsStressHarness(sample_rate_hz=200)
    frames = harness.generate_borderline_jerk_stream(duration_sec=0.5, threshold_g=2.5)
    assert len(frames) == 100
    for f in frames:
        assert 2.40 <= f.magnitude_g <= 2.60
        assert f.timestamp_ms >= 0


def test_simulate_freertos_queue_burst():
    harness = SparkKineticsStressHarness()
    pushed, dropped, drop_ratio = harness.simulate_freertos_queue_burst(
        queue_capacity=16, burst_size=64
    )
    assert pushed > 0
    assert dropped > 0
    assert 0.0 < drop_ratio < 1.0


def test_evaluate_fall_recall_barrier():
    harness = SparkKineticsStressHarness()
    h_safe, status_safe = harness.evaluate_fall_recall_barrier(0.98, minimum_safe_recall=0.95)
    assert h_safe > 0.0
    assert status_safe == "BARRIER_SAFE"

    h_breach, status_breach = harness.evaluate_fall_recall_barrier(0.92, minimum_safe_recall=0.95)
    assert h_breach < 0.0
    assert status_breach == "BARRIER_BREACH"


def test_run_full_kinetics_gauntlet():
    harness = SparkKineticsStressHarness()
    res = harness.run_full_kinetics_gauntlet()
    assert res["total_generators_evaluated"] >= 2
    assert res["runtime_ms"] < 200.0
