"""PWR-003: safe cable payout *planning* model.

No motor, reel or mains cable is energized by this module.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class PayoutInputs:
    current_out_m: float
    route_distance_m: float
    reserve_slack_m: float
    maximum_cable_m: float
    tension_n: float
    maximum_verified_tension_n: float
    elapsed_s: float
    maximum_verified_payout_rate_mps: float
    position_fresh: bool
    tension_sensor_healthy: bool
    route_clear: bool
    cable_thermally_approved: bool
    hands_clear_of_reel: bool
    emergency_stop: bool = False

@dataclass(frozen=True)
class PayoutDecision:
    next_length_m: float
    travel_ready: bool
    reason: str

def plan_payout(inputs: PayoutInputs) -> PayoutDecision:
    def refuse(reason):
        return PayoutDecision(inputs.current_out_m,False,reason)
    vals=(inputs.current_out_m, inputs.route_distance_m,
          inputs.reserve_slack_m, inputs.maximum_cable_m,
          inputs.tension_n, inputs.maximum_verified_tension_n,
          inputs.elapsed_s, inputs.maximum_verified_payout_rate_mps)
    if (not all(isfinite(v) for v in vals)
            or min(inputs.current_out_m,inputs.route_distance_m,
                   inputs.reserve_slack_m,inputs.tension_n) < 0
            or inputs.maximum_cable_m <= 0
            or inputs.current_out_m > inputs.maximum_cable_m
            or inputs.maximum_verified_tension_n <= 0
            or inputs.elapsed_s <= 0
            or inputs.maximum_verified_payout_rate_mps <= 0):
        return refuse("invalid_payout_inputs")
    if inputs.emergency_stop:
        return refuse("emergency_stop")
    if not (inputs.position_fresh and inputs.tension_sensor_healthy
            and inputs.route_clear and inputs.cable_thermally_approved
            and inputs.hands_clear_of_reel):
        return refuse("payout_safety_unavailable")
    if inputs.tension_n >= inputs.maximum_verified_tension_n:
        return refuse("excessive_tension")
    required=inputs.route_distance_m+inputs.reserve_slack_m
    if required>inputs.maximum_cable_m:
        return refuse("route_exceeds_available_cable")
    if required<=inputs.current_out_m:
        return PayoutDecision(inputs.current_out_m,True,"existing_slack_sufficient")
    maximum_extension=(inputs.maximum_verified_payout_rate_mps * inputs.elapsed_s)
    next_length=min(required,inputs.current_out_m+maximum_extension)
    if next_length+1e-9 < required:
        return PayoutDecision(next_length,False,"hold_robot_until_payout_catches_up")
    return PayoutDecision(next_length,True,"payout_length_planned")
