"""LCB-01 View Factor compatibility deviation investigation.

Research-only harness. It imports the frozen Reference for comparison, but the
physical numerical oracle and high-precision Hottel oracle do not call any
Reference view-factor helper.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any

import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "upstream/solarfactors"))
sys.path.insert(0, str(ROOT / "reference/tools"))

from pvfactors.geometry import OrderedPVArray
from pvfactors.viewfactors import VFCalculator
from pvfactors.viewfactors.vfmethods import VFTsMethods
from geometry_golden import ordered_surface_records, environment_report

ACTIVE_TOL = 1e-8
BOUND_TOL = 1e-12
AXIS_AZIMUTH = 180.0
SOLAR_ZENITH = 45.0
SOLAR_AZIMUTH = 270.0
HEIGHT = 1.0
WIDTH = 1.0
GCR = 0.5


def as_xy(pt) -> np.ndarray:
    a = np.asarray(pt, dtype=float)
    return a.reshape(2)


def norm2(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n == 0.0:
        return v
    return v / n


def surface_geometry(pvarray, idx: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    surf = pvarray.all_ts_surfaces[idx]
    a = np.array([surf.coords.b1.x[0], surf.coords.b1.y[0]], dtype=float)
    b = np.array([surf.coords.b2.x[0], surf.coords.b2.y[0]], dtype=float)
    length = float(surf.length[0])
    if surf.n_vector is None:
        normal = np.array([0.0, 1.0], dtype=float)
    else:
        normal = norm2(np.array(surf.n_vector[:, 0], dtype=float))
    return a, b, normal, length


def row_blockers(pvarray, excluded_rows: set[int]) -> list[tuple[np.ndarray, np.ndarray, int]]:
    out = []
    for row_idx, row in enumerate(pvarray.ts_pvrows):
        if row_idx in excluded_rows:
            continue
        c = np.array([row.full_pvrow_coords.b1.x[0], row.full_pvrow_coords.b1.y[0]], dtype=float)
        d = np.array([row.full_pvrow_coords.b2.x[0], row.full_pvrow_coords.b2.y[0]], dtype=float)
        out.append((c, d, row_idx))
    return out


def ray_blocked(P: np.ndarray, Q: np.ndarray, blockers: list[tuple[np.ndarray, np.ndarray, int]]) -> np.ndarray:
    """Return mask for interior intersection of P->Q rays with opaque row segments."""
    shape = P.shape[:-1]
    blocked = np.zeros(shape, dtype=bool)
    R = Q - P

    def cross2(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]

    for C, D, _ in blockers:
        S = D - C
        denom = cross2(R, S)
        mask = np.abs(denom) > 1e-14
        CP = C - P
        with np.errstate(divide="ignore", invalid="ignore"):
            t = cross2(CP, S) / denom
            u = cross2(CP, R) / denom
        hit = mask & (t > 1e-10) & (t < 1.0 - 1e-10) & (u > 1e-10) & (u < 1.0 - 1e-10)
        blocked |= hit
    return blocked


def numeric_vf(
    recv: tuple[np.ndarray, np.ndarray, np.ndarray, float],
    src: tuple[np.ndarray, np.ndarray, np.ndarray, float],
    blockers: list[tuple[np.ndarray, np.ndarray, int]],
    order: int,
) -> float:
    """Independent 2-D diffuse line-surface integration.

    F_i->j = (1/L_i) int_i int_j V cos(theta_i) cos(theta_j)/(2 r) ds_j ds_i.
    """
    a0, a1, na, La = recv
    b0, b1, nb, Lb = src
    if La <= ACTIVE_TOL or Lb <= ACTIVE_TOL:
        return 0.0
    x, w = np.polynomial.legendre.leggauss(order)
    t = (x + 1.0) * 0.5
    w = w * 0.5
    Pa = a0[None, :] + t[:, None] * (a1 - a0)[None, :]
    Pb = b0[None, :] + t[:, None] * (b1 - b0)[None, :]
    P = Pa[:, None, :]
    Q = Pb[None, :, :]
    R = Q - P
    r = np.linalg.norm(R, axis=2)
    rhat = R / r[:, :, None]
    cos_a = np.einsum("...k,k->...", rhat, na)
    cos_b = np.einsum("...k,k->...", -rhat, nb)
    kernel = np.maximum(cos_a, 0.0) * np.maximum(cos_b, 0.0) / (2.0 * r)
    if blockers:
        kernel = np.where(ray_blocked(P, Q, blockers), 0.0, kernel)
    return float(Lb * np.sum((w[:, None] * w[None, :]) * kernel))


def mp_distance(a: tuple[mp.mpf, mp.mpf], b: tuple[mp.mpf, mp.mpf]) -> mp.mpf:
    return mp.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def mp_hottel_unobstructed(a0, a1, b0, b1) -> mp.mpf:
    La = mp_distance(a0, a1)
    same = mp_distance(a0, b0) + mp_distance(a1, b1)
    cross = mp_distance(a0, b1) + mp_distance(a1, b0)
    return abs(cross - same) / (2 * La)


def ideal_target_hottel() -> str:
    mp.mp.dps = 100
    q = mp.mpf
    a0 = (q("-0.5"), q("1"))
    a1 = (q("0.5"), q("1"))
    b0 = (q("-1.5"), q("0"))
    b1 = (q("-0.5"), q("0"))
    return mp.nstr(mp_hottel_unobstructed(a0, a1, b0, b1), 100)


def make_pvarray(n_pvrows: int, tilt: float, surface_azimuth: float) -> OrderedPVArray:
    p = OrderedPVArray(
        n_pvrows=n_pvrows,
        pvrow_height=HEIGHT,
        pvrow_width=WIDTH,
        axis_azimuth=AXIS_AZIMUTH,
        gcr=GCR,
    )
    p.fit(
        np.array([SOLAR_ZENITH]),
        np.array([SOLAR_AZIMUTH]),
        np.array([tilt]),
        np.array([surface_azimuth]),
    )
    return p


def key_label(key: dict[str, Any]) -> str:
    if key["kind"] == "pvrow":
        return f"pv:r{key['row']}:{key['side']}:{key['segment']}:{key['illumination']}"
    return f"g:{key['source']}:{key['ground_element']}:{key['cut_interval']}:{key['illumination']}"


def scan_case(n: int, tilt: float, surface_azimuth: float) -> dict[str, Any]:
    p = make_pvarray(n, tilt, surface_azimuth)
    F = VFCalculator().build_ts_vf_matrix(p)[:, :, 0]
    L = np.array([s.length[0] for s in p.all_ts_surfaces], dtype=float)
    active = np.flatnonzero(L > ACTIVE_TOL)
    recs = ordered_surface_records(p)
    violations = []
    neg = 0
    gt1 = 0
    for i in active:
        for j in [*active, len(L)]:
            v = float(F[i, j])
            if v < -BOUND_TOL or v > 1.0 + BOUND_TOL:
                if v < 0:
                    neg += 1
                if v > 1:
                    gt1 += 1
                violations.append({
                    "receiver_reference_index": int(i),
                    "source_reference_index": int(j),
                    "receiver": key_label(recs[i]["logical_key"]),
                    "source": "sky" if j == len(L) else key_label(recs[j]["logical_key"]),
                    "F": v,
                })
    finite = F[np.ix_(active, np.r_[active, len(L)])]
    reciprocity = float(np.max(np.abs(
        L[:, None] * F[:-1, :-1] - L[None, :] * F[:-1, :-1].T
    )))
    closure = float(np.max(np.abs(F[active, :].sum(axis=1) - 1.0)))
    return {
        "n_pvrows": n,
        "tilt": tilt,
        "surface_azimuth": surface_azimuth,
        "rotation": float(p.rotation_vec[0]),
        "active_count": int(len(active)),
        "min_active_F": float(np.min(finite)),
        "max_active_F": float(np.max(finite)),
        "negative_count": neg,
        "greater_than_one_count": gt1,
        "violation_count": len(violations),
        "row_closure_max_error": closure,
        "reciprocity_max_error": reciprocity,
        "violations": violations,
    }


def numeric_compare_case(n: int, tilt: float, surface_azimuth: float, order: int = 48) -> dict[str, Any]:
    p = make_pvarray(n, tilt, surface_azimuth)
    F = VFCalculator().build_ts_vf_matrix(p)[:, :, 0]
    L = np.array([s.length[0] for s in p.all_ts_surfaces], dtype=float)
    active = np.flatnonzero(L > ACTIVE_TOL)
    recs = ordered_surface_records(p)
    rows = []
    for i in active:
        ki = recs[i]["logical_key"]
        for j in active:
            if i == j:
                continue
            kj = recs[j]["logical_key"]
            if ki["kind"] == "ground" and kj["kind"] == "ground":
                continue
            # Coincident front/back surfaces on the same PV row are not a radiative pair.
            if (
                ki["kind"] == "pvrow"
                and kj["kind"] == "pvrow"
                and ki["row"] == kj["row"]
            ):
                continue
            excluded = set()
            if ki["kind"] == "pvrow":
                excluded.add(int(ki["row"]))
            if kj["kind"] == "pvrow":
                excluded.add(int(kj["row"]))
            num = numeric_vf(
                surface_geometry(p, int(i)),
                surface_geometry(p, int(j)),
                row_blockers(p, excluded),
                order,
            )
            ref = float(F[i, j])
            rows.append({
                "receiver_reference_index": int(i),
                "source_reference_index": int(j),
                "receiver": key_label(ki),
                "source": key_label(kj),
                "reference": ref,
                "reference_abs": abs(ref),
                "numeric": num,
                "abs_error_reference": abs(ref - num),
                "abs_error_abs_reference": abs(abs(ref) - num),
            })
    max_ref = max((r["abs_error_reference"] for r in rows), default=0.0)
    max_abs = max((r["abs_error_abs_reference"] for r in rows), default=0.0)
    abs_counterexamples = [
        r for r in rows
        if r["abs_error_abs_reference"] > 5e-7 and max(abs(r["reference"]), r["numeric"]) > 1e-8
    ]
    return {
        "n_pvrows": n,
        "tilt": tilt,
        "surface_azimuth": surface_azimuth,
        "rotation": float(p.rotation_vec[0]),
        "quadrature_order": order,
        "pair_count": len(rows),
        "max_abs_error_reference": max_ref,
        "max_abs_error_abs_reference": max_abs,
        "abs_counterexample_count": len(abs_counterexamples),
        "abs_counterexamples": abs_counterexamples[:50],
        "pairs": rows,
    }


def ref_string_trace(pt_pv: np.ndarray, pt_gnd: np.ndarray, pt_obstr: np.ndarray, is_left: bool) -> dict[str, Any]:
    alpha_pv = math.atan2(pt_pv[1] - pt_gnd[1], pt_pv[0] - pt_gnd[0])
    alpha_ob = math.atan2(pt_obstr[1] - pt_gnd[1], pt_obstr[0] - pt_gnd[0])
    obstructing = alpha_pv > alpha_ob if is_left else alpha_pv < alpha_ob
    direct = float(np.linalg.norm(pt_pv - pt_gnd))
    broken = float(np.linalg.norm(pt_gnd - pt_obstr) + np.linalg.norm(pt_obstr - pt_pv))
    return {
        "alpha_pv": alpha_pv,
        "alpha_obstruction": alpha_ob,
        "obstructing": bool(obstructing),
        "direct_length": direct,
        "broken_length": broken,
        "used_length": broken if obstructing else direct,
    }


def target_trace(tilt: float, surface_azimuth: float = 270.0) -> dict[str, Any]:
    p = make_pvarray(3, tilt, surface_azimuth)
    recs = ordered_surface_records(p)

    def find_idx(pred):
        for idx, rec in enumerate(recs):
            if rec["active"][0] and pred(rec["logical_key"]):
                return idx
        raise RuntimeError("surface not found")

    pv_idx = find_idx(lambda k: k["kind"] == "pvrow" and k["row"] == 0 and k["side"] == "front")
    g_idx = find_idx(lambda k: k["kind"] == "ground" and k["source"] == "shadow" and k["ground_element"] == 0)
    pv = p.all_ts_surfaces[pv_idx]
    g = p.all_ts_surfaces[g_idx]
    left_indices = {s.index for s in p.ts_ground.ts_surfaces_side_of_cut_point("left", 0)}
    right_indices = {s.index for s in p.ts_ground.ts_surfaces_side_of_cut_point("right", 0)}
    is_left = g_idx in left_indices
    assert is_left ^ (g_idx in right_indices)

    hi = as_xy(pv.highest_point.at(0))
    lo = as_xy(pv.lowest_point.at(0))
    gb1 = as_xy(g.b1.at(0))
    gb2 = as_xy(g.b2.at(0))
    ob = as_xy(p.ts_pvrows[1].full_pvrow_coords.lowest_point.at(0))
    vfm = VFTsMethods()
    ref_h = float(vfm._vf_hottel_gnd_surf(
        pv.highest_point, pv.lowest_point, g.b1, g.b2,
        p.ts_pvrows[1].full_pvrow_coords.lowest_point,
        pv.length, is_left,
    )[0])
    ref_unobs = float(vfm._vf_surface_to_surface(pv.coords, g.coords, pv.length)[0])
    num = numeric_vf(surface_geometry(p, pv_idx), surface_geometry(p, g_idx), row_blockers(p, {0}), 128)
    labels = {}
    if is_left:
        labels = {
            "l1": ref_string_trace(hi, gb1, ob, True),
            "l2": ref_string_trace(lo, gb2, ob, True),
            "d1": ref_string_trace(hi, gb2, ob, True),
            "d2": ref_string_trace(lo, gb1, ob, True),
        }
    else:
        labels = {
            "l1": ref_string_trace(hi, gb2, ob, False),
            "l2": ref_string_trace(lo, gb1, ob, False),
            "d1": ref_string_trace(hi, gb1, ob, False),
            "d2": ref_string_trace(lo, gb2, ob, False),
        }
    return {
        "tilt": tilt,
        "surface_azimuth": surface_azimuth,
        "rotation": float(p.rotation_vec[0]),
        "pv_reference_index": pv_idx,
        "ground_reference_index": g_idx,
        "pv_coords": [as_xy(pv.b1.at(0)).tolist(), as_xy(pv.b2.at(0)).tolist()],
        "pv_normal": np.asarray(pv.n_vector[:, 0], dtype=float).tolist(),
        "highest_point": hi.tolist(),
        "lowest_point": lo.tolist(),
        "cut_point_row0": as_xy(p.ts_ground.cut_point_coords[0].at(0)).tolist(),
        "ground_coords": [gb1.tolist(), gb2.tolist()],
        "ground_classified_side": "left" if is_left else "right",
        "obstruction_point": ob.tolist(),
        "reference_obstructed_hottel": ref_h,
        "reference_unobstructed_hottel_magnitude": ref_unobs,
        "independent_numeric_vf_order128": num,
        "string_trace": labels,
        "all_strings_direct": all(not x["obstructing"] for x in labels.values()),
    }


def target_numeric_convergence() -> list[dict[str, Any]]:
    # Ideal exact geometry for the LCB-01 pair; no blockers.
    a0 = np.array([-0.5, 1.0])
    a1 = np.array([0.5, 1.0])
    b0 = np.array([-1.5, 0.0])
    b1 = np.array([-0.5, 0.0])
    recv = (a0, a1, np.array([0.0, -1.0]), 1.0)
    src = (b0, b1, np.array([0.0, 1.0]), 1.0)
    target = float(mp.mpf(ideal_target_hottel()))
    out = []
    for order in [8, 16, 32, 64, 128]:
        v = numeric_vf(recv, src, [], order)
        out.append({"order": order, "value": v, "abs_error_vs_mp100": abs(v - target)})
    return out


def invariant_mutation_self_tests() -> dict[str, bool]:
    def catches(M):
        return bool(np.any(M < -BOUND_TOL) or np.any(M > 1.0 + BOUND_TOL))

    negative_reciprocal = np.array([
        [0.0, -0.2, 1.2],
        [-0.2, 0.0, 1.2],
    ])
    closure_pass_invalid = np.array([
        [0.0, -0.2, 1.2],
        [0.0, 0.0, 1.0],
    ])
    greater_than_one = np.array([
        [0.0, 0.0, 1.01],
    ])
    return {
        "negative_but_reciprocal_caught": catches(negative_reciprocal),
        "closure_pass_but_invalid_entry_caught": catches(closure_pass_invalid),
        "greater_than_one_caught": catches(greater_than_one),
        "all_pass": all([
            catches(negative_reciprocal),
            catches(closure_pass_invalid),
            catches(greater_than_one),
        ]),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    # Required tilt domain on canonical n=3 orientation.
    tilts = [
        0.0, 1e-10, 1.0, 45.0, 89.9,
        90.0 - 1e-10, 90.0, 90.0 + 1e-10,
        100.0, 120.0, 150.0, 179.0, 179.9,
        179.999999, 180.0 - 1e-10, 180.0,
    ]
    specs: list[tuple[int, float, float, str]] = []
    for t in tilts:
        specs.append((3, t, 270.0, "canonical"))
    # Mirror orientation, focused around representative and singular cases.
    for t in [1.0, 45.0, 90.0, 120.0, 150.0, 179.9, 179.999999, 180.0]:
        specs.append((3, t, 90.0, "mirror"))
    # Row-count coverage without an unbounded Cartesian product.
    for n in [1, 2, 11]:
        for t in [45.0, 120.0, 180.0]:
            specs.append((n, t, 270.0, "row-count"))

    domain = []
    for n, t, azi, family in specs:
        row = scan_case(n, t, azi)
        row["family"] = family
        domain.append(row)

    # Independent physical pair oracle on representative cases.
    numeric_specs = [
        (3, 45.0, 270.0),
        (3, 120.0, 270.0),
        (3, 179.999999, 270.0),
        (3, 180.0, 270.0),
        (3, 45.0, 90.0),
        (3, 120.0, 90.0),
        (3, 179.999999, 90.0),
        (3, 180.0, 90.0),
    ]
    numeric = [numeric_compare_case(*s) for s in numeric_specs]

    traces = [
        target_trace(179.9, 270.0),
        target_trace(179.999999, 270.0),
        target_trace(180.0 - 1e-10, 270.0),
        target_trace(180.0, 270.0),
        target_trace(179.999999, 90.0),
        target_trace(180.0, 90.0),
    ]

    report = {
        "task": "LCB-01 View Factor Compatibility Deviation Investigation",
        "reference_revision": "ecbfc863657e239817603a43898ae173c7ccad9c",
        "base_commit": "d5bc38ebd6ba853c4cec530e4787d1ab6168203d",
        "environment": environment_report(),
        "high_precision": {
            "mpmath_dps": 100,
            "ideal_target_unobstructed_hottel": ideal_target_hottel(),
            "numeric_convergence": target_numeric_convergence(),
        },
        "target_traces": traces,
        "domain_scan": domain,
        "independent_numeric_cases": numeric,
        "invariant_mutation_self_tests": invariant_mutation_self_tests(),
        "guardrails": {
            "reference_helpers_used_by_independent_oracle": False,
            "reference_helpers_used_for_diagnostic_trace_only": True,
            "clamp_applied": False,
            "global_abs_correction_applied": False,
            "tilt_folded": False,
            "front_back_swapped": False,
            "geometry_modified": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    summary = {
        "domain_cases": len(domain),
        "cases_with_bounds_violations": sum(x["violation_count"] > 0 for x in domain),
        "violation_cases": [
            [x["n_pvrows"], x["tilt"], x["surface_azimuth"], x["violation_count"]]
            for x in domain if x["violation_count"]
        ],
        "max_abs_reference_numeric_error": max(x["max_abs_error_reference"] for x in numeric),
        "max_abs_absreference_numeric_error": max(x["max_abs_error_abs_reference"] for x in numeric),
        "abs_counterexamples": sum(x["abs_counterexample_count"] for x in numeric),
        "mutation_self_tests": report["invariant_mutation_self_tests"],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
