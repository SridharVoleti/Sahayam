import unittest
from math import pi
from sahayam.mobility.chassis import Chassis
from sahayam.mobility.simulator import Pose, Command, simulate_step
from sahayam.mobility.speed import MotionConditions

class MobilityIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.chassis = Chassis()

    def test_straight_line_moves_forward(self):
        result = simulate_step(Pose(), Command(0.8, 0, 2), self.chassis)
        self.assertAlmostEqual(result.pose.x_m, 1.6)
        self.assertAlmostEqual(result.pose.y_m, 0)

    def test_heading_rotates_motion(self):
        result = simulate_step(Pose(0, 0, pi/2), Command(0.8, 0, 1), self.chassis)
        self.assertAlmostEqual(result.pose.y_m, 0.8)

    def test_steering_produces_arc(self):
        result = simulate_step(Pose(), Command(0.3, 20, 1), self.chassis)
        self.assertGreater(result.pose.heading_rad, 0)
        self.assertGreater(result.pose.y_m, 0)

    def test_liquid_speed_cap(self):
        result = simulate_step(Pose(), Command(0.8, 0, 1), self.chassis,
                               MotionConditions(carrying_liquid=True))
        self.assertAlmostEqual(result.travelled_m, 0.25)

    def test_emergency_stop(self):
        result = simulate_step(Pose(), Command(0.8, 0, 1), self.chassis,
                               MotionConditions(emergency_stop=True))
        self.assertEqual(result.travelled_m, 0)

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            simulate_step(Pose(), Command(0.1, 0, -1), self.chassis)

    def test_invalid_steering(self):
        with self.assertRaises(ValueError):
            simulate_step(Pose(), Command(0.1, 76, 1), self.chassis)

    def test_nonfinite_command(self):
        with self.assertRaises(ValueError):
            simulate_step(Pose(), Command(float("nan"), 0, 1), self.chassis)

if __name__ == "__main__":
    unittest.main()
