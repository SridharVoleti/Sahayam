import unittest
from dataclasses import replace
from sahayam.mobility.payload import PayloadTask, plan_payload, verify_trip
from sahayam.mobility.stability import StabilityState

class PayloadTests(unittest.TestCase):
    def setUp(self):
        self.stability = StabilityState(0.65, 0.50, 0.35)
        self.task = PayloadTask(3, True, True, 1, 1, 0.25, self.stability)

    def test_three_trips(self):
        self.assertEqual(plan_payload(self.task).trip_masses_kg, (1, 1, 1))

    def test_single_safe_load(self):
        self.assertEqual(len(plan_payload(replace(self.task, total_mass_kg=0.5)).trip_masses_kg), 1)

    def test_indivisible_overweight(self):
        self.assertEqual(plan_payload(replace(self.task, divisible=False)).reason, "indivisible_overweight")

    def test_unmeasured_load(self):
        self.assertFalse(plan_payload(replace(self.task, measured_mass=False)).permitted)

    def test_no_manipulator_capacity(self):
        self.assertFalse(plan_payload(replace(self.task, manipulator_capacity_kg=0)).permitted)

    def test_stability_missing(self):
        self.assertFalse(plan_payload(replace(self.task, stability=None)).permitted)

    def test_unstable(self):
        unstable = replace(self.stability, center_of_mass_y_m=0.24)
        self.assertFalse(plan_payload(replace(self.task, stability=unstable)).permitted)

    def test_high_load_center_unverified(self):
        self.assertFalse(plan_payload(replace(self.task, load_center_height_m=0.5)).permitted)

    def test_trip_count_cap(self):
        self.assertFalse(plan_payload(replace(self.task, maximum_trips=2)).permitted)

    def test_invalid_mass(self):
        self.assertFalse(plan_payload(replace(self.task, total_mass_kg=float("nan"))).permitted)

    def test_verify_each_trip(self):
        plan = plan_payload(self.task)
        self.assertTrue(verify_trip(plan, 0, 1, 1, self.stability))
        self.assertFalse(verify_trip(plan, 1, 1.2, 1, self.stability))

    def test_trip_index_out_of_range(self):
        self.assertFalse(verify_trip(plan_payload(self.task), 3, 1, 1, self.stability))

if __name__ == "__main__":
    unittest.main()
