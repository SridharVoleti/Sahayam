import unittest
from dataclasses import replace
from math import isfinite
from sahayam.mobility.collision import (
    Obstacle, ObstacleObservation, avoidance_speed, simulate_avoiding_step)
from sahayam.mobility.simulator import Pose, Command
from sahayam.mobility.chassis import Chassis
from sahayam.mobility.speed import MotionConditions

class CollisionTests(unittest.TestCase):
    def setUp(self):
        self.clear = ObstacleObservation((), True, True, True)

    def test_clear_path_preserves_speed(self):
        self.assertEqual(avoidance_speed(self.clear, 0.8).allowed_speed_mps, 0.8)

    def test_stationary_obstacle_slows(self):
        d = avoidance_speed(replace(self.clear, obstacles=(Obstacle(0.55),)), 0.8)
        self.assertGreater(d.allowed_speed_mps, 0)
        self.assertLess(d.allowed_speed_mps, 0.8)

    def test_person_needs_extra_clearance(self):
        d = avoidance_speed(replace(self.clear, obstacles=(Obstacle(0.5, person_or_pet=True),)), 0.8)
        self.assertEqual(d.allowed_speed_mps, 0)

    def test_closing_obstacle_restricts_more_than_stationary(self):
        static = avoidance_speed(replace(self.clear, obstacles=(Obstacle(1.2),)), 0.8)
        moving = avoidance_speed(replace(self.clear, obstacles=(Obstacle(1.2, 1.0),)), 0.8)
        self.assertLess(moving.allowed_speed_mps, static.allowed_speed_mps)

    def test_obstacle_in_protected_zone_stops(self):
        d = avoidance_speed(replace(self.clear, obstacles=(Obstacle(0.3),)), 0.8)
        self.assertEqual(d.reason, "protected_distance_or_closing_risk")

    def test_out_of_path_object_does_not_slow(self):
        d = avoidance_speed(replace(self.clear, obstacles=(Obstacle(0.1, in_path=False),)), 0.8)
        self.assertEqual(d.allowed_speed_mps, 0.8)

    def test_stale_sensor_stops(self):
        d = avoidance_speed(replace(self.clear, observation_fresh=False), 0.8)
        self.assertEqual(d.allowed_speed_mps, 0)

    def test_faulty_sensor_stops(self):
        d = avoidance_speed(replace(self.clear, sensor_healthy=False), 0.8)
        self.assertEqual(d.allowed_speed_mps, 0)

    def test_path_geometry_unknown_stops(self):
        d = avoidance_speed(replace(self.clear, path_geometry_verified=False), 0.8)
        self.assertEqual(d.allowed_speed_mps, 0)

    def test_emergency_stop(self):
        self.assertEqual(avoidance_speed(replace(self.clear, emergency_stop=True), 0.8).allowed_speed_mps, 0)

    def test_invalid_range_fails_closed(self):
        d = avoidance_speed(replace(self.clear, obstacles=(Obstacle(float("nan")),)), 0.8)
        self.assertEqual(d.reason, "invalid_obstacles")

    def test_invalid_braking_deceleration_fails_closed(self):
        self.assertEqual(avoidance_speed(self.clear, 0.8, deceleration_mps2=0).allowed_speed_mps, 0)

    def test_never_exceeds_requested_speed(self):
        d = avoidance_speed(replace(self.clear, obstacles=(Obstacle(10),)), 0.07)
        self.assertLessEqual(d.allowed_speed_mps, 0.07)

    def test_multiple_obstacles_choose_closest_risk(self):
        d = avoidance_speed(replace(self.clear, obstacles=(Obstacle(3), Obstacle(0.5))), 0.8)
        self.assertEqual(d.limiting_obstacle_index, 1)

    def test_simulator_stops_before_person(self):
        obs = replace(self.clear, obstacles=(Obstacle(0.5, person_or_pet=True),))
        sim, _ = simulate_avoiding_step(Pose(), Command(0.8, 0, 1),
                                         Chassis(), MotionConditions(), obs)
        self.assertEqual(sim.travelled_m, 0)

    def test_simulation_moves_with_clear_route(self):
        sim, _ = simulate_avoiding_step(Pose(), Command(0.8, 0, 1),
                                         Chassis(), MotionConditions(), self.clear)
        self.assertAlmostEqual(sim.travelled_m, 0.8)

    def test_oncoming_object_before_reaction_requires_stop(self):
        obs = replace(self.clear, obstacles=(Obstacle(0.6, 1.5),))
        self.assertEqual(avoidance_speed(obs, 0.8).allowed_speed_mps, 0)

    def test_invalid_obstacle_container_fails_closed(self):
        obs = replace(self.clear, obstacles=[])
        self.assertEqual(avoidance_speed(obs, 0.8).allowed_speed_mps, 0)

if __name__ == "__main__":
    unittest.main()
