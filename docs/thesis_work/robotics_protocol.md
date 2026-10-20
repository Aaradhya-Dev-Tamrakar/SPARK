# Planned robotics experiment appendix: MuJoCo humanoid fall monitoring

Status: **planned protocol, not executed**. Human fall detection remains SPARK's primary objective. This appendix proposes a separate simulation study; it establishes neither robot performance nor physical robot validation.

## Documentation feasibility review

Official MuJoCo documentation supports a site-mounted accelerometer and gyroscope with local-frame outputs [R1]. Gymnasium Humanoid-v5 accepts a custom MJCF model through `xml_file` and permits disabling termination on unhealthy posture [R2]. Its supplied model contains lower-arm and torso bodies [R3]. These documented mechanisms make the proposed instrumentation technically plausible. No simulator was installed or run, no locomotion controller was validated, and no robot episodes were generated for this thesis preparation.

The stock humanoid model is a motion source, not a validated fall dataset or a ready-made walking controller. Before dataset generation, a reproducible controller must demonstrate stable locomotion and recovery from mild disturbances on development-only seeds. Pin simulator and Gymnasium versions, model and controller hashes, integrator, timestep, contact settings and random seeds. A controller acquired from an external source requires its own provenance and licence review. Random actions or dropping an unsupported model cannot represent stable locomotion.

The inspected XML uses a 0.003 s physics timestep [R3]; the inspected Humanoid-v5 implementation defaults to five physics steps per action [R4]. Hence the source-derived action interval is 0.015 s. The current documentation's timing prose is inconsistent, so actual model timestep and `frame_skip` must be recorded at runtime. Reading once per Gymnasium action would undersample the proposed IMU stream. Capture each physics substep through a dedicated instrumentation loop before resampling. This custom loop remains to be implemented and validated.

Set `terminate_when_unhealthy=False` and an explicit 30 s episode limit so height-based early termination does not censor impact or recovery [R2, R4]. Numerical instability still invalidates an episode; disabling termination is not permission to retain non-finite trajectories. A pilot must verify full contact and post-impact logging before the main batch.

## Bounded batch and split

The main batch contains exactly 40 accepted episodes, each targeted at 30 s:

| Condition | Development episodes | Held-out episodes | Ground-truth purpose |
|---|---:|---:|---|
| Stable locomotion | 5 | 5 | Non-fall exposure |
| Recoverable disturbances | 5 | 5 | Non-fall exposure with imbalance and recovery |
| Slips ending in falls | 5 | 5 | Fall events following verified foot slip |
| Other falls | 5 | 5 | Fall events caused by a separately specified perturbation |
| Total | 20 | 20 | Exploratory pilot, not deployment certification |

Use bounded torso perturbations for recoverable episodes, a reduced-friction floor patch for slip episodes, and stronger directional impulses or controlled actuator disturbance for other falls. Magnitudes and durations are not yet calibrated. Tune them only on development/pilot trajectories, then freeze a manifest before evaluating held-out episodes. A proposed slip must show foot tangential displacement during load-bearing contact followed by an independently annotated fall; reducing friction alone is not proof of slip.

Fix the five held-out IDs per condition before model adaptation or threshold tuning. Separate controller/reset seeds and perturbation realizations between development and held-out sets; do not reuse nearly identical trajectories or derive both sets from overlapping windows of one episode. Freeze controller, preprocessing, adaptation and detection thresholds before held-out evaluation. Preserve an attempt log, invalid traces and condition mismatches rather than silently selecting cases that the detector classifies correctly. Limit candidate-generation attempts to 20 per condition; report any inability to obtain ten valid episodes and revise the protocol openly. No candidate generation is authorized by this appendix.

## Sensor placement, units and preprocessing

Add a named MJCF site on the dorsal distal forearm of one fixed lower-arm body, near the wrist, as the primary six-channel IMU analogue. Add a torso site as an auxiliary reference and a separately evaluated placement. Store exact site positions and quaternions in the model manifest. The supplied humanoid has no separately articulated wrist; the distal-forearm approximation must be disclosed [R3]. Do not silently pool torso signals with wrist signals or claim direct equivalence to a human MPU6050 mounting.

Co-locate accelerometer and gyro at each site. MuJoCo describes acceleration including gravity and angular velocity in the site frame [R1]. Choose a consistent metre-kilogram-second model convention; MuJoCo itself does not impose SI units, and internal angular quantities use radians [R5]. Archive acceleration in m/s², gyro in rad/s, time in seconds and the exact gravity vector. Verify the stationary-upright and free-fall sensor sign/gravity conventions in a future calibration test before claiming MPU6050 equivalence. For SPARK event fields, convert acceleration by the documented reference gravity (e.g. 9.80665 m/s² per g) and gyro by 180/pi to degrees/s. Record the convention rather than mixing 9.81 and standard gravity silently.

Define right-handed sensor axes through an explicit site quaternion and a documented mapping to `[a_x,a_y,a_z,w_x,w_y,w_z]`. Preserve raw substep timestamps and values. Apply a documented low-pass anti-alias filter before downsampling to a uniform **200 Hz archive**, report filter delay, and flag gaps/non-finite values. Quantify any assumed noise, bias and clipping; these are simulation assumptions, not measured MPU6050 properties.

The current repository has a temporal-contract discrepancy: `training/data_prep/prepare_sisfall.py` sets `TARGET_HZ=100` and a default 200-sample window (2 s), `training/train_cnn.py` loads `(N,200,6)`, while the logger targets 200 Hz and `AGENT.md` describes 200 Hz, 3 s and 200×6 together. Those three values cannot all hold: 200 samples at 200 Hz cover 1 s; 3 s at 200 Hz needs 600 samples. For a current-model exploratory comparison, retain the 200 Hz archive and propose a separately documented **100 Hz, 200×6, 2 s model adapter**. Do not feed a 1 s 200 Hz window into a model trained on 2 s windows and call it equivalent. A new 200 Hz model requires retraining and evaluation.

Input shape alone does not establish preprocessing parity. The inspected SisFall preparation script selects integer sensor-count columns and performs interpolation, without an explicit physical-unit conversion in that path. Audit the provenance, scaling, normalization and quantization of the actual loaded model before choosing count-to-physical or physical-to-model transforms. Fit any new transform on development data only, version it and label changed preprocessing as a new experiment. Failure to recover the model input contract blocks transfer evaluation.

## Independent annotations

Save simulator state, torso height/orientation, foot motion and floor-contact body pairs separately from classifier output. Before held-out evaluation, freeze annotation rules and review synchronized videos/state traces without detector predictions. Record perturbation time, loss-of-balance onset, first fall-related contact, persistent collapsed posture, recovery onset, recovery completion and any ambiguity. Ground truth must never be derived from the classifier threshold or its confidence.

Proposed rules for development calibration are: loss of balance begins when torso tilt exceeds 45 degrees or torso height drops below 0.7 times the episode's calibrated upright height; a fall requires subsequent torso/head/pelvis floor contact or a persistent collapsed posture lasting at least 0.5 s. Record the first such contact separately from onset. Recovery requires return above 0.9 times upright height with tilt below 20 degrees for 2 s, without meeting the fall criterion. These thresholds are operational proposals, not established biomechanical facts. Final thresholds and the handling of kneeling, hand support and delayed recovery must be frozen in the annotation manifest. Disturbance onset and fall onset remain distinct timestamps.

## Evaluation and event interoperability

Report held-out **event sensitivity = matched detected falls / all annotated held-out falls**, separately for slips and other falls, and pooled with its denominator. If each of the ten held-out fall episodes contains one annotated fall, the pooled denominator is ten; it is not the count of overlapping windows. Use a prespecified one-to-one matching interval from loss-of-balance onset until 2 s after first fall contact; record a separate endpoint for contact-free collapse. Count extra alarms as unmatched events and freeze a 2 s duplicate-alarm merge rule before evaluation. Report missed events and exact/binomial uncertainty; ten falls cannot support a reliable deployment claim.

Report **false alarms per non-fall hour = unmatched alarms / valid non-fall exposure hours**, including stable and recoverable conditions separately. Ten held-out 30 s non-fall episodes provide at most 300 s (0.0833 h) of exposure; show actual valid duration. Zero alarms over this short exposure is not proof of a low operational alarm rate. Do not replace exposure-based reporting with window specificity alone.

For matched events, report `t_alarm - t_onset` and `t_alarm - t_first_contact` as separate distributions (median, interquartile range, range and counts). Negative contact-relative delay denotes an alarm before contact. Explain filter/buffer delay and timestamp conventions; missed events are reported separately rather than assigned zero delay. Simulator-time detection delay is not measured ESP32 inference latency, BLE delivery time or real-time execution performance.

A future replay adapter should construct existing Wire Format v1 records: `event_id`, `device_id`, `firmware_version`, uint32 `timestamp_ms`, `confidence=P(FALL)`, and six signed peak features in g and degrees/s. The firmware peak extractor selects the signed sample with greatest magnitude per channel. Use a clearly synthetic simulator device identifier; keep episode/model/simulator provenance in a linked sidecar. v1 does not transmit the raw window. `subject_type=bipedal_robot` is only a proposed v2 extension, so do not claim it is a locked or validated v1 routing capability. Validate JSON parsing/storage/report generation with replay fixtures and distinguish those software checks from physical BLE transport, clinical explanation validity and robot-specific report validity.

## Completion and limits

The future simulation study completes only when versioned motion generation is reproducible, sensor timing/units pass calibration, 40 accepted episodes and the frozen split/annotation manifest exist, the model input contract is recovered, all held-out denominators and exposure are reported, and replay records pass the unchanged gateway event contract. If stable/recoverable motion is unavailable, the planned four-condition study is blocked rather than relabelled as complete. Human-model transfer is exploratory and may fail because human datasets, arm motions, body geometry, controller dynamics and simulated sensors differ. Any adaptation must be reported separately from zero-shot transfer. Physical robot sensing, real disturbances, onboard timing and safety validation remain future work.

## Official source register (checked 2026-10-14)

- R1: MuJoCo, **XML Reference: accelerometer and gyro**. https://mujoco.readthedocs.io/en/stable/XMLreference.html#sensor-accelerometer and https://mujoco.readthedocs.io/en/stable/XMLreference.html#sensor-gyro (one reference page). Documentation establishes site-frame sensor APIs, not validation of this experiment.
- R2: Farama Foundation, **Gymnasium Humanoid**. https://gymnasium.farama.org/environments/mujoco/humanoid/ . Custom model and unhealthy-termination configuration.
- R3: Farama Foundation, **Humanoid MJCF asset**. https://raw.githubusercontent.com/Farama-Foundation/Gymnasium/main/gymnasium/envs/mujoco/assets/humanoid.xml . Inspected body names, geometry and physics timestep. `main` is mutable; pin a commit/hash before future execution.
- R4: Farama Foundation, **Humanoid-v5 implementation**. https://raw.githubusercontent.com/Farama-Foundation/Gymnasium/main/gymnasium/envs/mujoco/humanoid_v5.py . Inspected action stepping and termination behavior. `main` is mutable; pin a commit/hash before future execution.
- R5: MuJoCo, **Overview: Units are unspecified**. https://mujoco.readthedocs.io/en/stable/overview.html#units-are-unspecified . Consistent model units and radians for internal angular quantities.

Local evidence inspected: `AGENT.md`; `training/data_prep/prepare_sisfall.py`; `training/train_cnn.py`; `firmware/main/app_main.cpp`; `firmware/main/comms/peak_features.cpp`; `gateway/receiver/wire_format.py`; `docs/WIRE_FORMAT_v1.md`. These establish source-level contracts and inconsistencies, not executed robotics performance.
