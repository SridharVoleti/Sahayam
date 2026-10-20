import unittest
from dataclasses import replace
from math import pi
from sahayam.mobility.parking import (
    RectangleZone, ParkingPose, ParkingSite, evaluate_parking)

class ParkingTests(unittest.TestCase):
    def setUp(self):
        self.door = RectangleZone(0, 1, 1, 3, "exit")
        self.corridor = RectangleZone(2, 0, 3, 5, "circulation")
        self.site = ParkingSite(
            room_width_m=6, room_height_m=5,
            body_length_m=0.7, body_width_m=0.55,
            overhang_m=0.1,
            forbidden_zones=(self.door,self.corridor),
            map_fresh=True, localization_valid=True,
            boundaries_verified=True, tether_route_verified=True)

    def plan(self, *poses, **change):
        return evaluate_parking(replace(self.site, **change), tuple(poses))

    def test_clear_pose_accepted(self):
        self.assertTrue(self.plan(ParkingPose(4.8,3.0)).allowed)

    def test_exit_zone_refused(self):
        self.assertFalse(self.plan(ParkingPose(0.5,2)).allowed)

    def test_corridor_zone_refused(self):
        self.assertFalse(self.plan(ParkingPose(2.5,2)).allowed)

    def test_near_exit_margin_refused(self):
        self.assertFalse(self.plan(ParkingPose(1.25,2)).allowed)

    def test_rotated_pose_can_be_accepted(self):
        self.assertTrue(self.plan(ParkingPose(4.6,2.7,pi/4)).allowed)

    def test_beyond_room_boundary_refused(self):
        self.assertFalse(self.plan(ParkingPose(5.95,2)).allowed)

    def test_falls_back_to_second_safe_candidate(self):
        d=self.plan(ParkingPose(2.5,2),ParkingPose(4.5,3))
        self.assertTrue(d.allowed)
        self.assertEqual(d.pose,ParkingPose(4.5,3))

    def test_map_stale_refused(self):
        self.assertFalse(self.plan(ParkingPose(4.5,3),map_fresh=False).allowed)

    def test_localization_lost_refused(self):
        self.assertFalse(self.plan(ParkingPose(4.5,3),localization_valid=False).allowed)

    def test_tether_unverified_refused(self):
        self.assertFalse(self.plan(ParkingPose(4.5,3),tether_route_verified=False).allowed)

    def test_boundary_not_verified_refused(self):
        self.assertFalse(self.plan(ParkingPose(4.5,3),boundaries_verified=False).allowed)

    def test_emergency_stop_blocks(self):
        self.assertFalse(self.plan(ParkingPose(4.5,3),emergency_stop=True).allowed)

    def test_invalid_restricted_zone_fails_closed(self):
        z=RectangleZone(3,3,2,4)
        self.assertEqual(self.plan(ParkingPose(4.5,3),
                     forbidden_zones=(z,)).reason,"invalid_restricted_zone")

    def test_nan_candidate_fails_closed(self):
        self.assertFalse(self.plan(ParkingPose(float("nan"),2)).allowed)

    def test_no_poses_denied(self):
        self.assertEqual(self.plan().reason,"no_candidate_poses")

    def test_extra_overhang_blocks_near_edge(self):
        self.assertFalse(self.plan(ParkingPose(5.1,3),
                                   overhang_m=0.6).allowed)

    def test_all_candidates_obstructed(self):
        d=self.plan(ParkingPose(0.5,2),ParkingPose(2.5,2))
        self.assertEqual(d.reason,"no_safe_parking_pose")

    def test_zero_clearance_allowed_only_if_footprint_fits(self):
        d=evaluate_parking(self.site,(ParkingPose(5.3,3),),clearance_m=0)
        self.assertTrue(d.allowed)

if __name__ == "__main__":
    unittest.main()
