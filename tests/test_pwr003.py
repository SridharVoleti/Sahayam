import unittest
from dataclasses import replace
from sahayam.power_payout import PayoutInputs,plan_payout

class PayoutTests(unittest.TestCase):
    def setUp(self):
        self.v=PayoutInputs(4,4.5,0.5,20,1,5,2,1,
                            True,True,True,True,True)

    def test_sufficient_existing_slack(self):
        v=replace(self.v,route_distance_m=3)
        d=plan_payout(v)
        self.assertTrue(d.travel_ready)
        self.assertEqual(d.next_length_m,4)

    def test_payout_to_required_length(self):
        d=plan_payout(self.v)
        self.assertTrue(d.travel_ready)
        self.assertEqual(d.next_length_m,5)

    def test_rate_limited_payout_stops_travel(self):
        d=plan_payout(replace(self.v,route_distance_m=9))
        self.assertFalse(d.travel_ready)
        self.assertEqual(d.next_length_m,6)

    def test_overlength_route_rejected(self):
        d=plan_payout(replace(self.v,route_distance_m=25))
        self.assertEqual(d.reason,"route_exceeds_available_cable")

    def test_high_tension_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,tension_n=6)).travel_ready)

    def test_equal_to_tension_limit_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,tension_n=5)).travel_ready)

    def test_sensor_fault_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,tension_sensor_healthy=False)).travel_ready)

    def test_position_stale_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,position_fresh=False)).travel_ready)

    def test_route_not_clear_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,route_clear=False)).travel_ready)

    def test_reel_heat_not_qualified_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,cable_thermally_approved=False)).travel_ready)

    def test_human_hand_at_reel_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,hands_clear_of_reel=False)).travel_ready)

    def test_emergency_stop_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,emergency_stop=True)).travel_ready)

    def test_invalid_length_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,maximum_cable_m=-1)).travel_ready)

    def test_nan_tension_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,tension_n=float("nan"))).travel_ready)

    def test_elapsed_zero_blocks(self):
        self.assertFalse(plan_payout(replace(self.v,elapsed_s=0)).travel_ready)

    def test_outstanding_payout_never_shortens_cable(self):
        d=plan_payout(replace(self.v,route_distance_m=10))
        self.assertGreaterEqual(d.next_length_m,self.v.current_out_m)

    def test_payout_rate_calculated_from_elapsed_time(self):
        d=plan_payout(replace(self.v,route_distance_m=8,elapsed_s=0.25))
        self.assertAlmostEqual(d.next_length_m,4.25)

    def test_cable_already_over_limit_refused(self):
        self.assertFalse(plan_payout(replace(self.v,current_out_m=21)).travel_ready)

if __name__=="__main__":
    unittest.main()
