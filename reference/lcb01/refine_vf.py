"""Refined LCB-01 diagnostics for the exact -180 degree VF singularity.

Research-only. No production implementation and no Reference modification.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import sys

import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reference/lcb01"))
sys.path.insert(0, str(ROOT / "upstream/solarfactors"))
sys.path.insert(0, str(ROOT / "reference/tools"))

import investigate_vf as base
from pvfactors.config import DISTANCE_TOLERANCE
from pvfactors.viewfactors.vfmethods import VFTsMethods
from geometry_golden import ordered_surface_records, environment_report


class MagnitudeVFTsMethods(VFTsMethods):
    """Diagnostic candidate: orientation-invariant magnitude at obstructed Hottel primitive."""

    def _vf_hottel_gnd_surf(
        self, high_pt_pv, low_pt_pv, left_pt_gnd, right_pt_gnd,
        obstr_pt, width, shadow_is_left,
    ):
        signed = super()._vf_hottel_gnd_surf(
            high_pt_pv, low_pt_pv, left_pt_gnd, right_pt_gnd,
            obstr_pt, width, shadow_is_left,
        )
        return np.abs(signed)


class AuditVFTsMethods(VFTsMethods):
    def __init__(self):
        super().__init__()
        self.calls = []

    @staticmethod
    def _obstructed(pt_pv, pt_gnd, pt_obstr, is_left):
        alpha_pv = np.arctan2(pt_pv.y - pt_gnd.y, pt_pv.x - pt_gnd.x)
        alpha_ob = np.arctan2(pt_obstr.y - pt_gnd.y, pt_obstr.x - pt_gnd.x)
        return alpha_pv > alpha_ob if is_left else alpha_pv < alpha_ob

    def _vf_hottel_gnd_surf(
        self, high_pt_pv, low_pt_pv, left_pt_gnd, right_pt_gnd,
        obstr_pt, width, shadow_is_left,
    ):
        out = super()._vf_hottel_gnd_surf(
            high_pt_pv, low_pt_pv, left_pt_gnd, right_pt_gnd,
            obstr_pt, width, shadow_is_left,
        )
        flags = [
            self._obstructed(high_pt_pv, left_pt_gnd, obstr_pt, shadow_is_left),
            self._obstructed(high_pt_pv, right_pt_gnd, obstr_pt, shadow_is_left),
            self._obstructed(low_pt_pv, left_pt_gnd, obstr_pt, shadow_is_left),
            self._obstructed(low_pt_pv, right_pt_gnd, obstr_pt, shadow_is_left),
        ]
        for k in range(len(np.atleast_1d(out))):
            self.calls.append({
                "shadow_is_left": bool(shadow_is_left),
                "value": float(np.atleast_1d(out)[k]),
                "obstructed_string_count": int(sum(bool(np.atleast_1d(f)[k]) for f in flags)),
            })
        return out


def build_matrix(p, methods=None):
    methods = methods or VFTsMethods()
    tilted_to_left = p.rotation_vec > 0
    n = p.n_ts_surfaces
    steps = len(p.rotation_vec)
    m = np.zeros((n + 1, n + 1, steps), dtype=float)
    methods.vf_pvrow_gnd_surf(p.ts_pvrows, p.ts_ground, tilted_to_left, m)
    methods.vf_pvrow_to_pvrow(p.ts_pvrows, tilted_to_left, m)
    m[:-1, -1, :] = 1.0 - np.sum(m[:-1, :-1, :], axis=1)
    for i, s in enumerate(p.all_ts_surfaces):
        m[i, -1, :] = np.where(s.length > DISTANCE_TOLERANCE, m[i, -1, :], 0.0)
    return m[:, :, 0]


def active_metrics(p, F):
    L = np.array([s.length[0] for s in p.all_ts_surfaces], dtype=float)
    active = np.flatnonzero(L > base.ACTIVE_TOL)
    vals = F[np.ix_(active, np.r_[active, len(L)])]
    closure = float(np.max(np.abs(F[active, :].sum(axis=1) - 1.0))) if len(active) else 0.0
    rec = float(np.max(np.abs(
        L[:, None] * F[:-1, :-1] - L[None, :] * F[:-1, :-1].T
    ))) if len(L) else 0.0
    bad = []
    for i in active:
        for j in [*active, len(L)]:
            if F[i, j] < -base.BOUND_TOL or F[i, j] > 1.0 + base.BOUND_TOL:
                bad.append([int(i), int(j), float(F[i, j])])
    return {
        "active_count": int(len(active)),
        "min": float(np.min(vals)) if vals.size else 0.0,
        "max": float(np.max(vals)) if vals.size else 0.0,
        "closure_max_error": closure,
        "reciprocity_max_error": rec,
        "violation_count": len(bad),
        "violations": bad,
    }


def find_target_indices(p):
    recs = ordered_surface_records(p)
    pv = None
    g = None
    for i, rec in enumerate(recs):
        k = rec["logical_key"]
        if rec["active"][0] and k["kind"] == "pvrow" and k["row"] == 0 and k["side"] == "front":
            pv = i
        if (
            rec["active"][0]
            and k["kind"] == "ground"
            and k["source"] == "shadow"
            and k["ground_element"] == 0
        ):
            g = i
    if pv is None or g is None:
        raise RuntimeError("target pair not found")
    return pv, g


def mp_xy(pt):
    # Passing Python floats directly to mp.mpf preserves their binary value exactly.
    return (mp.mpf(float(pt[0])), mp.mpf(float(pt[1])))


def frozen_target_high_precision():
    mp.mp.dps = 100
    p = base.make_pvarray(3, 180.0, 270.0)
    pv_idx, g_idx = find_target_indices(p)
    pv = p.all_ts_surfaces[pv_idx]
    g = p.all_ts_surfaces[g_idx]
    a0 = mp_xy(pv.b1.at(0))
    a1 = mp_xy(pv.b2.at(0))
    b0 = mp_xy(g.b1.at(0))
    b1 = mp_xy(g.b2.at(0))
    Lp = base.mp_distance(a0, a1)
    Lg = base.mp_distance(b0, b1)
    pv_to_g = base.mp_hottel_unobstructed(a0, a1, b0, b1)
    g_to_pv = pv_to_g * Lp / Lg
    blockers = base.row_blockers(p, {0})
    num_pv_g = base.numeric_vf(
        base.surface_geometry(p, pv_idx), base.surface_geometry(p, g_idx), blockers, 128
    )
    num_g_pv = base.numeric_vf(
        base.surface_geometry(p, g_idx), base.surface_geometry(p, pv_idx), blockers, 128
    )
    return {
        "receiver_reference_index": g_idx,
        "source_reference_index": pv_idx,
        "pv_to_ground_mp100": mp.nstr(pv_to_g, 100),
        "ground_to_pv_mp100": mp.nstr(g_to_pv, 100),
        "pv_to_ground_numeric_order128": num_pv_g,
        "ground_to_pv_numeric_order128": num_g_pv,
        "ground_length_binary_exact_mp100": mp.nstr(Lg, 100),
    }


def candidate_case(n, tilt, azi):
    p = base.make_pvarray(n, tilt, azi)
    raw = build_matrix(p, VFTsMethods())
    cand = build_matrix(p, MagnitudeVFTsMethods())
    d = np.abs(cand - raw)
    return {
        "n_pvrows": n,
        "tilt": tilt,
        "surface_azimuth": azi,
        "rotation": float(p.rotation_vec[0]),
        "raw": active_metrics(p, raw),
        "candidate": active_metrics(p, cand),
        "changed_entries_gt_1e12": int(np.sum(d > 1e-12)),
        "max_abs_change": float(np.max(d)),
    }


def endpoint_scan():
    vals = [
        179.0, 179.9, 179.99, 179.999, 179.9999, 179.99999, 179.999999,
        180.0 - 1e-10, float(np.nextafter(180.0, 0.0)), 180.0,
    ]
    out = []
    for t in vals:
        p = base.make_pvarray(3, t, 270.0)
        F = build_matrix(p)
        pv_idx, g_idx = find_target_indices(p)
        surf = p.all_ts_surfaces[pv_idx]
        out.append({
            "tilt": repr(t),
            "rotation": repr(float(p.rotation_vec[0])),
            "b1_y": repr(float(surf.b1.y[0])),
            "b2_y": repr(float(surf.b2.y[0])),
            "highest_is_b1": bool(float(surf.b1.y[0]) >= float(surf.b2.y[0])),
            "target_pv_to_ground": float(F[pv_idx, g_idx]),
            "target_ground_to_pv": float(F[g_idx, pv_idx]),
            "sky_from_pv": float(F[pv_idx, -1]),
            "metrics": active_metrics(p, F),
        })
    return out


def continuity_check():
    near = float(np.nextafter(180.0, 0.0))
    p_near = base.make_pvarray(3, near, 270.0)
    p_exact = base.make_pvarray(3, 180.0, 270.0)
    F_near = build_matrix(p_near)
    F_cand = build_matrix(p_exact, MagnitudeVFTsMethods())
    Ln = np.array([s.length[0] for s in p_near.all_ts_surfaces])
    Le = np.array([s.length[0] for s in p_exact.all_ts_surfaces])
    active = np.flatnonzero((Ln > base.ACTIVE_TOL) & (Le > base.ACTIVE_TOL))
    idx = np.r_[active, len(Le)]
    delta = np.abs(F_cand[np.ix_(active, idx)] - F_near[np.ix_(active, idx)])
    return {
        "near_tilt": repr(near),
        "active_indices": active.tolist(),
        "max_abs_candidate_exact_vs_reference_nextafter": float(np.max(delta)),
        "mean_abs_candidate_exact_vs_reference_nextafter": float(np.mean(delta)),
    }


def full_matrix_abs_counterexample():
    p = base.make_pvarray(3, 180.0, 270.0)
    raw = build_matrix(p)
    whole_abs = np.abs(raw)
    m = active_metrics(p, whole_abs)
    pv_idx, _ = find_target_indices(p)
    return {
        "operation": "abs() applied to the already assembled full matrix, including sky",
        "metrics": m,
        "row0_front_row_sum_after_abs": float(np.sum(whole_abs[pv_idx, :])),
        "row0_front_sky_after_abs": float(whole_abs[pv_idx, -1]),
        "conclusion": "counterexample: whole-matrix abs violates summation and leaves sky > 1",
    }


def audit_exact_minus_180():
    p = base.make_pvarray(3, 180.0, 270.0)
    audit = AuditVFTsMethods()
    _ = build_matrix(p, audit)
    neg = [x for x in audit.calls if x["value"] < -1e-12]
    zeroish = [x for x in audit.calls if abs(x["value"]) <= 1e-12]
    return {
        "call_count": len(audit.calls),
        "negative_call_count": len(neg),
        "negative_all_strings_direct_count": sum(x["obstructed_string_count"] == 0 for x in neg),
        "negative_with_any_obstruction_count": sum(x["obstructed_string_count"] > 0 for x in neg),
        "negative_by_obstructed_string_count": {
            str(k): sum(x["obstructed_string_count"] == k for x in neg)
            for k in range(5)
        },
        "zeroish_call_count": len(zeroish),
        "negative_examples": neg[:50],
    }


def candidate_domain():
    specs = []
    for n in [1, 2, 3, 11]:
        specs.append((n, 180.0, 270.0))
        specs.append((n, 180.0, 90.0))
    for t in [0.0, 45.0, 90.0, 120.0, 150.0, 179.9, 179.999999, 180.0 - 1e-10]:
        specs.append((3, t, 270.0))
        specs.append((3, t, 90.0))
    return [candidate_case(*s) for s in specs]


def candidate_oracle_case():
    p = base.make_pvarray(3, 180.0, 270.0)
    F = build_matrix(p, MagnitudeVFTsMethods())
    L = np.array([s.length[0] for s in p.all_ts_surfaces], dtype=float)
    active = np.flatnonzero(L > base.ACTIVE_TOL)
    recs = ordered_surface_records(p)
    cols = np.r_[active, len(L)]
    surfaces = []
    for i in active:
        rec = recs[int(i)]
        surfaces.append({
            "reference_index": int(i),
            "logical_key": rec["logical_key"],
            "length_m": float(L[i]),
            "coordinates_m": rec["coordinates_m"][0],
            "normal": rec["normal"],
        })
    return {
        "status": "CANDIDATE / UNAPPROVED",
        "case_id": "LCB01_TILT_180_CORRECTED_CANDIDATE",
        "input": {
            "n_pvrows": 3,
            "pvrow_height": base.HEIGHT,
            "pvrow_width": base.WIDTH,
            "gcr": base.GCR,
            "axis_azimuth": base.AXIS_AZIMUTH,
            "surface_tilt": 180.0,
            "surface_azimuth": 270.0,
            "solar_zenith": base.SOLAR_ZENITH,
            "solar_azimuth": base.SOLAR_AZIMUTH,
        },
        "matrix_axes": ["receiver", "source"],
        "active_reference_indices": active.tolist(),
        "source_reference_indices_plus_sky": cols.tolist(),
        "sky_reference_index": int(len(L)),
        "surfaces": surfaces,
        "F_active_plus_sky": F[np.ix_(active, cols)].tolist(),
        "invariants": active_metrics(p, F),
        "construction": (
            "Reference geometry/topology + research-only orientation-invariant magnitude "
            "at _vf_hottel_gnd_surf, followed by normal sky closure. This is a candidate "
            "corrected oracle, not an approved Reference replacement."
        ),
    }


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    report = {
        "task": "LCB-01 refined endpoint/root-cause diagnostics",
        "base_commit": "d5bc38ebd6ba853c4cec530e4787d1ab6168203d",
        "environment": environment_report(),
        "frozen_target_high_precision": frozen_target_high_precision(),
        "endpoint_scan": endpoint_scan(),
        "continuity": continuity_check(),
        "candidate_magnitude_primitive_domain": candidate_domain(),
        "candidate_corrected_oracle_v0_1": candidate_oracle_case(),
        "whole_matrix_abs_counterexample": full_matrix_abs_counterexample(),
        "exact_minus_180_raw_hottel_audit": audit_exact_minus_180(),
        "root_cause_guardrail": {
            "geometry_modified": False,
            "reference_modified": False,
            "candidate_is_research_only": True,
            "candidate_operation_location": "_vf_hottel_gnd_surf primitive magnitude before sky closure",
            "not_equivalent_to": "abs(full VF matrix)",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    if not report["environment"]["canonical_environment_match"]:
        raise SystemExit("LCB-01 canonical environment contract mismatch")

    exact = [
        x for x in report["candidate_magnitude_primitive_domain"]
        if x["tilt"] == 180.0
    ]
    summary = {
        "canonical_environment_match": report["environment"]["canonical_environment_match"],
        "environment_id": report["environment"]["runtime"]["environment_id"],
        "frozen_target_ground_to_pv_mp100": report["frozen_target_high_precision"]["ground_to_pv_mp100"],
        "exact_180_candidate_cases": [
            {
                "n": x["n_pvrows"],
                "azi": x["surface_azimuth"],
                "raw_violations": x["raw"]["violation_count"],
                "candidate_violations": x["candidate"]["violation_count"],
                "max_abs_change": x["max_abs_change"],
            }
            for x in exact
        ],
        "continuity_max_abs": report["continuity"]["max_abs_candidate_exact_vs_reference_nextafter"],
        "whole_matrix_abs_row_sum": report["whole_matrix_abs_counterexample"]["row0_front_row_sum_after_abs"],
        "raw_negative_hottel_calls": report["exact_minus_180_raw_hottel_audit"]["negative_call_count"],
        "raw_negative_all_strings_direct": report["exact_minus_180_raw_hottel_audit"]["negative_all_strings_direct_count"],
        "raw_negative_with_obstruction": report["exact_minus_180_raw_hottel_audit"]["negative_with_any_obstruction_count"],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
