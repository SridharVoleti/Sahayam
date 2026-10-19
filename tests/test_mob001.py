import unittest
from sahayam.mobility.chassis import Chassis

class FourWheelTests(unittest.TestCase):
    def test_exactly_four_named_wheels(self):
        self.assertEqual(set(Chassis().wheels), {"front_left","front_right","rear_left","rear_right"})
    def test_positions_unique(self):
        self.assertEqual(len(set(Chassis().wheels.values())), 4)
    def test_invalid_geometry_rejected(self):
        with self.assertRaises(ValueError):
            Chassis(track_m=0)
