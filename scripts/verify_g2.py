#!/usr/bin/env python3
"""Canonical local/CI verification entry point for the G2 candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPROVED_VERSION = "geometry-golden-v0.1"
APPROVED_MANIFEST_SHA256 = "efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b"
APPROVED_ROOT = ROOT / "reference/approved" / APPROVED_VERSION
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
    head = git("rev-parse", "HEAD")
    failures = []

    try:
        origin_master = git(
            "rev-parse", "--verify", "refs/remotes/origin/master"
        )
    except subprocess.CalledProcessError:
        origin_master = None
        failures.append("authoritative ref refs/remotes/origin/master is missing")

    github_actions = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    base_branch = None

    if github_actions and event_name == "pull_request":
        mode = "github_pull_request"
        logical_branch = os.environ.get("GITHUB_HEAD_REF", "")
        base_branch = os.environ.get("GITHUB_BASE_REF", "")
        if not logical_branch:
            failures.append("GITHUB_HEAD_REF is missing for pull_request")
    elif github_actions and event_name == "push":
        mode = "github_push"
        logical_branch = os.environ.get("GITHUB_REF_NAME", "") or branch
        ref_type = os.environ.get("GITHUB_REF_TYPE", "")
        if ref_type and ref_type != "branch":
            failures.append(f"push ref is not a branch: {ref_type}")
        if not logical_branch:
            failures.append("push branch cannot be determined")
    else:
        mode = "local"
        logical_branch = branch
        if not branch:
            failures.append(
                "detached HEAD is only supported for GitHub pull_request"
            )

    if logical_branch == "master":
        failures.append("verification is running on master")

    return {
        "pass": not failures,
        "mode": mode,
        "branch": branch,
        "logical_branch": logical_branch,
        "base_branch": base_branch,
        "head": head,
        "authoritative_ref": "refs/remotes/origin/master",
        "origin_master": origin_master,
        "failures": failures,
    }


def approved_safety() -> dict:
    failures = []
    approved_parent = ROOT / "reference/approved"
    candidate = ROOT / "reference/candidate/geometry-golden-v0.1"
    symlinks = sorted(
        path.relative_to(approved_parent).as_posix()
        for path in approved_parent.rglob("*")
        if path.is_symlink()
    )
    if symlinks:
        failures.append(f"approved corpus must not contain symlinks: {symlinks}")
    top_level = sorted(path.name for path in approved_parent.iterdir())
    if top_level != ["README.md", APPROVED_VERSION]:
        failures.append(f"unexpected approved top-level inventory: {top_level}")

    approved_readme = (approved_parent / "README.md").read_text(encoding="utf-8")
    for token in ("APPROVED", APPROVED_VERSION, APPROVED_MANIFEST_SHA256, "immutable"):
        if token not in approved_readme:
            failures.append(f"approved README missing governance token: {token}")

    approval_path = APPROVED_ROOT / "APPROVAL.json"
    try:
        approval = read_json(approval_path)
    except (OSError, json.JSONDecodeError) as issue:
        approval = {}
        failures.append(f"invalid approval metadata: {issue}")

    expected_metadata = {
        "approved_version": APPROVED_VERSION,
        "approval_date": "2026-09-22",
        "source_candidate": "reference/candidate/geometry-golden-v0.1",
        "source_manifest_sha256": APPROVED_MANIFEST_SHA256,
        "approved_cdrs": ["CDR-003", "CDR-006"],
        "approved_tolerance": "geometry-tolerance-v0.1",
        "case_count": 55,
        "artifact_count": 165,
    }
    for field, expected in expected_metadata.items():
        if approval.get(field) != expected:
            failures.append(f"approval metadata {field} mismatch")
    if approval.get("owner_approval", {}).get("status") != "APPROVED":
        failures.append("owner approval status is not APPROVED")
    if approval.get("reference", {}).get("commit") != "ecbfc863657e239817603a43898ae173c7ccad9c":
        failures.append("approved reference commit mismatch")
    if approval.get("canonical_runtime", {}).get("environment_id") != "031158a1d1be8cdb9093":
        failures.append("approved R0 environment mismatch")
    expected_case_ids = [case["id"] for case in build()["cases"]]
    if approval.get("approved_case_ids") != expected_case_ids:
        failures.append("approved case IDs do not exactly match the 55-case catalog")
    expected_policy = {
        "candidate_auto_promotion": False,
        "test_failure_auto_update": False,
        "manifest_hash_change_requires_new_owner_approval": True,
        "approved_corpus_is_immutable_baseline": True,
    }
    if approval.get("immutability_policy") != expected_policy:
        failures.append("approved immutability policy mismatch")

    candidate_files = sorted(
        path.relative_to(candidate).as_posix() for path in candidate.rglob("*") if path.is_file()
    )
    approved_files = sorted(
        path.relative_to(APPROVED_ROOT).as_posix() for path in APPROVED_ROOT.rglob("*")
        if path.is_file() and path.name != "APPROVAL.json"
    )
    if approved_files != candidate_files:
        failures.append("approved payload inventory differs from source candidate")
    identity_mismatches = []
    for relative in sorted(set(candidate_files) & set(approved_files)):
        if (candidate / relative).read_bytes() != (APPROVED_ROOT / relative).read_bytes():
            identity_mismatches.append(relative)
    if identity_mismatches:
        failures.append(f"candidate/approved byte mismatch: {identity_mismatches[:10]}")

    manifest_hashes = {}
    for label, path in (
        ("candidate", candidate / "manifest.json"),
        ("approved", APPROVED_ROOT / "manifest.json"),
    ):
        if path.is_file():
            manifest_hashes[label] = hashlib.sha256(path.read_bytes()).hexdigest()
            if manifest_hashes[label] != APPROVED_MANIFEST_SHA256:
                failures.append(f"{label} manifest is not the approved manifest")
        else:
            failures.append(f"missing {label} manifest")

    artifact_hash_failures = []
    if (APPROVED_ROOT / "manifest.json").is_file():
        manifest = read_json(APPROVED_ROOT / "manifest.json")
        if manifest.get("coverage", {}).get("case_count") != 55:
            failures.append("approved manifest case count is not 55")
        if manifest.get("coverage", {}).get("artifact_count") != 165:
            failures.append("approved manifest artifact count is not 165")
        for entry in manifest.get("artifacts", []):
            path = APPROVED_ROOT / entry["file"]
            actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
            if actual != entry["payload_sha256"]:
                artifact_hash_failures.append(entry["file"])
    if artifact_hash_failures:
        failures.append(f"approved artifact hash mismatch: {artifact_hash_failures[:10]}")

    approved_schema_errors = schema_validate(APPROVED_ROOT) if APPROVED_ROOT.is_dir() else ["missing approved corpus"]
    if approved_schema_errors:
        failures.extend(f"approved schema: {error}" for error in approved_schema_errors)
    return {
        "pass": not failures,
        "approved_version": APPROVED_VERSION,
        "approved_manifest_sha256": APPROVED_MANIFEST_SHA256,
        "case_count": len(expected_case_ids),
        "artifact_count": 165,
        "source_file_count": len(candidate_files),
        "candidate_approved_byte_identity": not identity_mismatches and approved_files == candidate_files,
        "manifest_hashes": manifest_hashes,
        "approved_schema_validation": {"pass": not approved_schema_errors, "errors": approved_schema_errors},
        "failures": failures,
    }


def p3_entry_contract() -> dict:
    approval = read_json(APPROVED_ROOT / "APPROVAL.json")
    case_ids = approval["approved_case_ids"]
    failures = []
    documents = [
        ROOT / "docs/g2/P3_RUST_GEOMETRY_KERNEL_ENTRY_CONTRACT.en.md",
        ROOT / "docs/g2/P3_RUST_GEOMETRY_KERNEL_ENTRY_CONTRACT.zh-CN.md",
    ]
    required = [
        "**ACTIVE**", "G2 PASS", APPROVED_MANIFEST_SHA256,
        "geometry-golden-v0.1", "geometry-tolerance-v0.1", "CDR-003", "CDR-006",
        "NOT STARTED", "Point2", "input validation", "rotation", "solar 2D",
        "shadow projection", "PV side partition", "ground partition", "SurfaceKey",
        "ReferenceIndex", "ActiveIndex", "differential",
    ]
    for document in documents:
        text = document.read_text(encoding="utf-8")
        normalized_text = " ".join(text.split())
        for token in required:
            if token not in normalized_text:
                failures.append(f"{document.name}: missing {token}")
        missing_ids = [case_id for case_id in case_ids if f"`{case_id}`" not in text]
        if missing_ids:
            failures.append(f"{document.name}: missing approved case IDs {missing_ids}")
        for forbidden in (
            "View Factor", "Perez", "Radiosity", "solver", "Python binding",
            "serial/parallel", "Adaptive Planner", "SIMD", "GPU",
        ):
            if forbidden not in normalized_text:
                failures.append(f"{document.name}: missing forbidden-scope guard {forbidden}")
    return {"pass": not failures, "approved_case_count": len(case_ids), "failures": failures}


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
        "p3_entry_contract": p3_entry_contract(),
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
