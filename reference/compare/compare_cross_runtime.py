#!/usr/bin/env python3
"""Compare Geometry payloads across runtimes while separating metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TOLERANCE = ROOT / "reference/tolerance/geometry-tolerance-v0.1.json"
ARTIFACT_DIRS = ("raw", "normalized", "corrected")
METADATA_FIELDS = {"reference", "generator", "provenance"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def tolerance_class(path: str) -> str:
    field = path.rsplit(".", 1)[-1].split("[", 1)[0]
    if field.endswith("_deg") or field == "alpha_rad" or "azimuth" in field or "tilt" in field:
        return "angle"
    if field in {"normal", "front_normal", "back_normal", "solar_2d_vector"}:
        return "orientation"
    if "length" in field or field == "width_m":
        return "length"
    return "position"


class Comparison:
    def __init__(self, tolerance: dict[str, Any]):
        self.tolerance = tolerance["comparison"]
        self.exact_fields = set(tolerance["exact_fields"])
        self.topology_differences: list[dict[str, Any]] = []
        self.exact_payload_differences: list[dict[str, Any]] = []
        self.numerical_differences: list[dict[str, Any]] = []
        self.numerical_counts = {name: 0 for name in self.tolerance}
        self.max_absolute_difference = {name: 0.0 for name in self.tolerance}
        self.topology_checks = 0

    @staticmethod
    def difference(path: str, left: Any, right: Any) -> dict[str, Any]:
        return {"path": path, "left": left, "right": right}

    def compare_exact(self, left: Any, right: Any, path: str) -> None:
        self.topology_checks += 1
        if left != right:
            self.topology_differences.append(self.difference(path, left, right))

    def compare(self, left: Any, right: Any, path: str = "$", exact: bool = False) -> None:
        if exact:
            self.compare_exact(left, right, path)
            return
        if type(left) is not type(right):
            self.exact_payload_differences.append(
                self.difference(path, type(left).__name__, type(right).__name__)
            )
            return
        if isinstance(left, dict):
            if set(left) != set(right):
                self.exact_payload_differences.append(
                    self.difference(path, sorted(left), sorted(right))
                )
                return
            for key in sorted(left):
                child = f"{path}.{key}"
                self.compare(
                    left[key], right[key], child,
                    key in self.exact_fields or key == "input",
                )
            return
        if isinstance(left, list):
            if len(left) != len(right):
                self.exact_payload_differences.append(self.difference(path, len(left), len(right)))
                return
            for index, (left_item, right_item) in enumerate(zip(left, right, strict=True)):
                self.compare(left_item, right_item, f"{path}[{index}]")
            return
        if isinstance(left, float):
            category = tolerance_class(path)
            limits = self.tolerance[category]
            field = path.rsplit(".", 1)[-1].split("[", 1)[0]
            compared_left, compared_right = left, right
            if field == "alpha_rad":
                compared_left, compared_right = math.degrees(left), math.degrees(right)
            absolute_difference = abs(compared_left - compared_right)
            allowed = limits["absolute"] + limits["relative"] * max(
                abs(compared_left), abs(compared_right)
            )
            self.numerical_counts[category] += 1
            self.max_absolute_difference[category] = max(
                self.max_absolute_difference[category], absolute_difference
            )
            if not math.isfinite(left) or not math.isfinite(right) or absolute_difference > allowed:
                self.numerical_differences.append({
                    "path": path,
                    "class": category,
                    "left": left,
                    "right": right,
                    "absolute_difference": absolute_difference,
                    "allowed": allowed,
                })
            return
        if left != right:
            self.exact_payload_differences.append(self.difference(path, left, right))


def artifact_inventory(root: Path) -> list[Path]:
    return [
        path.relative_to(root)
        for folder in ARTIFACT_DIRS
        for path in sorted((root / folder).glob("*.json"))
    ]


def payload(artifact: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in artifact.items() if key not in METADATA_FIELDS}


def compare_candidates(left: Path, right: Path) -> dict[str, Any]:
    tolerance = read_json(TOLERANCE)
    comparison = Comparison(tolerance)
    left_inventory = artifact_inventory(left)
    right_inventory = artifact_inventory(right)
    inventory_match = left_inventory == right_inventory
    if inventory_match:
        for relative in left_inventory:
            comparison.compare(
                payload(read_json(left / relative)),
                payload(read_json(right / relative)),
                f"$.{relative.as_posix()}",
            )

    left_summary = read_json(left / "validation-summary.json")
    right_summary = read_json(right / "validation-summary.json")
    topology_pass = inventory_match and not comparison.topology_differences
    numerical_pass = inventory_match and not comparison.numerical_differences
    exact_payload_pass = inventory_match and not comparison.exact_payload_differences
    payload_pass = topology_pass and numerical_pass and exact_payload_pass
    canonical_runtime_match = right_summary["environment"]["canonical_environment_match"]
    return {
        "schema_version": "0.1",
        "comparison": (
            "cross-runtime Geometry payload with provenance/environment "
            "metadata separated"
        ),
        "tolerance_profile": {
            "id": tolerance["profile_id"],
            "sha256": sha256_file(TOLERANCE),
        },
        "left": {
            "path": str(left),
            "manifest_sha256": sha256_file(left / "manifest.json"),
            "environment": left_summary["environment"],
        },
        "right": {
            "path": str(right),
            "manifest_sha256": sha256_file(right / "manifest.json"),
            "environment": right_summary["environment"],
        },
        "inventory": {
            "pass": inventory_match,
            "left_artifacts": len(left_inventory),
            "right_artifacts": len(right_inventory),
        },
        "topology": {
            "pass": topology_pass,
            "exact_match": topology_pass,
            "checks": comparison.topology_checks,
            "differences": comparison.topology_differences[:100],
        },
        "numerical": {
            "pass": numerical_pass,
            "limits": comparison.tolerance,
            "counts": comparison.numerical_counts,
            "max_absolute_difference": comparison.max_absolute_difference,
            "differences": comparison.numerical_differences[:100],
        },
        "exact_payload": {
            "pass": exact_payload_pass,
            "differences": comparison.exact_payload_differences[:100],
        },
        "metadata": {
            "compared_as_payload": False,
            "excluded_artifact_fields": sorted(METADATA_FIELDS),
            "environment_ids_differ": (
                left_summary["environment"]["runtime"]["environment_id"]
                != right_summary["environment"]["runtime"]["environment_id"]
            ),
        },
        "canonical_runtime_match": canonical_runtime_match,
        "payload_pass": payload_pass,
        "pass": payload_pass and canonical_runtime_match,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = compare_candidates(args.left, args.right)
    if args.output:
        write_json(args.output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(not report["pass"])


if __name__ == "__main__":
    main()
