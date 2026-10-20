"""MOB-019: model validates that arms and attachments are in travel-safe configuration.

This is a supervision model. Mechanical retention and actuator controls
require separate verification before real-world robot motion.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class JointStow:
    measured_angle_deg: float
    travel_angle_deg: float
    tolerance_deg: float
    sensor_healthy: bool
    latch_verified: bool

@dataclass(frozen=True)
class StowObservation:
    joints: tuple[JointStow, ...]
    tool_protrusion_m: float
    maximum_travel_protrusion_m: float
    tool_mount_locked: bool
    gripper_empty: bool
    tray_load_secured: bool
    cable_secured: bool
    tool_cool: bool
    sensors_fresh: bool
    emergency_stop: bool = False

@dataclass(frozen=True)
class StowDecision:
    travel_permitted: bool
    reason: str

def evaluate_travel_stow(obs: StowObservation) -> StowDecision:
    def refuse(reason):
        return StowDecision(False, reason)
    if obs.emergency_stop:
        return refuse("emergency_stop")
    if not obs.sensors_fresh:
        return refuse("sensor_data_stale")
    if not isinstance(obs.joints, tuple) or not obs.joints:
        return refuse("joint_positions_unknown")
    for joint in obs.joints:
        if not isinstance(joint, JointStow):
            return refuse("invalid_joint_report")
        vals = (joint.measured_angle_deg, joint.travel_angle_deg, joint.tolerance_deg)
        if not all(isfinite(v) for v in vals) or joint.tolerance_deg < 0:
            return refuse("invalid_joint_report")
        if not joint.sensor_healthy or not joint.latch_verified:
            return refuse("joint_not_secured")
        if abs(joint.measured_angle_deg - joint.travel_angle_deg) > joint.tolerance_deg:
            return refuse("arm_not_stowed")
    if (not isfinite(obs.tool_protrusion_m)
            or not isfinite(obs.maximum_travel_protrusion_m)
            or min(obs.tool_protrusion_m, obs.maximum_travel_protrusion_m) < 0):
        return refuse("invalid_tool_envelope")
    if obs.tool_protrusion_m > obs.maximum_travel_protrusion_m:
        return refuse("tool_protrudes")
    if not obs.tool_mount_locked:
        return refuse("tool_mount_unlocked")
    if not obs.gripper_empty:
        return refuse("gripper_occupied")
    if not obs.tray_load_secured:
        return refuse("tray_load_unsecured")
    if not obs.cable_secured:
        return refuse("cable_unsecured")
    if not obs.tool_cool:
        return refuse("unsafe_tool_temperature")
    return StowDecision(True, "travel_configuration_verified")

def simulate_stowed_travel(pose, command, chassis, conditions, observation: StowObservation):
    """Apply MOB-019 travel gate to mobility simulator; not physical actuation."""
    from .simulator import Command, simulate_step
    verdict = evaluate_travel_stow(observation)
    guarded = Command(command.speed_mps if verdict.travel_permitted else 0.0,
                      command.steering_deg, command.duration_s)
    return simulate_step(pose, guarded, chassis, conditions), verdict
