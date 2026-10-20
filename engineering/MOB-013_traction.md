# MOB-013 — Slippery surface response

**Acceptance:** Robot reduces motion or stops when traction confidence is low.
**Status:** Python decision gate, unverified; no actual slip estimator or actuator connection.

## Electronics
- Preferred: reuse drive-wheel encoders (once specified), MOB-010 IMU and shared motor controller; estimate mismatch between wheel rotation and inertial motion, with filtering.
- **Important:** Wheel encoder/IMU disagreement is not a definitive measurement of friction, especially at low speed or during steady slip. Calibration and independent validation are essential.
- Optional future optical flow / ground-facing sensor only if existing sensors prove inadequate. Do not buy prematurely.

## Electrical
- Reuse low-voltage power, protected wiring and motor inhibit hardware. Wheel encoders must have correct logic voltage and noise protection.
- Stopping on slippery surfaces can itself create slip; actual braking deceleration must be validated. Independent emergency stop remains mandatory.

## Mechanical
- Compare inexpensive rubber tread wheels against hard plastic on dry and wet tile; check contact pressure, payload distribution and wheel contamination.
- Assess traction with **7 kg loaded-cooker scenario** only as a secured, unheated supervised test mass. No hot cooker handling.
- Tire choice may matter more than adding an expensive sensor.

## Software and simulation
- Implemented: external confidence 0..1 gates normal speed, caution <=0.10 m/s, or stop. Heavy/liquid loads stop under caution-level confidence. Missing or stale sensing fails closed.
- The 0.40 and 0.75 confidence thresholds are **provisional software parameters**, not calibrated physical friction thresholds.
- Pending: actual confidence estimation, motion-controller integration, dynamic braking, wet-floor simulation, sensor faults, traction loss under heavy loads, browser visualization and physical tests.

## Cost impact — provisional INR
| Item | Incremental estimate | Status |
|---|---:|---|
| Existing IMU, controller and future wheel encoders | ₹0 additional | Reuse, if suitable |
| Rubber tread wheel upgrade, if required | ₹300–900 | Optional, replaces rather than duplicates wheel budget |
| Ground-facing optical sensor/mount, if required | ₹300–800 | Optional |
| **Potential incremental budget exposure** | **₹0–1,700** | Unquoted and unpurchased |

Do not add the full potential exposure to the ₹50,000 ceiling. Reconcile wheel substitution with existing chassis/drive allocation; fund any additional sensor within controller/sensor allocation. No vendor quotes yet.
