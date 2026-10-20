# PWR-004 — Retraction

Software-only planning. Hardware is unbuilt and unverified.

Reuses the PWR-003 demonstration and sensing. Optional passive guides are provisionally ₹0–250. A powered reel is not funded or approved. No purchases are recorded. Independent overload and guarding tests remain required.

## Behavior and validation

The Python model calculates safe planning targets from measured route distance, slack, observed tension and a bounded take-up rate. It will not command retraction during uncertain sensor health, near people or under excessive tension. Retraction during motion is limited to the speed of approach toward the reel; stationary operation requires explicit supervision.

## Engineering

Electronics: reuse the PWR-003 controller, reel encoder and tension sensing if later qualified. Electrical: prototype unpowered only; a separately reviewed motor-control safety mechanism will be needed before a powered reel. Mechanical: independent tension-limiting mechanism, guarded pinch points, cable strain relief, thermal characterization and tests under cable snag and sudden stop conditions are mandatory.

## Verification

18 tests are written but have not yet been confirmed as executed. The model does not simulate elastic cable force, inertia or actual whipping hazards. No 230 V reel is authorized.

## Budget

The existing PWR-003 reel demonstration is reused at no further charge. Optional passive guides/markings ₹0–250 are provisional and unquoted. Powered motor, clutch, reel and protective hardware remain TBD. Preserve ₹50,000 total cap and avoid duplicate allocations.
