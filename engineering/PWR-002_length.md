# PWR-002 — Configurable safe cable length

**Acceptance:** Select and validate robot-specific cable length and route; Kitchen evaluate 15–20 m, other variants up to 50 m subject to electrical/thermal approval.

## Functional design
- Candidate length must exceed the measured intended route segments plus a separately specified slack allowance.
- Software study envelope: Kitchen ≤20 m; Clean/Laundry ≤50 m. **These are planning bounds, not engineering approvals or recommendations to deploy the full length.**
- Less cable may be safer in small rooms. A kitchen 8 m route is not forced to use 15–20 m; only the eventual workspace measurement determines the required length.
- Route study always requires verified path, avoidance of feet/wheels, wet-zone protection, qualified electrical approval, voltage drop, thermal loading, reel heating, strain/snags and independent stopping.
- Even when all documentary flags are true, the model **never energizes mains**. PWR-001 physical blocker applies.

## Electronics/electrical
- Future architecture options: fixed low-voltage tether from a certified external PSU (early prototype) versus engineered 230 V mains tether/reel (future safety project).
- Cable size/insulation/rating, reel heat build-up, conductor voltage drop, protective earth/leakage and fault protection depend on actual 230 V vs DC mode, robot current, full length and winding duty.
- 50 m tether is not automatically electrically or mechanically safe. Cable on a reel has different thermal rating when coiled versus fully extended.

## Mechanics
- Map robot route, door thresholds, sharp turns, human walking paths, children/pets and placement of stationary reel. Payout/retraction PWR-003/004 must prevent pulling, whipping and wheel entanglement.
- Cable clamp/strain relief and safe clearance around cleaning water, kitchen steam and hot tools are mandatory.

## Verification
- 19 written tests: kitchen study and 50 m alternate-variant limits, route+slack sizing, missing actual measurements, unsafe people/wet routing, voltage-drop, reel thermal, stop path and invalid data.
- Pending: actual cable source/route photos and dimensions, electrical load, conductor selection, thermal/current proof, qualified installation, physical reel, dashboard trace and cable/snag simulations.

## Incremental budget / INR
| First physical prototype decision | Cost | Assessment |
|---|---:|---|
| Keep low-voltage stationary supply and simulator | ₹0 added | Reuse earlier power safety envelope |
| Portable physical measuring tape / marking cord | ₹0–200 if not already owned | Optional, count once |
| Future 15–20 m or up-to-50 m qualified mains tether/reel | **TBD, not budgeted** | No purchase or unsafe low-cost guess |
| **Current software requirement** | **₹0** | Under ₹50,000 cap |

No additional mains wiring, reel or long cable procurement approved. Future reel and electrical protection will require a separately costed safety review.
