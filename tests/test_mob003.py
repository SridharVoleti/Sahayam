import unittest
from sahayam.mobility.chassis import Chassis
from sahayam.mobility.steering import ackermann

class FixedRearTests(unittest.TestCase):
    def test_rear_wheels_remain_straight_for_turns(self):
        for angle in (-30,-15,0,15,30):
            a=ackermann(Chassis(),angle)
            self.assertEqual((a.rear_left_deg,a.rear_right_deg),(0,0))
