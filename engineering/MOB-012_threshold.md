# MOB-012 — Uneven floor transitions

**Requirement:** Detect thresholds and refuse unsupported crossings.
**Status:** Software decision gate only; not a physical traversability demonstration.

## Prototype mechanical design
- Existing provisional wheel radius: 100 mm; provisional chassis clearance used in tests: 40 mm. Neither is a verified production specification.
- Target threshold capability is **TBD from measured home transitions**. The 20 mm verified limit used in tests is synthetic test input, **not a real-world qualified crossing rating**.
- Assess approach/departure angles, front bumper, wheel contact, axle torque, slip, underbody clearance and load retention. Threshold crossing with a 7 kg cooker must separately validate tipping and liquid dynamics.
- Lowering the center of mass improves stability but can reduce underbody clearance; larger wheels improve obstacle approach but can increase chassis height and cost.

## Sensors and electronics
- Candidate downward/forward ToF or optical range sensing plus wheel encoders and the existing MOB-010 IMU.
- Reuse the shared controller and power rails; sensor selection requires testing against reflective/dark flooring and ambient light.
- Detection failure or stale readings cause motion refusal.

## Electrical and safety
- Reuse protected low-voltage sensor supply, existing motor driver and emergency-stop path.
- Independently enforce motor inhibit for unsupported crossings before any unsupervised physical trials.
- Avoid unqualified mains electrical wiring in the mobile prototype.

## Software/simulation and verification
- Code evaluates measurement validity, configured verified step-height limit, ground clearance, wheel radius, approach angle, traction, secured load, MOB-010 stability and emergency-stop status.
- **Pending:** real sensor acquisition, floor profile geometry, drop-off detection, dynamic wheel-climb physics, motor torque, actual obstacle negotiation, dashboard visualization, field measurements and real hardware tests.
- Current model is a conservative heuristic; positive output means provisional planning only.

## Incremental budget estimate — INR
| Candidate item | Planning range | Accounting |
|---|---:|---|
| One extra ToF/distance module and mount (if existing sensors cannot cover floor edge) | ₹300–900 | Future optional |
| Bracket, protective shroud, cable and test threshold pieces | ₹200–500 | Future optional |
| Reused IMU, controller, wheel encoders and motor hardware | ₹0 additional | Shared |
| **Optional incremental hardware** | **₹500–1,400** | Not quoted, purchased or approved |

Allocate any selected parts within the existing ₹7,000 controller/sensors and ₹5,000 tool-interface/fabrication envelopes. Do **not** increase the ₹50,000 budget ceiling. Exact supplier prices, performance and safe crossing height remain unverified.
