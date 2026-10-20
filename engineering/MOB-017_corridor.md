# MOB-017 — Shared corridor coordination

**Acceptance:** Multiple robots negotiate narrow passages without deadlock.
**State:** Single-lane exclusive lease and deterministic FIFO queue simulation only; no network or verified real-robot coordination.

## Behavior and safety
- A named robot requests exclusive ownership of a narrow passage. An active owner prevents every other robot from receiving a lease.
- Pending robots wait FIFO, preventing priority-based starvation under normal repeated handoffs.
- Owner must confirm it exited and corridor is independently observed **empty** before releasing for the next robot.
- Stale/expired owner does **not** automatically release: a robot may still be stuck inside. Reclaim requires known expiration, independent vacancy proof, healthy sensors and a supervisor-authorized reset.
- Fail-closed on lost localization, sensor fault, E-stop, unknown occupancy and invalid event ordering.
- Simulated movement in this corridor is gated by active, unexpired ownership. Other collision/localization gates still need to be composed.
- **No unconditional deadlock freedom claim:** a stranded robot or failed vacancy sensor intentionally blocks the passage until manual recovery. Deadlock-safe behavior does not mean bypassing physical uncertainty.

## Electronics
- Initial 2027 prototype uses one chassis and **virtual three-robot agents**; no need to purchase three physical robots.
- Reuse MOB-014 location estimates, MOB-015 obstacle sensors, and same low-voltage controller.
- When three actual robots exist, use local Wi-Fi or wired simulation coordinator with lease acknowledgments, heartbeat, identity and fault isolation; network partition must cause stop/no-entry.
- Low-cost optional corridor status LED can help supervised bench demonstration, but is not a safety signaller.

## Electrical
- Reuse protected sensor and controller rails and motor driver inhibit.
- Do not depend on a Wi-Fi message alone to stop a moving robot; safety-critical robot-local detection and braking required.
- Inconsistent clocks and power loss must not free an occupied corridor automatically.

## Mechanical
- Room survey determines width, door swing, cable interference, accessible retreat/passing bays and minimum stopping distance.
- Shared 10 kg tentative cargo deck and extended tools must fit; cross with MOB-009 doorway and MOB-016 obstacle-inflated planning.
- Verify robot does not block emergency egress in any parked/waiting pose.

## Testing and simulation
- 21 written tests: exclusivity, FIFO, replay/duplicate requests, expired lease and supervisor recovery, sensor faults, E-stop and two virtual agents' simulated movement.
- Pending: distributed-clock/network failure testing, multi-agent timeline animation, formal starvation proof, real sensor integration and physical corridor demonstration.

## Cost ledger — provisional INR
| Candidate equipment | Incremental | Notes |
|---|---:|---|
| Shared robot chassis and sensors | ₹0 | Reused, one physical prototype |
| Virtual Kitchen/Clean/Laundry simulated robots | ₹0 | Python |
| Optional visible passage LED + bracket | ₹0–250 | Not required for safety |
| **Current new spend** | **₹0** | Do not count virtual agents as new hardware |

No quotes, purchases or verified hardware. Keep optional LED within current ₹7,000 controller/sensors envelope. **₹50,000 ceiling unchanged.**
