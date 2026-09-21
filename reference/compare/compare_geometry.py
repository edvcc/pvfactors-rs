#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reference/tools"))
from geometry_golden import compare_directories  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("left", type=Path)
parser.add_argument("right", type=Path)
args = parser.parse_args()
differences = compare_directories(args.left, args.right)
print(json.dumps({"pass": not differences, "differences": differences}, indent=2))
raise SystemExit(bool(differences))

