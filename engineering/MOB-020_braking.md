# MOB-020 — Emergency braking: protect people ahead of spill containment

**Acceptance:** Emergency stop prioritizes human safety over spill containment.

## Safety priority
1. Human danger, imminent collision or pressed emergency switch **latches a stop request**, including when a liquid load could spill. Containment decisions cannot override this.
2. Missing safety sensing or unverified independent stopping path also latches a stop request.
3. Latch can reset only with zero measured speed, healthy diagnostics, no hazard and supervisor permission; reset cycle still commands zero travel.
4. With **only** spill risk and no other emergency, planner caps motion at 0.10 m/s (provisional) instead of an abrupt stop.
5. Model estimates stopping distance from measured speed, assumed reaction delay and assumed deceleration. Default test values 0.25 s and 0.5 m/s² are NOT physical measurements. At 0.8 m/s those assumptions yield 0.84 m of stopping travel before additional margins. **The kinematic simulation instantly commands zero and does not simulate this physical distance.**

## Electronics
- A *normally closed, mechanically latching mushroom emergency-stop* device with verified contact configuration, a correctly rated motor-drive disable / isolation circuit, and independent local fault monitoring are **mandatory before powered movement trials with people nearby**.
- Cheap single-channel Arduino relay boards are not substitutes for a validated safety stop; check DC inductive and stall-current ratings, contact welding failure, wiring short and power-restoration behavior.
- Independent stop should not require Python, Wi-Fi, a camera feed or cloud.
- Human detection and dynamic collision models from MOB-015 also remain unvalidated; never treat them as certified pedestrian sensors.

## Electrical
- Low-voltage prototype only. Switch normally closed circuit to deenergize the motor-drive enable on push, wire break and controller reboot as engineered; validate safe deceleration rather than assuming power-cut causes instant stop.
- The stop may require a motor brake/energy discharge path and protected supply dependent on measured robot mass and motor driver design. Motor stall current, driver and cable sizes are not frozen.
- The user's proposed **230 V mains tether** is outside the present prototype safety qualification and must not be wired by unqualified experiment.
- Wet areas, cookware temperatures and tool power require isolated protected engineering design; outside this test stage.

## Mechanical
- Locate an accessible physical stop without reaching across moving arms; protect button from accidental obstruction.
- 7 kg **inert** cooker-equivalent payload is a future load test only. Ensure falling/sliding cargo or overturning robot does not create a worse injury risk when braking.
- Characterize actual wet-tile stopping distance, wheel load, tire compliance and brake torque before moving near people.

## Prototype budget and supplier benchmarks (checked 2026-10-20)
| Item | Evidence | Cost treatment |
|---|---|---|
| LAY37 22 mm 1NC latching switch | [FlyRobo listing: ₹98](https://www.flyrobo.in/lay37-01zs-1normally-closed-self-locking-22mm-mushroom-head-emergency-stop-switch) | Example listed price, not a quotation/certified solution |
| Metal 1NC emergency switch alternative | [RoboticsDNA listing: ₹354 incl. GST](https://roboticsdna.in/product/22mm-1nc-metal-mushroom-head-emergency-stop-push-switch-f-rotary/) | Example listed price, verify authenticity and datasheet |
| Appropriately engineered motor disable/braking hardware | ₹300–1,500 allowance | Not sourced/validated, **mandatory** |
| Wiring, mounting, connector, protection | ₹300–800 allowance | Estimate only |
| **Indicative total incremental subsystem exposure** | **₹700–2,800** | Must fit existing ₹5,000 power-and-safety allocation |

Example retail buttons lack demonstrated design-level performance here; actual safety functions may require higher-grade components that cost substantially more than allowances. Procurement and powered trials remain **blocked** pending a checked electrical drawing, verified motor and current ratings, and stop tests. The ₹50,000 prototype total **does not increase**.

## Written verification
- 20 tests cover a person approaching during liquid transport, manual emergency switch, collision, sensor loss, invalid braking inputs, stop distance estimates and supervised reset, including simulator stop gating.
- Pending: actually execute test suite and record CI evidence; physical motor stop and measured loaded/wet braking; fail-safe relay tests, time-to-stop measurement and safety review.
- Python success is **not** physical safety evidence.
