"""MOB-009: Conservative doorway clearance envelope check.

Static axis-aligned envelope only; does not validate swept-path, hinges,
thresholds, pose uncertainty, or actual physical dimensions.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Passage:
    clear_width_m: float
    clear_height_m: float
    threshold_height_m: float = 0.0
    measurement_valid: bool = True

@dataclass(frozen=True)
class RobotEnvelope:
    body_width_m: float
    body_height_m: float
    arm_extra_left_m: float = 0.0
    arm_extra_right_m: float = 0.0
    load_extra_left_m: float = 0.0
    load_extra_right_m: float = 0.0
    load_extra_height_m: float = 0.0
    cable_extra_left_m: float = 0.0
    cable_extra_right_m: float = 0.0
    cable_route_verified: bool = False

@dataclass(frozen=True)
class PassageDecision:
    allowed: bool
    reason: str
    required_width_m: float
    required_height_m: float

def assess_doorway(passage: Passage, robot: RobotEnvelope,
                   lateral_margin_m: float = 0.10,
                   overhead_margin_m: float = 0.05) -> PassageDecision:
    values = (passage.clear_width_m, passage.clear_height_m, passage.threshold_height_m,
              robot.body_width_m, robot.body_height_m, robot.arm_extra_left_m,
              robot.arm_extra_right_m, robot.load_extra_left_m, robot.load_extra_right_m,
              robot.load_extra_height_m, robot.cable_extra_left_m, robot.cable_extra_right_m,
              lateral_margin_m, overhead_margin_m)
    if not all(isfinite(v) for v in values) or any(v < 0 for v in values):
        return PassageDecision(False, "invalid_measurements", 0.0, 0.0)
    if robot.body_width_m <= 0 or robot.body_height_m <= 0:
        return PassageDecision(False, "invalid_robot_envelope", 0.0, 0.0)
    width = (robot.body_width_m
             + max(robot.arm_extra_left_m, robot.load_extra_left_m, robot.cable_extra_left_m)
             + max(robot.arm_extra_right_m, robot.load_extra_right_m, robot.cable_extra_right_m)
             + 2 * lateral_margin_m)
    height = robot.body_height_m + robot.load_extra_height_m + overhead_margin_m
    if not passage.measurement_valid:
        return PassageDecision(False, "measurement_unverified", width, height)
    if not robot.cable_route_verified:
        return PassageDecision(False, "cable_route_unverified", width, height)
    if passage.threshold_height_m > 0:
        return PassageDecision(False, "threshold_requires_separate_validation", width, height)
    if passage.clear_width_m < width:
        return PassageDecision(False, "insufficient_width", width, height)
    if passage.clear_height_m < height:
        return PassageDecision(False, "insufficient_height", width, height)
    return PassageDecision(True, "static_envelope_clear_only", width, height)
