# DEV-028 — View Factor orientation and finite-support candidate

Status: **PROPOSED / UNAPPROVED**. Date: 2026-09-22. The existing register ends at DEV-027; this new identifier does not amend its approved history. Related decision: CDR-008, itself awaiting Owner review.

## Reference behavior and trigger

Frozen solarfactors `ecbfc863657e239817603a43898ae173c7ccad9c`, `pvfactors/viewfactors/vfmethods.py`, exposes two distinct findings:

1. **Full F sign defect.** `_vf_hottel_gnd_surf` associates crossed/uncrossed strings with high/low and cut-point side, then returns a signed difference. On a rounded equal-height subsegment that order can reverse. All 408 negative PV→ground helper observations have an exact height tie. Reverse ground→PV inherits the sign. Residual sky can exceed one or be wrong while still within [0,1].
2. **Fast finite-support defect/limitation.** `calculate_vf_to_gnd` can construct an edge proxy outside [−100,100], with reversed endpoints and severe cancellation, or use an interior proxy that includes exchange outside the finite ground. Actual normal/finite-domain checks must precede magnitude evaluation. This is related to DEV-004's finite-ground context but was not closed by that Geometry policy; it concerns VF aggregation.

The observed Full failing domain is exact 180° and 180−1 ULP, depending on azimuth, row and subdivision. It is not simply “all tilts>90” or “only exact180”. Tested 0, 1e−10, 1, 45, 89.9, 90 and its ULP/epsilon neighborhood, 100, 120, 150, 179, 179.9 and extra near180 values pass outside the eight recorded cases. This covering set fixes height/width/pitch and is not an exhaustive domain proof. General trigger: the VF endpoint-order assumption fails even though the approved Geometry is valid. Fast finite-proxy differences occur much more broadly.

## Observable effect and mathematical behavior

For approved TILT_180, `F[3,28]` is −0.2038204263767998; independent Decimal90 is +0.2038204263767998815712607034… and numerical integration is +0.20382042637679987. The pair faces and is unobstructed. There are 36 bounds violations but 37 differing fields in that case, demonstrating why bounds alone also need differential/support evidence. At row0 back, the Fast ground helper returns +0.5 while finite visible ground exchange is zero.

The corrected mathematical object is the nonnegative cosine-weighted measure of mutually facing, unoccluded rays between finite surfaces. Its exchange is symmetric after multiplication by receiver length. Endpoint names and tilt are not sign selectors. Side/visibility is explicit; magnitude is evaluated only on supported rays. Sky remains the existing residual open-boundary source, not a reciprocal finite surface. Fast ground/PV groups are proposed as length-weighted aggregates of the same finite geometric exchange, while Fast irradiance remains a separate approximation.

Affected fields: geometric F PV→ground, ground→PV and residual sky; Fast back-ground aggregate fields. No significant PV→PV or Fast back→PV difference was found in the scan. AOI G, irradiance, solver, Full/Fast public result fields and production APIs have not been implemented or validated by this task.

## Compatibility and candidate boundary

Recommendation: correct physical F under CDR-008; preserve raw Reference as provenance/diagnostics. Do not expose its negative F as a valid physical result. The change intentionally differs from frozen Reference on identified cases. Fast finite aggregation also changes some otherwise valid Reference Fast numbers, so Owner approval must explicitly cover that compatibility impact; it is not an unnoticed helper refactor.

Geometry coordinates, finite extent, SurfaceKey, ReferenceIndex, active slots, normals, [0°,180°] domain and front/back identities remain unchanged. No P3 amendment is needed. Abs of the full matrix and clamps are rejected; the narrower abs helper patch fits this sample but is not proved across the domain. Independent implementation should follow visible-domain semantics, not line-by-line Python translation.

`reference/candidate/vf-lcb01-v0.1/manifest.json` contains 66 cases/198 artifacts and a separate proposed comparator profile. Raw and normalized outputs remain intact; corrected matrices and Fast group values identify field-level DEV/CDR/independent-oracle provenance. This is a targeted LCB-01 candidate, not the complete P4/AOI acceptance corpus. No candidate has been promoted. Geometry Golden/tolerance remain frozen.

Regression cases include VF053 (approved TILT_180), VF035 (TILT120), VF020 (TILT90), VF045 versus VF063 (near180 cut sensitivity), VF062/VF063 (both orientations), VF064/VF065, N1/2/3/11, cut1/2/4, blocked/unblocked ground, adjacent PV, edge/middle receivers and shaded/illuminated ground. Synthetic visibility/divider cases validate the independent oracle and are not relabeled as approved Geometry fixtures.

## Evidence and Owner action

The [investigation report](LCB-01_VF_INVESTIGATION_REPORT.en.md) links the minimal counterexample, first-divergence intermediates, 66-case scan, directed taxonomy, Decimal/line/tensor evidence, Fast differences, raw reproducibility and immutable candidate hashes. A no-Reference-helper oracle checks visibility; independent reverse/mirror/order tests complement generated reciprocity and closure. The invariant harness rejects negative, >1, reciprocal-negative and closed-but-invalid mutations.

Required response: approve/revise/reject DEV-028 together with CDR-008; explicitly choose whether corrected Fast groups use finite F aggregation. Default: **approve unified finite physical semantics**, review and approve the exact candidate manifest/profile as a named research acceptance subset, then resume the remaining P4–P7 closure preparation. Approval is not an implementation launch or a release decision. Until that response, DEV-028 is unapproved and LCB-01 remains a launch blocker.
