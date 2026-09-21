#!/usr/bin/env python3
"""Canonical local/CI verification entry point for the G2 candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reference/tools"))
from build_g2_cases import build  # noqa: E402
from geometry_golden import (  # noqa: E402
    CASES,
    DEFAULT_CANDIDATE,
    deviation_report,
    environment_report,
    read_json,
    schema_validate,
    validate_docs,
    validate_invariants,
    write_json,
)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def source_integrity() -> dict:
    entries = read_json(ROOT / "evidence/source-file-manifest.json")
    failures = []
    for entry in entries:
        path = ROOT / "upstream/solarfactors" / entry["path"]
        if not path.is_file():
            failures.append(f"missing {entry['path']}")
            continue
        data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if actual != entry["sha"]:
            failures.append(f"blob mismatch {entry['path']}")
    return {"pass": not failures, "files": len(entries), "failures": failures}


def case_rebuild() -> dict:
    expected = json.dumps(build(), indent=2, sort_keys=True, allow_nan=False) + "\n"
    actual = CASES.read_text(encoding="utf-8")
    return {"pass": expected == actual, "case_count": len(build()["cases"]),
            "failures": [] if expected == actual else ["g2 case catalog is not generator-exact"]}


def branch_safety() -> dict:
    branch = git("branch", "--show-current")
    master = git("rev-parse", "master")
    origin_master = git("rev-parse", "origin/master")
    failures = []
    if branch == "master":
        failures.append("verification is running on master")
    if master != origin_master:
        failures.append("local master differs from origin/master")
    return {"pass": not failures, "branch": branch, "master": master,
            "origin_master": origin_master, "failures": failures}


def approved_safety() -> dict:
    files = [path.relative_to(ROOT).as_posix() for path in
             (ROOT / "reference/approved").rglob("*") if path.is_file()]
    failures = [] if files == ["reference/approved/README.md"] else ["approved directory contains candidate artifacts"]
    return {"pass": not failures, "files": files, "failures": failures}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.candidate.is_dir():
        raise SystemExit(f"candidate directory not found: {args.candidate}")
    schema_errors = schema_validate(args.candidate)
    report = {
        "schema_version": "0.1",
        "source_integrity": source_integrity(),
        "case_rebuild": case_rebuild(),
        "schema_validation": {"pass": not schema_errors, "errors": schema_errors},
        "invariants": validate_invariants(args.candidate),
        "raw_vs_corrected": deviation_report(args.candidate),
        "document_pairs": validate_docs(),
        "branch_safety": branch_safety(),
        "approved_safety": approved_safety(),
        "environment": environment_report(),
    }
    required = [value["pass"] for key, value in report.items()
                if isinstance(value, dict) and "pass" in value and key != "environment"]
    report["pass"] = all(required)
    if args.output:
        write_json(args.output, report)
    print(json.dumps(report, indent=2))
    raise SystemExit(not report["pass"])


if __name__ == "__main__":
    main()

