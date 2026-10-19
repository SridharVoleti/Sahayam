"""MOB-007: Conservative rear-clearance reverse authorization.

This is an abstract simulation model, not a hardware safety controller.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class RearEnvironment:
    rear_distance_m: float | None
    rear_sensor_healthy: bool = True
    rear_sensor_fresh: bool = True
    emergency_stop: bool = False
    person_behind: bool = False
    pet_behind: bool = False
    cable_in_path: bool = False
    requested_reverse_mps: float = 0.15

@dataclass(frozen=True)
class ReverseDecision:
    permitted: bool
    commanded_speed_mps: float
    reason: str

REVERSE_SPEED_LIMIT_MPS = 0.15
MIN_REAR_CLEARANCE_M = 0.50

def evaluate_reverse(environment: RearEnvironment) -> ReverseDecision:
    """Stop unless every rear-travel permission gate is satisfied."""
    def stop(reason: str) -> ReverseDecision:
        return ReverseDecision(False, 0.0, reason)

    if environment.emergency_stop:
        return stop("emergency_stop")
    if not environment.rear_sensor_healthy or not environment.rear_sensor_fresh:
        return stop("rear_sensor_unavailable")
    if environment.rear_distance_m is None or not isfinite(environment.rear_distance_m):
        return stop("rear_distance_unknown")
    if environment.person_behind or environment.pet_behind:
        return stop("person_or_pet_behind")
    if environment.cable_in_path:
        return stop("cable_in_reverse_path")
    if environment.rear_distance_m < MIN_REAR_CLEARANCE_M:
        return stop("insufficient_clearance")
    if not isfinite(environment.requested_reverse_mps) or environment.requested_reverse_mps <= 0:
        return stop("invalid_reverse_request")
    return ReverseDecision(True, min(environment.requested_reverse_mps, REVERSE_SPEED_LIMIT_MPS), "clear")
