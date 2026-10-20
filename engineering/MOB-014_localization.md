# MOB-014 — Localization loss and recovery

**Approved acceptance:** Robot stops safely and recovers localization.
**State:** Model and kinematic integration written; *no physical sensor or safety-rated actuator validation*.

## Behavior
- Starts in `lost`, not automatically authorized to move.
- While tracking, a stale/faulty fix, failed independent landmark check, low confidence, position/heading error, or emergency stop latches `lost` and commands **zero speed** in the 2D simulator.
- Recovery needs a stationary robot and **three consecutive healthy position fixes** with a consistent absolute reference. A bad fix resets the count.
- Operator/supervisor release is required to rearm. The release cycle still commands zero travel; next healthy observation may allow travel.
- Confidence ≥0.80, position error ≤0.15 m and heading error ≤10° are *provisional test parameters*, not measured guarantees.
- This is not a real localization estimator, a proof of regained position or a safe real-world stopping-distance calculation. A production robot must verify localization by independent landmarks and independently enforce motor disable when position is unknown.

## Electronic hardware (cost-first)
1. Reuse the shared low-voltage controller, drive encoders and MOB-010 IMU to estimate **relative** position. Encoders+IMU drift and cannot by themselves prove an absolute pose.
2. For re-localization in a known room, trial **printed ArUco/AprilTag landmarks** with an existing laptop/phone/USB camera. Check scale, occlusion, lighting, calibration and privacy. No cloud upload required.
3. Optional USB camera only if no suitable existing camera is available. Evaluate 2D lidar much later if tests show landmarks insufficient; it is out of the present low-cost allocation.

## Electrical
- Use a protected 5 V camera supply and correctly regulated 3.3 V/5 V controller interfaces; include cable strain relief.
- Localization-loss **software stop** is not a hardware emergency stop. Before motorized operation, motor drive enable must have an independent fail-safe path and braking behavior must be tested.

## Mechanical
- Rigid camera/IMU/encoder mounts; lens orientation and vibration influence pose estimates.
- Mount landmarks in fixed, measurable positions. Test with 7 kg *inert* cooker-equivalent mass on a secured low platform and narrow doorways; no hot cooker or unvalidated liquid load.

## Verification and simulation
- Written: unit cases for quality loss, stale fixes, corrupt readings, latching, multi-fix recovery, release and integration to `simulate_step`. 
- Pending: executable regression confirmation/CI, video dashboard loss-and-recovery trace, actual fiducial detection, sensor fusion, blocked-corridor recovery, stopping distance on wet tile, motor inhibit and physical tests.
- A positive model state **does not certify** real autonomous navigation.

## Incremental BOM / INR (provisional, no quote)
| Component | Quantity | Planning incremental cost | Notes |
|---|---:|---:|---|
| Shared encoder, IMU, controller, laptop | Reused | ₹0 | Do not double count |
| Printed fiducial tags, tape, calibrated mounting | 1 set | ₹50–200 | If needed |
| USB webcam, only if no existing camera works | 1 | ₹500–1,200 | Optional |
| **New equipment exposure** | | **₹0–1,400** | No purchases, no supplier-verified quotes |

Budget ownership: `controller_sensors` ₹7,000 envelope and `tool_interface` ₹5,000 fabrication envelope. Price and capability must be verified before purchases. **₹50,000 remains the full initial prototype ceiling.**
