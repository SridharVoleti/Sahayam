"""MOB-010: Conservative quasi-static anti-tip motion authorization.

This simplified model uses the rectangular wheel contact footprint and a
projected center of gravity. It does not model suspension, dynamic slosh,
wheel lift, compliant tires or transient impact. Not a certified controller.
"""
from dataclasses import dataclass
from math import isfinite

GRAVITY_MPS2 = 9.80665

@dataclass(frozen=True)
class StabilityState:
    wheelbase_m: float
    track_m: float
    center_of_mass_height_m: float
    center_of_mass_x_m: float = 0.0
    center_of_mass_y_m: float = 0.0
    longitudinal_accel_mps2: float = 0.0
    lateral_accel_mps2: float = 0.0
    slope_longitudinal_rad: float = 0.0
    slope_lateral_rad: float = 0.0
    sensor_healthy: bool = True
    load_verified: bool = True
    emergency_stop: bool = False

@dataclass(frozen=True)
class StabilityDecision:
    motion_permitted: bool
    margin_m: float
    reason: str

def evaluate_stability(state: StabilityState, minimum_margin_m: float = 0.05) -> StabilityDecision:
    from math import tan
    values = (state.wheelbase_m, state.track_m, state.center_of_mass_height_m,
              state.center_of_mass_x_m, state.center_of_mass_y_m,
              state.longitudinal_accel_mps2, state.lateral_accel_mps2,
              state.slope_longitudinal_rad, state.slope_lateral_rad, minimum_margin_m)
    if not all(isfinite(v) for v in values) or minimum_margin_m < 0:
        return StabilityDecision(False, 0.0, "invalid_state")
    if min(state.wheelbase_m, state.track_m, state.center_of_mass_height_m) <= 0:
        return StabilityDecision(False, 0.0, "invalid_geometry")
    if state.emergency_stop:
        return StabilityDecision(False, 0.0, "emergency_stop")
    if not state.sensor_healthy or not state.load_verified:
        return StabilityDecision(False, 0.0, "stability_data_unavailable")
    # Reject near-vertical slopes rather than allowing tan() singularities.
    if abs(state.slope_longitudinal_rad) >= 1.4 or abs(state.slope_lateral_rad) >= 1.4:
        return StabilityDecision(False, 0.0, "slope_out_of_model")
    projected_x = (state.center_of_mass_x_m
                   - state.center_of_mass_height_m *
                   (state.longitudinal_accel_mps2 / GRAVITY_MPS2
                    + tan(state.slope_longitudinal_rad)))
    projected_y = (state.center_of_mass_y_m
                   - state.center_of_mass_height_m *
                   (state.lateral_accel_mps2 / GRAVITY_MPS2
                    + tan(state.slope_lateral_rad)))
    margin = min(state.wheelbase_m / 2 - abs(projected_x),
                 state.track_m / 2 - abs(projected_y))
    if not isfinite(margin):
        return StabilityDecision(False, 0.0, "invalid_projection")
    if margin < minimum_margin_m:
        return StabilityDecision(False, margin, "insufficient_stability_margin")
    return StabilityDecision(True, margin, "quasistatic_margin_sufficient")
