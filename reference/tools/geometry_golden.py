#!/usr/bin/env python3
"""G2 reference capture, normalization, comparison, and invariant tooling.

This module is development-only. It imports the frozen Python reference from
``upstream/solarfactors`` and never mutates it.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import importlib.metadata as md
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import warnings
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REFERENCE_SOURCE = ROOT / "upstream/solarfactors"
CASES = ROOT / "reference/cases/g2_geometry_cases_v0.1.json"
TOLERANCE = ROOT / "reference/tolerance/geometry-tolerance-v0.1.json"
SCHEMAS = ROOT / "reference/schemas"
DEFAULT_CANDIDATE = ROOT / "reference/candidate/geometry-golden-v0.1"
REFERENCE_SHA = "ecbfc863657e239817603a43898ae173c7ccad9c"
REFERENCE_VERSION = "v1.6.1"
GENERATOR_VERSION = "0.1.0"
REFERENCE_EXTENT = [-100.0, 100.0]

sys.path.insert(0, str(REFERENCE_SOURCE))


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False, allow_nan=False) + "\n").encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(value, sort_keys=True, indent=2,
                                ensure_ascii=False, allow_nan=False).encode() + b"\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def generator_identity() -> dict:
    files = sorted((ROOT / "reference/tools").glob("*.py"))
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(ROOT).as_posix().encode() + b"\0")
        digest.update(path.read_bytes())
    return {
        "version": GENERATOR_VERSION,
        "commit": git("log", "-1", "--format=%H", "--", "reference/tools"),
        "sha256": digest.hexdigest(),
        "files": [p.relative_to(ROOT).as_posix() for p in files],
    }


def runtime_identity() -> dict:
    packages = {}
    for name in ("numpy", "scipy", "pandas", "pvlib", "shapely", "jsonschema"):
        try:
            packages[name] = md.version(name)
        except md.PackageNotFoundError:
            packages[name] = "MISSING"
    base = {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "packages": packages,
        "thread_environment": {
            key: os.environ.get(key, "")
            for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "PYTHONHASHSEED")
        },
    }
    base["environment_id"] = sha256_bytes(canonical_bytes(base))[:20]
    return base


def reference_identity() -> dict:
    runtime = runtime_identity()
    return {
        "name": "pvlib/solarfactors",
        "version": REFERENCE_VERSION,
        "commit": REFERENCE_SHA,
        "python": runtime["python"],
        "numpy": runtime["packages"]["numpy"],
        "shapely": runtime["packages"]["shapely"],
        "pvlib": runtime["packages"]["pvlib"],
        "environment_id": runtime["environment_id"],
        "runtime": runtime,
    }


def decode_number(value: Any) -> Any:
    if isinstance(value, dict) and set(value) == {"nonfinite"}:
        return {"NaN": math.nan, "+Inf": math.inf, "-Inf": -math.inf}[value["nonfinite"]]
    if isinstance(value, list):
        return [decode_number(v) for v in value]
    if isinstance(value, dict):
        return {k: decode_number(v) for k, v in value.items()}
    return value


def encode_nonfinite(value: Any, path: str = "$", mask: list[str] | None = None) -> Any:
    mask = [] if mask is None else mask
    if isinstance(value, float) and not math.isfinite(value):
        token = "NaN" if math.isnan(value) else ("+Inf" if value > 0 else "-Inf")
        mask.append(path)
        return {"nonfinite": token}
    if isinstance(value, dict):
        return {str(k): encode_nonfinite(v, f"{path}.{k}", mask) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode_nonfinite(v, f"{path}[{i}]", mask) for i, v in enumerate(value)]
    try:
        import numpy as np
        if isinstance(value, np.ndarray):
            return encode_nonfinite(value.tolist(), path, mask)
        if isinstance(value, np.generic):
            return encode_nonfinite(value.item(), path, mask)
    except ImportError:
        pass
    return value


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def normalize_angle(value: float) -> float:
    normalized = value % 360.0
    return 0.0 if normalized == 360.0 else normalized


def circular_distance(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def validate_v1(case: dict) -> list[dict]:
    if case["kind"] == "primitive":
        return []
    errors: list[dict] = []
    geometry = decode_number(case["geometry"])
    inputs = decode_number(case["inputs"])

    def error(code: str, field: str, message: str) -> None:
        errors.append({"code": code, "field": field, "message": message})

    axis = geometry.get("axis_azimuth")
    if not finite_number(axis):
        error("GEOMETRY_NONFINITE", "geometry.axis_azimuth", "axis azimuth must be finite")
    n_rows = geometry.get("n_pvrows")
    width = geometry.get("pvrow_width")
    height = geometry.get("pvrow_height")
    gcr = geometry.get("gcr")
    if not isinstance(n_rows, int) or isinstance(n_rows, bool) or n_rows < 1:
        error("GEOMETRY_ROW_COUNT", "geometry.n_pvrows", "row count must be an integer >= 1")
    if not finite_number(width) or width <= 0:
        error("GEOMETRY_WIDTH", "geometry.pvrow_width", "row width must be finite and > 0")
    if not finite_number(height):
        error("GEOMETRY_HEIGHT", "geometry.pvrow_height", "row height must be finite")
    if not finite_number(gcr) or not (0 < gcr <= 1):
        error("GEOMETRY_GCR", "geometry.gcr", "V1 gcr must be in (0, 1]")
    extent = geometry.get("ground_extent")
    if not (isinstance(extent, list) and len(extent) == 2 and all(finite_number(v) for v in extent)):
        error("GEOMETRY_EXTENT", "geometry.ground_extent", "ground extent must contain two finite bounds")
    elif not extent[0] < extent[1]:
        error("GEOMETRY_EXTENT", "geometry.ground_extent", "ground extent lower bound must be less than upper bound")
    for row, sides in geometry.get("cut", {}).items():
        try:
            row_index = int(row)
        except (TypeError, ValueError):
            row_index = -1
        if not isinstance(n_rows, int) or not (0 <= row_index < n_rows):
            error("GEOMETRY_CUT_ROW", f"geometry.cut.{row}", "cut row index is outside the array")
        for side, count in sides.items():
            if side not in ("front", "back") or not isinstance(count, int) or isinstance(count, bool) or count < 1:
                error("GEOMETRY_CUT", f"geometry.cut.{row}.{side}", "cut must be an integer >= 1")
    vector_fields = ["solar_zenith", "solar_azimuth", "surface_tilt", "surface_azimuth"]
    lengths = {len(inputs.get(name, [])) for name in vector_fields if isinstance(inputs.get(name), list)}
    if len(lengths) != 1 or 0 in lengths:
        error("GEOMETRY_SHAPE", "inputs", "angle arrays must have equal nonzero length")
        return errors
    for field in vector_fields:
        values = inputs.get(field)
        if not isinstance(values, list):
            error("GEOMETRY_SHAPE", f"inputs.{field}", "angle input must be an array")
            continue
        for index, value in enumerate(values):
            if not finite_number(value):
                error("GEOMETRY_NONFINITE", f"inputs.{field}[{index}]", "angle input must be finite")
    if errors:
        return errors
    assert finite_number(axis) and finite_number(width) and finite_number(height) and finite_number(gcr)
    for index, (zenith, tilt, surface_azimuth) in enumerate(zip(
            inputs["solar_zenith"], inputs["surface_tilt"], inputs["surface_azimuth"], strict=True)):
        if not 0.0 <= zenith <= 90.0:
            error("GEOMETRY_SOLAR_DOMAIN", f"inputs.solar_zenith[{index}]", "V1 geometry supports zenith in [0, 90]")
        if not 0.0 <= tilt <= 90.0:
            error("GEOMETRY_TILT_UNSUPPORTED", f"inputs.surface_tilt[{index}]", "V1 supports tilt in [0, 90]")
        if tilt > 0.0:
            relationship = circular_distance(normalize_angle(surface_azimuth - axis), 90.0)
            relationship = min(relationship, circular_distance(normalize_angle(surface_azimuth - axis), 270.0))
            if relationship > 5e-11:
                error("GEOMETRY_AZIMUTH_RELATION", f"inputs.surface_azimuth[{index}]",
                      "non-flat surface azimuth must be axis azimuth plus or minus 90 degrees")
        rotation = tilt if normalize_angle(surface_azimuth - axis) > 180.0 else -tilt
        clearance = height - width * abs(math.sin(math.radians(rotation))) / 2.0
        if clearance <= 1e-10:
            error("GEOMETRY_CLEARANCE", f"inputs.surface_tilt[{index}]",
                  "row must remain more than 1e-10 m above ground")
        if isinstance(n_rows, int) and isinstance(extent, list) and extent[0] < extent[1]:
            pitch = width / gcr
            half_x = width * abs(math.cos(math.radians(rotation))) / 2.0
            if -half_x < extent[0] - 1e-10 or (n_rows - 1) * pitch + half_x > extent[1] + 1e-10:
                error("GEOMETRY_ROW_OUTSIDE_EXTENT", "geometry.ground_extent",
                      "all row endpoints must lie inside or on the finite ground extent")
    return errors


def coords_at(coords: Any, index: int) -> list[list[float]]:
    arr = coords.as_array[:, :, index]
    return [[float(arr[0, 0]), float(arr[0, 1])], [float(arr[1, 0]), float(arr[1, 1])]]


def vector_at(vector: Any, index: int) -> list[float] | None:
    if vector is None:
        return None
    return [float(vector[0, index]), float(vector[1, index])]


def surface_record(ts_surface: Any, key: dict, n_states: int) -> dict:
    lengths = [float(ts_surface.length[i]) for i in range(n_states)]
    active = [length > 1e-8 for length in lengths]
    return {
        "logical_key": key,
        "reference_index": int(ts_surface.index),
        "active": active,
        "active_index": [None] * n_states,
        "shaded": bool(ts_surface.shaded),
        "coordinates_m": [coords_at(ts_surface.coords, i) for i in range(n_states)],
        "length_m": lengths,
        "normal": [vector_at(ts_surface.n_vector, i) for i in range(n_states)] if ts_surface.n_vector is not None else None,
    }


def ordered_surface_records(pvarray: Any) -> list[dict]:
    records: list[dict] = []
    n_states = pvarray.n_states
    for element_index, element in enumerate(pvarray.ts_ground.shadow_elements):
        for interval, surface in enumerate(element.surface_list):
            records.append(surface_record(surface, {
                "kind": "ground", "source": "shadow", "ground_element": element_index,
                "cut_interval": interval, "row": None, "side": None, "segment": None,
                "illumination": "shaded",
            }, n_states))
    for element_index, element in enumerate(pvarray.ts_ground.illum_elements):
        for interval, surface in enumerate(element.surface_list):
            records.append(surface_record(surface, {
                "kind": "ground", "source": "illumination", "ground_element": element_index,
                "cut_interval": interval, "row": None, "side": None, "segment": None,
                "illumination": "illuminated",
            }, n_states))
    for row_index, row in enumerate(pvarray.ts_pvrows):
        for side_name in ("front", "back"):
            side = getattr(row, side_name)
            for segment_index, segment in enumerate(side.list_segments):
                for illumination, collection in (("illuminated", segment.illum), ("shaded", segment.shaded)):
                    for surface in collection.list_ts_surfaces:
                        records.append(surface_record(surface, {
                            "kind": "pvrow", "source": "pvrow", "ground_element": None,
                            "cut_interval": None, "row": row_index, "side": side_name,
                            "segment": segment_index, "illumination": illumination,
                        }, n_states))
    expected = pvarray.all_ts_surfaces
    if len(records) != len(expected):
        raise AssertionError("logical surface inventory differs from reference inventory")
    if [r["reference_index"] for r in records] != list(range(len(records))):
        raise AssertionError("reference index order is not contiguous")
    for frame in range(n_states):
        active_index = 0
        for record in records:
            if record["active"][frame]:
                record["active_index"][frame] = active_index
                active_index += 1
    return records


def capture_ordered(case: dict) -> tuple[str, dict, list[dict]]:
    import numpy as np
    from pvfactors.geometry import OrderedPVArray

    geometry = decode_number(case["geometry"])
    inputs = decode_number(case["inputs"])
    cut = {int(row): sides for row, sides in geometry.get("cut", {}).items()}
    pvarray = OrderedPVArray(
        axis_azimuth=geometry["axis_azimuth"], gcr=geometry["gcr"],
        pvrow_height=geometry["pvrow_height"], n_pvrows=geometry["n_pvrows"],
        pvrow_width=geometry["pvrow_width"], cut=cut,
    )
    arrays = {name: np.asarray(inputs[name], dtype=float) for name in
              ("solar_zenith", "solar_azimuth", "surface_tilt", "surface_azimuth")}
    caught: list[str] = []
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter("always")
        try:
            pvarray.fit(arrays["solar_zenith"], arrays["solar_azimuth"],
                        arrays["surface_tilt"], arrays["surface_azimuth"])
        except Exception as exc:  # reference behavior is evidence
            return "expected_reference_failure", {
                "outcome": "reference_exception",
                "exception": {"type": type(exc).__name__, "message": str(exc)},
            }, []
        caught = sorted({str(item.message) for item in seen})

    n_states = pvarray.n_states
    rotations = [float(v) for v in pvarray.rotation_vec]
    solar_vectors = [[float(pvarray.solar_2d_vectors[0, i]), float(pvarray.solar_2d_vectors[1, i])]
                     for i in range(n_states)]
    projection = []
    for index, vector in enumerate(solar_vectors):
        alpha = math.atan2(vector[1], vector[0])
        projection.append({
            "rotation_deg": rotations[index], "solar_2d_vector": vector, "alpha_rad": alpha,
            "classification": "parallel_ground" if abs(vector[1]) <= 1e-12 else "regular",
        })
    rows = []
    raw_shadows = []
    for row_index, row in enumerate(pvarray.ts_pvrows):
        row_entry = {
            "row": row_index,
            "center_m": [float(row.xy_center[0]), float(row.xy_center[1])],
            "endpoints_m": [coords_at(row.full_pvrow_coords, i) for i in range(n_states)],
            "front_normal": [vector_at(row.front.n_vector, i) for i in range(n_states)],
            "back_normal": [[-v for v in vector_at(row.front.n_vector, i)] for i in range(n_states)],
            "width_m": float(geometry["pvrow_width"]),
            "shaded_length_front_m": [float(row.front.shaded_length[i]) for i in range(n_states)],
            "shaded_length_back_m": [float(row.back.shaded_length[i]) for i in range(n_states)],
        }
        rows.append(row_entry)
        row_shadows = []
        for frame, endpoints in enumerate(row_entry["endpoints_m"]):
            alpha = projection[frame]["alpha_rad"]
            with np.errstate(all="ignore"):
                xs = [point[0] - point[1] / np.tan(alpha) for point in endpoints]
            row_shadows.append([[float(min(xs)), 0.0], [float(max(xs)), 0.0]])
        raw_shadows.append({"row": row_index, "coordinates_m": row_shadows})

    ground = pvarray.ts_ground
    ground_entry = {
        "reference_extent_m": REFERENCE_EXTENT,
        "requested_extent_m": geometry["ground_extent"],
        "cut_points_m": [[[float(point.x[i]), float(point.y[i])] for point in ground.cut_point_coords]
                         for i in range(n_states)],
        "raw_projected_shadows": raw_shadows,
        "clipped_shadow_elements": [
            {"element": i, "coordinates_m": [coords_at(element.coords, frame) for frame in range(n_states)]}
            for i, element in enumerate(ground.shadow_elements)
        ],
        "illuminated_elements": [
            {"element": i, "coordinates_m": [coords_at(element.coords, frame) for frame in range(n_states)]}
            for i, element in enumerate(ground.illum_elements)
        ],
        "overlap_flags": [bool(v) for v in ground.flag_overlap],
    }
    surfaces = ordered_surface_records(pvarray)
    active_counts = [sum(record["active"][frame] for record in surfaces) for frame in range(n_states)]
    result = {
        "outcome": "captured",
        "projection": projection,
        "pv_rows": rows,
        "ground": ground_entry,
        "surfaces": surfaces,
        "topology": {
            "logical_surface_count": len(surfaces),
            "active_surface_count": active_counts,
            "reference_order": [record["logical_key"] for record in surfaces],
            "reference_to_active": [record["active_index"] for record in surfaces],
        },
        "warnings": caught,
    }
    deviations = []
    if geometry["ground_extent"] != REFERENCE_EXTENT:
        deviations.append({
            "dev_id": "DEV-004", "cdr_id": "CDR-003", "field": "ground.extent",
            "raw_reference": REFERENCE_EXTENT, "corrected_expectation": geometry["ground_extent"],
            "explanation": "frozen reference hard-codes a numerical extent; V1 exposes a finite public extent",
        })
    return "candidate", result, deviations


def primitive_reference(case: dict) -> tuple[str, dict, list[dict]]:
    from shapely.geometry import LineString, Point
    from pvfactors.geometry.utils import difference, projection

    operation = case["primitive"]["operation"]
    args = case["primitive"]["arguments"]
    deviations: list[dict] = []
    if operation == "difference":
        geometry = difference(LineString(args["u"]), LineString(args["v"]))
        coords = [] if geometry.is_empty else (
            [list(geometry.coords)] if geometry.geom_type == "LineString"
            else [list(part.coords) for part in geometry.geoms]
        )
        result = {"outcome": "captured", "operation": operation,
                  "geometry_type": geometry.geom_type, "coordinates": coords, "length_m": float(geometry.length)}
        if case["id"] == "PRIM_COMPLETE_COVER_DIFFERENCE":
            deviations.append({
                "dev_id": "DEV-016", "cdr_id": "CDR-006", "field": "result.length_m",
                "raw_reference": float(geometry.length), "corrected_expectation": 0.0,
                "explanation": "the minuend is completely covered and the mathematical difference is empty",
            })
        return "candidate", result, deviations
    if operation == "projection":
        line = LineString(args["segment"])
        projected = projection(Point(args["origin"]), args["direction"], line)
        result = {"outcome": "captured", "operation": operation,
                  "reference_geometry_type": projected.geom_type,
                  "reference_empty": bool(projected.is_empty)}
        return "candidate", result, deviations
    if operation == "classify_intersection":
        u, v = LineString(args["u"]), LineString(args["v"])
        intersection = u.intersection(v)
        if intersection.geom_type == "Point":
            endpoints = [Point(p) for p in (args["u"][0], args["u"][1], args["v"][0], args["v"][1])]
            at_endpoint = sum(point.equals(intersection) for point in endpoints) >= 2
            classification = "endpoint_touch" if at_endpoint else "point_touch"
        elif intersection.length > 0:
            classification = "positive_length_overlap"
        else:
            classification = "disjoint"
        return "candidate", {"outcome": "captured", "operation": operation,
                             "classification": classification,
                             "intersection_length_m": float(intersection.length)}, deviations
    if operation == "classify_segment":
        line = LineString(args["segment"])
        length = float(line.length)
        return "candidate", {"outcome": "captured", "operation": operation,
                             "length_m": length, "active": length > 1e-8,
                             "logical_slot_retained": True}, deviations
    raise ValueError(f"unknown primitive operation: {operation}")


def artifact(case: dict, classification: str, status: str, result: dict,
             deviations: list[dict]) -> dict:
    mask: list[str] = []
    encoded_input = encode_nonfinite({
        "kind": case["kind"], "domain": case["domain"],
        "geometry": case.get("geometry"), "inputs": case.get("inputs"),
        "primitive": case.get("primitive"),
    }, "$.input", mask)
    encoded_result = encode_nonfinite(result, "$.result", mask)
    case_hash = sha256_bytes(canonical_bytes(case))
    payload_hash = sha256_bytes(canonical_bytes(encoded_result))
    return {
        "schema_version": "0.1",
        "case_id": case["id"],
        "classification": classification,
        "status": status,
        "reference": reference_identity(),
        "generator": generator_identity(),
        "input": encoded_input,
        "result": encoded_result,
        "provenance": {
            "source": f"pvlib/solarfactors@{REFERENCE_SHA}",
            "method": "direct frozen-reference introspection" if case["kind"] == "ordered_pvarray" else "direct frozen primitive invocation",
            "transformation": "none" if classification == "raw_reference" else classification,
            "license_relevance": "derived fixture; upstream BSD-3-Clause notice retained in reference/PVLIB_LICENSE.txt",
            "case_sha256": case_hash,
            "payload_sha256": payload_hash,
        },
        "nonfinite_mask": sorted(mask),
        "deviations": deviations,
    }


def capture_case(case: dict) -> dict:
    try:
        if case["kind"] == "ordered_pvarray":
            status, result, deviations = capture_ordered(case)
        else:
            status, result, deviations = primitive_reference(case)
    except Exception as exc:
        status, result, deviations = "expected_reference_failure", {
            "outcome": "reference_exception", "exception": {"type": type(exc).__name__, "message": str(exc)}
        }, []
    return artifact(case, "raw_reference", status, result, deviations)


def normalized_artifact(raw: dict) -> dict:
    value = copy.deepcopy(raw)
    value["classification"] = "normalized_reference"
    value["provenance"]["transformation"] = "canonical JSON; explicit nonfinite mask; stable logical ordering"
    value["provenance"]["payload_sha256"] = sha256_bytes(canonical_bytes(value["result"]))
    return value


def clip_ground(result: dict, extent: list[float]) -> dict:
    value = copy.deepcopy(result)
    value["ground"]["corrected_extent_m"] = extent
    for group in ("clipped_shadow_elements", "illuminated_elements"):
        for element in value["ground"][group]:
            for coords in element["coordinates_m"]:
                coords[0][0] = min(max(coords[0][0], extent[0]), extent[1])
                coords[1][0] = min(max(coords[1][0], extent[0]), extent[1])
                if coords[0][0] > coords[1][0]:
                    coords[0][0] = coords[1][0]
    for surface in value["surfaces"]:
        if surface["logical_key"]["kind"] != "ground":
            continue
        for frame, coords in enumerate(surface["coordinates_m"]):
            coords[0][0] = min(max(coords[0][0], extent[0]), extent[1])
            coords[1][0] = min(max(coords[1][0], extent[0]), extent[1])
            if coords[0][0] > coords[1][0]:
                coords[0][0] = coords[1][0]
            surface["length_m"][frame] = abs(coords[1][0] - coords[0][0])
            surface["active"][frame] = surface["length_m"][frame] > 1e-8
    n_states = len(value["topology"]["active_surface_count"])
    for frame in range(n_states):
        active_index = 0
        for surface in value["surfaces"]:
            surface["active_index"][frame] = active_index if surface["active"][frame] else None
            active_index += int(surface["active"][frame])
        value["topology"]["active_surface_count"][frame] = active_index
    value["topology"]["reference_to_active"] = [s["active_index"] for s in value["surfaces"]]
    return value


def corrected_artifact(case: dict, normalized: dict) -> dict:
    errors = validate_v1(case)
    deviations = copy.deepcopy(normalized["deviations"])
    if errors:
        result = {"outcome": "v1_error", "errors": errors, "panic": False}
        status = "v1_rejected_input"
    elif case["kind"] == "primitive":
        result = {"outcome": "corrected_expectation", **copy.deepcopy(case["expected"])}
        status = "candidate"
    else:
        inputs = decode_number(case["inputs"])
        if any(abs(value - 90.0) <= 5e-11 for value in inputs["solar_zenith"]):
            result = {
                "outcome": "classified_state",
                "state": "horizon_no_direct_projection",
                "pv_rows": copy.deepcopy(normalized["result"].get("pv_rows", [])),
                "ground_policy": "all finite extent illuminated; direct shadow surfaces inactive",
                "projection": copy.deepcopy(normalized["result"].get("projection", [])),
            }
        else:
            result = copy.deepcopy(normalized["result"])
            extent = decode_number(case["geometry"])["ground_extent"]
            if result.get("outcome") == "captured" and extent != REFERENCE_EXTENT:
                result = clip_ground(result, extent)
        status = "candidate"
    value = artifact(case, "corrected_expectation", status, result, deviations)
    value["provenance"]["method"] = "CDR-003/CDR-006 candidate policy applied to normalized reference"
    value["provenance"]["transformation"] = "field-level corrections are listed in deviations"
    return value


def load_cases(path: Path = CASES) -> list[dict]:
    return read_json(path)["cases"]


def capture(output: Path, cases_path: Path = CASES) -> None:
    raw_dir = output / "raw"
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    raw_dir.mkdir(parents=True)
    for case in load_cases(cases_path):
        write_json(raw_dir / f"{case['id']}.json", capture_case(case))
    print(f"captured {len(load_cases(cases_path))} raw artifacts in {raw_dir}")


def normalize(output: Path, cases_path: Path = CASES) -> None:
    normalized_dir, corrected_dir = output / "normalized", output / "corrected"
    normalized_dir.mkdir(parents=True, exist_ok=False)
    corrected_dir.mkdir(parents=True, exist_ok=False)
    for case in load_cases(cases_path):
        raw = read_json(output / "raw" / f"{case['id']}.json")
        normalized = normalized_artifact(raw)
        corrected = corrected_artifact(case, normalized)
        write_json(normalized_dir / f"{case['id']}.json", normalized)
        write_json(corrected_dir / f"{case['id']}.json", corrected)
    print(f"normalized and corrected {len(load_cases(cases_path))} artifacts")


def stable_timestamp() -> str:
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return dt.datetime.fromtimestamp(int(epoch), tz=dt.timezone.utc).isoformat().replace("+00:00", "Z")
    return git("show", "-s", "--format=%cI", "HEAD")


def build_manifest(output: Path, cases_path: Path = CASES) -> dict:
    cases = load_cases(cases_path)
    entries = []
    for classification, folder in (("raw_reference", "raw"), ("normalized_reference", "normalized"),
                                   ("corrected_expectation", "corrected")):
        for case in cases:
            path = output / folder / f"{case['id']}.json"
            item = read_json(path)
            surfaces = item["result"].get("surfaces", [])
            frames = 0
            if surfaces:
                frames = len(surfaces[0]["length_m"])
            entries.append({
                "case_id": case["id"], "classification": classification,
                "file": path.relative_to(output).as_posix(), "field_name": "geometry",
                "axes": ["logical_surface", "time", "endpoint", "xy"],
                "units": {"position": "m", "length": "m", "angle": "degree", "orientation": "dimensionless"},
                "dtype": "canonical-json/f64", "shape": [len(surfaces), frames, 2, 2] if surfaces else [],
                "payload_sha256": sha256_file(path), "nonfinite_mask": item["nonfinite_mask"],
                "status": item["status"], "provenance": item["provenance"],
            })
    tags = sorted({tag for case in cases for tag in case["tags"]})
    deviations = []
    for case in cases:
        corrected = read_json(output / "corrected" / f"{case['id']}.json")
        deviations.extend({"case_id": case["id"], **entry} for entry in corrected["deviations"])
    manifest = {
        "schema_version": "0.1",
        "golden_version": "geometry-golden-v0.1-candidate",
        "status": "candidate_recommended_for_approval",
        "generated_at_utc": stable_timestamp(),
        "reference": reference_identity(),
        "generator": generator_identity(),
        "case_catalog_sha256": sha256_file(cases_path),
        "tolerance_profile": {
            "id": "geometry-tolerance-v0.1", "status": "recommended_for_approval",
            "file": TOLERANCE.relative_to(ROOT).as_posix(), "sha256": sha256_file(TOLERANCE),
        },
        "artifacts": entries,
        "coverage": {"case_count": len(cases), "artifact_count": len(entries), "tags": tags},
        "known_deviations": deviations,
    }
    write_json(output / "manifest.json", manifest)
    return manifest


def schema_validate(output: Path, cases_path: Path = CASES) -> list[str]:
    from jsonschema import Draft202012Validator
    errors: list[str] = []
    for schema_path in sorted(SCHEMAS.glob("*.schema.json")):
        try:
            Draft202012Validator.check_schema(read_json(schema_path))
        except Exception as issue:
            errors.append(f"{schema_path.relative_to(ROOT)}: invalid JSON Schema: {issue}")
    checks = [
        (ROOT / "reference/cases/canonical_cases.json", SCHEMAS / "case.schema.json"),
        (cases_path, SCHEMAS / "g2-geometry-case.schema.json"),
    ]
    for folder in ("raw", "normalized", "corrected"):
        checks += [(path, SCHEMAS / "geometry-golden.schema.json") for path in sorted((output / folder).glob("*.json"))]
    checks.append((output / "manifest.json", SCHEMAS / "geometry-golden-manifest.schema.json"))
    for data_path, schema_path in checks:
        validator = Draft202012Validator(read_json(schema_path))
        for issue in validator.iter_errors(read_json(data_path)):
            location = ".".join(str(v) for v in issue.absolute_path)
            errors.append(f"{data_path.relative_to(ROOT)}:{location}: {issue.message}")
    return errors


def compare_directories(left: Path, right: Path) -> list[str]:
    differences: list[str] = []
    left_files = sorted(path.relative_to(left) for path in left.rglob("*.json"))
    right_files = sorted(path.relative_to(right) for path in right.rglob("*.json"))
    if left_files != right_files:
        differences.append("file inventories differ")
        return differences
    for relative in left_files:
        if (left / relative).read_bytes() != (right / relative).read_bytes():
            differences.append(relative.as_posix())
    return differences


def numeric_close(a: float, b: float, absolute: float, relative: float) -> bool:
    return abs(a - b) <= absolute + relative * max(abs(a), abs(b))


def validate_invariants(output: Path, cases_path: Path = CASES) -> dict:
    tolerance = read_json(TOLERANCE)
    length_tol = tolerance["comparison"]["length"]
    reports = []
    failures = []
    case_map = {case["id"]: case for case in load_cases(cases_path)}
    for path in sorted((output / "normalized").glob("*.json")):
        item = read_json(path)
        case = case_map[item["case_id"]]
        if (case["kind"] != "ordered_pvarray" or case["domain"] == "invalid"
                or item["result"].get("outcome") != "captured"):
            continue
        result = item["result"]
        surfaces = result["surfaces"]
        n_frames = len(result["topology"]["active_surface_count"])
        case_failures = []
        serialized_keys = [json.dumps(surface["logical_key"], sort_keys=True) for surface in surfaces]
        if len(serialized_keys) != len(set(serialized_keys)):
            case_failures.append("logical SurfaceKey values are not unique")
        if [surface["reference_index"] for surface in surfaces] != list(range(len(surfaces))):
            case_failures.append("ReferenceIndex is not exact contiguous reference order")
        width = decode_number(case["geometry"])["pvrow_width"]
        for frame in range(n_frames):
            for row in range(decode_number(case["geometry"])["n_pvrows"]):
                for side in ("front", "back"):
                    side_surfaces = [s for s in surfaces if s["logical_key"]["kind"] == "pvrow"
                                     and s["logical_key"]["row"] == row and s["logical_key"]["side"] == side]
                    total = sum(s["length_m"][frame] for s in side_surfaces)
                    shaded = sum(s["length_m"][frame] for s in side_surfaces if s["shaded"])
                    if not numeric_close(total, width, length_tol["absolute"], length_tol["relative"]):
                        case_failures.append(f"frame {frame} row {row} {side}: side conservation {total} != {width}")
                    if shaded < -length_tol["absolute"] or shaded > width + length_tol["absolute"]:
                        case_failures.append(f"frame {frame} row {row} {side}: shade bounds {shaded}")
            for surface in surfaces:
                length = surface["length_m"][frame]
                if surface["active"][frame] != (length > 1e-8):
                    case_failures.append(f"frame {frame} reference {surface['reference_index']}: active mismatch")
                coords = surface["coordinates_m"][frame]
                if surface["active"][frame] and not all(math.isfinite(value) for point in coords for value in point):
                    case_failures.append(f"frame {frame} reference {surface['reference_index']}: active nonfinite endpoint")
            ground = [s for s in surfaces if s["logical_key"]["kind"] == "ground" and s["active"][frame]]
            intervals = sorted((s["coordinates_m"][frame][0][0], s["coordinates_m"][frame][1][0],
                                s["reference_index"]) for s in ground)
            cursor = REFERENCE_EXTENT[0]
            for lo, hi, reference_index in intervals:
                if lo > cursor + length_tol["absolute"]:
                    case_failures.append(f"frame {frame}: unexplained ground gap {cursor}..{lo}")
                if lo < cursor - length_tol["absolute"]:
                    case_failures.append(f"frame {frame}: positive ground overlap at reference {reference_index}")
                cursor = max(cursor, hi)
            if cursor < REFERENCE_EXTENT[1] - length_tol["absolute"]:
                case_failures.append(f"frame {frame}: ground ends at {cursor}")
            active_indices = [surface["active_index"][frame] for surface in surfaces if surface["active"][frame]]
            if active_indices != list(range(len(active_indices))):
                case_failures.append(f"frame {frame}: ActiveIndex is not contiguous")
        reports.append({"case_id": case["id"], "pass": not case_failures, "failures": case_failures})
        failures.extend(f"{case['id']}: {failure}" for failure in case_failures)

    # Corrected finite extents must have complete, non-overlapping coverage.
    for case_id in ("GROUND_NORMAL_EXTENT", "GROUND_BOUNDARY_ENDPOINT", "GROUND_NEAR_BOUNDARY"):
        case = case_map[case_id]
        result = read_json(output / "corrected" / f"{case_id}.json")["result"]
        extent = decode_number(case["geometry"])["ground_extent"]
        case_failures = []
        surfaces = result["surfaces"]
        n_frames = len(result["topology"]["active_surface_count"])
        for frame in range(n_frames):
            intervals = sorted((surface["coordinates_m"][frame][0][0],
                                surface["coordinates_m"][frame][1][0])
                               for surface in surfaces
                               if surface["logical_key"]["kind"] == "ground" and surface["active"][frame])
            cursor = extent[0]
            for lo, hi in intervals:
                if lo > cursor + length_tol["absolute"]:
                    case_failures.append(f"frame {frame}: corrected extent gap {cursor}..{lo}")
                if lo < cursor - length_tol["absolute"]:
                    case_failures.append(f"frame {frame}: corrected extent overlap at {lo}")
                cursor = max(cursor, hi)
            if cursor < extent[1] - length_tol["absolute"]:
                case_failures.append(f"frame {frame}: corrected extent ends at {cursor}")
        reports.append({"case_id": f"{case_id}_CORRECTED", "pass": not case_failures,
                        "failures": case_failures})
        failures.extend(f"{case_id}_CORRECTED: {failure}" for failure in case_failures)

    # Invalid cases must use the structured, non-panic V1 error contract.
    for case in case_map.values():
        if case["domain"] != "invalid":
            continue
        corrected = read_json(output / "corrected" / f"{case['id']}.json")
        valid_error = (corrected["status"] == "v1_rejected_input"
                       and corrected["result"].get("outcome") == "v1_error"
                       and corrected["result"].get("panic") is False
                       and bool(corrected["result"].get("errors")))
        reports.append({"case_id": f"{case['id']}_ERROR_CONTRACT", "pass": valid_error,
                        "failures": [] if valid_error else ["missing structured non-panic V1 error"]})
        if not valid_error:
            failures.append(f"{case['id']}: missing structured non-panic V1 error")

    for case in case_map.values():
        if case["kind"] != "primitive":
            continue
        corrected = read_json(output / "corrected" / f"{case['id']}.json")["result"]
        expected = case["expected"]
        mismatches = [key for key, value in expected.items() if corrected.get(key) != value]
        reports.append({"case_id": f"{case['id']}_EXPECTATION", "pass": not mismatches,
                        "failures": [f"corrected field mismatch: {key}" for key in mismatches]})
        failures.extend(f"{case['id']}: corrected field mismatch: {key}" for key in mismatches)

    # Full mirror check on corrected artifacts.
    base = read_json(output / "corrected/MIRROR_BASE.json")["result"]
    image = read_json(output / "corrected/MIRROR_IMAGE.json")["result"]
    mirror_failures = []
    center = 2.0
    base_rows = base.get("pv_rows", [])
    image_rows = image.get("pv_rows", [])
    for row_index, base_row in enumerate(base_rows):
        image_row = image_rows[len(image_rows) - 1 - row_index]
        for base_point, image_point in zip(base_row["endpoints_m"][0], reversed(image_row["endpoints_m"][0]), strict=True):
            if not numeric_close(2 * center - base_point[0], image_point[0], 5e-12, 5e-13):
                mirror_failures.append(f"row {row_index} x-coordinate")
            if not numeric_close(base_point[1], image_point[1], 5e-12, 5e-13):
                mirror_failures.append(f"row {row_index} y-coordinate")
        base_normal = base_row["front_normal"][0]
        image_normal = image_row["front_normal"][0]
        if not (numeric_close(-base_normal[0], image_normal[0], 5e-12, 5e-13)
                and numeric_close(base_normal[1], image_normal[1], 5e-12, 5e-13)):
            mirror_failures.append(f"row {row_index} normal")
    reports.append({"case_id": "MIRROR_PAIR", "pass": not mirror_failures, "failures": mirror_failures})
    failures.extend(f"MIRROR_PAIR: {failure}" for failure in mirror_failures)
    return {"pass": not failures, "case_reports": reports, "failures": failures}


def deviation_report(output: Path) -> dict:
    rows = []
    for path in sorted((output / "corrected").glob("*.json")):
        item = read_json(path)
        rows.extend({"case_id": item["case_id"], **entry} for entry in item["deviations"])
    return {"schema_version": "0.1", "pass": all(row.get("dev_id") and row.get("cdr_id") for row in rows),
            "differences": rows}


def validate_docs() -> dict:
    pairs = [
        "CDR-003_GEOMETRY_INPUT_DOMAIN_POLICY",
        "CDR-006_GEOMETRY_NUMERICAL_TOPOLOGY_POLICY",
        "GEOMETRY_GOLDEN_CONTRACT",
        "GEOMETRY_GOLDEN_APPROVAL_RECORD",
        "GEOMETRY_TOLERANCE_PROFILE_V0.1",
        "G2_GEOMETRY_ACCEPTANCE_REVIEW",
        "P3_RUST_GEOMETRY_KERNEL_ENTRY_CONTRACT",
        "RAW_REFERENCE_VS_CORRECTED_EXPECTATION_REPORT",
    ]
    failures = []
    constants = [REFERENCE_SHA, "geometry-golden-v0.1-candidate", "geometry-tolerance-v0.1"]
    for stem in pairs:
        en, zh = ROOT / f"docs/g2/{stem}.en.md", ROOT / f"docs/g2/{stem}.zh-CN.md"
        if not en.is_file() or not zh.is_file():
            failures.append(f"missing pair: {stem}")
            continue
        en_text, zh_text = en.read_text(), zh.read_text()
        for constant in constants:
            if (constant in en_text) != (constant in zh_text):
                failures.append(f"constant pair mismatch {stem}: {constant}")
        for token in ("Recommended for Approval", "CONDITIONALLY PASS", "Awaiting Repository Owner Approval"):
            if (token in en_text) != (token in zh_text):
                failures.append(f"status pair mismatch {stem}: {token}")
    return {"pass": not failures, "pairs": len(pairs), "failures": failures}


def environment_report() -> dict:
    requirements = {}
    for line in (ROOT / "reference/requirements-canonical.txt").read_text().splitlines():
        if line and not line.startswith("#"):
            name, version = line.split("==", 1)
            requirements[name] = version
    runtime = runtime_identity()
    mismatches = []
    if runtime["python"] != "3.12.14":
        mismatches.append(f"Python {runtime['python']} != canonical 3.12.14")
    for name, expected in requirements.items():
        try:
            actual = md.version(name)
        except md.PackageNotFoundError:
            actual = "MISSING"
        if actual != expected:
            mismatches.append(f"{name} {actual} != {expected}")
    return {"canonical_environment_match": not mismatches, "runtime": runtime,
            "canonical_requirements": requirements, "mismatches": mismatches}


def run_pipeline(output: Path, cases_path: Path = CASES) -> dict:
    capture(output, cases_path)
    normalize(output, cases_path)
    manifest = build_manifest(output, cases_path)
    schema_errors = schema_validate(output, cases_path)
    invariants = validate_invariants(output, cases_path)
    deviations = deviation_report(output)
    summary = {
        "schema_version": "0.1",
        "pass": not schema_errors and invariants["pass"] and deviations["pass"],
        "schema_validation": {"pass": not schema_errors, "errors": schema_errors},
        "invariants": invariants,
        "raw_vs_corrected": deviations,
        "environment": environment_report(),
        "manifest_sha256": sha256_file(output / "manifest.json"),
        "artifact_count": manifest["coverage"]["artifact_count"],
    }
    write_json(output / "validation-summary.json", summary)
    if not summary["pass"]:
        raise SystemExit(1)
    print(f"pipeline PASS: {manifest['coverage']['case_count']} cases, {manifest['coverage']['artifact_count']} artifacts")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("capture", "normalize", "manifest", "validate-schema", "invariants", "pipeline"):
        command = sub.add_parser(name)
        command.add_argument("--output", type=Path, default=DEFAULT_CANDIDATE)
        command.add_argument("--cases", type=Path, default=CASES)
    compare = sub.add_parser("compare")
    compare.add_argument("left", type=Path)
    compare.add_argument("right", type=Path)
    docs = sub.add_parser("validate-docs")
    docs.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "capture":
        capture(args.output, args.cases)
    elif args.command == "normalize":
        normalize(args.output, args.cases)
    elif args.command == "manifest":
        build_manifest(args.output, args.cases)
    elif args.command == "validate-schema":
        errors = schema_validate(args.output, args.cases)
        print(json.dumps({"pass": not errors, "errors": errors}, indent=2))
        raise SystemExit(bool(errors))
    elif args.command == "invariants":
        report = validate_invariants(args.output, args.cases)
        print(json.dumps(report, indent=2))
        raise SystemExit(not report["pass"])
    elif args.command == "compare":
        differences = compare_directories(args.left, args.right)
        print(json.dumps({"pass": not differences, "differences": differences}, indent=2))
        raise SystemExit(bool(differences))
    elif args.command == "validate-docs":
        report = validate_docs()
        if args.output:
            write_json(args.output, report)
        print(json.dumps(report, indent=2))
        raise SystemExit(not report["pass"])
    elif args.command == "pipeline":
        run_pipeline(args.output, args.cases)


if __name__ == "__main__":
    main()
