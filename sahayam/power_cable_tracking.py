"""PWR-005: geometric cable route tracking and prospective path-crossing veto.

2-D line-segment reasoning only; no camera tracking, live occupancy or physical
cable wheel-contact model. A safe planning result is not motor permission.
"""
from dataclasses import dataclass
from math import isfinite

Point = tuple[float,float]

@dataclass(frozen=True)
class CablePathObservation:
    cable_points: tuple[Point,...]
    planned_robot_points: tuple[Point,...]
    cable_route_fresh: bool
    localization_valid: bool
    sensors_healthy: bool
    cable_fully_observed: bool
    wheel_envelope_verified: bool
    cable_under_robot: bool
    snag_detected: bool
    emergency_stop: bool = False

@dataclass(frozen=True)
class CablePathDecision:
    route_permitted_for_planning: bool
    reason: str

def _cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def _on_segment(a,b,p):
    eps=1e-9
    return (abs(_cross(a,b,p))<=eps
            and min(a[0],b[0])-eps<=p[0]<=max(a[0],b[0])+eps
            and min(a[1],b[1])-eps<=p[1]<=max(a[1],b[1])+eps)

def _intersects(a,b,c,d):
    v1,v2,v3,v4=_cross(a,b,c),_cross(a,b,d),_cross(c,d,a),_cross(c,d,b)
    eps=1e-9
    if ((v1>eps and v2<-eps or v1<-eps and v2>eps)
            and (v3>eps and v4<-eps or v3<-eps and v4>eps)):
        return True
    return (abs(v1)<=eps and _on_segment(a,b,c)
            or abs(v2)<=eps and _on_segment(a,b,d)
            or abs(v3)<=eps and _on_segment(c,d,a)
            or abs(v4)<=eps and _on_segment(c,d,b))

def evaluate_cable_route(obs: CablePathObservation) -> CablePathDecision:
    def deny(why):
        return CablePathDecision(False,why)
    if obs.emergency_stop:
        return deny("emergency_stop")
    if not (obs.cable_route_fresh and obs.localization_valid
            and obs.sensors_healthy and obs.cable_fully_observed
            and obs.wheel_envelope_verified):
        return deny("cable_tracking_unavailable")
    if obs.cable_under_robot or obs.snag_detected:
        return deny("cable_trapping_or_snag")
    paths=(obs.cable_points,obs.planned_robot_points)
    if not all(isinstance(path,tuple) and len(path)>=2 for path in paths):
        return deny("invalid_cable_or_robot_path")
    for path in paths:
        for p in path:
            if (not isinstance(p,tuple) or len(p)!=2
                    or not all(isinstance(v,(float,int)) and isfinite(v) for v in p)):
                return deny("invalid_cable_or_robot_path")
        if any(path[i]==path[i+1] for i in range(len(path)-1)):
            return deny("degenerate_path_segment")
    cable=obs.cable_points
    for i in range(len(cable)-1):
        for j in range(i+2,len(cable)-1):
            if _intersects(cable[i],cable[i+1],cable[j],cable[j+1]):
                return deny("self_crossing_cable_route")
    route=obs.planned_robot_points
    for i in range(len(route)-1):
        for j in range(len(cable)-1):
            if _intersects(route[i],route[i+1],cable[j],cable[j+1]):
                return deny("planned_route_crosses_tether")
    return CablePathDecision(True,"no_2d_cable_crossing_detected")
