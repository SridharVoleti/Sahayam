"""Parse the approved requirement baseline without third-party dependencies."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "requirements" / "HOME_MATE_Functional_Specification_v1.0.md"
PATTERN = re.compile(r"^- \*\*([A-Z]+-\d{3})\*\* \(([^)]+)\): (.*?)\. \*\*Acceptance:\*\* (.*)$")

def load_requirements(path=SPEC):
    records = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        match = PATTERN.match(line)
        if match:
            identifier, domain, title, acceptance = match.groups()
            records.append({"id": identifier, "domain": domain, "title": title, "acceptance": acceptance})
    if len({r["id"] for r in records}) != len(records):
        raise ValueError("Duplicate requirement IDs")
    return records
