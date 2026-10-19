import unittest
from dataclasses import replace
from sahayam.mobility.reverse import RearEnvironment, evaluate_reverse

class ReverseTravelTests(unittest.TestCase):
    def setUp(self):
        self.safe = RearEnvironment(rear_distance_m=2.0)

    def test_clear_rear_path_allows_reverse(self):
        decision = evaluate_reverse(self.safe)
        self.assertTrue(decision.permitted)
        self.assertEqual(decision.commanded_speed_mps, 0.15)

    def test_reverse_speed_is_capped(self):
        decision = evaluate_reverse(replace(self.safe, requested_reverse_mps=0.7))
        self.assertEqual(decision.commanded_speed_mps, 0.15)

    def test_obstacle_too_close_blocks_reverse(self):
        self.assertFalse(evaluate_reverse(replace(self.safe, rear_distance_m=0.49)).permitted)

    def test_person_behind_blocks_reverse(self):
        self.assertFalse(evaluate_reverse(replace(self.safe, person_behind=True)).permitted)

    def test_pet_behind_blocks_reverse(self):
        self.assertFalse(evaluate_reverse(replace(self.safe, pet_behind=True)).permitted)

    def test_cable_in_path_blocks_reverse(self):
        self.assertFalse(evaluate_reverse(replace(self.safe, cable_in_path=True)).permitted)

    def test_sensor_failure_blocks_reverse(self):
        self.assertFalse(evaluate_reverse(replace(self.safe, rear_sensor_healthy=False)).permitted)

    def test_stale_sensor_blocks_reverse(self):
        self.assertFalse(evaluate_reverse(replace(self.safe, rear_sensor_fresh=False)).permitted)

    def test_unknown_distance_blocks_reverse(self):
        self.assertFalse(evaluate_reverse(replace(self.safe, rear_distance_m=None)).permitted)

    def test_nan_distance_blocks_reverse(self):
        self.assertFalse(evaluate_reverse(replace(self.safe, rear_distance_m=float("nan"))).permitted)

    def test_emergency_stop_blocks_reverse(self):
        self.assertFalse(evaluate_reverse(replace(self.safe, emergency_stop=True)).permitted)

    def test_invalid_speed_blocks_reverse(self):
        self.assertFalse(evaluate_reverse(replace(self.safe, requested_reverse_mps=-1)).permitted)

if __name__ == "__main__":
    unittest.main()
