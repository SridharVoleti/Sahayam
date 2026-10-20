"""MOB-013: conservative traction-confidence speed gate.

Planning-only: traction confidence is an externally supplied estimate, not
measured by this module. Do not use as a certified anti-slip controller.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class TractionObservation:
    confidence: float
    sensor_healthy: bool
    observation_fresh: bool
    requested_speed_mps: float
    carrying_liquid: bool = False
    carrying_heavy_load: bool = False
    emergency_stop: bool = False

@dataclass(frozen=True)
class TractionDecision:
    permitted_speed_mps: float
    mode: str
    reason: str

def evaluate_traction(obs: TractionObservation,
                      cautious_confidence: float = 0.75,
                      stop_confidence: float = 0.40,
                      cautious_speed_mps: float = 0.10) -> TractionDecision:
    def stop(reason: str) -> TractionDecision:
        return TractionDecision(0.0, "stop", reason)
    values = (obs.confidence, obs.requested_speed_mps,
              cautious_confidence, stop_confidence, cautious_speed_mps)
    if not all(isfinite(x) for x in values):
        return stop("invalid_input")
    if (not 0 <= obs.confidence <= 1 or obs.requested_speed_mps < 0
            or not 0 <= stop_confidence < cautious_confidence <= 1
            or cautious_speed_mps <= 0):
        return stop("invalid_limits")
    if obs.emergency_stop:
        return stop("emergency_stop")
    if not obs.sensor_healthy or not obs.observation_fresh:
        return stop("traction_observation_unavailable")
    if obs.confidence < stop_confidence:
        return stop("traction_too_low")
    if obs.confidence < cautious_confidence:
        if obs.carrying_liquid or obs.carrying_heavy_load:
            return stop("loaded_low_traction")
        return TractionDecision(min(obs.requested_speed_mps, cautious_speed_mps),
                                "caution", "reduced_speed_low_confidence")
    return TractionDecision(obs.requested_speed_mps, "normal",
                            "traction_confidence_sufficient")
