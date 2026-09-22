#!/usr/bin/env python3
"""Repository-native acceptance gates. A missing oracle/checker never passes.

No physics is implemented here. Geometry comparison composes the frozen G2
comparator; later adapters require an approved case/oracle contract first.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib

ROOT = Path(__file__).resolve().parents[1]
BASE = "c2bc8572a976279abacbcd1d4f9c460233785bdb"
MASTER = "bc0b7ec1cb17938be9f4d53c83e1fb80a1abd9ba"
REFERENCE = "ecbfc863657e239817603a43898ae173c7ccad9c"
DOCS = ROOT / "docs/execution"
GOLDEN = ROOT / "reference/approved/geometry-golden-v0.1"
TOLERANCE = ROOT / "reference/tolerance/geometry-tolerance-v0.1.json"
PAIRS = (
    "V1_COMPLETION_CONTRACT", "ACCEPTANCE_MATRIX", "LONG_TASK_EXECUTION_CONTRACT",
    "REMAINING_OWNER_DECISIONS", "LOOP_ENGINEERING_READINESS_REPORT",
    "CONTRACT_EXECUTABILITY_AUDIT", "ENVIRONMENT_CI_AND_GOVERNANCE", "EXECUTION_PLAN",
    "HARNESS_CONTRACT",
)


def read(path):
    def reject(value):
        raise ValueError(f"non-standard JSON constant: {value}")
    return json.loads(Path(path).read_text(encoding="utf-8"), parse_constant=reject)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def result(status, **details):
    return {"status": status, **details}


def command(argv, *, cwd=ROOT, env=None, timeout=180):
    start = time.monotonic()
    try:
        p = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True,
                           timeout=timeout, check=False)
        return {"argv": argv, "exit_code": p.returncode,
                "stdout": p.stdout, "stderr": p.stderr,
                "seconds": round(time.monotonic() - start, 3)}
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"argv": argv, "exit_code": -1, "stdout": "", "stderr": str(error),
                "seconds": round(time.monotonic() - start, 3)}


def git(*args):
    p = command(["git", *args])
    if p["exit_code"]:
        raise ValueError(p["stderr"])
    return p["stdout"].strip()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify_files(root, entries):
    errors = []
    for relative, expected in entries.items():
        path = root / relative
        if path.is_symlink() or not path.is_file():
            errors.append(f"missing/non-regular baseline: {relative}")
        elif blob(path.read_bytes()) != expected:
            errors.append(f"baseline changed: {relative}")
    return errors


def baseline_integrity():
    lock = read(DOCS / "baseline-lock.json")
    errors = []
    if lock["base_commit"] != BASE:
        errors.append("base commit changed")
    # Reconstruct from the Owner-named commit, never trust a mutable local hash list.
    original = {}
    raw = git("ls-tree", "-r", BASE, "--", *lock["paths"])
    for line in raw.splitlines():
        meta, path = line.split("\t")
        original[path] = meta.split()[2]
    required_paths = ["docs", "upstream", "reference", "evidence/source-file-manifest.json",
                      "scripts/verify_g2.py", "scripts/tests",
                      ".github/workflows/g2-geometry.yml", "LICENSE", "SHA256SUMS"]
    if lock["paths"] != required_paths or not original or original != lock["files"]:
        errors.append("baseline lock inventory differs from trusted base commit")
    errors.extend(verify_files(ROOT, original))
    for prefix in ("upstream", "reference/approved/geometry-golden-v0.1",
                   "reference/candidate/geometry-golden-v0.1"):
        actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / prefix).rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts
                  and ".pytest_cache" not in p.parts and not p.name.endswith(".pyc")}
        expected = {p for p in original if p.startswith(prefix + "/")}
        if actual != expected:
            errors.append(f"frozen directory inventory changed: {prefix}")
    return result("FAIL" if errors else "PASS", files=len(original), errors=errors)


def branch_safety(expected=None, clean=False):
    branch = git("branch", "--show-current")
    logical = branch
    if os.getenv("GITHUB_ACTIONS") == "true":
        logical = (os.getenv("GITHUB_HEAD_REF") if os.getenv("GITHUB_EVENT_NAME") == "pull_request"
                   else os.getenv("GITHUB_REF_NAME")) or branch
    errors = []
    if not logical or logical in {"master", "develop"} or logical.startswith("release/"):
        errors.append("execution must use a named, non-protected work branch")
    if expected and logical != expected:
        errors.append(f"expected branch {expected}; found {logical}")
    ancestor = command(["git", "merge-base", "--is-ancestor", BASE, "HEAD"])
    if ancestor["exit_code"]:
        errors.append("HEAD does not descend from approved P3 baseline")
    remote_master = git("rev-parse", "refs/remotes/origin/master")
    if remote_master != MASTER:
        errors.append("formal master baseline changed; Owner reconciliation required")
    dirty = git("status", "--porcelain", "--untracked-files=normal")
    if clean and dirty:
        errors.append("launch/acceptance requires a clean worktree")
    return result("FAIL" if errors else "PASS", branch=logical, head=git("rev-parse", "HEAD"),
                  origin_master=remote_master, clean=not dirty, errors=errors)


def environment():
    probes = {name: command(argv) for name, argv in {
        "rustc": ["rustc", "--version"], "cargo": ["cargo", "--version"],
        "rustfmt": ["rustfmt", "--version"], "clippy": ["cargo", "clippy", "--version"],
        "metadata": ["cargo", "metadata", "--locked", "--no-deps", "--format-version", "1"],
    }.items()}
    errors = [name for name, p in probes.items() if p["exit_code"]]
    for name in ("rustc", "cargo"):
        if not probes[name]["stdout"].startswith(name + " 1.98.1 "):
            errors.append(f"{name} must be 1.98.1")
    if sys.version_info < (3, 11):
        errors.append("verification requires Python >=3.11 (tomllib)")
    manifest = tomllib.loads((ROOT / "Cargo.toml").read_text())
    toolchain = tomllib.loads((ROOT / "rust-toolchain.toml").read_text())
    pkg = manifest["workspace"]["package"]
    if (str(manifest["workspace"]["resolver"]), str(pkg["edition"]), pkg["rust-version"],
            toolchain["toolchain"]["channel"]) != ("3", "2024", "1.98.1", "1.98.1"):
        errors.append("workspace/toolchain contract mismatch")
    if "crates/solarfactors-core" not in manifest["workspace"]["members"]:
        errors.append("workspace must contain solarfactors-core")
    for path in ("Cargo.lock", "crates/solarfactors-core/Cargo.toml", "crates/solarfactors-core/src/lib.rs"):
        if not (ROOT / path).is_file():
            errors.append(f"workspace file missing: {path}")
    try:
        schema_version = importlib.metadata.version("jsonschema")
        if schema_version != "4.25.1":
            errors.append("jsonschema must match the existing G2 pin 4.25.1")
    except importlib.metadata.PackageNotFoundError:
        schema_version = None
        errors.append("existing G2 dependency jsonschema missing")
    return result("FAIL" if errors else "PASS", python=sys.version, platform=platform.platform(),
                  jsonschema=schema_version, probes=probes, errors=errors)


def inventory():
    errors = []
    for stem in PAIRS:
        texts = []
        for lang in ("en", "zh-CN"):
            path = DOCS / f"{stem}.{lang}.md"
            if not path.is_file() or len(path.read_text()) < 200:
                errors.append(f"missing/incomplete formal document {path.name}")
            else:
                texts.append(path.read_text())
        if len(texts) == 2:
            # Chinese text can directly follow a Latin identifier; Unicode \b
            # would incorrectly omit M9 in "M9和".
            pattern = (r"(?<![A-Za-z0-9])(?:CAP\d{2}|CDR-\d{3}|OD-\d{2}|BF-\d{2}|"
                       r"M\d+|[0-9a-f]{40,64})(?![A-Za-z0-9])")
            if set(re.findall(pattern, texts[0])) != set(re.findall(pattern, texts[1])):
                errors.append(f"bilingual evidence/decision identifiers differ: {stem}")
    for name in ("CODEX_FULL_IMPLEMENTATION_TASK.md", "acceptance-matrix.json",
                 "owner-decisions.json", "execution-state.json", "contract-audit.json"):
        if not (DOCS / name).is_file():
            errors.append(f"missing execution contract {name}")
    matrix = read(DOCS / "acceptance-matrix.json")
    caps = matrix["capabilities"]
    if [c["id"] for c in caps] != [f"CAP{i:02}" for i in range(1, 33)]:
        errors.append("capability inventory must exactly preserve CAP01-CAP32")
    milestones = matrix["milestones"]
    if [m["id"] for m in milestones] != [f"M{i}" for i in range(3, 14)]:
        errors.append("milestone inventory incomplete")
    for c in caps[:22]:
        if c["scope"] != "Must Have V1" or not c["milestones"]:
            errors.append(f"Must Have V1 mapping incomplete: {c['id']}")
        if not set(c["milestones"]) <= {m["id"] for m in milestones}:
            errors.append(f"unknown milestone mapped by {c['id']}")
    for c in caps[22:]:
        if c["scope"] == "Must Have V1" or c["milestones"]:
            errors.append(f"excluded/future capability became a V1 blocker: {c['id']}")
    if [layer["id"] for layer in matrix["layers"]] != [f"A{i}" for i in range(12)]:
        errors.append("acceptance architecture must cover A0-A11")
    for m in milestones:
        if not m["required_tests"] or not m["required_artifacts"] or not m["layers"]:
            errors.append(f"empty acceptance definition: {m['id']}")
        if len(m["required_tests"]) != len(set(m["required_tests"])):
            errors.append(f"duplicate required tests: {m['id']}")
    audit = read(DOCS / "contract-audit.json")
    expected_algorithms = re.findall(r"^## ((?:MATH|GEO|VF|IRR|ENG|EXEC)-\d+)",
                                    (ROOT / "docs/02_ALGORITHM_INVENTORY.md").read_text(), re.M)
    if [a["id"] for a in audit["algorithms"]] != expected_algorithms:
        errors.append("algorithm audit inventory differs from source")
    if {a["id"] for a in audit["deviations"]} != {f"DEV-{i:03}" for i in range(1, 28)}:
        errors.append("deviation audit inventory incomplete")
    return result("FAIL" if errors else "PASS", capabilities=len(caps), milestones=len(milestones),
                  algorithms=len(expected_algorithms), errors=errors)


def g2():
    with tempfile.TemporaryDirectory(prefix="pvfactors-g2-") as temp:
        output = Path(temp) / "g2.json"
        p = command([sys.executable, "scripts/verify_g2.py", "--output", str(output)])
        report = read(output) if output.is_file() else {}
        return result("PASS" if p["exit_code"] == 0 and report.get("pass") is True else "FAIL",
                      report=report, command=p)


def contract_digest():
    # Pin normative semantics, not implementation bytes. Tool/adapter code can
    # evolve within that contract; its exact hashes are recorded separately.
    # A digest is not proof that mutable verification code obeys the contract.
    files = [ROOT / "AGENTS.md"]
    files += [DOCS / f"{stem}.{lang}.md" for stem in PAIRS
              if stem != "LOOP_ENGINEERING_READINESS_REPORT" for lang in ("en", "zh-CN")]
    files += [DOCS / name for name in ("acceptance-matrix.json", "baseline-lock.json",
                                      "contract-audit.json", "CODEX_FULL_IMPLEMENTATION_TASK.md")]
    h = hashlib.sha256()
    for p in sorted(files):
        h.update(p.relative_to(ROOT).as_posix().encode() + b"\0" + p.read_bytes())
    return h.hexdigest()


def owner_gate(scope="full"):
    data = read(DOCS / "owner-decisions.json")
    expected_ids = [f"OD-{i:02}" for i in range(1, 13)]
    errors = []
    if [d["id"] for d in data["decisions"]] != expected_ids:
        errors.append("Owner decision inventory changed")
    required = expected_ids if scope == "full" else ["OD-01", "OD-10", "OD-11"]
    pending = [d["id"] for d in data["decisions"] if d["id"] in required and
               (d["status"] != "APPROVED" or not d["owner_evidence"])]
    approval = data["approval"]
    for key in ("reviewer", "evidence", "implementation_branch", "readiness_commit"):
        if not approval.get(key):
            errors.append(f"launch approval missing {key}")
    revision = approval.get("readiness_commit")
    if revision:
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            errors.append("readiness approval must name a full commit SHA")
        elif command(["git", "merge-base", "--is-ancestor", revision, "HEAD"])["exit_code"]:
            errors.append("reviewed readiness commit is not an ancestor of HEAD")
    if approval.get("status") != "APPROVED" or approval.get("contract_sha256") != contract_digest():
        errors.append("Owner launch approval does not bind the current contract digest")
    for key in ("environment", "governance"):
        record = data[key]
        if record.get("status") != "APPROVED" or not record.get("receipt"):
            errors.append(f"{key} launch evidence pending")
        else:
            receipt = ROOT / record["receipt"]["path"]
            if not receipt.is_file() or digest(receipt) != record["receipt"]["sha256"]:
                errors.append(f"{key} evidence hash mismatch")
    if pending:
        errors.append("Owner decisions pending: " + ", ".join(pending))
    # A new mandatory-stop finding cannot disappear merely because the original
    # twelve decisions were approved. Closure needs explicit Owner evidence.
    for blocker in data.get("new_launch_blockers", []):
        evidence = ROOT / blocker["evidence"]
        if not evidence.is_file() or digest(evidence) != blocker["sha256"]:
            errors.append(f"launch blocker evidence missing/changed: {blocker['id']}")
        if blocker.get("status") != "CLOSED_BY_OWNER" or not blocker.get("owner_evidence"):
            errors.append(f"new launch blocker requires Owner closure: {blocker['id']}")
    return result("NOT_READY" if errors else "PASS", pending=pending, errors=errors,
                  contract_sha256=contract_digest())


def r0_probe():
    # No image pull, build or Golden generation. Existing image must really run.
    expression = ("import json,sys; sys.path.insert(0,'reference/tools'); "
                  "from geometry_golden import environment_report; "
                  "print(json.dumps(environment_report()))")
    argv = ["docker", "run", "--rm", "--pull=never", "--platform", "linux/amd64",
            "--network=none", "--read-only", "--tmpfs", "/tmp",
            "--volume", f"{ROOT}:/workspace:ro", "--workdir", "/workspace"]
    for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "PYTHONHASHSEED"):
        argv += ["--env", f"{key}={'0' if key == 'PYTHONHASHSEED' else '1'}"]
    argv += ["pvfactors-rs-g2-r0", "python3.12", "-c", expression]
    p = command(argv, timeout=60)
    observed = None
    if p["exit_code"] == 0:
        try:
            observed = json.loads(p["stdout"])
        except json.JSONDecodeError:
            pass
    ok = (observed and observed.get("canonical_environment_match") is True
          and observed.get("runtime", {}).get("environment_id") == "031158a1d1be8cdb9093")
    return result("PASS" if ok else "NOT_READY", category="ENVIRONMENT GAP" if not ok else "R0",
                  observed=observed, command=p)


def parse_tests(text, required=()):
    """Require real libtest cases and summaries; exit zero alone is never enough."""
    records = re.findall(r"^test (\S+) \.\.\. (ok|FAILED|ignored)\s*$", text, re.M)
    summaries = re.findall(r"test result: (ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;", text)
    names = [name for name, state in records]
    counts = {"passed": sum(int(s[1]) for s in summaries),
              "failed": sum(int(s[2]) for s in summaries),
              "skipped": sum(int(s[3]) for s in summaries), "waived": 0}
    errors = []
    if not summaries or not names or counts["passed"] == 0:
        errors.append("no executed acceptance tests (zero-test success rejected)")
    if len(names) != len(set(names)):
        errors.append("duplicate test execution IDs")
    if len(names) != counts["passed"] + counts["failed"] + counts["skipped"]:
        errors.append("test records do not match summary counts")
    if counts["failed"] or counts["skipped"] or any(s[0] != "ok" for s in summaries):
        errors.append("failed/ignored required tests")
    if any(state != "ok" for _, state in records):
        errors.append("non-passing test record")
    missing = sorted(set(required) - {n for n, state in records if state == "ok"})
    if missing:
        errors.append("missing required tests: " + ", ".join(missing))
    return result("FAIL" if errors else "PASS", tests=names, **counts, errors=errors)


def geometry_payload(artifact):
    """Project only computational obligations, keeping all topology exact.

    Historical Python warnings/reference-only annotations are not Rust behavior.
    P3 section 8 explicitly makes error messages non-protocol diagnostic text.
    These exclusions are fixed, path-specific, and part of Owner review.
    """
    data = {k: artifact[k] for k in ("case_id", "input", "result", "nonfinite_mask")}
    data = json.loads(json.dumps(data, allow_nan=False))
    computational = data["result"]
    computational.pop("warnings", None)
    computational.pop("reference_length_m", None)
    if isinstance(computational.get("ground"), dict):
        computational["ground"].pop("reference_extent_m", None)
    for error in computational.get("errors", []):
        error.pop("message", None)
    return data


def compare_geometry(actual, expected=GOLDEN / "corrected", case_ids=None):
    sys.path.insert(0, str(ROOT / "reference/compare"))
    from compare_cross_runtime import Comparison
    case_ids = case_ids if case_ids is not None else read(GOLDEN / "APPROVAL.json")["approved_case_ids"]
    errors = []
    actual_files = sorted(p.name for p in actual.glob("*.json"))
    expected_files = sorted(f"{case}.json" for case in case_ids)
    if not case_ids or len(case_ids) != len(set(case_ids)) or actual_files != expected_files:
        errors.append("case omission/addition/duplicate: actual inventory differs from required cases")
    comparison = Comparison(read(TOLERANCE))
    checked = 0
    for case in case_ids:
        path = actual / f"{case}.json"
        if path.is_symlink():
            errors.append(f"actual payload must not be a symlink: {case}")
            continue
        if not path.is_file():
            continue
        wanted = read(expected / f"{case}.json")
        observed = read(path)
        # Test-only adapter payload. Metadata/provenance is supplied by the harness,
        # never accepted as proof that Rust ran. All result fields are compared.
        wanted = geometry_payload(wanted)
        errors.extend(json_type_errors(wanted, observed, f"$.{case}"))
        comparison.compare(wanted, observed, f"$.{case}")
        checked += 1
    differences = (comparison.topology_differences + comparison.exact_payload_differences
                   + comparison.numerical_differences)
    if differences:
        errors.append(f"{len(differences)} exact/numeric mismatches")
    return result("FAIL" if errors else "PASS", cases_run=checked, cases_required=len(case_ids),
                  exact_checks=comparison.topology_checks,
                  numeric_checks=comparison.numerical_counts,
                  differences=differences[:30], errors=errors)


def json_type_errors(expected, actual, path):
    # Python equality considers 0 == False; exact index/status fields must not.
    if type(expected) is not type(actual):
        return [f"JSON type mismatch: {path}"]
    if isinstance(expected, dict):
        return [error for key in expected.keys() & actual.keys()
                for error in json_type_errors(expected[key], actual[key], f"{path}.{key}")]
    if isinstance(expected, list):
        return [error for i, (a, b) in enumerate(zip(expected, actual))
                for error in json_type_errors(a, b, f"{path}[{i}]")]
    return []


def required_artifacts(directory, names):
    errors = []
    for name in names:
        path = directory / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing/empty artifact: {name}")
    return result("FAIL" if errors else "PASS", errors=errors)


def milestone(m, execute=True):
    missing = [p for p in m["implementation_files"] if not (ROOT / p).is_file()]
    if not m.get("runner_file") or not (ROOT / m["runner_file"]).is_file():
        missing.append(m.get("runner_file") or "approved executable test adapter")
    if missing:
        return result("NOT_READY", milestone=m["id"], reason="implementation/test adapter absent",
                      missing=missing, tests_run=0)
    if m["oracle_status"] != "APPROVED" or m["checker"] != "geometry-v1":
        return result("NOT_READY", milestone=m["id"], reason="approved oracle/comparator binding absent")
    if not execute:
        return result("NOT_READY", milestone=m["id"], reason="execution suppressed by failed integrity/approval gate")
    with tempfile.TemporaryDirectory(prefix="pvfactors-acceptance-") as temp:
        folder = Path(temp)
        env = dict(os.environ, PVFACTORS_ACCEPTANCE_OUTPUT=str(folder),
                   RUST_TEST_THREADS="1", CARGO_TERM_COLOR="never")
        # Fresh output directory and live subprocess prevent accepting a stale report.
        p = command(m["command"], env=env, timeout=900)
        (folder / "test.log").write_text(p["stdout"] + p["stderr"])
        tests = parse_tests(p["stdout"], m["required_tests"])
        artifacts = required_artifacts(folder, ["run.json", "test.log"])
        receipt_errors = []
        if (folder / "run.json").is_file():
            receipt = read(folder / "run.json")
            for key, expected in {"schema_version": 1, "git_commit": git("rev-parse", "HEAD"),
                                  "producer": "solarfactors-core", "milestone": m["id"]}.items():
                if receipt.get(key) != expected:
                    receipt_errors.append(f"run receipt {key} mismatch")
        comparison = compare_geometry(folder / "results")
        good = (p["exit_code"] == 0 and not receipt_errors and all(x["status"] == "PASS"
                for x in (tests, artifacts, comparison)))
        store = ROOT / "reference/work/acceptance"
        store.mkdir(parents=True, exist_ok=True)
        saved = Path(tempfile.mkdtemp(prefix=m["id"] + "-", dir=store))
        shutil.copytree(folder, saved, dirs_exist_ok=True)
        return result("PASS" if good else "FAIL", milestone=m["id"], tests=tests,
                      artifacts=artifacts, comparison=comparison, command=p,
                      artifact_root=saved.relative_to(ROOT).as_posix(),
                      artifact_hashes={p.relative_to(folder).as_posix(): digest(p)
                                       for p in folder.rglob("*") if p.is_file()},
                      errors=receipt_errors)


def overall(checks):
    statuses = [v["status"] for v in checks.values()]
    return "FAIL" if "FAIL" in statuses else ("NOT_READY" if "NOT_READY" in statuses else "PASS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["assets", "preflight", "milestone", "final", "compare-geometry"])
    parser.add_argument("milestone", nargs="?")
    parser.add_argument("--scope", choices=["full", "geometry"], default="full")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--actual", type=Path, help="standalone Geometry payload comparison; not milestone acceptance")
    args = parser.parse_args()
    report = {"schema_version": 1, "mode": args.mode, "base_commit": BASE,
              "reference_revision": REFERENCE, "golden_versions": ["geometry-golden-v0.1"],
              "tolerance_versions": ["geometry-tolerance-v0.1"]}
    try:
        if args.scope == "geometry" and not (
                args.mode == "preflight" or
                (args.mode == "milestone" and args.milestone in {"geometry", "M3"})):
            raise ValueError("geometry-only approval is limited to preflight or milestone M3; "
                             "later milestones and final require full-project approval")
        matrix = read(DOCS / "acceptance-matrix.json")
        decisions = read(DOCS / "owner-decisions.json")
        clean = args.mode != "assets"
        checks = {"baseline_integrity": baseline_integrity(), "inventory": inventory(),
                  "branch": branch_safety(clean=clean), "environment": environment(), "g2": g2()}
        if args.mode not in {"assets", "compare-geometry"}:
            checks["owner_launch"] = owner_gate(args.scope)
            expected_branch = decisions["approval"].get("implementation_branch")
            if expected_branch:
                checks["launch_branch"] = branch_safety(expected=expected_branch, clean=True)
        if args.mode == "compare-geometry":
            if args.actual is None or not args.actual.is_dir():
                raise ValueError("compare-geometry requires --actual pointing to exported results")
            checks["geometry_comparison_only"] = compare_geometry(args.actual)
            report["boundary"] = "Comparator result only; no claim of implementation execution or milestone PASS"
        if args.mode == "preflight":
            checks["r0"] = r0_probe()
            p = command([sys.executable, "-m", "unittest", "discover", "-s", "scripts/tests",
                         "-p", "test_verify_project*.py", "-v"])
            count = re.search(r"Ran (\d+) tests", p["stderr"])
            checks["harness_self_tests"] = result("PASS" if p["exit_code"] == 0 and count and
                int(count[1]) > 0 else "FAIL", command=p, tests_run=int(count[1]) if count else 0)
        runs = {}
        if args.mode in {"milestone", "final"}:
            selected = matrix["milestones"] if args.mode == "final" else [m for m in matrix["milestones"]
                        if args.milestone in (m["id"], m["slug"])]
            if not selected:
                raise ValueError("unknown/missing milestone; use a slug from acceptance-matrix.json")
            for m in selected:
                runs[m["id"]] = milestone(m, execute=overall(checks) == "PASS")
            checks["milestones"] = result(overall(runs), runs=runs)
        if args.mode == "final":
            # Release evidence has no approved schema/adapter yet: never infer it from file names.
            checks["release_evidence"] = result("NOT_READY", reason=
                "Owner-approved package/platform/performance evidence adapters required by OD-08/09/12")
            report["capabilities_implemented"] = [c["id"] for c in matrix["capabilities"][:22]
                if all(runs.get(m, {}).get("status") == "PASS" for m in c["milestones"])]
            report["capabilities_unmet"] = [c["id"] for c in matrix["capabilities"][:22]
                                           if c["id"] not in report["capabilities_implemented"]]
            report["capabilities_excluded"] = [{"id": c["id"], "scope": c["scope"]}
                                                for c in matrix["capabilities"][22:]]
            report["platforms"] = [{"platform": p, "status": "NOT_READY"}
                                    for p in matrix["required_platforms"]]
            report["packages"] = []
            report["performance_evidence"] = []
            report["test_counts"] = {k: sum(r.get("tests", {}).get(k, 0) for r in runs.values())
                                     for k in ("passed", "failed", "skipped", "waived")}
            report["test_counts"]["tests_run"] = sum(report["test_counts"].values())
        report.update(checks=checks, status=overall(checks), git_commit=git("rev-parse", "HEAD"),
                      cdrs={"approved": ["CDR-003", "CDR-006"],
                            "pending": ["CDR-001", "CDR-002", "CDR-004", "CDR-005", "CDR-007"]},
                      contract_sha256=contract_digest(),
                      verification_tool_sha256=digest(Path(__file__)),
                      verification_self_tests_sha256={p.relative_to(ROOT).as_posix(): digest(p)
                          for p in sorted((ROOT / "scripts/tests").glob("test_verify_project*.py"))})
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        report.update(status="FAIL", error=f"{type(error).__name__}: {error}")
    text = json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("mode", "status", "git_commit", "error") if k in report},
                     ensure_ascii=False))
    if not args.output:
        print(text)
    return {"PASS": 0, "FAIL": 1, "NOT_READY": 2}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
