"""Conservative verification reporting: untested is never passed."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "results.json"
VALID = {"not_started", "implemented_unverified", "sim_pass", "sim_fail", "physical_pass", "physical_fail", "blocked"}

def load_evidence(path=EVIDENCE):
    if not Path(path).exists():
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Evidence must be a JSON object")
    for key, value in data.items():
        if value.get("status") not in VALID:
            raise ValueError(f"Invalid evidence status for {key}")
    return data

def summarize(requirements, evidence):
    totals = {status: 0 for status in VALID}
    for requirement in requirements:
        totals[evidence.get(requirement["id"], {}).get("status", "not_started")] += 1
    return totals
