"""test_cohort_collection.py -- Unit tests for Nepal cohort data collection and transfer pipeline."""

import os
import tempfile

import numpy as np
import pytest

from tools.record_cohort_data import (
    ACTIVITY_TAXONOMY,
    generate_mock_trial,
    parse_raw_line,
    save_trial_csv,
    validate_recording,
)
from tools.verify_cohort_dataset import scan_cohort_dataset, verify_file
from training.data_prep.prepare_nepal_cohort import process_cohort_dataset
from training.train_transfer import (
    calibrate_threshold,
    create_base_or_load_model,
    run_transfer_training,
)


class TestCohortRecordingTools:
    def test_activity_taxonomy_integrity(self):
        assert len(ACTIVITY_TAXONOMY) == 34
        falls = [k for k in ACTIVITY_TAXONOMY if k.startswith("F")]
        adls = [k for k in ACTIVITY_TAXONOMY if k.startswith("D")]
        assert len(falls) == 15
        assert len(adls) == 19

    def test_parse_raw_line(self):
        # Header or comment returns None
        assert parse_raw_line("Timestamp,Ax,Ay,Az,Gx,Gy,Gz") is None
        assert parse_raw_line("# comment") is None

        # 7 columns (timestamp_ms + 6 raw LSB channels)
        line_7 = "1000, 2048, -2048, 0, 164, -164, 0"
        res_7 = parse_raw_line(line_7)
        assert res_7 is not None
        assert pytest.approx(res_7[0], 0.01) == 1.0
        assert pytest.approx(res_7[1], 0.01) == -1.0
        assert pytest.approx(res_7[3], 0.1) == 10.0

        # 6 columns (already in engineering units)
        line_6 = "0.98, -0.12, 0.05, 12.5, -4.2, 1.1"
        res_6 = parse_raw_line(line_6)
        assert res_6 is not None
        assert len(res_6) == 6
        assert pytest.approx(res_6[0], 0.01) == 0.98

    def test_mock_trial_generation_and_validation(self):
        samples_fall = generate_mock_trial("F01", duration_s=2.0, sample_rate=200)
        assert len(samples_fall) == 400
        report_fall = validate_recording(samples_fall, target_hz=200)
        assert report_fall.status == "VALID"
        assert report_fall.total_samples == 400
        assert report_fall.effective_hz == 200.0

        # Test empty trial validation
        report_empty = validate_recording([], target_hz=200)
        assert report_empty.status == "EMPTY_TRIAL"

    def test_save_and_verify_trial_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            samples = generate_mock_trial("F02", duration_s=2.0)
            csv_path = save_trial_csv(samples, tmpdir, "SA01", "F02", "R01")
            assert os.path.exists(csv_path)

            is_valid, count, msg = verify_file(csv_path)
            assert is_valid is True
            assert count == 400
            assert msg == "OK"

            # Check directory scanning
            stats = scan_cohort_dataset(tmpdir)
            assert stats["total_files"] == 1
            assert stats["fall_trials"] == 1
            assert stats["adl_trials"] == 0
            assert "SA01" in stats["unique_subjects"]


class TestNepalCohortPreprocessing:
    def test_window_slicing_and_aggregation(self):
        with tempfile.TemporaryDirectory() as raw_dir, tempfile.TemporaryDirectory() as out_dir:
            # Create a mock fall trial and a mock ADL trial
            fall_samples = generate_mock_trial("F01", duration_s=2.0)
            adl_samples = generate_mock_trial("D01", duration_s=3.0)

            save_trial_csv(fall_samples, raw_dir, "SA01", "F01", "R01")
            save_trial_csv(adl_samples, raw_dir, "SA01", "D01", "R01")

            summary = process_cohort_dataset(raw_dir, out_dir, window_size=200)
            assert summary["total_windows"] > 0
            assert summary["fall_windows"] > 0
            assert summary["adl_windows"] > 0

            # Verify saved files
            X = np.load(os.path.join(out_dir, "nepal_windows.npy"))
            y = np.load(os.path.join(out_dir, "nepal_labels.npy"))
            assert X.shape[1:] == (200, 6)
            assert len(X) == len(y)


class TestTransferLearningPipeline:
    def test_freeze_conv_layers(self):
        model = create_base_or_load_model(freeze_conv=True)
        conv_layers = [layer for layer in model.layers if "conv1d" in layer.name.lower()]
        assert len(conv_layers) >= 2
        for layer in conv_layers:
            assert layer.trainable is False

        # Dense head should remain trainable
        dense_layers = [layer for layer in model.layers if "dense" in layer.name.lower()]
        assert len(dense_layers) >= 1
        for layer in dense_layers:
            assert layer.trainable is True

    def test_calibrate_threshold(self):
        y_true = np.array([0, 0, 0, 1, 1, 1])
        y_probs = np.array([0.1, 0.2, 0.35, 0.40, 0.85, 0.95])
        best_thresh, best_sens, best_spec = calibrate_threshold(y_true, y_probs)
        assert 0.0 < best_thresh < 1.0
        assert best_sens >= 0.8
        assert best_spec >= 0.8

    def test_end_to_end_transfer_training(self):
        with tempfile.TemporaryDirectory() as data_dir, tempfile.TemporaryDirectory() as model_dir:
            # Generate dummy windows: 20 fall windows, 20 ADL windows
            np.random.seed(42)
            X = np.random.randn(40, 200, 6).astype(np.float32)
            # Add fall signal to positive class
            X[:20, 80:120, 2] += 4.0
            y = np.array([1] * 20 + [0] * 20, dtype=np.int32)
            subjects = np.array(["SA01"] * 20 + ["SA02"] * 20, dtype=object)

            np.save(os.path.join(data_dir, "nepal_windows.npy"), X)
            np.save(os.path.join(data_dir, "nepal_labels.npy"), y)
            np.save(os.path.join(data_dir, "nepal_subjects.npy"), subjects)

            res = run_transfer_training(
                data_dir=data_dir,
                out_dir=model_dir,
                epochs=2,
                batch_size=16,
                freeze_conv=True,
            )

            assert "optimal_threshold" in res
            assert "validation_sensitivity" in res
            assert os.path.exists(os.path.join(model_dir, "spark_cnn_transfer.keras"))
            assert os.path.exists(os.path.join(model_dir, "model_config_transfer.json"))
