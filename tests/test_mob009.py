import unittest
from dataclasses import replace
from sahayam.mobility.doorway import Passage, RobotEnvelope, assess_doorway

class DoorwayClearanceTests(unittest.TestCase):
    def setUp(self):
        self.door = Passage(1.0, 2.0)
        self.robot = RobotEnvelope(0.5, 1.2, cable_route_verified=True)

    def test_clear_doorway(self):
        self.assertTrue(assess_doorway(self.door, self.robot).allowed)

    def test_narrow_doorway(self):
        self.assertEqual(assess_doorway(replace(self.door, clear_width_m=0.6), self.robot).reason, "insufficient_width")

    def test_low_doorway(self):
        self.assertEqual(assess_doorway(replace(self.door, clear_height_m=1.0), self.robot).reason, "insufficient_height")

    def test_extended_arm(self):
        robot = replace(self.robot, arm_extra_left_m=0.4)
        self.assertFalse(assess_doorway(self.door, robot).allowed)

    def test_load_overhang(self):
        robot = replace(self.robot, load_extra_right_m=0.4)
        self.assertFalse(assess_doorway(self.door, robot).allowed)

    def test_cable_overhang(self):
        robot = replace(self.robot, cable_extra_right_m=0.4)
        self.assertFalse(assess_doorway(self.door, robot).allowed)

    def test_cable_route_not_verified(self):
        robot = replace(self.robot, cable_route_verified=False)
        self.assertEqual(assess_doorway(self.door, robot).reason, "cable_route_unverified")

    def test_unmeasured_doorway(self):
        self.assertFalse(assess_doorway(replace(self.door, measurement_valid=False), self.robot).allowed)

    def test_threshold_requires_validation(self):
        self.assertFalse(assess_doorway(replace(self.door, threshold_height_m=0.02), self.robot).allowed)

    def test_invalid_dimension(self):
        self.assertFalse(assess_doorway(replace(self.door, clear_width_m=float("nan")), self.robot).allowed)

    def test_invalid_robot_dimension(self):
        self.assertFalse(assess_doorway(self.door, replace(self.robot, body_width_m=0)).allowed)

    def test_margin_included(self):
        result = assess_doorway(self.door, self.robot)
        self.assertAlmostEqual(result.required_width_m, 0.7)

if __name__ == "__main__":
    unittest.main()
