import unittest
from dataclasses import replace
from sahayam.mobility.replanning import OccupancyMap, replan_route

class ReplanningTests(unittest.TestCase):
    def setUp(self):
        self.grid = OccupancyMap(12, 8, frozenset(), cell_size_m=0.1,
                                 fresh=True, sensors_healthy=True,
                                 mapped_boundaries_verified=True)

    def plan(self, grid=None, start=(2,3), goal=(9,3), **options):
        return replan_route(grid or self.grid, start, goal,
                            localization_valid=True, **options)

    def test_clear_route(self):
        r = self.plan()
        self.assertTrue(r.permitted)
        self.assertEqual((r.cells[0], r.cells[-1]), ((2,3),(9,3)))

    def test_replans_around_blocked_corridor(self):
        grid = replace(self.grid, occupied=frozenset({(5,3)}))
        r = self.plan(grid)
        self.assertTrue(r.permitted)
        self.assertNotIn((5,3), r.cells)
        self.assertTrue(all(not (abs(x-5) <= 1 and abs(y-3) <= 1) for x,y in r.cells))

    def test_path_only_four_neighbor_steps(self):
        r = self.plan(replace(self.grid, occupied=frozenset({(5,3)})))
        self.assertTrue(all(abs(a[0]-b[0])+abs(a[1]-b[1])==1
                            for a,b in zip(r.cells, r.cells[1:])))

    def test_no_route_if_wall_separates_regions(self):
        grid = replace(self.grid, occupied=frozenset({(5,y) for y in range(8)}))
        self.assertEqual(self.plan(grid).reason, "no_safe_route")

    def test_forbidden_cells_are_avoided(self):
        grid = replace(self.grid, forbidden=frozenset({(5,3)}))
        r = self.plan(grid)
        self.assertTrue(r.permitted)
        self.assertNotIn((5,3), r.cells)

    def test_unsafe_goal_rejected(self):
        self.assertEqual(self.plan(goal=(0,0)).reason, "endpoint_unsafe")

    def test_goal_inside_obstacle_rejected(self):
        grid = replace(self.grid, occupied=frozenset({(9,3)}))
        self.assertEqual(self.plan(grid).reason, "endpoint_unsafe")

    def test_stale_map_refused(self):
        self.assertFalse(self.plan(replace(self.grid, fresh=False)).permitted)

    def test_sensor_fault_refused(self):
        self.assertFalse(self.plan(replace(self.grid, sensors_healthy=False)).permitted)

    def test_unverified_boundary_refused(self):
        self.assertFalse(self.plan(replace(self.grid,
                                          mapped_boundaries_verified=False)).permitted)

    def test_localization_lost_refused(self):
        self.assertEqual(replan_route(self.grid, (2,3), (9,3)).reason,
                         "navigation_evidence_unavailable")

    def test_expansion_limit(self):
        self.assertEqual(self.plan(max_expansions=1).reason, "planning_budget_exceeded")

    def test_same_start_and_goal(self):
        self.assertEqual(self.plan(goal=(2,3)).reason, "already_at_goal")

    def test_emergency_stop(self):
        self.assertFalse(self.plan(emergency_stop=True).permitted)

    def test_bad_resolution_refused(self):
        self.assertFalse(self.plan(replace(self.grid, cell_size_m=float("nan"))).permitted)

    def test_hazard_outside_map_refused(self):
        grid = replace(self.grid, occupied=frozenset({(15,2)}))
        self.assertEqual(self.plan(grid).reason, "invalid_map_cells")

    def test_inflation_blocks_narrow_passage(self):
        hazards = frozenset({(x,2) for x in range(12)}
                            | {(x,4) for x in range(12)})
        grid = replace(self.grid, occupied=hazards)
        self.assertFalse(self.plan(grid, start=(2,3), goal=(9,3),
                                   clearance_cells=1).permitted)
        self.assertTrue(self.plan(grid, start=(2,3), goal=(9,3),
                                  clearance_cells=0).permitted)

    def test_unknown_endpoints_refused(self):
        self.assertFalse(self.plan(start=(99,3)).permitted)

if __name__ == "__main__":
    unittest.main()
