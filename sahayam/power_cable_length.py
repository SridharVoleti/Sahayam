"""PWR-002: robot-specific cable-length planning and validation.

Planning only. It does not energize 230 V, size conductors, certify insulation,
operate a reel, or validate the physical room layout from measurements.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class CableRoutePlan:
    robot_variant: str
    selected_length_m: float
    route_segment_lengths_m: tuple[float, ...]
    slack_margin_m: float
    route_measured: bool
    route_clear_of_people_and_wheels: bool
    wet_zone_protected: bool
    electrical_approval: bool
    conductor_voltage_drop_verified: bool
    cable_thermal_rating_verified: bool
    reel_thermal_verified: bool
    strain_and_snag_controls_verified: bool
    stop_path_verified: bool

@dataclass(frozen=True)
class CableLengthDecision:
    route_length_sufficient: bool
    plan_accepted_for_review: bool
    mains_energization_authorized: bool
    reason: str
    required_length_m: float | None = None

def evaluate_cable_length(plan: CableRoutePlan) -> CableLengthDecision:
    def deny(reason,required=None,feasible=False):
        return CableLengthDecision(feasible,False,False,reason,required)
    if plan.robot_variant not in ("kitchen","clean","laundry"):
        return deny("unknown_robot_variant")
    if (not isinstance(plan.route_segment_lengths_m,tuple)
            or not plan.route_segment_lengths_m
            or not all(isinstance(v,(int,float)) and isfinite(v) and v>0
                       for v in plan.route_segment_lengths_m)):
        return deny("unverified_route_geometry")
    if (not all(isfinite(v) for v in (plan.selected_length_m,plan.slack_margin_m))
            or plan.selected_length_m <= 0 or plan.slack_margin_m < 0):
        return deny("invalid_cable_length")
    needed=sum(plan.route_segment_lengths_m)+plan.slack_margin_m
    if not isfinite(needed):
        return deny("invalid_cable_length")
    max_study_length=20.0 if plan.robot_variant=="kitchen" else 50.0
    if plan.selected_length_m>max_study_length:
        return deny("outside_provisional_variant_length_study",needed)
    if plan.selected_length_m<needed:
        return deny("insufficient_length_for_measured_route",needed)
    if not plan.route_measured:
        return deny("route_not_physically_verified",needed,True)
    checks=(plan.route_clear_of_people_and_wheels,plan.wet_zone_protected,
            plan.electrical_approval,plan.conductor_voltage_drop_verified,
            plan.cable_thermal_rating_verified,plan.reel_thermal_verified,
            plan.strain_and_snag_controls_verified,plan.stop_path_verified)
    if not all(value is True for value in checks):
        return deny("electrical_thermal_or_route_controls_missing",needed,True)
    return CableLengthDecision(
        True,True,False,"planning_review_complete_no_mains_permission",needed)
