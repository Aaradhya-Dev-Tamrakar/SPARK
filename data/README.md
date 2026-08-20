# SPARK Data Directory

This directory manages motion sensor recordings, calibration sequences, and benchmark dataset archives for the SPARK fall detection pipeline.

---

## Directory Organization

```
data/
├── raw/                # Unprocessed benchmark datasets & trial logs (GITIGNORED)
│   ├── SisFall/        # Official SisFall dataset uncompressed activities
│   └── trials_nepal/   # Self-collected local validation recordings (Action #23)
├── processed/          # Windowed, normalized, and pre-extracted samples (GITIGNORED)
│   ├── sisfall_windows_200hz.npy
│   └── sisfall_labels.npy
└── README.md           # Dataset documentation & sourcing instructions
```

---

## Dataset Sourcing

### 1. SisFall Benchmark Dataset
- **Description**: Public dataset containing 4,506 files across 38 subjects (23 young adults, 15 elderly adults) performing 34 distinct ADL and fall activities at 200 Hz.
- **Acquisition**: Download official `activities.rar` / `SisFall_dataset.zip` from the SisFall repository.
- **Preprocessing**: Run [`training/data_prep/prepare_sisfall.py`](../training/data_prep/prepare_sisfall.py):
  ```bash
  python training/data_prep/prepare_sisfall.py --input data/raw/SisFall --output data/processed/
  ```

### 2. Local Nepal Elderly Fall Validation Dataset
- **Protocol**: Under evaluation with HOD (see `SPARK_TRACKER.md` Action #23).
- **Target**: Complementary validation subset recorded under realistic dorsal wrist placement.

---

## Data Hygiene & Git Policy
- **Never commit raw or processed motion sensor data (`.csv`, `.txt`, `.npy`, `.rar`, `.zip`) to git.**
- `.gitignore` is configured to ignore all files in `data/*` with the exception of `data/.gitkeep` and `data/README.md`.
