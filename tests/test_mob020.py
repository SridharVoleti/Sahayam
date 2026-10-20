import unittest
from dataclasses import replace
from sahayam.mobility.braking import (
    BrakeInputs,BrakeState,evaluate_braking,simulate_brake_step)
from sahayam.mobility.simulator import Pose,Command
from sahayam.mobility.chassis import Chassis
from sahayam.mobility.speed import MotionConditions

class EmergencyBrakingTests(unittest.TestCase):
    def setUp(self):
        self.obs=BrakeInputs(
            requested_speed_mps=0.8,measured_speed_mps=0.8,
            deceleration_mps2=0.5,detection_latency_s=0.25,
            person_in_danger=False,collision_imminent=False,
            manual_emergency_stop=False,sensors_healthy=True,
            physical_stop_circuit_verified=True)

    def test_no_hazard_normal_speed(self):
        self.assertEqual(evaluate_braking(self.obs).commanded_speed_mps,0.8)

    def test_human_danger_overrides_liquid_spill(self):
        d=evaluate_braking(replace(self.obs,person_in_danger=True,
                                   liquid_spill_risk=True,carrying_liquid=True))
        self.assertEqual(d.mode,"emergency_stop")
        self.assertTrue(d.spill_control_deprioritized)
        self.assertEqual(d.commanded_speed_mps,0)

    def test_manual_estop_priority(self):
        d=evaluate_braking(replace(self.obs,manual_emergency_stop=True))
        self.assertTrue(d.state.stop_latched)

    def test_imminent_collision_stops(self):
        self.assertEqual(evaluate_braking(replace(self.obs,collision_imminent=True)).mode,
                         "emergency_stop")

    def test_spill_only_slows_not_emergency_stops(self):
        d=evaluate_braking(replace(self.obs,carrying_liquid=True,liquid_spill_risk=True))
        self.assertEqual(d.commanded_speed_mps,0.10)
        self.assertEqual(d.mode,"spill_caution")

    def test_no_liquid_does_not_apply_spill_cap(self):
        d=evaluate_braking(replace(self.obs,carrying_liquid=False,liquid_spill_risk=True))
        self.assertEqual(d.commanded_speed_mps,0.8)

    def test_sensor_fault_stops(self):
        self.assertEqual(evaluate_braking(replace(self.obs,sensors_healthy=False)).commanded_speed_mps,0)

    def test_physical_stop_path_unverified_blocks(self):
        self.assertEqual(evaluate_braking(
            replace(self.obs,physical_stop_circuit_verified=False)).commanded_speed_mps,0)

    def test_speed_invalid_fails_closed(self):
        self.assertEqual(evaluate_braking(replace(self.obs,requested_speed_mps=float("nan"))).mode,
                         "emergency_stop")

    def test_invalid_deceleration_fails_closed(self):
        d=evaluate_braking(replace(self.obs,deceleration_mps2=0))
        self.assertEqual(d.mode,"emergency_stop")
        self.assertIsNone(d.estimated_stop_distance_m)

    def test_stop_distance_estimate(self):
        d=evaluate_braking(self.obs)
        self.assertAlmostEqual(d.estimated_stop_distance_m,0.8*0.25+0.8*0.8/1)

    def test_human_stop_with_invalid_data_still_prioritized(self):
        d=evaluate_braking(replace(self.obs,person_in_danger=True,
                                   deceleration_mps2=float("nan"),
                                   liquid_spill_risk=True))
        self.assertEqual(d.reason,"human_safety_priority")

    def test_latched_state_does_not_autoresume(self):
        d=evaluate_braking(self.obs,BrakeState(True))
        self.assertEqual(d.reason,"reset_required")

    def test_reset_requires_stopped_robot(self):
        d=evaluate_braking(self.obs,BrakeState(True),supervisor_reset=True)
        self.assertTrue(d.state.stop_latched)

    def test_supervised_reset_still_commands_zero(self):
        d=evaluate_braking(replace(self.obs,measured_speed_mps=0),
                           BrakeState(True),supervisor_reset=True)
        self.assertFalse(d.state.stop_latched)
        self.assertEqual(d.commanded_speed_mps,0)

    def test_next_normal_cycle_after_reset(self):
        d=evaluate_braking(replace(self.obs,measured_speed_mps=0),
                           BrakeState(True),supervisor_reset=True)
        self.assertEqual(evaluate_braking(self.obs,d.state).commanded_speed_mps,0.8)

    def test_simulated_stop_for_person(self):
        obs=replace(self.obs,person_in_danger=True,carrying_liquid=True,
                    liquid_spill_risk=True)
        step,_=simulate_brake_step(Pose(),Command(0.8,0,1),Chassis(),
                                  MotionConditions(),obs)
        self.assertEqual(step.travelled_m,0)

    def test_simulated_spill_cap(self):
        obs=replace(self.obs,carrying_liquid=True,liquid_spill_risk=True)
        step,_=simulate_brake_step(Pose(),Command(0.8,0,1),Chassis(),
                                  MotionConditions(),obs)
        self.assertAlmostEqual(step.travelled_m,0.1)

    def test_emergency_stop_wins_over_supervised_reset(self):
        obs=replace(self.obs,person_in_danger=True,measured_speed_mps=0)
        d=evaluate_braking(obs,BrakeState(True),supervisor_reset=True)
        self.assertTrue(d.state.stop_latched)

    def test_spill_slowdown_never_increases_speed(self):
        d=evaluate_braking(replace(self.obs,requested_speed_mps=0.03,
                                   carrying_liquid=True,liquid_spill_risk=True))
        self.assertEqual(d.commanded_speed_mps,0.03)

if __name__=="__main__":
    unittest.main()
