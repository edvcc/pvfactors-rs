#!/usr/bin/env python3
"""Build the concrete, reviewable G2 Geometry case catalog."""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "reference/cases/canonical_cases.json"
DEFAULT_OUTPUT = ROOT / "reference/cases/g2_geometry_cases_v0.1.json"


def load_source() -> dict[str, dict]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    return {case["id"]: case for case in payload["cases"]}


def ordered(source: dict[str, dict], case_id: str, *, new_id: str | None = None,
            domain: str | None = None, tags: list[str] | None = None) -> dict:
    item = copy.deepcopy(source[case_id])
    return {
        "id": new_id or case_id,
        "kind": "ordered_pvarray",
        "domain": domain or item["domain"],
        "description": item["description"],
        "tags": tags or item["tags"],
        "source_case_id": case_id,
        "geometry": item["geometry"],
        "inputs": item["inputs"],
        "expected": {"reference": "capture", "v1": "normalize_and_validate"},
    }


def primitive(case_id: str, operation: str, arguments: dict, *,
              domain: str = "boundary_policy", tags: list[str],
              description: str, expected: dict) -> dict:
    return {
        "id": case_id,
        "kind": "primitive",
        "domain": domain,
        "description": description,
        "tags": tags,
        "primitive": {"operation": operation, "arguments": arguments},
        "expected": expected,
    }


def build() -> dict:
    source = load_source()
    ids = [
        "C01", "C02", "C03", "C04",
        "TILT_LEFT", "TILT_FLAT", "TILT_1e-10", "TILT_NEAR_LEFT", "TILT_90.0",
        "SHADING_NONE_CANDIDATE", "SHADING_PARTIAL_CANDIDATE", "SHADING_HIGH_CANDIDATE",
        "SUN_90.0", "SUN_ALONG_AXIS",
        "CUT_2", "CUT_8", "CUT_ASYMMETRIC",
        "UNDERGROUND", "CUT_ZERO",
    ]
    cases = [ordered(source, case_id) for case_id in ids]

    # Concrete ground-extent cases. The frozen reference still computes on
    # [-100, 100]; corrected_expectation applies the proposed public extent.
    for case_id, extent, description, domain in [
        ("GROUND_NORMAL_EXTENT", [-10.0, 10.0], "finite configurable ground extent", "valid"),
        ("GROUND_BOUNDARY_ENDPOINT", [-0.5, 0.5], "single row endpoints exactly on extent boundary", "boundary_policy"),
        ("GROUND_NEAR_BOUNDARY", [-0.500000000001, 0.500000000001], "single row one picometre inside extent", "boundary_policy"),
    ]:
        item = ordered(source, "C01", new_id=case_id, domain=domain,
                       tags=["ground_extent", "derived_concrete"])
        item["description"] = description
        item["geometry"]["ground_extent"] = extent
        if case_id in ("GROUND_BOUNDARY_ENDPOINT", "GROUND_NEAR_BOUNDARY"):
            item["inputs"]["surface_tilt"] = [0.0]
        cases.append(item)

    # Full mirror pair: row geometry, sun vector, normals, extent, row order,
    # and side interpretation are all transformed by the validator.
    mirror_base = ordered(source, "C03", new_id="MIRROR_BASE", tags=["mirror", "derived_concrete"])
    mirror_base["description"] = "mirror property base"
    mirror_image = copy.deepcopy(mirror_base)
    mirror_image["id"] = "MIRROR_IMAGE"
    mirror_image["description"] = "full x-mirror of MIRROR_BASE"
    mirror_image["inputs"]["solar_azimuth"] = [90.0]
    mirror_image["inputs"]["surface_azimuth"] = [90.0]
    cases += [mirror_base, mirror_image]

    # Structured invalid input cases. Nonfinite values use an explicit JSON
    # token so the catalog remains standards-compliant and hash-stable.
    invalid_axis = ordered(source, "C03", new_id="INVALID_AXIS_AZIMUTH", domain="invalid",
                           tags=["invalid", "axis_azimuth", "derived_concrete"])
    invalid_axis["geometry"]["axis_azimuth"] = {"nonfinite": "NaN"}
    invalid_axis["description"] = "nonfinite axis azimuth"
    invalid_surface = ordered(source, "C03", new_id="INVALID_SURFACE_AZIMUTH", domain="invalid",
                              tags=["invalid", "surface_azimuth", "derived_concrete"])
    invalid_surface["inputs"]["surface_azimuth"] = [180.0]
    invalid_surface["description"] = "non-flat surface azimuth is not axis plus or minus 90 degrees"
    invalid_nan = ordered(source, "C03", new_id="INVALID_NAN", domain="invalid",
                          tags=["invalid", "nonfinite", "derived_concrete"])
    invalid_nan["inputs"]["solar_zenith"] = [{"nonfinite": "NaN"}]
    invalid_nan["description"] = "NaN solar zenith"
    invalid_inf = ordered(source, "C03", new_id="INVALID_INF", domain="invalid",
                          tags=["invalid", "nonfinite", "derived_concrete"])
    invalid_inf["inputs"]["surface_tilt"] = [{"nonfinite": "+Inf"}]
    invalid_inf["description"] = "positive infinity surface tilt"
    invalid_extent = ordered(source, "C01", new_id="INVALID_EXTENT_REVERSED", domain="invalid",
                             tags=["invalid", "ground_extent", "derived_concrete"])
    invalid_extent["geometry"]["ground_extent"] = [1.0, -1.0]
    invalid_extent["description"] = "ground extent lower bound is not less than upper bound"
    cases += [invalid_axis, invalid_surface, invalid_nan, invalid_inf, invalid_extent]

    tol = 1e-8
    cases += [
        primitive(
            "PRIM_COMPLETE_COVER_DIFFERENCE", "difference",
            {"u": [[0.0, 0.0], [1.0, 0.0]], "v": [[-1.0, 0.0], [2.0, 0.0]]},
            domain="reference_deviation", tags=["difference", "complete_cover", "DEV-016"],
            description="subtracting a complete cover must return empty",
            expected={"reference_length_m": 1.0, "corrected_intervals": []},
        ),
        primitive(
            "PRIM_ENDPOINT_TOUCH", "classify_intersection",
            {"u": [[0.0, 0.0], [1.0, 0.0]], "v": [[1.0, 0.0], [2.0, 0.0]]},
            tags=["touch", "endpoint"], description="segments share exactly one endpoint",
            expected={"classification": "endpoint_touch", "positive_length_overlap": False},
        ),
        primitive(
            "PRIM_POINT_TOUCH", "classify_intersection",
            {"u": [[0.0, 0.0], [2.0, 0.0]], "v": [[1.0, -1.0], [1.0, 1.0]]},
            tags=["touch", "point"], description="non-collinear segments intersect at one point",
            expected={"classification": "point_touch", "positive_length_overlap": False},
        ),
        primitive(
            "PRIM_POSITIVE_OVERLAP", "classify_intersection",
            {"u": [[0.0, 0.0], [2.0, 0.0]], "v": [[1.0, 0.0], [3.0, 0.0]]},
            tags=["touch", "overlap"], description="collinear segments overlap with positive length",
            expected={"classification": "positive_length_overlap", "positive_length_overlap": True},
        ),
        primitive(
            "PRIM_ZERO_LENGTH", "classify_segment",
            {"segment": [[1.0, 1.0], [1.0, 1.0]]}, tags=["zero_length", "topology"],
            description="zero-length numerical surface retains a logical slot",
            expected={"active": False, "logical_slot_retained": True},
        ),
        primitive(
            "PRIM_PARALLEL_PROJECTION", "projection",
            {"segment": [[0.0, 1.0], [1.0, 1.0]], "origin": [0.0, 0.0], "direction": [1.0, 0.0]},
            tags=["projection", "parallel"], description="parallel non-coincident projection",
            expected={"classification": "parallel", "intersection": None},
        ),
        primitive(
            "PRIM_COINCIDENT_PROJECTION", "projection",
            {"segment": [[0.0, 0.0], [1.0, 0.0]], "origin": [2.0, 0.0], "direction": [1.0, 0.0]},
            tags=["projection", "coincident"], description="projection line is coincident with segment",
            expected={"classification": "coincident", "intersection": None},
        ),
    ]
    for label, value in [
        ("MINUS_ULP", math.nextafter(tol, 0.0)),
        ("EXACT", tol),
        ("PLUS_ULP", math.nextafter(tol, math.inf)),
    ]:
        cases.append(primitive(
            f"PRIM_ACTIVE_TOL_{label}", "classify_segment",
            {"segment": [[0.0, 0.0], [value, 0.0]]},
            tags=["tolerance", "ulp", "active_length"],
            description=f"active-length threshold {label.lower().replace('_', ' ')}",
            expected={"active": value > tol, "logical_slot_retained": True, "length_m": value},
        ))

    return {
        "schema_version": "0.1",
        "status": "candidate_recommended_for_approval",
        "reference": {
            "name": "pvlib/solarfactors",
            "version": "v1.6.1",
            "commit": "ecbfc863657e239817603a43898ae173c7ccad9c",
        },
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(f"wrote {len(payload['cases'])} concrete cases to {args.output}")


if __name__ == "__main__":
    main()
