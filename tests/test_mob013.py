import unittest
from dataclasses import replace
from sahayam.mobility.traction import TractionObservation, evaluate_traction

class TractionTests(unittest.TestCase):
    def setUp(self):
        self.obs = TractionObservation(confidence=0.9, sensor_healthy=True,
                                      observation_fresh=True, requested_speed_mps=0.8)

    def test_normal_traction(self):
        self.assertEqual(evaluate_traction(self.obs).permitted_speed_mps, 0.8)

    def test_uncertain_traction_slows(self):
        d = evaluate_traction(replace(self.obs, confidence=0.6))
        self.assertEqual((d.mode, d.permitted_speed_mps), ("caution", 0.10))

    def test_low_traction_stops(self):
        self.assertEqual(evaluate_traction(replace(self.obs, confidence=0.2)).permitted_speed_mps, 0)

    def test_unknown_sensor_stops(self):
        self.assertEqual(evaluate_traction(replace(self.obs, sensor_healthy=False)).mode, "stop")

    def test_stale_reading_stops(self):
        self.assertEqual(evaluate_traction(replace(self.obs, observation_fresh=False)).mode, "stop")

    def test_heavy_load_low_traction_stops(self):
        self.assertEqual(evaluate_traction(replace(self.obs, confidence=0.6,
                                                  carrying_heavy_load=True)).mode, "stop")

    def test_liquid_low_traction_stops(self):
        self.assertEqual(evaluate_traction(replace(self.obs, confidence=0.6,
                                                  carrying_liquid=True)).mode, "stop")

    def test_emergency_stop(self):
        self.assertEqual(evaluate_traction(replace(self.obs, emergency_stop=True)).mode, "stop")

    def test_nan_stops(self):
        self.assertEqual(evaluate_traction(replace(self.obs, confidence=float("nan"))).mode, "stop")

    def test_invalid_confidence_stops(self):
        self.assertEqual(evaluate_traction(replace(self.obs, confidence=1.2)).mode, "stop")

    def test_never_increases_requested_speed(self):
        self.assertEqual(evaluate_traction(replace(self.obs, confidence=0.6,
                                                  requested_speed_mps=0.04)).permitted_speed_mps, 0.04)

    def test_custom_stop_threshold(self):
        self.assertEqual(evaluate_traction(replace(self.obs, confidence=0.6),
                                          stop_confidence=0.65).mode, "stop")

if __name__ == "__main__":
    unittest.main()
