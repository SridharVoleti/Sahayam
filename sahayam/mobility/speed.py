"""Abstract safety-constrained speed planner; NOT a certified physical controller."""
from dataclasses import dataclass

CRUISE_TARGET_MPS = 0.8
CAUTION_SPEED_MPS = 0.2
TURN_SPEED_MPS = 0.3
LIQUID_LOAD_SPEED_MPS = 0.25

@dataclass(frozen=True)
class MotionConditions:
    clear_route: bool = True
    load_safe: bool = True
    people_nearby: bool = False
    emergency_stop: bool = False
    turning: bool = False
    carrying_liquid: bool = False
    obstacle_nearby: bool = False
    sensor_healthy: bool = True

def allowed_speed_mps(conditions: MotionConditions) -> float:
    """Return maximum commanded speed; multiple hazards combine by taking minimum."""
    if conditions.emergency_stop or not conditions.load_safe or not conditions.sensor_healthy:
        return 0.0
    limits = [CRUISE_TARGET_MPS]
    if conditions.people_nearby or conditions.obstacle_nearby or not conditions.clear_route:
        limits.append(CAUTION_SPEED_MPS)
    if conditions.turning:
        limits.append(TURN_SPEED_MPS)
    if conditions.carrying_liquid:
        limits.append(LIQUID_LOAD_SPEED_MPS)
    return min(limits)
