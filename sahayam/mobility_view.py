"""Server-rendered steering diagram, geometry only."""
from html import escape
from urllib.parse import parse_qs
from .mobility.chassis import Chassis
from .mobility.steering import ackermann
from .mobility.speed import MotionConditions,allowed_speed_mps

def render_mobility(query=""):
    try:
        angle=float(parse_qs(query).get("angle",["20"])[0])
        chassis=Chassis()
        steering=ackermann(chassis,angle)
        error=""
    except (ValueError,OverflowError) as exc:
        angle=20.0
        steering=ackermann(Chassis(),angle)
        error=f"<p style='color:#f9a7a7'>Invalid steering request: {escape(str(exc))}</p>"
    wheels=[("Front left",120,100,steering.front_left_deg),("Front right",300,100,steering.front_right_deg),("Rear left",120,310,0),("Rear right",300,310,0)]
    shapes=[]
    for name,x,y,deg in wheels:
        shapes.append(f'<g transform="translate({x} {y}) rotate({-deg})"><rect x="-15" y="-37" width="30" height="74" rx="8" fill="#4bd6b2" stroke="#d6fff6" stroke-width="3"/></g><text x="{x}" y="{y+57}" text-anchor="middle" fill="#dce8ff" font-size="13">{escape(name)}</text>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sahayam Mobility Simulation</title><style>body{{background:#0d1524;color:#f1f6ff;font-family:system-ui;margin:0;padding:24px}}main{{max-width:880px;margin:auto}}a{{color:#75dbff}}.panel{{background:#19263b;padding:24px;border-radius:16px}}input{{padding:10px;font-size:16px}}button{{padding:10px 18px;cursor:pointer}}</style></head><body><main><p><a href="/">← Requirements dashboard</a></p><h1>Four-wheel steering visualizer</h1><p>Geometry-only demonstration of MOB-001 to MOB-005. Not hardware validation or test evidence.</p><div class="panel"><form method="get" action="/mobility"><label>Equivalent front steering angle (-74 to 74°): <input name="angle" type="number" min="-74" max="74" step="1" value="{angle:g}"></label> <button type="submit">Visualize</button></form>{error}<svg viewBox="0 0 420 420" style="max-width:480px;width:100%" role="img" aria-label="Top view of chassis with front wheels steered"><rect x="85" y="70" width="250" height="280" rx="35" fill="#344d6b" stroke="#a9bdd8" stroke-width="3"/><text x="210" y="205" text-anchor="middle" fill="white">SAHAYAM</text><text x="210" y="225" text-anchor="middle" fill="#c5d6ee">FRONT ↑</text>{''.join(shapes)}</svg><p>Front left: {steering.front_left_deg:.2f}° · Front right: {steering.front_right_deg:.2f}°</p><p>Rear left: 0° · Rear right: 0° · Nominal clear-route speed: {allowed_speed_mps(MotionConditions()):.1f} m/s</p></div><p>75° inner-wheel steering remains a provisional target. Physical clearance, actuator torque, tire slip and real collision avoidance have not been tested.</p></main></body></html>"""
