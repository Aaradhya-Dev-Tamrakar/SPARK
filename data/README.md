# SPARK Data Directory

This directory manages motion sensor recordings, calibration sequences, and benchmark dataset archives for the SPARK fall detection pipeline.

---

## Directory Organization

```
data/
├── SisFall_dataset/       # Official SisFall benchmark dataset (uncompressed from SisFall_dataset.zip)
│   ├── SA01/ … SA23/      # Young adult subjects (23 subjects, 34 activities each)
│   ├── SE01/ … SE15/      # Elderly adult subjects (15 subjects, 19 ADL activities each)
│   └── Readme.txt         # Original SisFall dataset documentation
├── SisFall_dataset.zip    # Original compressed SisFall archive (~227 MB)
├── processed_sisfall/     # Windowed, normalized, and pre-extracted samples (GITIGNORED)
│   ├── windows.npy        # 38,426 motion windows (200 × 6 float32 arrays)
│   ├── labels.npy         # Binary fall/non-fall labels per window
│   ├── meta.csv           # Per-window metadata (subject, activity, trial, source file)
│   └── model/             # Trained Keras model artifacts (spark_cnn.keras)
├── gateway_events/        # Replay-generated fall incident records & clinical PDFs
│   ├── *.json             # Per-event JSON records with SHAP attribution data
│   ├── SPARK_Report_*.pdf # One-page clinical PDF incident reports (ReportLab)
│   └── index.jsonl        # Event index for gateway REST API queries
├── nepal_cohort/          # [FUTURE] Self-collected KEC validation recordings (Action #23)
├── .gitkeep
└── README.md              # This file
```

---

## Dataset Sourcing

### 1. SisFall Benchmark Dataset
- **Description**: Public dataset containing 4,506 files across 38 subjects (23 young adults, 15 elderly adults) performing 34 distinct ADL and fall activities at 200 Hz.
- **Acquisition**: Download official `SisFall_dataset.zip` from the SisFall repository.
- **Preprocessing**: Run [`training/data_prep/prepare_sisfall.py`](../training/data_prep/prepare_sisfall.py):
  ```bash
  python training/data_prep/prepare_sisfall.py --input data/SisFall_dataset --output data/processed_sisfall/
  ```

### 2. Local Nepal Fall Validation Dataset
- **Protocol**: Fully specified in [`docs/DATA_COLLECTION_PROTOCOL.md`](../docs/DATA_COLLECTION_PROTOCOL.md) (Action #23 / Issue #6).
- **Target**: Complementary validation subset recorded under realistic dorsal wrist placement using 34 standardized activity trials (15 falls, 19 ADLs).
- **Execution Plan**: See [`docs/SPARK_POST_BOARDS_MASTER_PLAN.md`](../docs/SPARK_POST_BOARDS_MASTER_PLAN.md), Phase 3.
- **Status**: Pending physical hardware assembly and board exam completion.

### 3. Gateway Event Archives
- **Description**: Replay-generated fall incident records produced by `gateway/main.py` during pipeline verification.
- **Contents**: 13 event JSON records with SHAP attribution breakdowns + 13 corresponding one-page clinical PDF reports.

---

## Data Hygiene & Git Policy
- **Never commit raw or processed motion sensor data (`.csv`, `.txt`, `.npy`, `.rar`, `.zip`) to git.**
- `.gitignore` is configured to ignore all files in `data/*` with the exception of `data/.gitkeep` and `data/README.md`.

