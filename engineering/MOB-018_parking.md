# MOB-018 — Safe parking pose selection

**Acceptance:** Robot parks without obstructing exits or circulation.
**State:** 2D planning and clearance gate, no actual docking or moving-person sensing.

## Software and spatial verification
- Evaluate candidate center + heading poses against verified room bounds and rectangular keep-out zones representing doors, egress routes, circulation, furniture.
- Expand robot footprint by configured arm/tool/load/cable-overhang allowance; perform rotated quadrilateral **separating-axis overlap** tests with each forbidden zone expanded by clearance. Touching a restricted zone is rejected.
- Reject unknown/stale map, lost localization, unverified tether route, malformed geometry, E-stop, or every unsafe candidate.
- A valid *pose* does **not guarantee a collision-free approach path**, intact door sweep, unblocked emergency egress when other people move, or actual safe tether route. Combine with MOB-009 doorway, MOB-014 localization, MOB-016 route planning and MOB-017 corridor arbitration in integrated tests before physical trials.

## Electronics
- Reuse controller, existing localization markers/camera and proximity sensors. For bench demonstrations, a printed parking fiducial or floor tape can aid calibrated docking.
- Optional end-stop switch/contact sensor for repeatable parking; no extra navigation computer.

## Electrical
- Verify final tether path, powered stop, coil/reel tension and protected low-voltage wiring separately; `tether_route_verified` is currently an **external assertion**, not a geometric cable-snag model.
- Park with emergency-stop access and without extension cords across public walking paths.

## Mechanical
- Include 0.65 m wheelbase/0.50 m track chassis **provisional geometry**, guards, arm stow, 10 kg target cargo cradle, bumper, attachment and cable.
- Physical parked envelope may be larger than wheel footprint. Never reduce safety clearance just to force a successful virtual parking.
- Measure room, doorway swings and minimum required egress width rather than assigning unverified universal values.

## Tests
- 18 written cases cover exit and corridor obstruction, rotated poses, overhang, bounds, invalid/stale maps and candidates, tether gate, E-stop and multiple-pose fallback.
- Pending: actual floorplan measurements, blocked approach route, obstacle updates, human movement, cable path, dashboard animation, live camera integration and physical stop/parking demonstration.

## INR planning, under ₹50,000 total
| Optional materials | Amount | Charge once |
|---|---:|---|
| Existing sensors, camera, controller | ₹0 | Reuse |
| Floor tape / printed fiducial marker | ₹0–150 | Fabrication/tools |
| Optional docking switch + bracket | ₹0–350 | Sensor/interface |
| **Potential incremental exposure** | **₹0–500** | None purchased or quoted |

No purchases. A parking dock/charging apparatus is **not** included in this amount; mains tether is a separate safety engineering program.
