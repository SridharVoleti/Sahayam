import unittest
from dataclasses import replace
from sahayam.power_cable_tracking import (
    CablePathObservation,evaluate_cable_route)

class CableTrackingTests(unittest.TestCase):
    def setUp(self):
        self.obs=CablePathObservation(
            cable_points=((0.,0.),(0.,2.)),
            planned_robot_points=((2.,0.),(2.,2.)),
            cable_route_fresh=True,localization_valid=True,
            sensors_healthy=True,cable_fully_observed=True,
            wheel_envelope_verified=True,cable_under_robot=False,
            snag_detected=False)

    def test_parallel_non_crossing_routes(self):
        self.assertTrue(evaluate_cable_route(self.obs).route_permitted_for_planning)

    def test_robot_crosses_tether_rejected(self):
        obs=replace(self.obs,planned_robot_points=((-1.,1.),(1.,1.)))
        self.assertEqual(evaluate_cable_route(obs).reason,"planned_route_crosses_tether")

    def test_endpoint_touch_conservatively_rejected(self):
        obs=replace(self.obs,planned_robot_points=((1.,2.),(0.,2.)))
        self.assertFalse(evaluate_cable_route(obs).route_permitted_for_planning)

    def test_self_crossing_tether_rejected(self):
        pts=((0.,0.),(2.,2.),(0.,2.),(2.,0.))
        self.assertEqual(evaluate_cable_route(
            replace(self.obs,cable_points=pts)).reason,"self_crossing_cable_route")

    def test_under_wheel_cable_hazard(self):
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,cable_under_robot=True)).route_permitted_for_planning)

    def test_snag_hazard(self):
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,snag_detected=True)).route_permitted_for_planning)

    def test_cable_route_stale(self):
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,cable_route_fresh=False)).route_permitted_for_planning)

    def test_loss_of_localization(self):
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,localization_valid=False)).route_permitted_for_planning)

    def test_sensor_fault(self):
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,sensors_healthy=False)).route_permitted_for_planning)

    def test_cable_partly_unobserved(self):
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,cable_fully_observed=False)).route_permitted_for_planning)

    def test_wheel_envelope_unknown(self):
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,wheel_envelope_verified=False)).route_permitted_for_planning)

    def test_estop(self):
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,emergency_stop=True)).route_permitted_for_planning)

    def test_invalid_cable_route(self):
        self.assertEqual(evaluate_cable_route(
            replace(self.obs,cable_points=((0.,0.),))).reason,
            "invalid_cable_or_robot_path")

    def test_nan_position(self):
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,cable_points=((0.,0.),(float("nan"),1.)))).route_permitted_for_planning)

    def test_degenerate_segment(self):
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,cable_points=((0.,0.),(0.,0.)))).route_permitted_for_planning)

    def test_multiple_robot_segments(self):
        route=((2.,0.),(3.,1.),(2.,2.))
        self.assertTrue(evaluate_cable_route(
            replace(self.obs,planned_robot_points=route)).route_permitted_for_planning)

    def test_collinear_cable_and_robot_overlap_denied(self):
        route=((0.,0.5),(0.,1.5))
        self.assertFalse(evaluate_cable_route(
            replace(self.obs,planned_robot_points=route)).route_permitted_for_planning)

if __name__=="__main__":
    unittest.main()
