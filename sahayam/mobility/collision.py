"""MOB-015: conservative in-path obstacle approach and braking-speed gate.

Supports 1-D corridor geometry for static and approaching objects only.
No actual sensor, human classifier, steering avoidance or physical brakes.
"""
from dataclasses import dataclass
from math import isfinite, sqrt
from .chassis import Chassis
from .simulator import Pose, Command, SimulationStep, simulate_step
from .speed import MotionConditions

@dataclass(frozen=True)
class Obstacle:
    distance_m: float
    approaching_speed_mps: float = 0.0
    person_or_pet: bool = False
    in_path: bool = True

@dataclass(frozen=True)
class ObstacleObservation:
    obstacles: tuple[Obstacle, ...]
    sensor_healthy: bool
    observation_fresh: bool
    path_geometry_verified: bool
    emergency_stop: bool = False

@dataclass(frozen=True)
class CollisionDecision:
    allowed_speed_mps: float
    reason: str
    limiting_obstacle_index: int | None = None

def avoidance_speed(
    observation: ObstacleObservation,
    requested_speed_mps: float,
    *,
    deceleration_mps2: float = 0.5,
    reaction_s: float = 0.25,
    clearance_m: float = 0.30,
    human_clearance_m: float = 0.80,
) -> CollisionDecision:
    """Constrain requested speed using reaction + braking distance.

    An approaching object's constant closing motion during reaction and braking
    is included. Safety parameters are provisional and require physical tests.
    """
    vals = (requested_speed_mps, deceleration_mps2, reaction_s,
            clearance_m, human_clearance_m)
    if not all(isfinite(x) for x in vals) or requested_speed_mps < 0:
        return CollisionDecision(0, "invalid_speed_or_limits")
    if (deceleration_mps2 <= 0 or reaction_s < 0 or clearance_m < 0
            or human_clearance_m < clearance_m):
        return CollisionDecision(0, "invalid_speed_or_limits")
    if observation.emergency_stop:
        return CollisionDecision(0, "emergency_stop")
    if not (observation.sensor_healthy and observation.observation_fresh
            and observation.path_geometry_verified):
        return CollisionDecision(0, "obstacle_detection_unavailable")
    if not isinstance(observation.obstacles, tuple):
        return CollisionDecision(0, "invalid_obstacles")
    speed = requested_speed_mps
    limiting_index = None
    for i, obstacle in enumerate(observation.obstacles):
        if not isinstance(obstacle, Obstacle) or not all(isfinite(x) for x in
                (obstacle.distance_m, obstacle.approaching_speed_mps)):
            return CollisionDecision(0, "invalid_obstacles", i)
        if obstacle.distance_m < 0:
            return CollisionDecision(0, "invalid_obstacles", i)
        if not obstacle.in_path:
            continue
        distance = obstacle.distance_m
        approach = max(0.0, obstacle.approaching_speed_mps)
        gap = distance - (human_clearance_m if obstacle.person_or_pet else clearance_m)
        # No speed can be safe if an oncoming object can enter the
        # protected distance during the assumed sensing/reaction delay.
        effective = gap - approach * reaction_s
        if effective <= 0:
            return CollisionDecision(0, "protected_distance_or_closing_risk", i)
        coeff = reaction_s + approach / deceleration_mps2
        safe = deceleration_mps2 * (
            sqrt(coeff * coeff + 2 * effective / deceleration_mps2) - coeff)
        safe = max(0.0, safe)
        if safe < speed:
            speed = safe
            limiting_index = i
    if speed == 0 and requested_speed_mps > 0:
        return CollisionDecision(0, "obstacle_requires_stop", limiting_index)
    if speed < requested_speed_mps - 1e-9:
        return CollisionDecision(speed, "obstacle_speed_restricted", limiting_index)
    return CollisionDecision(speed, "no_detected_in_path_collision")

def simulate_avoiding_step(
    pose: Pose, command: Command, chassis: Chassis,
    conditions: MotionConditions, observation: ObstacleObservation
) -> tuple[SimulationStep, CollisionDecision]:
    decision = avoidance_speed(observation, command.speed_mps)
    gated = Command(decision.allowed_speed_mps, command.steering_deg, command.duration_s)
    return simulate_step(pose, gated, chassis, conditions), decision
