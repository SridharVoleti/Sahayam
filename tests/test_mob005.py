import unittest
from sahayam.mobility.speed import MotionConditions,allowed_speed_mps

class SpeedTests(unittest.TestCase):
    def test_clear_route_cruise(self):
        self.assertEqual(allowed_speed_mps(MotionConditions()),0.8)
    def test_person_proximity_slows(self):
        self.assertEqual(allowed_speed_mps(MotionConditions(people_nearby=True)),0.2)
    def test_emergency_stop(self):
        self.assertEqual(allowed_speed_mps(MotionConditions(emergency_stop=True)),0)
    def test_unsafe_load_stops(self):
        self.assertEqual(allowed_speed_mps(MotionConditions(load_safe=False)),0)
