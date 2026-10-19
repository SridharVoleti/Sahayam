# SAHAYAM — ₹50,000 prototype budget tracker

Source of truth: [prototype_budget.json](prototype_budget.json). This is a **planning ledger**, not a record of purchases. Update it after each requirement with incremental equipment, reused hardware, vendor quotations and actual invoices.

| Allocation | Planned ₹ | Quoted ₹ | Purchased ₹ |
|---|---:|---:|---:|
| Chassis, drive and steering | 12,000 | 0 | 0 |
| Controller and sensors | 7,000 | 0 | 0 |
| Low-voltage power and safety | 5,000 | 0 | 0 |
| Basic robotic arm | 7,000 | 0 | 0 |
| Cleaning tool prototype | 5,000 | 0 | 0 |
| Tool interface and fabrication | 5,000 | 0 | 0 |
| Contingency | 9,000 | 0 | 0 |
| **Total** | **50,000** | **0** | **0** |

**Unallocated budget: ₹0** (all ₹50,000 assigned to provisional envelopes). **Unspent cash: ₹50,000** (no purchases recorded). These are different concepts.

## Update rules
1. Each new requirement gets an incremental BOM estimate, existing/reused component IDs, and subsystem budget impact.
2. Quotes must include vendor, URL, quantity, shipping/tax treatment, quote date and currency. Do not record an estimate as a quote.
3. Purchases require date, quantity, actual total cost and invoice/receipt reference.
4. Never count the same shared component twice. If the design exceeds an envelope, propose substitutions or reallocations before buying.
5. Keep safety-critical systems as mandatory requirements; mark any unfunded safety hardware as a blocker, not as implicitly satisfied.
6. Distinguish simulated verification, benchtop verification and real household operation.

The previously discussed ~₹18,000 mobility working estimate is a *cross-cutting estimate* and must not be added on top of this ₹50,000 allocation.
