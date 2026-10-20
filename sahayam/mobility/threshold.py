"""MOB-012: Conservative threshold crossing authorization.

Software planning only: no sensor driver, wheel-contact simulation, or
physical proof of traversability. All capabilities require independent tests.
"""
from dataclasses import dataclass
from math import isfinite
from .stability import StabilityState, evaluate_stability

@dataclass(frozen=True)
class FloorTransition:
    measured_step_height_m: float
    maximum_verified_step_height_m: float
    ground_clearance_m: float
    wheel_radius_m: float
    approach_angle_deg: float
    maximum_verified_approach_angle_deg: float
    measurement_fresh: bool = False
    sensor_healthy: bool = False
    traction_verified: bool = False
    payload_secured: bool = False
    stability: StabilityState | None = None
    emergency_stop: bool = False

@dataclass(frozen=True)
class CrossingDecision:
    permitted: bool
    reason: str

def evaluate_crossing(t: FloorTransition) -> CrossingDecision:
    def refuse(reason: str) -> CrossingDecision:
        return CrossingDecision(False, reason)
    values = (t.measured_step_height_m, t.maximum_verified_step_height_m,
              t.ground_clearance_m, t.wheel_radius_m, t.approach_angle_deg,
              t.maximum_verified_approach_angle_deg)
    if not all(isfinite(v) for v in values):
        return refuse("invalid_measurement")
    if (t.measured_step_height_m < 0 or t.maximum_verified_step_height_m <= 0
            or t.ground_clearance_m <= 0 or t.wheel_radius_m <= 0
            or not 0 <= t.approach_angle_deg <= 90
            or not 0 < t.maximum_verified_approach_angle_deg <= 90):
        return refuse("invalid_geometry_or_limit")
    if t.emergency_stop:
        return refuse("emergency_stop")
    if not t.sensor_healthy or not t.measurement_fresh:
        return refuse("threshold_detection_unavailable")
    if not t.traction_verified or not t.payload_secured:
        return refuse("crossing_conditions_unverified")
    if t.stability is None or not evaluate_stability(t.stability).motion_permitted:
        return refuse("stability_not_verified")
    if t.measured_step_height_m > t.maximum_verified_step_height_m:
        return refuse("threshold_exceeds_verified_limit")
    if t.measured_step_height_m >= min(t.ground_clearance_m, t.wheel_radius_m):
        return refuse("geometry_clearance_insufficient")
    if t.approach_angle_deg > t.maximum_verified_approach_angle_deg:
        return refuse("approach_angle_unsupported")
    return CrossingDecision(True, "provisional_crossing_requires_runtime_recheck")
