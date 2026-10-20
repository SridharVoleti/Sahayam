import unittest
from dataclasses import replace, fields
from sahayam.power_mains import MainsSafetyEvidence,assess_mains_safety

class MainsIsolationTests(unittest.TestCase):
    def setUp(self):
        self.complete = MainsSafetyEvidence(True, *([True]*11))

    def test_no_unreviewed_mains_enable(self):
        d=assess_mains_safety(MainsSafetyEvidence(True))
        self.assertFalse(d.mains_energization_authorized)
        self.assertEqual(d.review_state,"mains_configuration_rejected")

    def test_all_documentary_checks_still_cannot_energize(self):
        d=assess_mains_safety(self.complete)
        self.assertEqual(d.review_state,
                         "documentary_prechecks_complete_independent_certification_pending")
        self.assertFalse(d.mains_energization_authorized)
        self.assertFalse(d.robot_motion_authorized)

    def test_no_mains_selected_not_motion_authorized(self):
        d=assess_mains_safety(MainsSafetyEvidence(False))
        self.assertFalse(d.robot_motion_authorized)
        self.assertFalse(d.mains_energization_authorized)

    def test_missing_qualified_review_fails_closed(self):
        d=assess_mains_safety(replace(self.complete,qualified_electrical_review=False))
        self.assertIn("qualified_electrical_review",d.missing_controls)

    def test_exposed_live_parts_rejected(self):
        d=assess_mains_safety(replace(self.complete,live_parts_inaccessible=False))
        self.assertIn("live_parts_inaccessible",d.missing_controls)

    def test_unknown_earth_rejected(self):
        d=assess_mains_safety(replace(self.complete,protective_earth_verified=False))
        self.assertIn("protective_earth_verified",d.missing_controls)

    def test_missing_leakage_protection_rejected(self):
        d=assess_mains_safety(replace(self.complete,leakage_protection_verified=False))
        self.assertIn("leakage_protection_verified",d.missing_controls)

    def test_missing_strain_relief_rejected(self):
        d=assess_mains_safety(replace(self.complete,strain_relief_verified=False))
        self.assertIn("strain_relief_verified",d.missing_controls)

    def test_failed_ingress_protection_rejected(self):
        d=assess_mains_safety(replace(self.complete,enclosure_ingress_verified=False))
        self.assertIn("enclosure_ingress_verified",d.missing_controls)

    def test_reel_thermal_unverified_rejected(self):
        d=assess_mains_safety(replace(self.complete,cable_and_reel_thermal_verified=False))
        self.assertIn("cable_and_reel_thermal_verified",d.missing_controls)

    def test_wet_zone_separation_required(self):
        d=assess_mains_safety(replace(self.complete,wet_area_separation_verified=False))
        self.assertIn("wet_area_separation_verified",d.missing_controls)

    def test_stale_inspection_rejected(self):
        d=assess_mains_safety(replace(self.complete,inspection_fresh=False))
        self.assertIn("inspection_fresh",d.missing_controls)

    def test_type_error_fails_closed(self):
        self.assertEqual(assess_mains_safety(None).review_state,"invalid_input")

    def test_boolean_not_one_does_not_satisfy_check(self):
        d=assess_mains_safety(replace(self.complete,inspection_fresh=1))
        self.assertIn("inspection_fresh",d.missing_controls)

if __name__=="__main__":
    unittest.main()
