import unittest
from sahayam.mobility.speed import MotionConditions, allowed_speed_mps

class SpeedReductionTests(unittest.TestCase):
    def test_people_nearby(self):
        self.assertEqual(allowed_speed_mps(MotionConditions(people_nearby=True)), 0.2)
    def test_turning(self):
        self.assertEqual(allowed_speed_mps(MotionConditions(turning=True)), 0.3)
    def test_liquid_load(self):
        self.assertEqual(allowed_speed_mps(MotionConditions(carrying_liquid=True)), 0.25)
    def test_obstacle(self):
        self.assertEqual(allowed_speed_mps(MotionConditions(obstacle_nearby=True)), 0.2)
    def test_combined_risks_use_lowest_limit(self):
        self.assertEqual(allowed_speed_mps(MotionConditions(turning=True, carrying_liquid=True, people_nearby=True)), 0.2)
    def test_unhealthy_sensor_stops(self):
        self.assertEqual(allowed_speed_mps(MotionConditions(sensor_healthy=False)), 0.0)
    def test_emergency_overrides_all(self):
        self.assertEqual(allowed_speed_mps(MotionConditions(emergency_stop=True, turning=True)), 0.0)
    def test_clear_route_retains_cruise(self):
        self.assertEqual(allowed_speed_mps(MotionConditions()), 0.8)
if __name__ == "__main__":
    unittest.main()
