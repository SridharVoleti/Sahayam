"""MOB-017: single-lane corridor reservation with FIFO fairness and fail-closed handoff.

Only one robot may hold a corridor lease. Expired leases are NOT silently
released: corridor vacancy must be independently verified before regrant.
"""
from dataclasses import dataclass
from math import isfinite
from .simulator import Pose, Command, SimulationStep, simulate_step
from .chassis import Chassis
from .speed import MotionConditions

@dataclass(frozen=True)
class CorridorState:
    owner: str | None = None
    lease_expires_s: float = 0.0
    waiting: tuple[str, ...] = ()
    last_event_s: float = 0.0

@dataclass(frozen=True)
class CorridorDecision:
    state: CorridorState
    grant: bool
    reason: str

def _valid_robot(robot_id: str) -> bool:
    return (isinstance(robot_id, str) and 0 < len(robot_id) <= 64
            and bool(robot_id.strip()))

def request_corridor(
    state: CorridorState, robot_id: str, now_s: float, *,
    verified_empty: bool, localization_valid: bool,
    sensors_healthy: bool, emergency_stop: bool = False,
    lease_duration_s: float = 20.0
) -> CorridorDecision:
    if (not _valid_robot(robot_id) or not isfinite(now_s)
            or not isfinite(lease_duration_s) or lease_duration_s <= 0
            or now_s < 0 or now_s < state.last_event_s
            or not isfinite(state.lease_expires_s)
            or not isinstance(state.waiting, tuple)
            or any(not _valid_robot(r) for r in state.waiting)
            or len(state.waiting) != len(set(state.waiting))
            or (state.owner is not None and not _valid_robot(state.owner))
            or (state.owner is not None and state.owner in state.waiting)):
        return CorridorDecision(state, False, "invalid_reservation_state")
    if emergency_stop or not localization_valid or not sensors_healthy:
        return CorridorDecision(state, False, "coordination_safety_inhibit")
    queue = state.waiting if robot_id == state.owner or robot_id in state.waiting else state.waiting + (robot_id,)
    updated = CorridorState(state.owner, state.lease_expires_s, queue, now_s)
    if state.owner is not None:
        if state.owner == robot_id:
            if now_s >= state.lease_expires_s:
                return CorridorDecision(updated, False, "lease_expired_requires_clearance")
            return CorridorDecision(updated, True, "existing_exclusive_lease")
        return CorridorDecision(updated, False, "corridor_reserved")
    if not verified_empty:
        return CorridorDecision(updated, False, "corridor_occupancy_not_verified")
    if queue[0] != robot_id:
        return CorridorDecision(updated, False, "waiting_fair_turn")
    grant_state = CorridorState(robot_id, now_s + lease_duration_s, queue[1:], now_s)
    return CorridorDecision(grant_state, True, "exclusive_corridor_lease_granted")

def release_corridor(
    state: CorridorState, robot_id: str, now_s: float, *,
    confirmed_exited: bool, verified_empty: bool
) -> CorridorDecision:
    if (not _valid_robot(robot_id) or not isfinite(now_s)
            or now_s < state.last_event_s or now_s < 0):
        return CorridorDecision(state, False, "invalid_release")
    if state.owner != robot_id:
        return CorridorDecision(state, False, "not_corridor_owner")
    if not confirmed_exited or not verified_empty:
        return CorridorDecision(state, False, "clearance_not_confirmed")
    return CorridorDecision(CorridorState(None, 0.0, state.waiting, now_s),
                            False, "corridor_released")

def simulate_corridor_step(
    state: CorridorState, robot_id: str, now_s: float,
    pose: Pose, command: Command, chassis: Chassis,
    conditions: MotionConditions = MotionConditions(),
) -> SimulationStep:
    """Model exclusive corridor motion; not a physical inter-robot controller."""
    lease_valid = (state.owner == robot_id
                   and isfinite(now_s)
                   and state.last_event_s <= now_s < state.lease_expires_s)
    gated = Command(command.speed_mps if lease_valid else 0.0,
                    command.steering_deg, command.duration_s)
    return simulate_step(pose, gated, chassis, conditions)
