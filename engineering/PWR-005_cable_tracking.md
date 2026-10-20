# PWR-005 — Cable route tracking

**Acceptance:** Robot tracks cable path and avoids crossing or entanglement.

## Software
- Stores an observed cable polyline and a prospective robot path; detects crossings, collinear overlap and cable self-intersection.
- Requires fresh/complete cable observation, known localization, wheel envelope verification and no snag or under-wheel alert. Unknown conditions refuse the route.
- The current geometry is **two-dimensional, zero-width segments**. It does not account for rope sagging, bend radius, cable diameter, a cable moving when the robot moves, or the wheel/chassis swept footprint. A positive answer is for planning only, never motor authorization.
- Supports MOB-016 planned routes conceptually. The planner must integrate the cable polyline as an inflated obstacle before real navigation.

## Electronics
- Reuse localization camera (MOB-014) if capable of detecting tagged low-voltage test cord, wheel encoders and existing controller.
- Actual long wire color and difficult lighting may require additional dedicated cable detection. No hardware selected or certified.
- A separate reel length/tension estimate from PWR-003 and 004 can corroborate path consistency, but cannot prove cable never passes under wheels.

## Electrical
- Prototype with **unpowered test cord only**. Mains tether tracking is unavailable and requires PWR-001 qualified review and PWR-008 wet-zone protection.
- Route/cable hazard must inhibit drive independently of web UI/AI when later deployed.

## Mechanical
- Survey passageways, doors, chair legs and wheel clearances, including a 10 kg tentative cargo platform and cleaning tools.
- Place cable guides beyond wheels and gripper sweep. A cable attached near the robot may create unavoidable overlapping geometry and needs physical attachment routing and explicit modeling rather than ignoring collisions.

## Tests
- 17 written checks for robot crossing, endpoint touch, collinear overlap, cable self-cross, stale/partial sensing, loss of localization, wheel entrapment and emergency stop.
- Pending simulator animation, actual cord images, recognition robustness, sensor test execution and whole-body path collision.

## INR incremental budget
| Component | Proposed cost | Allocation |
|---|---:|---|
| Reuse MOB-014 camera/controller and PWR-003 reel sensors | ₹0 | Existing |
| Additional colored tags/tape for dry, unpowered cord | ₹0–150 | Optional, share PWR-002 materials |
| Dedicated cable tracking hardware | TBD | Not approved |
| **Current spending** | **₹0** | No purchase |

Keep ₹50,000 unchanged. Prevent duplicate counting of camera, controller, reel and tape. Powered mains work remains outside initial build.
