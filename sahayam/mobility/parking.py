"""MOB-018: choose a parking pose clear of egress and circulation zones.

2-D conservative footprint checks only. The approach route, people moving,
door mechanics, tether snagging and physical docking are not validated.
"""
from dataclasses import dataclass
from math import cos, sin, isfinite

@dataclass(frozen=True)
class RectangleZone:
    xmin_m: float
    ymin_m: float
    xmax_m: float
    ymax_m: float
    purpose: str = "restricted"

@dataclass(frozen=True)
class ParkingPose:
    x_m: float
    y_m: float
    heading_rad: float = 0.0

@dataclass(frozen=True)
class ParkingSite:
    room_width_m: float
    room_height_m: float
    body_length_m: float
    body_width_m: float
    overhang_m: float
    forbidden_zones: tuple[RectangleZone, ...]
    map_fresh: bool
    localization_valid: bool
    boundaries_verified: bool
    tether_route_verified: bool
    emergency_stop: bool = False

@dataclass(frozen=True)
class ParkingDecision:
    allowed: bool
    pose: ParkingPose | None
    reason: str

def _corners(pose: ParkingPose, length: float, width: float):
    c, s = cos(pose.heading_rad), sin(pose.heading_rad)
    return tuple((pose.x_m+x*c-y*s, pose.y_m+x*s+y*c)
                 for x,y in ((-length/2,-width/2), (length/2,-width/2),
                             (length/2,width/2), (-length/2,width/2)))

def _overlap_sat(a, b):
    """Separating-axis test for convex quadrilaterals; touching counts as overlap."""
    for poly in (a,b):
        for i in range(len(poly)):
            x1,y1=poly[i]
            x2,y2=poly[(i+1)%len(poly)]
            nx,ny=-(y2-y1),x2-x1
            p=[x*nx+y*ny for x,y in a]
            q=[x*nx+y*ny for x,y in b]
            if max(p) < min(q)-1e-10 or max(q) < min(p)-1e-10:
                return False
    return True

def evaluate_parking(
    site: ParkingSite, candidates: tuple[ParkingPose, ...],
    *, clearance_m: float = 0.10
) -> ParkingDecision:
    def deny(reason):
        return ParkingDecision(False,None,reason)
    vals=(site.room_width_m, site.room_height_m, site.body_length_m,
          site.body_width_m, site.overhang_m, clearance_m)
    if (not all(isfinite(v) for v in vals)
            or min(site.room_width_m, site.room_height_m,
                   site.body_length_m, site.body_width_m) <= 0
            or site.overhang_m < 0 or clearance_m < 0
            or not isinstance(site.forbidden_zones, tuple)
            or not isinstance(candidates, tuple)):
        return deny("invalid_site")
    if site.emergency_stop:
        return deny("emergency_stop")
    if not (site.map_fresh and site.localization_valid
            and site.boundaries_verified and site.tether_route_verified):
        return deny("parking_evidence_unavailable")
    for z in site.forbidden_zones:
        if (not isinstance(z, RectangleZone)
                or not all(isfinite(v) for v in
                           (z.xmin_m,z.ymin_m,z.xmax_m,z.ymax_m))
                or not (0 <= z.xmin_m < z.xmax_m <= site.room_width_m)
                or not (0 <= z.ymin_m < z.ymax_m <= site.room_height_m)):
            return deny("invalid_restricted_zone")
    if not candidates:
        return deny("no_candidate_poses")
    length=site.body_length_m+2*site.overhang_m
    width=site.body_width_m+2*site.overhang_m
    for pose in candidates:
        if (not isinstance(pose,ParkingPose)
                or not all(isfinite(x) for x in (pose.x_m,pose.y_m,pose.heading_rad))):
            return deny("invalid_candidate_pose")
        footprint=_corners(pose,length,width)
        if any(not (clearance_m <= x <= site.room_width_m-clearance_m
                    and clearance_m <= y <= site.room_height_m-clearance_m)
               for x,y in footprint):
            continue
        overlaps=False
        for z in site.forbidden_zones:
            restricted=((z.xmin_m-clearance_m,z.ymin_m-clearance_m),
                        (z.xmax_m+clearance_m,z.ymin_m-clearance_m),
                        (z.xmax_m+clearance_m,z.ymax_m+clearance_m),
                        (z.xmin_m-clearance_m,z.ymax_m+clearance_m))
            if _overlap_sat(footprint,restricted):
                overlaps=True
                break
        if not overlaps:
            return ParkingDecision(True,pose,"clear_of_exits_and_circulation")
    return deny("no_safe_parking_pose")
