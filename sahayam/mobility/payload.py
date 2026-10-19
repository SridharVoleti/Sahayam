"""MOB-011: conservative multi-trip payload planning, software-only.

Mass estimates and limits must be externally verified; this planner does not
weigh objects, actuate lifting, or certify dynamic stability.
"""
from dataclasses import dataclass
from math import isfinite, ceil
from .stability import StabilityState, evaluate_stability

@dataclass(frozen=True)
class PayloadTask:
    total_mass_kg: float
    divisible: bool
    measured_mass: bool = False
    trip_capacity_kg: float = 0.0
    manipulator_capacity_kg: float = 0.0
    load_center_height_m: float = 0.0
    stability: StabilityState | None = None
    maximum_trips: int = 100

@dataclass(frozen=True)
class PayloadPlan:
    permitted: bool
    trip_masses_kg: tuple[float, ...]
    reason: str

def plan_payload(task: PayloadTask) -> PayloadPlan:
    def blocked(reason: str) -> PayloadPlan:
        return PayloadPlan(False, (), reason)
    vals = (task.total_mass_kg, task.trip_capacity_kg,
            task.manipulator_capacity_kg, task.load_center_height_m)
    if not all(isfinite(v) for v in vals) or task.total_mass_kg <= 0 or min(vals[1:]) < 0:
        return blocked("invalid_payload_data")
    if not task.measured_mass:
        return blocked("mass_not_verified")
    if task.trip_capacity_kg <= 0 or task.manipulator_capacity_kg <= 0:
        return blocked("capacity_not_verified")
    if task.stability is None:
        return blocked("stability_not_verified")
    if not evaluate_stability(task.stability).motion_permitted:
        return blocked("stability_margin_inadequate")
    if task.load_center_height_m > task.stability.center_of_mass_height_m:
        return blocked("loaded_center_of_mass_not_verified")
    capacity = min(task.trip_capacity_kg, task.manipulator_capacity_kg)
    if not task.divisible and task.total_mass_kg > capacity:
        return blocked("indivisible_overweight")
    n = ceil(task.total_mass_kg / capacity) if task.divisible else 1
    if not isinstance(task.maximum_trips, int) or isinstance(task.maximum_trips, bool) or task.maximum_trips <= 0 or n > task.maximum_trips:
        return blocked("trip_count_exceeded")
    # Equal batches avoid accumulating rounding error and keep each trip below limit.
    masses = tuple(task.total_mass_kg / n for _ in range(n))
    if any(m > capacity + 1e-9 for m in masses):
        return blocked("batch_capacity_exceeded")
    return PayloadPlan(True, masses, "provisional_batches_require_per_trip_recheck")

def verify_trip(plan: PayloadPlan, trip_index: int, actual_mass_kg: float,
                capacity_kg: float, stability: StabilityState) -> bool:
    if not plan.permitted or not 0 <= trip_index < len(plan.trip_masses_kg):
        return False
    if not all(isfinite(v) for v in (actual_mass_kg, capacity_kg)):
        return False
    return (0 < actual_mass_kg <= capacity_kg
            and actual_mass_kg <= plan.trip_masses_kg[trip_index] + 1e-9
            and evaluate_stability(stability).motion_permitted)
