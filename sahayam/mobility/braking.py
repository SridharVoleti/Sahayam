"""MOB-020: emergency-braking priority and latched stop semantics.

Commands to stop are simulated; the physical motor-disconnect circuit,
actual braking deceleration and fail-safe hardware are not implemented.
"""
from dataclasses import dataclass
from math import isfinite
from .chassis import Chassis
from .simulator import Pose, Command, SimulationStep, simulate_step
from .speed import MotionConditions

@dataclass(frozen=True)
class BrakeInputs:
    requested_speed_mps: float
    measured_speed_mps: float
    deceleration_mps2: float
    detection_latency_s: float
    person_in_danger: bool
    collision_imminent: bool
    manual_emergency_stop: bool
    sensors_healthy: bool
    physical_stop_circuit_verified: bool
    liquid_spill_risk: bool = False
    carrying_liquid: bool = False

@dataclass(frozen=True)
class BrakeState:
    stop_latched: bool = False

@dataclass(frozen=True)
class BrakeDecision:
    state: BrakeState
    commanded_speed_mps: float
    mode: str
    reason: str
    estimated_stop_distance_m: float | None
    spill_control_deprioritized: bool

def evaluate_braking(
    obs: BrakeInputs, state: BrakeState = BrakeState(),
    *, supervisor_reset: bool = False,
    contained_liquid_speed_mps: float = 0.10
) -> BrakeDecision:
    def result(latched, speed, mode, reason, distance=None, human_priority=False):
        return BrakeDecision(BrakeState(latched), speed, mode, reason,
                             distance, human_priority)
    # Emergency and human hazard override load/spill concerns even if other
    # measurements are invalid. No software action guarantees physical stop.
    severe = (obs.manual_emergency_stop or obs.person_in_danger
              or obs.collision_imminent)
    inputs=(obs.requested_speed_mps,obs.measured_speed_mps,
            obs.deceleration_mps2,obs.detection_latency_s,
            contained_liquid_speed_mps)
    valid=(all(isfinite(v) for v in inputs)
           and obs.requested_speed_mps >= 0 and obs.measured_speed_mps >= 0
           and obs.deceleration_mps2 > 0 and obs.detection_latency_s >= 0
           and contained_liquid_speed_mps > 0)
    distance=(obs.measured_speed_mps * obs.detection_latency_s
              + obs.measured_speed_mps**2 / (2*obs.deceleration_mps2)) if valid else None
    if severe:
        reason=("human_safety_priority" if obs.person_in_danger else
                "manual_emergency_stop" if obs.manual_emergency_stop else
                "imminent_collision")
        return result(True,0,"emergency_stop",reason,distance,
                      bool(obs.person_in_danger and obs.liquid_spill_risk))
    if not valid:
        return result(True,0,"emergency_stop","invalid_brake_data")
    if not obs.sensors_healthy or not obs.physical_stop_circuit_verified:
        return result(True,0,"emergency_stop","brake_safety_unavailable",distance)
    if state.stop_latched:
        if not supervisor_reset or obs.measured_speed_mps > 0:
            return result(True,0,"emergency_stop","reset_required",distance)
        return result(False,0,"rearmed_still_stopped","supervised_reset_complete",distance)
    if obs.carrying_liquid and obs.liquid_spill_risk:
        return result(False,min(obs.requested_speed_mps,contained_liquid_speed_mps),
                      "spill_caution","low_speed_to_reduce_spill_risk",distance)
    return result(False,obs.requested_speed_mps,"normal",
                  "no_emergency_braking_hazard",distance)

def simulate_brake_step(
    pose: Pose, command: Command, chassis: Chassis,
    conditions: MotionConditions, observation: BrakeInputs,
    state: BrakeState = BrakeState(), *,
    supervisor_reset: bool = False
) -> tuple[SimulationStep, BrakeDecision]:
    decision = evaluate_braking(observation,state,supervisor_reset=supervisor_reset)
    gated = Command(min(command.speed_mps, decision.commanded_speed_mps),
                    command.steering_deg,command.duration_s)
    return simulate_step(pose,gated,chassis,conditions),decision
