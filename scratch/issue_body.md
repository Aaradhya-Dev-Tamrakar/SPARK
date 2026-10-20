## Overview
Quantify and bridge the cross-body domain gap between the waist-origin SisFall benchmark dataset (Sucerquia et al., 2017) and SPARK's dorsal wrist wearable form factor, and generalize the mathematical formulation to mobile robotics state estimation (chassis base vs end-effector links). Establishes a major thesis novelty chapter on geriatric compliance-first fall detection, biomechanical kinematic transfer modeling, multi-tier domain adaptation, and cyber-physical spatial normalization.

## Scope & Architectural Alignment
- **Primary Reference**: Sucerquia et al. (2017) confirms SisFall's sensor placement at the elastic waist belt near the body's Center of Mass (CoM).
- **Dual-Domain Kinematic Invariant**: Connects human serial limb biomechanics (Torso -> Clavicle -> Humerus -> Wrist) with mobile robotics multi-link kinematic chains (Base Pelvis/Chassis -> Serial Link Tree -> End-Effector).
- **Spatial IMU Normalization Layer**: Derives both forward distal projection and inverse "Virtual CoM" canonical standardization to allow models trained on canonical benchmarks to generalize across heterogeneous sensor placements.
- **Sim-to-Real Solution to the "Falling Bottleneck"**: Resolves the physical and ethical impossibility of subjecting elderly adults or multi-thousand-dollar robots to thousands of destructive high-impact falls via physics-informed kinematic simulation.
- **Empirical Validation**: Targeted UMAFall ratio validation and formalization of a Synchronized Dual-Sensor Protocol (2-node ESP32-S3) in the Nepal Cohort.

## Acceptance Criteria & Tasks
- [ ] Implement literature and empirical kinematic scaling priors for human and robotic links (`training/analysis/biomechanical_priors.py`)
- [ ] Implement generalized kinematic simulator with 3D rotation, lever-arm scaling, protective impact spike, colored gesture/motor noise, and inverse Virtual-CoM transform (`training/analysis/wrist_simulator.py`)
- [ ] Implement targeted empirical benchmark ratio validator (`training/analysis/benchmark_harvester.py`)
- [ ] Implement 4-tier domain adaptation benchmark runner (`training/analysis/cross_body_eval.py`)
- [ ] Update `training/train_transfer.py` to seamlessly accept synthetic and real wrist arrays
- [ ] Formalize Synchronized Dual-Sensor Protocol in `docs/DATA_COLLECTION_PROTOCOL.md` Section 3.4
- [ ] Author publication-ready thesis chapter in Markdown (`docs/thesis_chapters/chapter_cross_body_transfer_analysis.md`) and modular LaTeX (`chapter_cross_body_transfer_analysis.tex`), featuring a dedicated section on Mobile Robotics State Estimation
- [ ] Author unit tests in `tests/test_cross_body_simulator.py` (including Virtual-CoM reconstruction roundtrip) and verify 100% test pass (`pytest`) and clean lint (`ruff`)
