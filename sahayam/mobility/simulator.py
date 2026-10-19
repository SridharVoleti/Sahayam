"""Shared 2D kinematic mobility simulator, intended for software verification only.

Coordinates are metres, heading is radians. Uses rear-axle bicycle kinematics.
Not a physical safety controller or a swept-body collision validator.
"""
from dataclasses import dataclass
from math import cos, sin, tan, radians, isfinite
from .chassis import Chassis
from .steering import ackermann
from .speed import MotionConditions, allowed_speed_mps

@dataclass(frozen=True)
class Pose:
    x_m: float = 0.0
    y_m: float = 0.0
    heading_rad: float = 0.0

@dataclass(frozen=True)
class Command:
    speed_mps: float
    steering_deg: float
    duration_s: float

@dataclass(frozen=True)
class SimulationStep:
    pose: Pose
    commanded_speed_mps: float
    allowed_speed_mps: float
    travelled_m: float

def simulate_step(pose: Pose, command: Command, chassis: Chassis,
                  conditions: MotionConditions = MotionConditions()) -> SimulationStep:
    values = (pose.x_m, pose.y_m, pose.heading_rad,
              command.speed_mps, command.steering_deg, command.duration_s)
    if not all(isfinite(v) for v in values):
        raise ValueError("Pose and command must be finite")
    if command.duration_s < 0:
        raise ValueError("Duration must not be negative")
    ackermann(chassis, command.steering_deg)
    speed_limit = allowed_speed_mps(conditions)
    speed = max(0.0, min(command.speed_mps, speed_limit))
    distance = speed * command.duration_s
    if abs(command.steering_deg) < 1e-10:
        new_pose = Pose(pose.x_m + distance*cos(pose.heading_rad),
                        pose.y_m + distance*sin(pose.heading_rad), pose.heading_rad)
    else:
        curvature = tan(radians(command.steering_deg)) / chassis.wheelbase_m
        delta_heading = distance * curvature
        new_heading = pose.heading_rad + delta_heading
        new_pose = Pose(
            pose.x_m + (sin(new_heading)-sin(pose.heading_rad))/curvature,
            pose.y_m + (cos(pose.heading_rad)-cos(new_heading))/curvature,
            new_heading)
    return SimulationStep(new_pose, speed, speed_limit, distance)
