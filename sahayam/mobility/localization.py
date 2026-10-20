"""MOB-014: Latched localization-loss stop and conservative recovery.

This is deterministic software policy, not a localization algorithm or a
hardware-certified stop path. Confidence and absolute reference consistency
must come from separately verified sensors.
"""
from dataclasses import dataclass
from math import isfinite
from .simulator import Command, Pose, SimulationStep, simulate_step
from .chassis import Chassis
from .speed import MotionConditions

TRACKING = "tracking"
LOST = "lost"
RECOVERING = "recovering"

@dataclass(frozen=True)
class LocalizationObservation:
    confidence: float
    position_error_m: float
    heading_error_deg: float
    fresh: bool
    sensor_healthy: bool
    absolute_reference_consistent: bool
    robot_stationary: bool
    emergency_stop: bool = False

@dataclass(frozen=True)
class LocalizationState:
    mode: str = LOST
    consecutive_good: int = 0

@dataclass(frozen=True)
class LocalizationDecision:
    state: LocalizationState
    motion_permitted: bool
    reason: str

def evaluate_localization(
    state: LocalizationState,
    observation: LocalizationObservation,
    *,
    recovery_release: bool = False,
    required_good_observations: int = 3,
    min_confidence: float = 0.80,
    max_position_error_m: float = 0.15,
    max_heading_error_deg: float = 10.0,
) -> LocalizationDecision:
    """Require consecutive stationary absolute-reference fixes before rearming.

    Motion remains stopped on the rearm cycle; a following healthy observation
    is required before movement is permitted.
    """
    values = (observation.confidence, observation.position_error_m,
              observation.heading_error_deg, min_confidence,
              max_position_error_m, max_heading_error_deg)
    if (not all(isfinite(v) for v in values)
            or not 0 <= observation.confidence <= 1
            or observation.position_error_m < 0
            or observation.heading_error_deg < 0
            or not 0 < min_confidence <= 1
            or max_position_error_m <= 0 or max_heading_error_deg <= 0
            or not isinstance(required_good_observations, int)
            or isinstance(required_good_observations, bool)
            or required_good_observations < 2
            or state.mode not in (TRACKING, LOST, RECOVERING)
            or not isinstance(state.consecutive_good, int)
            or isinstance(state.consecutive_good, bool)
            or state.consecutive_good < 0):
        return LocalizationDecision(LocalizationState(LOST), False, "invalid_localization_data")
    if observation.emergency_stop:
        return LocalizationDecision(LocalizationState(LOST), False, "emergency_stop")
    good = (observation.fresh and observation.sensor_healthy
            and observation.absolute_reference_consistent
            and observation.confidence >= min_confidence
            and observation.position_error_m <= max_position_error_m
            and observation.heading_error_deg <= max_heading_error_deg)
    if not good:
        return LocalizationDecision(LocalizationState(LOST), False, "localization_lost")
    if state.mode == TRACKING:
        return LocalizationDecision(LocalizationState(TRACKING), True, "localization_healthy")
    if not observation.robot_stationary:
        return LocalizationDecision(LocalizationState(LOST), False, "stationary_recovery_required")
    streak = min(required_good_observations, state.consecutive_good + 1)
    if streak < required_good_observations:
        return LocalizationDecision(LocalizationState(RECOVERING, streak),
                                    False, "accumulating_good_fixes")
    if not recovery_release:
        return LocalizationDecision(LocalizationState(RECOVERING, streak),
                                    False, "recovery_release_required")
    return LocalizationDecision(LocalizationState(TRACKING), False, "rearmed_motion_still_inhibited")

def simulate_localized_step(
    pose: Pose, command: Command, chassis: Chassis,
    conditions: MotionConditions, state: LocalizationState,
    observation: LocalizationObservation, *,
    recovery_release: bool = False
) -> tuple[SimulationStep, LocalizationDecision]:
    """Integrate MOB-014 gate into existing MOB-001..006 kinematics.

    The simulator is not a real actuator inhibit or localization estimator.
    """
    decision = evaluate_localization(
        state, observation, recovery_release=recovery_release)
    gated = Command(command.speed_mps if decision.motion_permitted else 0.0,
                    command.steering_deg, command.duration_s)
    return simulate_step(pose, gated, chassis, conditions), decision
