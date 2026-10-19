import unittest
from sahayam.mobility.chassis import Chassis
from sahayam.mobility.steering import ackermann

class FrontSteeringTests(unittest.TestCase):
    def test_straight(self):
        a=ackermann(Chassis(),0)
        self.assertEqual((a.front_left_deg,a.front_right_deg),(0,0))
    def test_left_inner_steers_more(self):
        a=ackermann(Chassis(),20)
        self.assertGreater(a.front_left_deg,a.front_right_deg)
        self.assertGreater(a.front_right_deg,0)
    def test_right_inner_steers_more(self):
        a=ackermann(Chassis(),-20)
        self.assertLess(a.front_right_deg,a.front_left_deg)
        self.assertLess(a.front_left_deg,0)
