#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reference/tools"))
from geometry_golden import CASES, DEFAULT_CANDIDATE, schema_validate, validate_invariants  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, default=DEFAULT_CANDIDATE)
parser.add_argument("--cases", type=Path, default=CASES)
args = parser.parse_args()
schema_errors = schema_validate(args.output, args.cases)
invariants = validate_invariants(args.output, args.cases)
report = {"pass": not schema_errors and invariants["pass"],
          "schema": {"pass": not schema_errors, "errors": schema_errors},
          "invariants": invariants}
print(json.dumps(report, indent=2))
raise SystemExit(not report["pass"])

