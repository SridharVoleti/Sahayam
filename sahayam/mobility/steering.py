"""Ideal low-speed Ackermann geometry; tire slip and interference not simulated."""
from dataclasses import dataclass
from math import atan, degrees, radians, tan
from .chassis import Chassis

@dataclass(frozen=True)
class Steering:
    front_left_deg: float
    front_right_deg: float
    rear_left_deg: float = 0.0
    rear_right_deg: float = 0.0

def ackermann(chassis: Chassis, center_angle_deg: float) -> Steering:
    if not -75 < center_angle_deg < 75:
        raise ValueError("Equivalent steering angle must be strictly within +/-75 degrees")
    if center_angle_deg == 0:
        return Steering(0, 0)
    radius = chassis.wheelbase_m / tan(abs(radians(center_angle_deg)))
    if radius <= chassis.track_m / 2:
        raise ValueError("Requested steering radius is geometrically infeasible")
    inner = degrees(atan(chassis.wheelbase_m / (radius - chassis.track_m / 2)))
    outer = degrees(atan(chassis.wheelbase_m / (radius + chassis.track_m / 2)))
    if center_angle_deg > 0:
        return Steering(inner, outer)
    return Steering(-outer, -inner)
