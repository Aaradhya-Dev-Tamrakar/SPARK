#!/usr/bin/env python3
"""
prepare_sisfall.py

Parses the raw SisFall dataset (38 subjects, 15 fall types [F01-F15],
19 ADL types [D01-D19], 4506 trial files) into fixed-length windows
matching SPARK's on-device pipeline spec (proposal main.md,
sec:imu_acquisition / Sliding Window Buffer):

  - 6 channels: a_x, a_y, a_z, w_x, w_y, w_z  (100 Hz)
  - 200-sample windows (2s), stride configurable (default = window,
    i.e. non-overlapping; use --stride to overlap)
  - Labels kept at native granularity (D01..D19, F01..F15) so the
    binary-vs-multiclass decision (still open, per session Q&A) is
    made downstream at train time, not baked in here.

Source file format (verified against actual SisFall_dataset/SA01/
D01_SA01_R01.txt): 9 columns, semicolon+CRLF-terminated rows:
    ADXL345_x, ADXL345_y, ADXL345_z,   <- accelerometer #1 (selected)
    ITG3200_x, ITG3200_y, ITG3200_z,   <- gyroscope
    MMA8451Q_x, MMA8451Q_y, MMA8451Q_z <- accelerometer #2 (unused)

SPARK's MPU6050 node is a single 6-axis accel+gyro device, so this
script uses the ADXL345 accelerometer columns (cols 1-3) + ITG3200
gyroscope columns (cols 4-6) as the 6-channel analogue. This is a
device-mapping choice made here, not stated in the proposal itself
(which only specifies MPU6050's own 6 channels) -- flagged so it's
reviewable, not silently assumed.

Native sampling rate is 200 Hz (confirmed: D01_SA01_R01.txt has
19999 rows =~ 100s trial at 200 Hz, matching proposal's Dataset
Preparation section). Downsampled to 100 Hz via linear interpolation,
matching the proposal's stated method for both source datasets.

Usage:
    python prepare_sisfall.py \\
        --src /path/to/SisFall_dataset \\
        --out /path/to/output_dir \\
        [--stride 200] [--window 200]

Output:
    <out>/windows.npy   float32, shape (N, 200, 6)
    <out>/labels.npy    str,     shape (N,)   e.g. "F03", "D11"
    <out>/meta.csv       one row per window: subject, activity_code,
                          trial, source_file, window_index_in_trial
"""

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

NATIVE_HZ = 200
TARGET_HZ = 100
WINDOW_SAMPLES_DEFAULT = 200  # 2s @ 100Hz, per proposal Sliding Window Buffer spec

# Column indices (0-based) into the raw 9-column file.
# ADXL345 = accel #1, ITG3200 = gyro. See module docstring.
ACCEL_COLS = (0, 1, 2)
GYRO_COLS = (3, 4, 5)


def parse_trial_file(path: Path) -> np.ndarray:
    """
    Parse one SisFall .txt trial file into a (T, 9) float array.

    Verified format: rows separated by ';\\r\\n' (or ';\\n'), comma-
    separated integer values, inconsistent internal whitespace
    (columns are space-padded, e.g. '  17,-179, -99, -18,...').
    Trailing empty entries after the final ';' are dropped.
    """
    text = path.read_text()
    rows = text.replace(" ", "").split(";")
    parsed = []
    for row in rows:
        row = row.strip()
        if not row:
            continue
        try:
            values = [int(v) for v in row.split(",")]
        except ValueError:
            # A malformed row in raw sensor dumps is a data-quality
            # signal, not something to silently drop -- surface it.
            raise ValueError(f"Malformed row in {path}: {row!r}")
        if len(values) != 9:
            raise ValueError(
                f"Expected 9 columns in {path}, got {len(values)}: {row!r}"
            )
        parsed.append(values)
    if not parsed:
        raise ValueError(f"No data rows parsed from {path}")
    return np.array(parsed, dtype=np.float64)


def downsample_200_to_100(arr: np.ndarray) -> np.ndarray:
    """
    Linear-interpolation resample from 200Hz to 100Hz, per proposal
    Dataset Preparation section's stated method ("Downsampled to
    100 Hz").

    arr: (T, C) at 200Hz -> returns (T//2, C) at 100Hz.
    """
    n_samples_200 = arr.shape[0]
    duration_s = n_samples_200 / NATIVE_HZ
    n_samples_100 = int(round(duration_s * TARGET_HZ))

    t_200 = np.linspace(0, duration_s, n_samples_200, endpoint=False)
    t_100 = np.linspace(0, duration_s, n_samples_100, endpoint=False)

    out = np.empty((n_samples_100, arr.shape[1]), dtype=np.float64)
    for c in range(arr.shape[1]):
        out[:, c] = np.interp(t_100, t_200, arr[:, c])
    return out


def window_trial(
    arr_100hz: np.ndarray, window: int, stride: int
) -> list[np.ndarray]:
    """Slice a (T, 6) 100Hz array into fixed-length windows."""
    windows = []
    n = arr_100hz.shape[0]
    if n < window:
        # A trial shorter than one window is a real data-completeness
        # issue -- report it, don't silently zero-pad or skip.
        return windows
    for start in range(0, n - window + 1, stride):
        windows.append(arr_100hz[start : start + window, :])
    return windows


def find_trial_files(src_root: Path):
    """
    Yield (path, subject_id, activity_code, trial_num) for every
    trial file under src_root, matching the verified naming pattern
    {ActivityCode}_{SubjectID}_{TrialNum}.txt inside per-subject
    folders (SA01-SA23, SE01-SE15).
    """
    for subject_dir in sorted(src_root.iterdir()):
        if not subject_dir.is_dir():
            continue
        subject_id = subject_dir.name
        for f in sorted(subject_dir.glob("*.txt")):
            stem = f.stem  # e.g. "D01_SA01_R01"
            parts = stem.split("_")
            if len(parts) != 3:
                print(
                    f"WARNING: unexpected filename pattern, skipping: {f}",
                    file=sys.stderr,
                )
                continue
            activity_code, file_subject, trial_tag = parts
            if file_subject != subject_id:
                print(
                    f"WARNING: subject mismatch (folder={subject_id}, "
                    f"filename={file_subject}), skipping: {f}",
                    file=sys.stderr,
                )
                continue
            yield f, subject_id, activity_code, trial_tag


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--src",
        required=True,
        type=Path,
        help="Path to extracted SisFall_dataset/ directory (contains SA01/, SE01/, ...)",
    )
    ap.add_argument(
        "--out", required=True, type=Path, help="Output directory for windows/labels/meta"
    )
    ap.add_argument(
        "--window",
        type=int,
        default=WINDOW_SAMPLES_DEFAULT,
        help=f"Window length in 100Hz samples (default {WINDOW_SAMPLES_DEFAULT} = 2s)",
    )
    ap.add_argument(
        "--stride",
        type=int,
        default=None,
        help="Stride in 100Hz samples between window starts (default = --window, i.e. non-overlapping)",
    )
    args = ap.parse_args()

    if not args.src.is_dir():
        print(f"ERROR: --src not found or not a directory: {args.src}", file=sys.stderr)
        sys.exit(1)

    stride = args.stride if args.stride is not None else args.window
    args.out.mkdir(parents=True, exist_ok=True)

    all_windows = []
    all_labels = []
    meta_rows = []

    trial_files = list(find_trial_files(args.src))
    if not trial_files:
        print(f"ERROR: no trial files found under {args.src}", file=sys.stderr)
        sys.exit(1)

    n_short_trials = 0
    n_files_processed = 0

    for f, subject_id, activity_code, trial_tag in trial_files:
        raw = parse_trial_file(f)
        selected = raw[:, ACCEL_COLS + GYRO_COLS]  # (T, 6) at 200Hz
        resampled = downsample_200_to_100(selected)  # (T', 6) at 100Hz

        trial_windows = window_trial(resampled, args.window, stride)
        if not trial_windows:
            n_short_trials += 1
            print(
                f"WARNING: trial shorter than window ({resampled.shape[0]} "
                f"samples < {args.window}), skipped: {f}",
                file=sys.stderr,
            )
            continue

        for w_idx, w in enumerate(trial_windows):
            all_windows.append(w)
            all_labels.append(activity_code)
            meta_rows.append(
                {
                    "subject": subject_id,
                    "activity_code": activity_code,
                    "trial": trial_tag,
                    "source_file": str(f.relative_to(args.src)),
                    "window_index_in_trial": w_idx,
                }
            )
        n_files_processed += 1

    if not all_windows:
        print("ERROR: zero windows produced from any trial file", file=sys.stderr)
        sys.exit(1)

    windows_arr = np.stack(all_windows).astype(np.float32)  # (N, window, 6)
    labels_arr = np.array(all_labels, dtype="<U3")  # "F01".."F15", "D01".."D19"

    np.save(args.out / "windows.npy", windows_arr)
    np.save(args.out / "labels.npy", labels_arr)

    with open(args.out / "meta.csv", "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(meta_rows[0].keys()))
        writer.writeheader()
        writer.writerows(meta_rows)

    n_fall = int(np.char.startswith(labels_arr, "F").sum())
    n_adl = int(np.char.startswith(labels_arr, "D").sum())
    unique_subjects = len({r["subject"] for r in meta_rows})
    unique_activities = len({r["activity_code"] for r in meta_rows})

    print(f"Files processed:      {n_files_processed} / {len(trial_files)}")
    if n_short_trials:
        print(f"Files skipped (short): {n_short_trials}")
    print(f"Windows produced:     {windows_arr.shape[0]}")
    print(f"  fall windows (F*):  {n_fall}")
    print(f"  ADL windows (D*):   {n_adl}")
    print(f"Subjects represented: {unique_subjects} / 38")
    print(f"Activity codes seen:  {unique_activities} / 34 (15 fall + 19 ADL)")
    print(f"Window shape:         {windows_arr.shape[1:]} (samples, channels)")
    print(f"Output written to:    {args.out}")


if __name__ == "__main__":
    main()
