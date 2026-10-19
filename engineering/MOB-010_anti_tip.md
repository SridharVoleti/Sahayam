# MOB-010 — Anti-tip monitoring: engineering and prototype cost

Status: preliminary engineering estimate, **not** a validated physical design.

## Mechanical
- Candidate rectangular contact footprint: 0.65 m wheelbase × 0.50 m track, inherited from provisional MOB-001.
- Measure fully loaded mass, center of gravity, arm extension and liquid movement. The stability model requires actual center-of-mass coordinates.
- Prefer a low battery/power module position and wide-enough support footprint; assess doorway trade-off with MOB-009.
- 50 mm minimum calculated static margin is a *provisional software threshold*, not a proven safe margin.

## Electronics
- Candidate low-cost 6-axis IMU (MPU-6050 class) to measure angular rates and estimate tilt with sensor fusion.
- Existing shared microcontroller should process IMU readings and command inhibit; do not purchase another controller for this requirement.
- IMU alone cannot measure the center of mass, mass distribution or guarantee tip prevention.
- A separately engineered safety channel and actuator-disable mechanism are required before autonomous operation.

## Electrical
- Candidate IMU board operates at low voltage; verify module input rating, I2C voltage levels, noise immunity, mounting and cable length.
- Reuse protected low-voltage sensor supply. Allocate no new mains wiring for this feature.
- Sensor failure must inhibit motion; electrical power-loss stopping behavior needs independent validation.

## Software and simulation
- Implemented: quasi-static projected-center-of-mass stability margin for acceleration and floor slope.
- Pending: time-domain robot motion coupling, IMU emulation, tip-event scenarios, liquid slosh, braking transients and actual motor inhibit wiring.
- The simulator currently does not call this gate automatically.

## Prototype cost allocation (INR, provisional)
| Item | Quantity | Budget INR | Incremental? |
|---|---:|---:|---|
| MPU-6050-class IMU breakout | 1 | 150–350 | Yes |
| IMU mount, fasteners and wiring | 1 set | 100–250 | Yes |
| Shared microcontroller, power and motor driver | Existing | 0 | No double count |
| Calibration/tilt test fixture materials | 1 | 150–400 | Yes |
| **Incremental MOB-010 budget** | | **400–1,000** | |
| **Prior working budget (MOB-001..009)** | | **18,000** | |
| **New working total** | | **18,400–19,000** | |

Costs are planning allowances, not current supplier quotations. The prior budget itself has a wider ₹15,000–₹25,000 uncertainty band. The estimate excludes a safety-rated stop subsystem and full-scale mechanical redesign.
