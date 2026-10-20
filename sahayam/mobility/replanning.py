"""MOB-016: conservative grid route replanning without unsafe shortcuts.

Four-connected A* grid with configurable obstacle inflation. Route plans
require known localization and a fresh, verified map; no motor commands.
"""
from dataclasses import dataclass
from heapq import heappush, heappop
from math import isfinite

Cell = tuple[int, int]

@dataclass(frozen=True)
class OccupancyMap:
    width: int
    height: int
    occupied: frozenset[Cell]
    forbidden: frozenset[Cell] = frozenset()
    cell_size_m: float = 0.10
    fresh: bool = False
    sensors_healthy: bool = False
    mapped_boundaries_verified: bool = False

@dataclass(frozen=True)
class RoutePlan:
    permitted: bool
    cells: tuple[Cell, ...]
    reason: str
    explored_cells: int = 0

def replan_route(grid: OccupancyMap, start: Cell, goal: Cell,
                 *, localization_valid: bool = False,
                 clearance_cells: int = 1,
                 max_expansions: int = 10000,
                 emergency_stop: bool = False) -> RoutePlan:
    def blocked(reason: str, count: int = 0) -> RoutePlan:
        return RoutePlan(False, (), reason, count)
    if emergency_stop:
        return blocked("emergency_stop")
    if not (grid.fresh and grid.sensors_healthy
            and grid.mapped_boundaries_verified and localization_valid):
        return blocked("navigation_evidence_unavailable")
    if (not isinstance(grid.width, int) or isinstance(grid.width, bool)
            or not isinstance(grid.height, int) or isinstance(grid.height, bool)
            or grid.width < 1 or grid.height < 1
            or not isfinite(grid.cell_size_m) or grid.cell_size_m <= 0
            or not isinstance(clearance_cells, int) or isinstance(clearance_cells, bool)
            or clearance_cells < 0
            or not isinstance(max_expansions, int) or isinstance(max_expansions, bool)
            or max_expansions < 1):
        return blocked("invalid_map_or_limit")
    if not isinstance(grid.occupied, frozenset) or not isinstance(grid.forbidden, frozenset):
        return blocked("invalid_map_cells")
    def valid(cell):
        return (isinstance(cell, tuple) and len(cell) == 2
                and all(isinstance(n, int) and not isinstance(n, bool) for n in cell)
                and 0 <= cell[0] < grid.width and 0 <= cell[1] < grid.height)
    if not valid(start) or not valid(goal) or not all(map(valid, grid.occupied | grid.forbidden)):
        return blocked("invalid_map_cells")
    hazards = grid.occupied | grid.forbidden
    def safe(cell):
        x,y = cell
        # Keep robot's estimated radius inside known map boundary.
        if not (clearance_cells <= x < grid.width-clearance_cells
                and clearance_cells <= y < grid.height-clearance_cells):
            return False
        return all(not (abs(x-hx) <= clearance_cells and abs(y-hy) <= clearance_cells)
                   for hx,hy in hazards)
    if not safe(start) or not safe(goal):
        return blocked("endpoint_unsafe")
    if start == goal:
        return RoutePlan(True, (start,), "already_at_goal", 0)
    frontier = []
    heappush(frontier, (abs(start[0]-goal[0])+abs(start[1]-goal[1]), 0, start))
    best = {start: 0}
    parent = {}
    expanded = 0
    while frontier and expanded < max_expansions:
        _, dist, cell = heappop(frontier)
        if dist != best.get(cell):
            continue
        expanded += 1
        if cell == goal:
            path = [cell]
            while path[-1] != start:
                path.append(parent[path[-1]])
            path.reverse()
            return RoutePlan(True, tuple(path), "safe_route_found", expanded)
        x,y = cell
        for candidate in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if not safe(candidate):
                continue
            tentative = dist+1
            if tentative < best.get(candidate, float("inf")):
                best[candidate] = tentative
                parent[candidate] = cell
                heuristic = abs(candidate[0]-goal[0])+abs(candidate[1]-goal[1])
                heappush(frontier, (tentative+heuristic, tentative, candidate))
    if frontier:
        return blocked("planning_budget_exceeded", expanded)
    return blocked("no_safe_route", expanded)
