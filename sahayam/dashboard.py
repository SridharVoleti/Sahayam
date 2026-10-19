"""Local HTML dashboard served by the Python standard library."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from html import escape
from urllib.parse import urlparse
from .mobility_view import render_mobility
import json
import webbrowser
from .requirements import load_requirements
from .evidence import load_evidence, summarize

def render():
    requirements = load_requirements()
    evidence = load_evidence()
    totals = summarize(requirements, evidence)
    rows = []
    for req in requirements:
        status = evidence.get(req["id"], {}).get("status", "not_started")
        rows.append(f'<tr data-status="{escape(status)}"><td>{escape(req["id"])}</td><td>{escape(req["domain"])}</td><td>{escape(req["title"])}</td><td><span class="status">{escape(status)}</span></td></tr>')
    complete = totals["sim_pass"] + totals["physical_pass"]
    percent = 100 * complete / len(requirements) if requirements else 0
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sahayam | Requirements Dashboard</title>
<style>body{font-family:system-ui,Arial,sans-serif;background:#0d1524;color:#f2f6ff;margin:0;padding:24px}main{max-width:1150px;margin:auto}h1{margin-bottom:4px}.muted{color:#a9b7cc}.cards{display:flex;flex-wrap:wrap;gap:14px;margin:25px 0}.card{background:#19263b;border:1px solid #32435a;padding:20px;border-radius:14px;min-width:150px}.card strong{display:block;font-size:30px}.bar{background:#2b394f;height:14px;border-radius:12px;overflow:hidden}.fill{background:#3cd5a5;height:100%}input,select{padding:12px;background:#19263b;color:white;border:1px solid #506078;border-radius:8px;margin:16px 8px 16px 0}table{border-collapse:collapse;width:100%;background:#19263b}th,td{padding:12px;border-bottom:1px solid #30405a;text-align:left}th{position:sticky;top:0;background:#24344c}.status{font-size:12px;background:#344258;padding:5px 9px;border-radius:12px}tr[hidden]{display:none}</style></head>
<body><main><h1>SAHAYAM <span class="muted">/ Verification dashboard</span></h1><p class="muted">Requirement evidence, not a claim of physical robot readiness. Refresh to see latest test results.</p><p><a href="/mobility" style="color:#76d8ff">Open interactive four-wheel steering visualizer →</a></p>
<div class="cards"><div class="card">Requirements<strong>__COUNT__</strong></div><div class="card">Simulation passes<strong>__SIM__</strong></div><div class="card">Physical passes<strong>__PHYS__</strong></div><div class="card">Not started<strong>__PENDING__</strong></div></div>
<p>Simulation or physical evidence recorded: __PERCENT__%</p><div class="bar"><div class="fill" style="width:__PERCENT__%"></div></div>
<p><input id="search" placeholder="Search requirement ID or title" aria-label="Search requirements"><select id="filter"><option value="">All statuses</option><option>not_started</option><option>implemented_unverified</option><option>sim_pass</option><option>sim_fail</option><option>physical_pass</option><option>physical_fail</option><option>blocked</option></select></p>
<table><thead><tr><th>ID</th><th>Domain</th><th>Requirement</th><th>Evidence status</th></tr></thead><tbody>__ROWS__</tbody></table></main>
<script>function apply(){const q=document.getElementById('search').value.toLowerCase(),f=document.getElementById('filter').value;for(const r of document.querySelectorAll('tbody tr'))r.hidden=!(r.textContent.toLowerCase().includes(q)&&(!f||r.dataset.status===f))}document.getElementById('search').addEventListener('input',apply);document.getElementById('filter').addEventListener('change',apply)</script></body></html>""".replace("__COUNT__",str(len(requirements))).replace("__SIM__",str(totals["sim_pass"])).replace("__PHYS__",str(totals["physical_pass"])).replace("__PENDING__",str(totals["not_started"])).replace("__PERCENT__",f"{percent:.1f}").replace("__ROWS__","".join(rows))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/mobility":
            data, content_type = render_mobility(parsed.query).encode("utf-8"), "text/html; charset=utf-8"
        elif path == "/":
            data, content_type = render().encode("utf-8"), "text/html; charset=utf-8"
        elif path == "/api/status":
            requirements, evidence = load_requirements(), load_evidence()
            data, content_type = json.dumps({"requirements":len(requirements),"totals":summarize(requirements,evidence)}).encode(), "application/json"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type",content_type)
        self.send_header("Content-Length",str(len(data)))
        self.end_headers()
        self.wfile.write(data)

def main():
    address = "http://127.0.0.1:8765"
    print(f"Sahayam dashboard: {address}", flush=True)
    webbrowser.open(address)
    ThreadingHTTPServer(("127.0.0.1",8765), Handler).serve_forever()

if __name__ == "__main__":
    main()
