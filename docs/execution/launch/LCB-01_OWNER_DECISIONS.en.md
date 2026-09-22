# LCB-01 Owner decision record

Date: 2026-09-22. Authority: Repository Owner's explicit **Owner Decision Propagation + Evidence Provenance Repair Task v1.0**, preserved verbatim and hashed in `evidence/execution/launch-closure/lcb-01/owner-decision/source-request.txt`. This is an Owner decision record, not an Agent recommendation or inferred approval. Machine-readable authority and exact approved object hashes: [LCB-01_OWNER_DECISIONS.json](LCB-01_OWNER_DECISIONS.json).

| Decision | Approved policy |
|---|---|
| OD-LCB01-01 | Full endpoint-orientation/signed-Hottel Reference behavior is a confirmed compatibility defect. Rust V1 does not reproduce it. DEV-028 covers this alone. |
| OD-LCB01-02 | P3 Geometry, coordinates, finite extent, SurfaceKey, ReferenceIndex, ActiveIndex, front/back identity, approved Geometry Golden and Geometry tolerance remain unchanged. |
| OD-LCB01-03 | Semantic identity/outward normal, physical line-of-sight and nonnegative finite exchange are authoritative. Hottel realizes that measure; endpoint order is a local construction. |
| OD-LCB01-04 | Applicable active physical/residual F lies in [0,1]. Reciprocity and closure are necessary but insufficient; preserve the illegal-matrix mutation tests. |
| OD-LCB01-05 | Prohibit global matrix abs, invalid-F clamp, tilt folding, side swap, adapting Geometry to Reference and tolerance relaxation to absorb nonphysical values. |
| OD-LCB01-06 | Fast geometric groups use the same finite exchange, aggregated by receiver length or proved equivalent direct computation. DEV-029 covers this independently. Fast simulation stays distinct; CDR-007 remains open. |

[DEV-028](DEV-028_VIEW_FACTOR_ENDPOINT_ORIENTATION_DEFECT.en.md), [DEV-029](DEV-029_FAST_FINITE_GROUND_AGGREGATION.en.md) and [CDR-008](CDR-008_VIEW_FACTOR_VISIBILITY_HOTTEL_POLICY.en.md) are **APPROVED**. Production numerical algorithms are not frozen. Approval does not initiate implementation, accept P4 or approve the remaining project decisions.

The existing corpus is approved only as **LCB-01 Targeted Corrected VF Oracle Subset / P4 Oracle Seed**: 66 cases/198 artifacts, geometric F plus finite Fast geometric groups. Its path remains `reference/candidate/vf-lcb01-v0.1/`; directory naming does not override the explicit targeted approval status. Raw/normalized bytes and scientific numeric/Geometry payloads are preserved. Only status/provenance metadata and necessary verifier bindings change. Full matrix changes cite DEV-028, Fast group changes DEV-029; both cite CDR-008.

Comparator: **APPROVED FOR LCB-01 TARGETED ORACLE SEED**, **NOT YET FINAL P4 CROSS-PLATFORM TOLERANCE**. Existing budgets are unchanged: bounds1e−10, expected_abs2e−9, length reciprocity1e−10, closure1e−10. Future final P4 tolerance needs independent evidence and approval; failing implementation cannot silently enlarge it. AOI G is a separate operator.

LCB-01 closure is conditional on renewed verification at a clean real commit and remote-resolvable content/receipt commits. The prior `8b0208b4ae471bf81d70e4358e8cdc22a38e0384` receipt is historical only; GitHub returned HTTP422 during this task. Initial remote `3d854a564afd44b6f50f860454c37582f1ad5302` resolved successfully. See the initial remote audit and [closure handoff](LCB-01_CLOSURE_HANDOFF.en.md).

The original OD-01..OD-12, other CDRs, complete P4–P7 oracle package and platform/governance decisions are not approved by this narrow record. Final current LCB-01 status comes from the verification receipt, not duplicated status text. This task stops after propagation, repair, verification and push.
