# MOB-011 — Adaptive multi-trip payload transport

**Status:** software implementation only; no executed tests or physical payload qualification.

## Functional approach
- Reject unknown mass, unknown lift/travel capacity, inadequate stability, and indivisible overweight objects.
- Split divisible loads into equal batches below the smaller of the verified lift and transport capacities.
- Recheck actual mass and MOB-010 stability for every trip.
- Current mass verification is an external assertion, **not** an electronic weighing measurement. A verified loaded center of mass is also required before physical operation.
- Pending: trip completion acknowledgments, item inventory tracking, pick/place actuation, load-dependent center-of-mass recomputation, route and cable safety, dynamic acceleration and liquid slosh.

## Mechanical
- Determine gripper/tray dimensions, load placement, payload mass, total vehicle mass and center-of-mass movement.
- Reuse low-mounted tray and structural mounts if they can satisfy required payload. Do not assume the proposed educational arm can lift 1 kg.
- Structural strength, gripping force and tipping stability require test evidence.

## Electronics and electrical
- Initially use supervised, manually verified load entries; **no additional hardware required** for software planning.
- Later consider a low-cost strain-gauge load cell and HX711-class amplifier for measuring tray mass; requires calibration and mechanical mounting.
- Reuse controller, protected sensor rail and MOB-010 IMU. No independent controller purchase.
- An actuator interlock must prevent an overweight lift independently of task-planning software before autonomous operation.

## Incremental prototype budget (planning allowance, INR)
| Item | Quantity | Planned ₹ | Phase |
|---|---:|---:|---|
| Python batching logic | 1 | 0 | Current |
| Existing shared controller, IMU, tray | Reused | 0 | Current |
| Candidate load cell + HX711 module | 1 | 250–600 | Future validation |
| Bracket, tray reinforcement and calibration weights | 1 set | 250–500 | Future validation |
| **Optional incremental physical equipment** | | **500–1,100** | **Not allocated or purchased** |

The ₹500–₹1,100 is an **unverified estimate**, not a supplier quotation. It must be funded from the existing ₹50,000 subsystem envelopes through reallocation or savings, **not added to the ceiling**. The arm and tool interface allocations already exist; do not count them again.
