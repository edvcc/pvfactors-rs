#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reference/tools"))
from geometry_golden import CASES, compare_directories, run_pipeline, write_json  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--cases", type=Path, default=CASES)
parser.add_argument("--report", type=Path)
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix="pvfactors-g2-repro-a-") as a, \
     tempfile.TemporaryDirectory(prefix="pvfactors-g2-repro-b-") as b:
    left, right = Path(a) / "candidate", Path(b) / "candidate"
    run_pipeline(left, args.cases)
    run_pipeline(right, args.cases)
    differences = compare_directories(left, right)
report = {
    "pass": not differences,
    "runs": 2,
    "comparison": "byte-for-byte canonical JSON, including topology, keys, ReferenceIndex, active map and nonfinite mask",
    "differences": differences,
}
if args.report:
    write_json(args.report, report)
print(json.dumps(report, indent=2))
raise SystemExit(bool(differences))
