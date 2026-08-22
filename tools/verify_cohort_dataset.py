"""verify_cohort_dataset.py -- Verifier and completion grid generator for SPARK Nepal Cohort.

Scans data/nepal_cohort/ for all recorded trials, checks file integrity,
and generates a structured completion report across subjects and activities.
"""

import argparse
import csv
import glob
import os
import sys


def verify_file(filepath: str) -> tuple[bool, int, str]:
    """Verifies a single CSV trial file. Returns (is_valid, row_count, error_msg)."""
    try:
        with open(filepath, newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header or len(header) != 6:
                return False, 0, "Invalid header schema (expected 6 columns: Ax,Ay,Az,Gx,Gy,Gz)"

            row_count = 0
            for row in reader:
                if len(row) != 6:
                    return False, row_count, f"Corrupted row at line {row_count + 2}"
                row_count += 1

            if row_count < 100:
                return False, row_count, "Trial too short (<100 samples)"

            return True, row_count, "OK"
    except Exception as e:
        return False, 0, f"Read error: {e}"


def scan_cohort_dataset(dataset_dir: str) -> dict[str, object]:
    """Scans and analyzes the cohort directory."""
    pattern = os.path.join(dataset_dir, "*.csv")
    files = glob.glob(pattern)

    subjects: set[str] = set()
    activities: set[str] = set()
    fall_trials = 0
    adl_trials = 0
    total_samples = 0
    corrupted_files: list[tuple[str, str]] = []
    subject_grid: dict[str, dict[str, int]] = {}

    for fpath in files:
        fname = os.path.basename(fpath)
        parts = fname.replace(".csv", "").split("_")
        if len(parts) >= 3:
            act, subj, _ = parts[0], parts[1], parts[2]
            subjects.add(subj)
            activities.add(act)

            if subj not in subject_grid:
                subject_grid[subj] = {}
            subject_grid[subj][act] = subject_grid[subj].get(act, 0) + 1

            is_valid, count, msg = verify_file(fpath)
            if not is_valid:
                corrupted_files.append((fname, msg))
            else:
                total_samples += count
                if act.startswith("F"):
                    fall_trials += 1
                else:
                    adl_trials += 1

    duration_hours = (total_samples / 200.0) / 3600.0

    return {
        "total_files": len(files),
        "unique_subjects": sorted(subjects),
        "unique_activities": sorted(activities),
        "fall_trials": fall_trials,
        "adl_trials": adl_trials,
        "total_samples": total_samples,
        "total_duration_hours": round(duration_hours, 3),
        "corrupted_count": len(corrupted_files),
        "corrupted_files": corrupted_files,
        "subject_grid": subject_grid,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SPARK Nepal Cohort Dataset Verifier")
    parser.add_argument(
        "--data-dir", type=str, default="data/nepal_cohort", help="Path to cohort data"
    )
    parser.add_argument(
        "--min-subjects", type=int, default=12, help="Target minimum subject cohort"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("=" * 70)
    print("SPARK Nepal Cohort Dataset Verification & Completion Audit")
    print(f"Directory: {args.data_dir}")
    print("=" * 70)

    if not os.path.exists(args.data_dir):
        print(f"[INFO] Directory {args.data_dir} does not exist yet. No trials recorded.")
        return 0

    stats = scan_cohort_dataset(args.data_dir)
    print(f"Total CSV Trials:      {stats['total_files']}")
    print(
        f"Total Subjects:        {len(stats['unique_subjects'])} ({', '.join(stats['unique_subjects'][:10])}...)"
    )
    print(f"Fall Trials (Positive): {stats['fall_trials']}")
    print(f"ADL Trials (Negative):  {stats['adl_trials']}")
    print(
        f"Total 200 Hz Samples:  {stats['total_samples']:,} ({stats['total_duration_hours']} hours)"
    )
    print(f"Corrupted / Short:     {stats['corrupted_count']}")

    if stats["corrupted_files"]:
        print("\n[WARNING] Corrupted files detected:")
        for fname, err in stats["corrupted_files"]:
            print(f"  - {fname}: {err}")

    print("=" * 70)
    return 0 if stats["corrupted_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
