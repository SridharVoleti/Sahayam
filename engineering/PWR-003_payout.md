# PWR-003 — Automatic cable payout

**Acceptance:** Pay out cable as routed distance increases while maintaining controlled safe tension.
**State:** Software planning model only. Never energizes a reel or 230 V tether.

## Planning behavior
- Compute required payout as verified traveled route distance + slack reserve.
- Never contract a cable in this payout mode. If available spool length, payout rate or measured tension cannot satisfy current movement, command a **robot-motion hold**, not a forced drag.
- Validate a fresh pose, functioning tension sensor, safe route, reel/cable thermal approval and hands clear of the reel. If any fail, inhibit robot movement.
- Test values (5 N max tension, 1 m/s payout rate) are **external inputs** for simulation, not safety-rated limits.
- Actual control dynamics, spool inertia, cable elasticity, take-up clutch and sensor latency require mechanical model and physical trials.

## Electronics
- Future: low-cost encoder for reel payout length, load/force sensor for tension and motor-driver torque supervision.
- Reuse shared controller and MOB-014 localization input. Do not buy duplicate encoder/IMU.
- A tension sensor must be installed on a properly designed force path, not inferred from uncertain motor current alone.

## Electrical
- Stage one: **unpowered thread/cord payout demonstrator** or isolated low-voltage spool bench rig (no live 230 V cable).
- No open mains reel, DIY 230 V slip ring, DIY rotating mains connectors or exposed live cable operations. PWR-001 electrical safety blocker remains.
- Reel actuators need fused low-voltage supply, mechanical pinch protection and verified inability to tug robot or people when power is lost.

## Mechanical
- Cable reel radius changes as cable layers accumulate; payout length per shaft revolution must be calibrated.
- Route guidance and fairlead, pinch guard, spool clutch/brake, strain relief and extension stops need physical design and independent testing.
- Size spool by real cable diameter and selected length only after PWR-002; long 50 m tether may make spool heavy and costly.

## Cost within ₹50,000
| Prototype-only candidate | Provisional INR | Status |
|---|---:|---|
| Python model, existing controller | ₹0 | Current |
| Unpowered rope/spool mock-up | ₹0–500 | Optional learning demonstrator |
| Future low-voltage motor/encoder/tension-control reel | **TBD** | Design and quote required |
| Motorized mains payout system | **Excluded** | Unqualified and unfunded |

No purchases/quotes. Do not include unpriced future devices as free. Confirm whether a reel is necessary in the first prototype before allocating cost.
## Evidence
18 written tests for safe reserve, rate limiting, maximum length, high tension, thermal/sensor faults and emergency stop.
Pending: Python execution evidence, temporal payout simulation, dashboard animation, power-off tests and physical mechanical/electrical proof.
