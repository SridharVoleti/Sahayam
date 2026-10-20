import unittest
from dataclasses import replace
from sahayam.power_cable_length import CableRoutePlan,evaluate_cable_length

class CableLengthTests(unittest.TestCase):
    def setUp(self):
        self.kitchen=CableRoutePlan("kitchen",18,(4,5,6),2,
                                  True,True,True,True,True,True,True,True,True)

    def test_kitchen_18m_passes_document_review_only(self):
        d=evaluate_cable_length(self.kitchen)
        self.assertTrue(d.plan_accepted_for_review)
        self.assertFalse(d.mains_energization_authorized)

    def test_kitchen_20m_study(self):
        self.assertTrue(evaluate_cable_length(replace(self.kitchen,selected_length_m=20)).plan_accepted_for_review)

    def test_kitchen_longer_than_study_limit_rejected(self):
        d=evaluate_cable_length(replace(self.kitchen,selected_length_m=21))
        self.assertEqual(d.reason,"outside_provisional_variant_length_study")

    def test_clean_50m_study_requires_review(self):
        d=evaluate_cable_length(replace(self.kitchen,robot_variant="clean",
                                        selected_length_m=50))
        self.assertTrue(d.plan_accepted_for_review)
        self.assertFalse(d.mains_energization_authorized)

    def test_laundry_50m_study(self):
        d=evaluate_cable_length(replace(self.kitchen,robot_variant="laundry",
                                        selected_length_m=50))
        self.assertTrue(d.plan_accepted_for_review)

    def test_clean_51m_exceeds_study_limit(self):
        d=evaluate_cable_length(replace(self.kitchen,robot_variant="clean",
                                        selected_length_m=51))
        self.assertFalse(d.plan_accepted_for_review)

    def test_requires_slack_allowance(self):
        d=evaluate_cable_length(replace(self.kitchen,selected_length_m=16))
        self.assertEqual(d.reason,"insufficient_length_for_measured_route")
        self.assertAlmostEqual(d.required_length_m,17)

    def test_unmeasured_route_fails(self):
        d=evaluate_cable_length(replace(self.kitchen,route_measured=False))
        self.assertFalse(d.plan_accepted_for_review)

    def test_crossing_people_not_approved(self):
        d=evaluate_cable_length(replace(self.kitchen,route_clear_of_people_and_wheels=False))
        self.assertEqual(d.reason,"electrical_thermal_or_route_controls_missing")

    def test_wet_zone_unprotected_fails(self):
        self.assertFalse(evaluate_cable_length(
            replace(self.kitchen,wet_zone_protected=False)).plan_accepted_for_review)

    def test_electrical_approval_missing(self):
        self.assertFalse(evaluate_cable_length(
            replace(self.kitchen,electrical_approval=False)).plan_accepted_for_review)

    def test_voltage_drop_missing(self):
        self.assertFalse(evaluate_cable_length(
            replace(self.kitchen,conductor_voltage_drop_verified=False)).plan_accepted_for_review)

    def test_reel_thermal_unknown(self):
        self.assertFalse(evaluate_cable_length(
            replace(self.kitchen,reel_thermal_verified=False)).plan_accepted_for_review)

    def test_snag_controls_missing(self):
        self.assertFalse(evaluate_cable_length(
            replace(self.kitchen,strain_and_snag_controls_verified=False)).plan_accepted_for_review)

    def test_stop_path_unverified(self):
        self.assertFalse(evaluate_cable_length(
            replace(self.kitchen,stop_path_verified=False)).plan_accepted_for_review)

    def test_nan_length_rejected(self):
        self.assertFalse(evaluate_cable_length(
            replace(self.kitchen,selected_length_m=float("nan"))).route_length_sufficient)

    def test_empty_route_rejected(self):
        self.assertFalse(evaluate_cable_length(
            replace(self.kitchen,route_segment_lengths_m=())).route_length_sufficient)

    def test_negative_segment_rejected(self):
        self.assertFalse(evaluate_cable_length(
            replace(self.kitchen,route_segment_lengths_m=(-1,))).route_length_sufficient)

    def test_unknown_robot_type_fails_closed(self):
        self.assertEqual(evaluate_cable_length(
            replace(self.kitchen,robot_variant="other")).reason,"unknown_robot_variant")

if __name__=="__main__":
    unittest.main()
