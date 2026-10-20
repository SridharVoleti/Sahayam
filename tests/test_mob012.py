import unittest
from dataclasses import replace
from sahayam.mobility.threshold import FloorTransition, evaluate_crossing
from sahayam.mobility.stability import StabilityState

class ThresholdTests(unittest.TestCase):
    def setUp(self):
        self.case = FloorTransition(
            measured_step_height_m=0.01,
            maximum_verified_step_height_m=0.02,
            ground_clearance_m=0.04,
            wheel_radius_m=0.10,
            approach_angle_deg=0,
            maximum_verified_approach_angle_deg=15,
            measurement_fresh=True, sensor_healthy=True,
            traction_verified=True, payload_secured=True,
            stability=StabilityState(0.65, 0.50, 0.35))

    def test_supported_crossing_provisional(self):
        self.assertTrue(evaluate_crossing(self.case).permitted)

    def test_oversized_step_refused(self):
        self.assertEqual(evaluate_crossing(replace(self.case, measured_step_height_m=0.03)).reason,
                         "threshold_exceeds_verified_limit")

    def test_clearance_refused(self):
        self.assertEqual(evaluate_crossing(replace(self.case, ground_clearance_m=0.009)).reason,
                         "geometry_clearance_insufficient")

    def test_bad_approach_angle(self):
        self.assertFalse(evaluate_crossing(replace(self.case, approach_angle_deg=25)).permitted)

    def test_sensor_failure(self):
        self.assertFalse(evaluate_crossing(replace(self.case, sensor_healthy=False)).permitted)

    def test_stale_measurement(self):
        self.assertFalse(evaluate_crossing(replace(self.case, measurement_fresh=False)).permitted)

    def test_traction_unknown(self):
        self.assertFalse(evaluate_crossing(replace(self.case, traction_verified=False)).permitted)

    def test_unsecured_payload(self):
        self.assertFalse(evaluate_crossing(replace(self.case, payload_secured=False)).permitted)

    def test_missing_stability(self):
        self.assertFalse(evaluate_crossing(replace(self.case, stability=None)).permitted)

    def test_emergency_stop(self):
        self.assertFalse(evaluate_crossing(replace(self.case, emergency_stop=True)).permitted)

    def test_nan_refused(self):
        self.assertFalse(evaluate_crossing(replace(self.case, measured_step_height_m=float("nan"))).permitted)

    def test_invalid_geometry(self):
        self.assertFalse(evaluate_crossing(replace(self.case, wheel_radius_m=0)).permitted)

if __name__ == "__main__":
    unittest.main()
