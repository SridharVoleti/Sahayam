import unittest
from dataclasses import replace
from sahayam.mobility.multipoint import TurningSpace, plan_three_point_turn
from sahayam.mobility.reverse import RearEnvironment

class MultiPointTurnTests(unittest.TestCase):
    def setUp(self):
        self.space = TurningSpace(available_width_m=2.0, available_length_m=3.0)

    def test_three_point_sequence(self):
        plan = plan_three_point_turn(self.space)
        self.assertTrue(plan.feasible)
        self.assertEqual([s.direction for s in plan.steps], ["forward", "reverse", "forward"])
        self.assertEqual([s.steering for s in plan.steps], ["left", "right", "left"])

    def test_steps_require_safety_recheck(self):
        self.assertTrue(all(s.requires_recheck for s in plan_three_point_turn(self.space).steps))

    def test_speed_limits(self):
        self.assertTrue(all(s.max_speed_mps <= 0.15 for s in plan_three_point_turn(self.space).steps))

    def test_narrow_width_rejected(self):
        self.assertFalse(plan_three_point_turn(replace(self.space, available_width_m=0.7)).feasible)

    def test_short_length_rejected(self):
        self.assertFalse(plan_three_point_turn(replace(self.space, available_length_m=1.0)).feasible)

    def test_front_obstacle_rejected(self):
        self.assertFalse(plan_three_point_turn(replace(self.space, front_clear=False)).feasible)

    def test_rear_obstacle_rejected(self):
        self.assertFalse(plan_three_point_turn(replace(self.space, rear=RearEnvironment(0.1))).feasible)

    def test_rear_sensor_fault_rejected(self):
        self.assertFalse(plan_three_point_turn(replace(self.space, rear=RearEnvironment(2.0, rear_sensor_healthy=False))).feasible)

    def test_emergency_stop_rejected(self):
        self.assertFalse(plan_three_point_turn(replace(self.space, emergency_stop=True)).feasible)

    def test_main_sensor_fault_rejected(self):
        self.assertFalse(plan_three_point_turn(replace(self.space, sensor_healthy=False)).feasible)

    def test_invalid_dimensions_rejected(self):
        self.assertFalse(plan_three_point_turn(replace(self.space, available_width_m=float("nan"))).feasible)

    def test_reverse_cable_rejected(self):
        self.assertFalse(plan_three_point_turn(replace(self.space, rear=RearEnvironment(2.0, cable_in_path=True))).feasible)

if __name__ == "__main__":
    unittest.main()
