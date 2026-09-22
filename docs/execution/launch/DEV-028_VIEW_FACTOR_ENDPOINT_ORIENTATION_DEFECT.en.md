# DEV-028 — View Factor Endpoint-Orientation / Signed-Hottel Reference Defect

Status: **APPROVED**. Owner decision: 2026-09-22, OD-LCB01-01 through OD-LCB01-05 in [Owner record](LCB-01_OWNER_DECISIONS.en.md). This record covers **Full geometric F only**. Fast finite-ground behavior is separately governed by [DEV-029](DEV-029_FAST_FINITE_GROUND_AGGREGATION.en.md).

## Confirmed Reference defect

Frozen pvlib/solarfactors v1.6.1, commit `ecbfc863657e239817603a43898ae173c7ccad9c`, uses a signed crossed-minus-uncrossed expression in `_vf_hottel_gnd_surf`. Its endpoint high/low construction assumes an orientation that cutting and binary64 equal-height ties/reversals can invalidate. The resulting negative finite physical exchange is a confirmed compatibility defect; Rust V1 must not reproduce it.

The approved TILT_180 pair receiver ReferenceIndex3/source28 has Reference −0.2038204263767998, independent Decimal90 +0.2038204263767998815712607034… and line integration +0.20382042637679987. The pair is physically supported and unobstructed. Geometry is correct and unchanged.

## Affected domain and fields

The 66-case investigation found 8 Full failing cases and 922 differing fields: 408 PV→ground, 408 ground→PV, 70 ground→residual-sky and 36 PV→residual-sky. All 408 negative PV→ground helper observations have exact endpoint-height ties. Exact180 and180−1 ULP fail depending on azimuth, subdivision and row count (N2/3/11; cut1/2/4). This is neither an exact180-only defect nor a defect in every tilt>90 configuration. The general trigger is loss of the VF endpoint-order assumption while Geometry remains valid; the finite covering set is not an exhaustive continuous-domain proof.

Affected fields are Full finite physical F and its reciprocal/residual consequences. No significant PV→PV mismatch was observed in that scan. Fast's 53 cases/139 fields are **not** assigned to DEV-028.

## Approved corrected behavior

CDR-008 makes semantic surface identity/outward normal and physical line-of-sight authoritative. Exchange is nonnegative, finite and bounded; Hottel is an analytic realization of that measure after valid support is established. Endpoint order is a local computational construction and cannot define identity, visibility or physical sign. Partial obstruction requires the visible domain first. Reciprocity and closure remain necessary but insufficient.

The P3 Geometry model, finite extent, coordinates, SurfaceKey, ReferenceIndex, ActiveIndex, activity, normals, front/back identity, approved Geometry Golden and geometry-tolerance-v0.1 remain unchanged. No >90 folding, side exchange, geometry endpoint reordering to fit Reference, global matrix abs, invalid-value clamp or tolerance relaxation is allowed.

## Compatibility, oracle and provenance

Corrected physical F intentionally differs from the defective Reference behavior. Preserve every raw/normalized Reference output; corrected matrix fields cite DEV-028 and CDR-008. Fast corrected fields instead cite DEV-029. The existing 66-case/198-artifact corpus remains at `reference/candidate/vf-lcb01-v0.1/` for path stability, with status **APPROVED_TARGETED_ORACLE_SEED**. Approval is only the LCB-01 targeted corrected VF subset/P4 seed, never complete VF/P4 Golden or AOI coverage. Accurate manifest/profile hashes are bound by `LCB-01_OWNER_DECISIONS.json`.

Regression evidence includes VF053, VF052/054/055, VF062/063 near180 in both orientations, VF064/065, and nonfailing90/120/near180 controls. Independent analytic, angular/line and tensor evidence plus negative/reciprocal/closed-invalid mutation tests are retained. The [investigation](LCB-01_VF_INVESTIGATION_REPORT.en.md) is historical scientific evidence; current validation authority is the remotely anchored closure receipt described in [closure handoff](LCB-01_CLOSURE_HANDOFF.en.md).

Approval closes this semantic decision only. Production numerical realization is not frozen; P4–P7 and full implementation are not accepted or started.
