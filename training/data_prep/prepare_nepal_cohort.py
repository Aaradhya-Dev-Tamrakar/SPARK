"""prepare_nepal_cohort.py -- Window segmentation and preprocessing for Nepal cohort data.

Loads raw CSV files from data/nepal_cohort/, slices them into 200x6 windows,
standardizes features, and exports numpy arrays for transfer learning and validation.
"""

import argparse
import glob
import os
import sys

import numpy as np
import pandas as pd


def load_and_slice_trial(
    csv_path: str,
    window_size: int = 200,
    fall_stride: int = 100,
    adl_stride: int = 200,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Loads a single CSV trial file and extracts 200x6 sliding windows.

    Returns: (windows, labels, subjects, activities)
    """
    fname = os.path.basename(csv_path).replace(".csv", "")
    parts = fname.split("_")
    if len(parts) < 3:
        return (
            np.empty((0, window_size, 6)),
            np.empty((0,)),
            np.empty((0,), dtype=object),
            np.empty((0,), dtype=object),
        )

    act_code, subject_id, _ = parts[0], parts[1], parts[2]
    is_fall = 1 if act_code.startswith("F") else 0
    stride = fall_stride if is_fall else adl_stride

    try:
        df = pd.read_csv(csv_path)
        # Expected columns: Ax, Ay, Az, Gx, Gy, Gz
        req_cols = ["Ax", "Ay", "Az", "Gx", "Gy", "Gz"]
        if not all(col in df.columns for col in req_cols):
            # Fallback if unlabelled: take first 6 numeric columns
            data = df.iloc[:, :6].to_numpy(dtype=np.float32)
        else:
            data = df[req_cols].to_numpy(dtype=np.float32)
    except Exception as e:
        print(f"[WARN] Failed to read {csv_path}: {e}")
        return (
            np.empty((0, window_size, 6)),
            np.empty((0,)),
            np.empty((0,), dtype=object),
            np.empty((0,), dtype=object),
        )

    num_samples = len(data)
    if num_samples < window_size:
        # Pad with edge values if slightly short
        pad_len = window_size - num_samples
        data = np.pad(data, ((0, pad_len), (0, 0)), mode="edge")
        num_samples = window_size

    windows = []
    for start in range(0, num_samples - window_size + 1, stride):
        end = start + window_size
        windows.append(data[start:end, :])

    if not windows:
        return (
            np.empty((0, window_size, 6)),
            np.empty((0,)),
            np.empty((0,), dtype=object),
            np.empty((0,), dtype=object),
        )

    win_arr = np.array(windows, dtype=np.float32)
    n_win = len(windows)
    lbl_arr = np.full((n_win,), is_fall, dtype=np.int32)
    sbj_arr = np.full((n_win,), subject_id, dtype=object)
    act_arr = np.full((n_win,), act_code, dtype=object)

    return win_arr, lbl_arr, sbj_arr, act_arr


def process_cohort_dataset(
    raw_dir: str,
    out_dir: str,
    window_size: int = 200,
) -> dict[str, object]:
    """Processes all raw trials in raw_dir and saves processed numpy arrays to out_dir."""
    os.makedirs(out_dir, exist_ok=True)
    pattern = os.path.join(raw_dir, "*.csv")
    csv_files = glob.glob(pattern)

    all_windows = []
    all_labels = []
    all_subjects = []
    all_activities = []

    for fpath in csv_files:
        wins, lbls, sbjs, acts = load_and_slice_trial(fpath, window_size=window_size)
        if len(wins) > 0:
            all_windows.append(wins)
            all_labels.append(lbls)
            all_subjects.append(sbjs)
            all_activities.append(acts)

    if not all_windows:
        print(f"[INFO] No valid windows found in {raw_dir}.")
        return {"total_windows": 0, "fall_windows": 0, "adl_windows": 0}

    X = np.concatenate(all_windows, axis=0)
    y = np.concatenate(all_labels, axis=0)
    subjects = np.concatenate(all_subjects, axis=0)
    activities = np.concatenate(all_activities, axis=0)

    np.save(os.path.join(out_dir, "nepal_windows.npy"), X)
    np.save(os.path.join(out_dir, "nepal_labels.npy"), y)
    np.save(os.path.join(out_dir, "nepal_subjects.npy"), subjects)
    np.save(os.path.join(out_dir, "nepal_activities.npy"), activities)

    fall_count = int(np.sum(y == 1))
    adl_count = int(np.sum(y == 0))

    print(f"[PREPARED COHORT] Total Windows: {len(X)} | Falls: {fall_count} | ADLs: {adl_count}")
    print(f"[SAVED] Saved arrays to: {out_dir}")

    return {
        "total_windows": len(X),
        "fall_windows": fall_count,
        "adl_windows": adl_count,
        "unique_subjects": len(np.unique(subjects)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SPARK Nepal Cohort Data Preprocessor")
    parser.add_argument(
        "--raw-dir", type=str, default="data/nepal_cohort", help="Directory with raw CSV files"
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="data/processed_nepal",
        help="Output directory for npy arrays",
    )
    parser.add_argument(
        "--window-size", type=int, default=200, help="Window length in samples (200 = 1.0s)"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("=" * 70)
    print("SPARK Nepal Cohort Window Segmentation & Preprocessing")
    print(f"Input: {args.raw_dir} -> Output: {args.out_dir}")
    print("=" * 70)

    if not os.path.exists(args.raw_dir):
        print(f"[ERROR] Raw directory not found: {args.raw_dir}")
        return 1

    process_cohort_dataset(args.raw_dir, args.out_dir, window_size=args.window_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
