import unittest
from dataclasses import replace
from sahayam.power_retraction import RetractionInputs,plan_retraction

class RetractionTests(unittest.TestCase):
    def setUp(self):
        self.v=RetractionInputs(8,5,1,2,0.5,0.4,1,5,
                                False,False,True,True,True,True,True)

    def test_move_toward_anchor_retracts_excess(self):
        d=plan_retraction(self.v)
        self.assertTrue(d.reel_motion_planned)
        self.assertAlmostEqual(d.planned_out_m,7.2)

    def test_maintains_minimum_route_plus_slack(self):
        d=plan_retraction(replace(self.v,current_out_m=6.2,elapsed_s=5))
        self.assertEqual(d.planned_out_m,6)

    def test_never_retracts_when_slack_already_minimal(self):
        d=plan_retraction(replace(self.v,current_out_m=6))
        self.assertFalse(d.reel_motion_planned)

    def test_not_moving_toward_anchor_holds(self):
        d=plan_retraction(replace(self.v,moving_toward_anchor_mps=0))
        self.assertEqual(d.reason,"robot_not_approaching_anchor")

    def test_reel_speed_does_not_exceed_anchor_approach(self):
        d=plan_retraction(replace(self.v,moving_toward_anchor_mps=0.1))
        self.assertAlmostEqual(d.planned_out_m,7.8)

    def test_stationary_retraction_requires_supervision(self):
        d=plan_retraction(replace(self.v,robot_stationary=True))
        self.assertFalse(d.reel_motion_planned)

    def test_supervised_stationary_retraction_uses_low_speed(self):
        d=plan_retraction(replace(self.v,robot_stationary=True,
                                  supervised_stationary_retraction=True))
        self.assertAlmostEqual(d.planned_out_m,7.9)

    def test_high_tension_halts(self):
        d=plan_retraction(replace(self.v,measured_tension_n=5))
        self.assertFalse(d.reel_motion_planned)

    def test_unknown_tension_halts(self):
        d=plan_retraction(replace(self.v,tension_sensor_healthy=False))
        self.assertFalse(d.reel_motion_planned)

    def test_route_stale_halts(self):
        d=plan_retraction(replace(self.v,route_fresh=False))
        self.assertFalse(d.reel_motion_planned)

    def test_people_near_reel_halt(self):
        d=plan_retraction(replace(self.v,people_clear=False))
        self.assertFalse(d.reel_motion_planned)

    def test_no_spool_guard_halt(self):
        d=plan_retraction(replace(self.v,spool_guard_verified=False))
        self.assertFalse(d.reel_motion_planned)

    def test_reel_thermal_unknown_halts(self):
        d=plan_retraction(replace(self.v,reel_thermal_verified=False))
        self.assertFalse(d.reel_motion_planned)

    def test_estop_halts(self):
        d=plan_retraction(replace(self.v,emergency_stop=True))
        self.assertFalse(d.reel_motion_planned)

    def test_negative_tension_refused(self):
        d=plan_retraction(replace(self.v,measured_tension_n=-1))
        self.assertFalse(d.reel_motion_planned)

    def test_nan_route_distance_refused(self):
        d=plan_retraction(replace(self.v,route_distance_m=float("nan")))
        self.assertFalse(d.reel_motion_planned)

    def test_negative_elapsed_time_refused(self):
        d=plan_retraction(replace(self.v,elapsed_s=-1))
        self.assertFalse(d.reel_motion_planned)

    def test_retraction_never_adds_cable(self):
        d=plan_retraction(self.v)
        self.assertLessEqual(d.planned_out_m,self.v.current_out_m)

if __name__=="__main__":
    unittest.main()
