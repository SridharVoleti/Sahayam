import unittest
from dataclasses import replace
from sahayam.mobility.arm_stow import (
    JointStow, StowObservation, evaluate_travel_stow, simulate_stowed_travel)
from sahayam.mobility.chassis import Chassis
from sahayam.mobility.simulator import Pose,Command
from sahayam.mobility.speed import MotionConditions

class StowTests(unittest.TestCase):
    def setUp(self):
        self.joint=JointStow(0,0,2,True,True)
        self.obs=StowObservation((self.joint,),0.05,0.1,True,True,
                                 True,True,True,True)

    def test_stowed_arm_authorizes_travel(self):
        self.assertTrue(evaluate_travel_stow(self.obs).travel_permitted)

    def test_misaligned_arm_blocks(self):
        joint=replace(self.joint,measured_angle_deg=20)
        self.assertEqual(evaluate_travel_stow(replace(self.obs,joints=(joint,))).reason,
                         "arm_not_stowed")

    def test_unlatched_joint_blocks(self):
        self.assertFalse(evaluate_travel_stow(
            replace(self.obs,joints=(replace(self.joint,latch_verified=False),))).travel_permitted)

    def test_joint_sensor_fault_blocks(self):
        self.assertFalse(evaluate_travel_stow(
            replace(self.obs,joints=(replace(self.joint,sensor_healthy=False),))).travel_permitted)

    def test_stale_sensor_blocks(self):
        self.assertFalse(evaluate_travel_stow(replace(self.obs,sensors_fresh=False)).travel_permitted)

    def test_missing_joint_blocks(self):
        self.assertFalse(evaluate_travel_stow(replace(self.obs,joints=())).travel_permitted)

    def test_tool_protrusion_blocks(self):
        self.assertEqual(evaluate_travel_stow(replace(self.obs,tool_protrusion_m=0.15)).reason,
                         "tool_protrudes")

    def test_unlocked_tool_mount_blocks(self):
        self.assertFalse(evaluate_travel_stow(replace(self.obs,tool_mount_locked=False)).travel_permitted)

    def test_gripper_carrying_object_blocks(self):
        self.assertFalse(evaluate_travel_stow(replace(self.obs,gripper_empty=False)).travel_permitted)

    def test_unsecured_cooker_tray_blocks(self):
        self.assertFalse(evaluate_travel_stow(replace(self.obs,tray_load_secured=False)).travel_permitted)

    def test_cable_out_blocks(self):
        self.assertFalse(evaluate_travel_stow(replace(self.obs,cable_secured=False)).travel_permitted)

    def test_hot_attachment_blocks(self):
        self.assertFalse(evaluate_travel_stow(replace(self.obs,tool_cool=False)).travel_permitted)

    def test_estop_blocks(self):
        self.assertFalse(evaluate_travel_stow(replace(self.obs,emergency_stop=True)).travel_permitted)

    def test_nan_geometry_blocks(self):
        self.assertFalse(evaluate_travel_stow(
            replace(self.obs,tool_protrusion_m=float("nan"))).travel_permitted)

    def test_invalid_joint_tolerance_blocks(self):
        j=replace(self.joint,tolerance_deg=-1)
        self.assertFalse(evaluate_travel_stow(replace(self.obs,joints=(j,))).travel_permitted)

    def test_simulator_stops_when_arm_extended(self):
        j=replace(self.joint,measured_angle_deg=45)
        step,_=simulate_stowed_travel(Pose(),Command(0.8,0,1),Chassis(),
                                      MotionConditions(),replace(self.obs,joints=(j,)))
        self.assertEqual(step.travelled_m,0)

    def test_simulator_moves_when_stowed(self):
        step,_=simulate_stowed_travel(Pose(),Command(0.8,0,1),Chassis(),
                                      MotionConditions(),self.obs)
        self.assertAlmostEqual(step.travelled_m,0.8)

    def test_multiple_joints_each_must_be_stowed(self):
        bad=replace(self.joint,measured_angle_deg=10)
        self.assertFalse(evaluate_travel_stow(replace(self.obs,joints=(self.joint,bad))).travel_permitted)

if __name__=="__main__":
    unittest.main()
