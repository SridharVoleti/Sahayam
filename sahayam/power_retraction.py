"""PWR-004: conservative cable retraction planning, not a powered reel.

Designed to maintain slack and stop retraction when sensing/guarding fails.
Does not implement a physical tension controller or whip/pull prevention.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class RetractionInputs:
    current_out_m: float
    route_distance_m: float
    reserve_slack_m: float
    elapsed_s: float
    maximum_verified_retract_rate_mps: float
    moving_toward_anchor_mps: float
    measured_tension_n: float
    maximum_verified_tension_n: float
    robot_stationary: bool
    supervised_stationary_retraction: bool
    route_fresh: bool
    tension_sensor_healthy: bool
    people_clear: bool
    spool_guard_verified: bool
    reel_thermal_verified: bool
    emergency_stop: bool = False

@dataclass(frozen=True)
class RetractionDecision:
    planned_out_m: float
    reel_motion_planned: bool
    reason: str

def plan_retraction(v: RetractionInputs) -> RetractionDecision:
    def hold(reason):
        return RetractionDecision(v.current_out_m,False,reason)
    nums=(v.current_out_m,v.route_distance_m,v.reserve_slack_m,
          v.elapsed_s,v.maximum_verified_retract_rate_mps,
          v.moving_toward_anchor_mps,v.measured_tension_n,
          v.maximum_verified_tension_n)
    if (not all(isfinite(x) for x in nums)
            or min(v.current_out_m,v.route_distance_m,v.reserve_slack_m,
                   v.moving_toward_anchor_mps,v.measured_tension_n) < 0
            or v.elapsed_s<=0 or v.maximum_verified_retract_rate_mps<=0
            or v.maximum_verified_tension_n<=0):
        return hold("invalid_retraction_inputs")
    if v.emergency_stop:
        return hold("emergency_stop")
    if not (v.route_fresh and v.tension_sensor_healthy and v.people_clear
            and v.spool_guard_verified and v.reel_thermal_verified):
        return hold("retraction_safety_unavailable")
    if v.measured_tension_n>=v.maximum_verified_tension_n:
        return hold("tension_excessive")
    required=v.route_distance_m+v.reserve_slack_m
    if v.current_out_m<=required:
        return hold("reserve_slack_already_at_minimum")
    if v.robot_stationary:
        if not v.supervised_stationary_retraction:
            return hold("stationary_retraction_not_supervised")
        rate=min(v.maximum_verified_retract_rate_mps,0.05)
    else:
        if v.moving_toward_anchor_mps<=0:
            return hold("robot_not_approaching_anchor")
        rate=min(v.maximum_verified_retract_rate_mps,v.moving_toward_anchor_mps)
    target=max(required,v.current_out_m-rate*v.elapsed_s)
    if target>=v.current_out_m:
        return hold("no_retraction_required")
    return RetractionDecision(target,True,"conservative_retraction_planned")
