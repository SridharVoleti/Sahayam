# MOB-019 — Arm and tool stow for travel

**Acceptance:** Arms/tools enter travel-safe configuration.
**Status:** Python verification gate and kinematic simulator connection. No real arm or sensing hardware.

## Software
- Check each joint is measured near its verified travel angle with configured tolerance and a functioning sensor and mechanical latch.
- Tool extension must remain within its known travel envelope; tool mount must be locked, gripper empty, tray payload secured, cable secured and tool at safe temperature.
- Any stale/invalid sensor, failed latch, extended arm, unsecured cargo or emergency stop forces speed zero in the simulated travel gate.
- Values for joint angles, latches, temperature and tool envelope are supplied by another system. **A Boolean confirmation is not physical proof**.
- Pending: autonomous retract-to-stow actuation, controlled joint sequencing, collision-free arm/tool motions, independent proof of closed latches and stopped motors.

## Electronics
- Reuse educational arm servos (if eventually purchased) and common controller, but basic position-commanded servos may not report actual angular position or independently hold a heavy load.
- Candidate external micro-limit switches or hall sensors for actual travel-position evidence; latch switch for removable tools. Prefer inexpensive simple switches to purchasing extra encoders unless testing requires them.
- Optionally monitor motor current/torque and independent end-stop to detect obstruction; not present in prototype yet.

## Electrical
- Servo stall current and suitable regulated supply must be separately calculated for simultaneous movement.
- Tool-side harness must permit arm folding without pinching cables, coolant or fluids. Cable and connector retention validated with tug tests.
- Latches must remain mechanically secure through power loss; motion inhibition must occur in the motor controller, not only web/Python logic.

## Mechanical
- Fold arms/tools within **measured** doorway and body envelope from MOB-009/MOB-018.
- For a 7 kg cooker, store the load on a secured low cargo cradle, **never carried in an unqualified manipulator during travel**.
- Verify vibration locking, arm weight, servo back-drive, tool clearance and crush/pinch zones.

## Tests
- 18 written tests for joint position/sensor/locking, extension, tool latch, cargo, cable, hot tool and zero simulated motion when un-stowed.
- Pending real motors, actual limit switches, hardware fault injection, arm-sweep tests and browser proof.

## Incremental ₹ budget estimate
| Item | Optional amount | Source allocation |
|---|---:|---|
| Shared servo/control chassis and simulation | ₹0 | Already allocated |
| Joint travel micro-switches / magnets and brackets | ₹150–450 | Shared controller/sensor |
| Locking pin/retention and cable clips | ₹150–400 | Tool interface/fabrication |
| **Future incremental estimate** | **₹0–850** | Within ₹50,000 hard cap |

These are unquoted planning allowances. If the arm cannot hold its own mass, revise the mechanical design instead of treating a switch as a structural solution.
