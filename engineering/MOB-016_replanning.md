# MOB-016 — Route replanning and unsafe-shortcut prevention

**Acceptance:** Blocked routes are replanned without unsafe shortcuts. **Status:** deterministic grid-based planner; no autonomous physical routing.

## Software/design
- Uses four-connected A* (no diagonal corner cutting) over a rectangular occupancy grid.
- Obstacles and keep-out zones are inflated by `clearance_cells` and the same margin is kept from the map boundary. This prevents a footprint of unknown size from taking apparent shortcuts through narrow gaps.
- Replanning requires fresh/healthy map sensing, independently validated room boundaries and valid localization (MOB-014).
- If start/goal are inside an inflated hazard, the route is absent or a search budget expires, it **refuses** movement. An output path is not motor authorization.
- Current prototype grid resolution: default **0.10 m/cell**; `clearance_cells=1` is only a software scenario. Actual inflated radius must be derived from measured body width, arm, cable and loaded 10 kg deck target, pose uncertainty and stopping distance. Cells are not tied to a robot footprint yet.

## Electronics
- Reuse existing IMU, encoders, camera-based fiducials (MOB-014) and ranging sensors (MOB-015). Room occupancy may initially be hand-measured and entered by a supervisor.
- Dynamic obstacles, doors and moving people require continuous map update; do not classify human trajectories from this static planner.
- No new motor controller, IMU or computer purchase allocated.

## Electrical/mechanical
- Reuse protected low-voltage sensor harness and actuator-disable mechanism. Do not run the planner directly in an emergency-stop circuit.
- Observe actual clearance including wheels, bumper, tools, cable swept path and a secured inert 7 kg payload.
- Narrow passages may become impassable after correct footprint inflation. **Refusing a route is safer than reducing the clearance arbitrarily to fit.**

## Tests and simulation
- 18 written cases for A* path, blocked walls, forbidden areas, four-neighbor moves, inflated corridor, stale maps, unknown localization, faulty sensors and search limits.
- Pending: hardware localization, real 2D/3D obstacle map, dynamic replanning, map-to-floor calibration, integrated swept-volume collision check, dashboard trace, hardware tests, GitHub Actions execution evidence.
- Current planned route does not actuate motors and its position certainty depends on external inputs.

## Incremental prototype BOM — INR, planning only
| Item | Optional cost | Decision |
|---|---:|---|
| Existing controller, camera, IMU, sensors | ₹0 | Reuse, not purchased here |
| Printed floor-plan markers, tape, measuring consumables | ₹0–300 | Optional |
| Extra positioning or ranging sensors | **TBD** | Defer until MOB-014/015 tests identify a gap |
| **New quantified exposure** | **₹0–300** | Fund from existing tool-interface allowance |

All estimates are unquoted; no equipment purchased. **Do not raise the ₹50,000 cap or double-count earlier sensors.**
