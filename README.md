# Sahayam — Household Robotics

Sahayam is a modular household robotics project with a shared common platform and three specialized robots, developed in this order:

1. **Sahayam Kitchen** — cooking and serving (first reference implementation)
2. **Sahayam Clean** — household and bathroom cleaning
3. **Sahayam Laundry** — washing, drying, folding and organizing clothes

## Requirements baseline

- [Approved functional requirements v1.0](requirements/HOME_MATE_Functional_Specification_v1.0.md) — **271 parent requirements**, **542 proposed verification checks**, and **20 priority simulation scenarios**.
- Approval of a requirement is not evidence of simulation or physical validation.
- Changes must preserve requirement IDs, record rationale and assess regression impact.
- Numerical and safety-critical parameters remain provisional until engineering validation.

## Implementation principles

- Target ~70% reusable platform capability and ~30% robot specialization, without compromising safety.
- Safety is independent of AI and overrides task completion.
- Develop simulations and automated acceptance tests before physical hardware.
- Target integrated household simulation by December 2027; full physical capability is an aspirational December 2033 milestone.

## Next steps

1. Decompose parent requirements into executable, measurable test cases.
2. Define shared interfaces: four-wheel mobility, mains cable management, cooling, tool dock, manipulation, safety, local AI, and coordination.
3. Build and validate simulation scenarios, starting with the Kitchen reference robot.
4. Record test evidence and track passing, failing and not-yet-executed requirements separately.

> **Safety and IP:** The repository is public. Do not publish novel patent-sensitive designs before an appropriate prior-art and disclosure review. Mains electrical, hot appliance, blade and moving robot systems require professional safety assessment before physical use.
