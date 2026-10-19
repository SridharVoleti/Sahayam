# MOB-011 — Adaptive multi-trip payload transport

**Status:** software implementation only; no executed tests or physical payload qualification.

## Functional approach
- Reject unknown mass, unknown lift/travel capacity, inadequate stability, and indivisible overweight objects.
- Split divisible loads into equal batches below the smaller of the verified lift and transport capacities.
- Recheck actual mass and MOB-010 stability for every trip.
- Current mass verification is an external assertion, **not** an electronic weighing measurement. A verified loaded center of mass is also required before physical operation.
- Pending: trip completion acknowledgments, item inventory tracking, pick/place actuation, load-dependent center-of-mass recomputation, route and cable safety, dynamic acceleration and liquid slosh.

## Household validation case: loaded 5 L pressure cooker
- User-provided design example: **5 L cooker can weigh approximately 6–7 kg when loaded**; verify actual combined mass of cooker, lid, contents and accessories rather than assuming all models weigh this amount.
- **Design target, not certified rating:** aim for a **10 kg supported-deck transport capacity** for the first supervised prototype, while respecting its overall ₹50,000 ceiling. Confirm wheel/axle load, motor starting torque, braking, stability and doorway clearance before adopting this rating.
- A 7 kg **indivisible cooker cannot be split into trips**. A low, secured support platform may transport it only after loading by a person or separately qualified mechanism. This is categorically different from a robot lifting it.
- For a 7 kg load at 0.40 m arm reach, gravity alone creates ~27.5 N·m shoulder torque, *excluding* arm mass, dynamics and safety factors. The ₹7,000 educational-arm envelope is **not** a qualifying cooker-lift solution.
- **Hot cooker handling is blocked**, including hot surfaces, steam, pressure and spill hazards. **Unvalidated liquid transport is blocked** due to slosh and braking dynamics. Never grasp a pressurized vessel by its lid/pressure regulator.
- Full physically safe transport requires validated **loaded** center of mass, acceleration/braking, secure cradle geometry, temperature and contamination controls. Existing software does not yet derive the combined loaded center of gravity from measured masses; current authorization is *only a planning scenario*, not permission to actuate real motors.

## Mechanical
- Determine gripper/tray dimensions, support-cradle and retention features, load placement, payload mass, total vehicle mass and center-of-mass movement.
- Reuse low-mounted tray and structural mounts if they can satisfy required payload. Do not assume the proposed educational arm can lift 1 kg.
- Structural strength, gripping force and tipping stability require test evidence.

## Electronics and electrical
- Initially use supervised, manually verified load entries; **no additional hardware required** for software planning.
- Later consider a low-cost strain-gauge load cell and HX711-class amplifier for measuring tray mass; requires calibration and mechanical mounting.
- Reuse controller, protected sensor rail and MOB-010 IMU. No independent controller purchase.
- An actuator interlock must prevent an overweight lift independently of task-planning software before autonomous operation.

## Handling-mode trade-off
- `robot_lift`: enforcing both separately verified manipulation and travel capacities; an overweight indivisible object is rejected.
- `preloaded_tray`: permit planning against separately verified **transport** capacity without falsely requiring a 7 kg robotic arm; requires a secured load and external placement. No automatic pick-up is implied.
- Mode flags, load mass and capacity remain external trusted inputs to a Python model, **not** sensor attestations or final safety validation. Sensor integration and a fail-safe actuator interlock remain open.

## Incremental prototype budget (planning allowance, INR)
| Item | Quantity | Planned ₹ | Phase |
|---|---:|---:|---|
| Python batching logic | 1 | 0 | Current |
| Existing shared controller, IMU, tray | Reused | 0 | Current |
| Candidate load cell + HX711 module | 1 | 250–600 | Future validation |
| Bracket, tray reinforcement and calibration weights | 1 set | 250–500 | Future validation |
| **Optional incremental physical equipment** | | **500–1,100** | **Not allocated or purchased** |

The ₹500–₹1,100 is an **unverified estimate**, not a supplier quotation. It must be funded from the existing ₹50,000 subsystem envelopes through reallocation or savings, **not added to the ceiling**. The arm and tool interface allocations already exist; do not count them again.

### Budget impact of cooker case
No new hardware purchase is authorized or priced merely by adopting the 7 kg example. Existing **₹12,000 chassis/drive** and **₹5,000 tool-interface/fabrication** envelopes need engineering validation for a 10 kg supported-deck target. Reinforcement or higher-torque motors may require reallocating existing funds; **cost TBD pending measured robot mass, deck height, motor torque, doorway constraints and supplier quotes**. Preserve ₹50,000 ceiling and ₹9,000 contingency until actual quotes exist.
