# MOB-015 — Collision avoidance

**Acceptance:** Avoid stationary and moving obstacles. **Status:** 1-D approaching-obstacle speed restriction model and mobility simulator hook; not full geometric avoidance, steering, or safety-certified collision avoidance.

## Approach / physical limitations
- Conservative predicted stopping gap = clearance + speed × reaction time + speed²/(2 × deceleration) + extra oncoming-traffic closure during reaction and braking.
- Limit speed when an object intersects the assumed current corridor. People/pets receive a larger nominal protected clearance. Stale sensors, inconsistent path geometry and unknown inputs cause an immediate **commanded** stop.
- Actual thresholds are *test parameters only*: 0.5 m/s² deceleration, 0.25 s latency, 0.30 m generic object clearance, 0.80 m human clearance. **Not measured** for loaded chassis, wet floors, narrow rooms or moving persons.
- Robot has **no proven collision avoidance until obstacle positions are estimated in 2D/3D, the swept chassis/arm/load volume is checked, real braking characterized, and a fast independent stop path demonstrated**. Stopping a simulated kinematic body instantly cannot reproduce braking distance.

## Electronics
- Reuse existing/proposed forward and rear sensing from MOB-007/009, encoder odometry, shared microcontroller, localization camera (MOB-014) if available.
- Low-price ultrasonic modules may miss fabric, oblique/soft furniture, glass and fast small pets. Favor diversity (short-range ToF/bumper + visual tracking) after actual sensor tests.
- Future bumper contact strip/limit switch provides a simple last-resort stop signal; no expensive lidar authorization now.

## Electrical
- Sensor rail fused and protected; digital hardware input for bump switches, dedicated power-cut/enable relay path to motor driver later.
- A software speed cap does not satisfy independently verified emergency stop, safety-rated person detection or electrical isolation.
- Wiring must not dangle into wheel track, tool path or wet cleaning area.

## Mechanical
- Measure full **swept** envelope (wheel, chassis, arm, 10 kg provisional cargo-deck target, tool, cable) and dynamic stopping response.
- Bumper placement must cover first-contact edges; wheel and arm mounting must not create pinch points.
- Inert 7 kg test mass can be used for controlled transport trials; hot cooker or liquid loads not authorized.

## Verification
- 18 written unit/integration scenarios incl stationary and oncoming obstacles, people/pets, stale sensor, multiple hazards and kinematic simulation.
- Pending: CI confirmation, 2D obstacle simulator and path collision checks, live sensor integration, detection misses, emergency braking, safety-stop circuit, loaded wet-floor tests, browser replay.
- **Do not claim verified avoidance of moving humans/pets from this model.**

## Prototype incremental cost — INR provisional
| Item | Quantity | Incremental estimate | Budget category |
|---|---:|---:|---|
| Existing ranging, IMU, controller, camera | Reused if suitable | ₹0 | Shared |
| Bumper microswitches + safe mounting/wire | 2–4 | ₹150–450 | Controller/sensors and fabrication |
| Additional short-range distance sensor | 1–2 | ₹300–900 | Only if reused sensors inadequate |
| **Optional additional equipment** | | **₹0–1,350** | Within existing ₹50,000 budget |

Prices are **planning allowances**, not current quotations; no purchase recorded. A real independent emergency-stop subsystem remains a separately funded and verified mandatory safety requirement (MOB-020). Do not double-count it here.
