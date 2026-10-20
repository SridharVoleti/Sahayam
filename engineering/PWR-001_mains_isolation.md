# PWR-001 — 230 V mains tether isolation

**Acceptance:** Treat mains power as hazardous and isolate it from accessible surfaces.
**Status:** Requirements/hazard gate in Python; **actual 230 V tether and physical isolation NOT BUILT OR VALIDATED**.

## Safe prototype strategy
- The initial ₹50,000 modular prototype should use **protected low-voltage motor and control rails** and a commercially approved external adapter/bench supply.
- **Do not place accessible DIY 230 V wiring, homemade reels or exposed power switching in the moving robot.** Household operation with a tether requires a separately engineered architecture.
- This Python module is deliberately incapable of authorizing mains energization, even when all evidence flags are asserted. It only enumerates missing design/safety controls.
- Qualified electrical review and formal test evidence are prerequisites to any actual mains tether prototype, independent of software status.

## Electronics and electrical
- Required future analysis: touch-protected enclosure and double barriers, earthing strategy, protective leakage/fault devices, cable strain relief, reel cable temperature, conductor sizing, ingress/water separation, fault-activated power isolation, stop during outage and safe restoration.
- Verify whether mains is required at all on the moving body versus carrying only isolated DC from an external certified converter.
- **Never infer product safety from a cheap relay, emergency button or insulation claim without supporting rated datasheets, installation calculations and measured results.**
- Electrical designs should be prepared or approved by a suitably qualified professional. No mains switching instructions or wiring diagrams are authorized in this initial stage.

## Mechanical
- Prevent strain, tugging, kinking, wheel crushing, water entry, cable entrapment, sharp edges and hot cooker/tool contact.
- Adjustable tether length depends on robot variant, measured route, thermal and electrical loads and reel construction (PWR-002–PWR-014). A longer cable has higher handling burden, voltage drop and snag exposure.
- Chassis grounding, accessible metal, conductive wet tools and vibration must be considered as a coupled hazard review.

## Software and evidence
- Written 14 tests confirm each missing hazard control prevents a positive review and even complete documentary prerequisites never enable live mains.
- Pending qualified design, electric shock protection, dielectric/continuity tests, fault injection, physical casing, reel and cables, environmental testing, stop-circuit evidence and regulatory review.
- This module does **not** authorize motion on the low-voltage robot either; motor authorization belongs to the combined mobility/safety stack.

## BOM and ₹50,000 accounting
| Choice | First prototype cost | Qualification |
|---|---:|---|
| Existing low-voltage protected supply allocation | **₹0 added** | Reuse `power_safety` ₹5,000 envelope, actual purchase not reported |
| Future moving 230 V tether subsystem and qualified engineering | **TBD, NOT BUDGETED** | No price can responsibly be committed without electrical architecture |
| **Current PWR-001 incremental spending** | **₹0** | Documentation/software only |

**Blocker:** If safe mains tethering cannot be engineered and funded inside ₹50,000, retain low-voltage-only supervised simulation/prototype and defer the mains physical milestone. Never compromise electrical safety to meet the cap.
