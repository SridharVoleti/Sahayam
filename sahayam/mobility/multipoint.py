"""MOB-008: Abstract three-point-turn planner for constrained spaces.

Geometric feasibility is a coarse envelope check, not swept-path collision proof.
Every step requires a fresh independent safety clearance before execution.
"""
from dataclasses import dataclass
from math import isfinite
from .reverse import RearEnvironment, evaluate_reverse

@dataclass(frozen=True)
class TurningSpace:
    available_width_m: float
    available_length_m: float
    robot_width_m: float = 0.50
    robot_length_m: float = 0.75
    margin_m: float = 0.15
    front_clear: bool = True
    rear: RearEnvironment = RearEnvironment(rear_distance_m=2.0)
    sensor_healthy: bool = True
    emergency_stop: bool = False

@dataclass(frozen=True)
class TurnStep:
    direction: str
    steering: str
    max_speed_mps: float
    requires_recheck: bool = True

@dataclass(frozen=True)
class TurnPlan:
    feasible: bool
    steps: tuple[TurnStep, ...]
    reason: str

def plan_three_point_turn(space: TurningSpace) -> TurnPlan:
    def blocked(reason: str) -> TurnPlan:
        return TurnPlan(False, (), reason)

    values = (space.available_width_m, space.available_length_m,
              space.robot_width_m, space.robot_length_m, space.margin_m)
    if not all(isfinite(v) and v > 0 for v in values):
        return blocked("invalid_dimensions")
    if space.emergency_stop or not space.sensor_healthy:
        return blocked("safety_unavailable")
    if (space.available_width_m < space.robot_width_m + 2 * space.margin_m
            or space.available_length_m < space.robot_length_m + 2 * space.margin_m):
        return blocked("insufficient_envelope")
    if not space.front_clear:
        return blocked("front_path_blocked")
    reverse = evaluate_reverse(space.rear)
    if not reverse.permitted:
        return blocked("reverse_blocked:" + reverse.reason)
    return TurnPlan(True, (
        TurnStep("forward", "left", 0.15),
        TurnStep("reverse", "right", min(0.15, reverse.commanded_speed_mps)),
        TurnStep("forward", "left", 0.15),
    ), "provisional_plan_requires_swept_path_validation")
