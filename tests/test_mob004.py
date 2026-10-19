import unittest
from sahayam.mobility.chassis import Chassis
from sahayam.mobility.limits import validate_inner_target

class SteeringLimitTests(unittest.TestCase):
    def test_75_degree_kinematics_not_physical_clearance(self):
        result=validate_inner_target(Chassis())
        self.assertTrue(result["feasible_kinematically"])
        self.assertAlmostEqual(result["inner_angle_deg"],75)
        self.assertFalse(result["physical_interference_validated"])
    def test_invalid_target(self):
        with self.assertRaises(ValueError):
            validate_inner_target(Chassis(),90)
