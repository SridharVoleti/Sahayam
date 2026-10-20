import unittest
from sahayam.mobility.corridor import (
    CorridorState, request_corridor, release_corridor,
    recover_expired_corridor, simulate_corridor_step)
from sahayam.mobility.simulator import Pose, Command
from sahayam.mobility.chassis import Chassis

def req(state, robot, now=1, **changes):
    options = dict(verified_empty=True, localization_valid=True,
                   sensors_healthy=True, lease_duration_s=10)
    options.update(changes)
    return request_corridor(state, robot, now, **options)

class CorridorTests(unittest.TestCase):
    def test_first_robot_granted(self):
        d = req(CorridorState(), "kitchen")
        self.assertTrue(d.grant)
        self.assertEqual(d.state.owner, "kitchen")

    def test_two_robots_cannot_own_simultaneously(self):
        first = req(CorridorState(), "kitchen")
        second = req(first.state, "clean", 2)
        self.assertFalse(second.grant)
        self.assertEqual(second.state.owner, "kitchen")

    def test_owner_lease_does_not_block_itself(self):
        first = req(CorridorState(), "kitchen")
        self.assertTrue(req(first.state, "kitchen", 2).grant)

    def test_queue_is_fifo(self):
        held = req(CorridorState(), "kitchen")
        clean = req(held.state, "clean", 2)
        laundry = req(clean.state, "laundry", 3)
        self.assertEqual(laundry.state.waiting, ("clean", "laundry"))
        released = release_corridor(laundry.state, "kitchen", 4,
                                    confirmed_exited=True, verified_empty=True)
        self.assertFalse(req(released.state, "laundry", 5).grant)
        next_one = req(released.state, "clean", 5)
        self.assertTrue(next_one.grant)
        self.assertEqual(next_one.state.waiting, ("laundry",))

    def test_repeat_request_does_not_duplicate_queue(self):
        occupied = req(CorridorState(), "kitchen")
        waiter = req(occupied.state, "clean", 2)
        again = req(waiter.state, "clean", 3)
        self.assertEqual(again.state.waiting, ("clean",))

    def test_unknown_occupancy_blocks_initial_grant(self):
        d = req(CorridorState(), "kitchen", verified_empty=False)
        self.assertFalse(d.grant)
        self.assertEqual(d.state.waiting, ("kitchen",))

    def test_releasing_occupied_corridor_is_forbidden(self):
        held = req(CorridorState(), "kitchen")
        d = release_corridor(held.state, "kitchen", 2,
                             confirmed_exited=True, verified_empty=False)
        self.assertEqual(d.state.owner, "kitchen")

    def test_non_owner_cannot_release(self):
        held = req(CorridorState(), "kitchen")
        self.assertEqual(release_corridor(held.state, "clean", 2,
                                         confirmed_exited=True,
                                         verified_empty=True).state.owner, "kitchen")

    def test_expired_lease_is_not_valid(self):
        held = req(CorridorState(), "kitchen")
        self.assertFalse(req(held.state, "kitchen", 11).grant)

    def test_expired_lease_does_not_grant_to_other_robot(self):
        held = req(CorridorState(), "kitchen")
        self.assertFalse(req(held.state, "laundry", 12).grant)

    def test_safe_supervised_stale_recovery(self):
        held = req(CorridorState(), "kitchen")
        queued = req(held.state, "clean", 2)
        recovered = recover_expired_corridor(
            queued.state, 12, independently_verified_empty=True,
            supervisor_reset=True, sensors_healthy=True)
        self.assertIsNone(recovered.state.owner)
        self.assertTrue(req(recovered.state, "clean", 13).grant)

    def test_stale_recovery_requires_independent_vacancy(self):
        held = req(CorridorState(), "kitchen")
        recovered = recover_expired_corridor(
            held.state, 12, independently_verified_empty=False,
            supervisor_reset=True, sensors_healthy=True)
        self.assertEqual(recovered.state.owner, "kitchen")

    def test_stale_recovery_requires_supervisor(self):
        held = req(CorridorState(), "kitchen")
        recovered = recover_expired_corridor(
            held.state, 12, independently_verified_empty=True,
            supervisor_reset=False, sensors_healthy=True)
        self.assertEqual(recovered.state.owner, "kitchen")

    def test_stale_recovery_blocked_if_sensors_bad(self):
        held = req(CorridorState(), "kitchen")
        recovered = recover_expired_corridor(
            held.state, 12, independently_verified_empty=True,
            supervisor_reset=True, sensors_healthy=False)
        self.assertEqual(recovered.state.owner, "kitchen")

    def test_loss_of_localization_denies_grant(self):
        self.assertFalse(req(CorridorState(), "kitchen",
                             localization_valid=False).grant)

    def test_sensor_fault_denies_grant(self):
        self.assertFalse(req(CorridorState(), "kitchen",
                             sensors_healthy=False).grant)

    def test_emergency_stop_denies_grant(self):
        self.assertFalse(req(CorridorState(), "kitchen",
                             emergency_stop=True).grant)

    def test_out_of_order_timestamp_rejected(self):
        held = req(CorridorState(), "kitchen", now=10)
        self.assertEqual(req(held.state, "clean", 9).reason,
                         "invalid_reservation_state")

    def test_no_lease_no_simulated_motion(self):
        result = simulate_corridor_step(CorridorState(), "kitchen", 2,
                                        Pose(), Command(0.8, 0, 1), Chassis())
        self.assertEqual(result.travelled_m, 0)

    def test_owner_moves_while_lease_active(self):
        held = req(CorridorState(), "kitchen")
        result = simulate_corridor_step(held.state, "kitchen", 2,
                                        Pose(), Command(0.8, 0, 1), Chassis())
        self.assertAlmostEqual(result.travelled_m, 0.8)

    def test_waiting_robot_stopped_in_simulation(self):
        held = req(CorridorState(), "kitchen")
        result = simulate_corridor_step(held.state, "clean", 2,
                                        Pose(), Command(0.8, 0, 1), Chassis())
        self.assertEqual(result.travelled_m, 0)

if __name__ == "__main__":
    unittest.main()
