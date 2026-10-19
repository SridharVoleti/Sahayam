"""Steering envelope and geometry-only feasibility checks."""
from .chassis import Chassis
from .steering import ackermann

TARGET_INNER_STEERING_DEG = 75.0

def validate_inner_target(chassis: Chassis, angle_deg: float = TARGET_INNER_STEERING_DEG):
    """Check theoretical wheel angle only, NOT collision clearance or actuator feasibility."""
    if not 0 <= angle_deg < 90:
        raise ValueError("Inner angle must be in [0, 90)")
    from math import radians, tan, atan, degrees
    if angle_deg == 0:
        return {"feasible_kinematically": True, "center_angle_deg": 0.0}
    radius = chassis.track_m / 2 + chassis.wheelbase_m / tan(radians(angle_deg))
    center = degrees(atan(chassis.wheelbase_m / radius))
    actual = ackermann(chassis, center)
    return {"feasible_kinematically": abs(actual.front_left_deg-angle_deg) < 1e-7,
            "center_angle_deg": center,
            "inner_angle_deg": actual.front_left_deg,
            "physical_interference_validated": False}
