# Requirement-by-requirement development workflow

## Run on Windows

Double-click `run_dashboard.bat` to open http://127.0.0.1:8765.

Run tests:

```bat
py -3 -m unittest discover -s tests -v
```

No third-party Python packages are required for the dashboard.

## Per-requirement implementation rule

1. Select exactly one requirement ID and define testable acceptance criteria.
2. Add a Python implementation or simulation with measurable assertions.
3. Run tests, inspect failures, and capture reproducible evidence.
4. Commit that requirement's implementation and tests to GitHub with `feat(ID): ...` (or `test(ID): ...`).
5. Only after tests pass, update `evidence/results.json` with `sim_pass`, referencing the test run, commit SHA and simulation limitations.
6. Never use `physical_pass` without separate physical validation.
7. Re-run affected tests after changes to common components.

## Important limits

The current dashboard is an initial development framework. The requirement registry and truthful default status are implemented; this does **not** mean 271 robotic capabilities are implemented. Browser UI is generated and served by Python, with a small client-side search/filter script. Actual robot control remains future work.

The project is publicly visible: review patent-sensitive inventions before publication.
