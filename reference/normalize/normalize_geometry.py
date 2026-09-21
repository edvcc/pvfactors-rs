#!/usr/bin/env python3
from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reference/tools"))
from geometry_golden import CASES, DEFAULT_CANDIDATE, normalize  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, default=DEFAULT_CANDIDATE)
parser.add_argument("--cases", type=Path, default=CASES)
args = parser.parse_args()
normalize(args.output, args.cases)

