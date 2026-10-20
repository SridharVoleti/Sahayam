import unittest
from dataclasses import replace
from sahayam.mobility.localization import (
    LocalizationObservation, LocalizationState, evaluate_localization,
    simulate_localized_step, TRACKING, LOST, RECOVERING)
from sahayam.mobility.simulator import Pose, Command
from sahayam.mobility.chassis import Chassis
from sahayam.mobility.speed import MotionConditions

class LocalizationTests(unittest.TestCase):
    def setUp(self):
        self.good = LocalizationObservation(
            confidence=0.96, position_error_m=0.03, heading_error_deg=2,
            fresh=True, sensor_healthy=True,
            absolute_reference_consistent=True, robot_stationary=True)

    def test_healthy_tracking(self):
        result = evaluate_localization(LocalizationState(TRACKING), self.good)
        self.assertTrue(result.motion_permitted)

    def test_starts_without_localization(self):
        result = evaluate_localization(LocalizationState(), self.good)
        self.assertFalse(result.motion_permitted)
        self.assertEqual(result.state.mode, RECOVERING)

    def test_low_confidence_latches_stop(self):
        result = evaluate_localization(LocalizationState(TRACKING),
                                       replace(self.good, confidence=0.4))
        self.assertEqual(result.state.mode, LOST)
        self.assertFalse(result.motion_permitted)

    def test_stale_data_blocks(self):
        self.assertFalse(evaluate_localization(
            LocalizationState(TRACKING), replace(self.good, fresh=False)).motion_permitted)

    def test_faulty_sensor_blocks(self):
        self.assertFalse(evaluate_localization(
            LocalizationState(TRACKING), replace(self.good, sensor_healthy=False)).motion_permitted)

    def test_absolute_reference_required(self):
        self.assertFalse(evaluate_localization(
            LocalizationState(TRACKING),
            replace(self.good, absolute_reference_consistent=False)).motion_permitted)

    def test_position_error_threshold(self):
        self.assertFalse(evaluate_localization(
            LocalizationState(TRACKING),
            replace(self.good, position_error_m=0.3)).motion_permitted)

    def test_heading_error_threshold(self):
        self.assertFalse(evaluate_localization(
            LocalizationState(TRACKING),
            replace(self.good, heading_error_deg=15)).motion_permitted)

    def test_recovery_needs_stationary_robot(self):
        result = evaluate_localization(LocalizationState(LOST),
                                       replace(self.good, robot_stationary=False))
        self.assertEqual(result.state, LocalizationState(LOST))

    def test_recovery_requires_three_fixes_and_release(self):
        state = LocalizationState(LOST)
        for _ in range(3):
            decision = evaluate_localization(state, self.good)
            self.assertFalse(decision.motion_permitted)
            state = decision.state
        self.assertEqual(state, LocalizationState(RECOVERING, 3))
        decision = evaluate_localization(state, self.good, recovery_release=True)
        self.assertFalse(decision.motion_permitted)
        self.assertEqual(decision.state.mode, TRACKING)
        self.assertTrue(evaluate_localization(decision.state, self.good).motion_permitted)

    def test_single_good_fix_cannot_rearm(self):
        decision = evaluate_localization(LocalizationState(LOST),
                                         self.good, recovery_release=True)
        self.assertEqual(decision.state.mode, RECOVERING)

    def test_bad_fix_resets_recovery_streak(self):
        state = LocalizationState(RECOVERING, 2)
        decision = evaluate_localization(state, replace(self.good, fresh=False))
        self.assertEqual(decision.state, LocalizationState(LOST))

    def test_emergency_stop_during_tracking(self):
        decision = evaluate_localization(LocalizationState(TRACKING),
                                         replace(self.good, emergency_stop=True))
        self.assertEqual(decision.reason, "emergency_stop")
        self.assertFalse(decision.motion_permitted)

    def test_nonfinite_confidence_fails_closed(self):
        decision = evaluate_localization(LocalizationState(TRACKING),
                                         replace(self.good, confidence=float("nan")))
        self.assertFalse(decision.motion_permitted)

    def test_malformed_state_fails_closed(self):
        decision = evaluate_localization(LocalizationState("unknown"), self.good)
        self.assertFalse(decision.motion_permitted)

    def test_simulator_stops_on_loss(self):
        step, decision = simulate_localized_step(
            Pose(), Command(0.8, 0, 1), Chassis(), MotionConditions(),
            LocalizationState(TRACKING),
            replace(self.good, confidence=0.1))
        self.assertEqual(step.travelled_m, 0)
        self.assertFalse(decision.motion_permitted)

    def test_simulator_moves_when_healthy(self):
        step, _ = simulate_localized_step(
            Pose(), Command(0.8, 0, 1), Chassis(), MotionConditions(),
            LocalizationState(TRACKING), self.good)
        self.assertAlmostEqual(step.travelled_m, 0.8)

    def test_simulator_no_motion_on_rearm_cycle(self):
        step, decision = simulate_localized_step(
            Pose(), Command(0.8, 0, 1), Chassis(), MotionConditions(),
            LocalizationState(RECOVERING, 3), self.good, recovery_release=True)
        self.assertEqual(step.travelled_m, 0)
        self.assertEqual(decision.state.mode, TRACKING)

if __name__ == "__main__":
    unittest.main()
