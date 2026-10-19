"""Conservative nominal speed limiter for an abstract simulation."""
from dataclasses import dataclass

CRUISE_TARGET_MPS = 0.8

@dataclass(frozen=True)
class MotionConditions:
    clear_route: bool = True
    load_safe: bool = True
    people_nearby: bool = False
    emergency_stop: bool = False

def allowed_speed_mps(conditions: MotionConditions) -> float:
    if conditions.emergency_stop or not conditions.load_safe:
        return 0.0
    if conditions.people_nearby or not conditions.clear_route:
        return 0.2
    return CRUISE_TARGET_MPS
