import unittest
from dataclasses import replace
from sahayam.mobility.stability import StabilityState, evaluate_stability

class AntiTipTests(unittest.TestCase):
    def setUp(self):
        self.state = StabilityState(wheelbase_m=0.65, track_m=0.50,
                                    center_of_mass_height_m=0.35)

    def test_stationary_level_ground(self):
        self.assertTrue(evaluate_stability(self.state).motion_permitted)

    def test_lateral_acceleration_tipping_risk(self):
        self.assertFalse(evaluate_stability(replace(self.state, lateral_accel_mps2=7)).motion_permitted)

    def test_longitudinal_acceleration_tipping_risk(self):
        self.assertFalse(evaluate_stability(replace(self.state, longitudinal_accel_mps2=9)).motion_permitted)

    def test_high_center_of_mass_reduces_margin(self):
        low = evaluate_stability(replace(self.state, lateral_accel_mps2=2))
        high = evaluate_stability(replace(self.state, lateral_accel_mps2=2, center_of_mass_height_m=0.8))
        self.assertLess(high.margin_m, low.margin_m)

    def test_offset_load(self):
        self.assertFalse(evaluate_stability(replace(self.state, center_of_mass_y_m=0.23)).motion_permitted)

    def test_slope_effect(self):
        self.assertFalse(evaluate_stability(replace(self.state, slope_lateral_rad=0.6)).motion_permitted)

    def test_unverified_load(self):
        self.assertEqual(evaluate_stability(replace(self.state, load_verified=False)).reason, "stability_data_unavailable")

    def test_sensor_failure(self):
        self.assertFalse(evaluate_stability(replace(self.state, sensor_healthy=False)).motion_permitted)

    def test_emergency_stop(self):
        self.assertFalse(evaluate_stability(replace(self.state, emergency_stop=True)).motion_permitted)

    def test_invalid_geometry(self):
        self.assertFalse(evaluate_stability(replace(self.state, track_m=0)).motion_permitted)

    def test_nonfinite_input(self):
        self.assertFalse(evaluate_stability(replace(self.state, center_of_mass_y_m=float("nan"))).motion_permitted)

    def test_minimum_margin_configurable(self):
        self.assertFalse(evaluate_stability(self.state, minimum_margin_m=0.30).motion_permitted)

if __name__ == "__main__":
    unittest.main()
