# DEV-029 — Fast finite-ground proxy / finite-domain aggregation compatibility deviation

Status: **APPROVED**. Owner decision: 2026-09-22, OD-LCB01-06. Related: CDR-008, DEV-004 finite-ground context. This is separate from DEV-028's Full signed-Hottel defect.

## Reference behavior, cause and domain

Frozen solarfactors `ecbfc863657e239817603a43898ae173c7ccad9c`, `calculate_vf_to_gnd`, uses edge ground segments and interior lowest-endpoint proxies. An edge proxy may extend beyond finite ground [−100,100], reverse endpoints and suffer catastrophic cancellation; an interior proxy may include exchange outside the finite domain. Its positive magnitude is not sufficient evidence of physical validity.

At tilt180, row0 back in VF053 returns Reference back_ground=0.5 while the upward-facing back has finite ground exchange0. A near180 edge case also retains positive cancellation error. In the covering set, 53 cases/139 Fast ground fields differ, across0/45/90/100/120/150/179/179.9/near180 and exact180 configurations. These are broader than the eight Full failure cases. Domain evidence is a finite scan, not a universal bound on all dimensions/pitches. No significant aggregate back→PV difference was observed in the scan.

## Approved geometric policy and compatibility impact

Fast ground/PV geometric groups aggregate the **same finite physical exchange** as CDR-008. For receiver segments i in a group, use `sum(Li * Fi,group) / sum(Li)`; a directly computed group is permitted only if proved equivalent. Preserve the original finite Geometry and identities. Out-of-domain proxies, endpoint reversals or cancellation artifacts do not define physical groups. The Adaptive Planner must not change underlying physical geometry.

Correcting these groups intentionally changes some Reference Fast numbers, including positive ones and cases where Full F already passes. This is an approved geometric compatibility deviation, not a tolerance adjustment. Corrected Fast provenance cites DEV-029/CDR-008; raw `back_ground`, `back_pv` and `back_shaded_pv` values remain intact as Reference observations. The seed independently supplies ground and total PV group expectations; it is not full Fast shaded-source/irradiance coverage.

## Approval boundary and evidence

Fast irradiance and Fast simulation remain distinct approximate models. **This does not close CDR-007, equate Fast with Full, approve all Fast semantics or complete P4/P5/P6/P7.** AOI G is a separate operator. Production numerical algorithms remain open implementation choices within approved semantics.

The approved targeted seed is `reference/candidate/vf-lcb01-v0.1/` (66 cases/198 artifacts); its corrected `fast_group_candidate` field keeps its historical schema name but now carries Owner-approved geometric expectations. A file/field name is not an approval state. The exact manifest and targeted comparator are bound by `LCB-01_OWNER_DECISIONS.json`; production cross-platform tolerance is not frozen. Verification must recompute finite aggregation, compare fresh independent expectations and preserve raw fields, not merely check F bounds.

Evidence: `fast-helper-comparison.json`, `global-abs-counterexamples.json`, directed Full taxonomy (separate), and newly rerun closure receipts. [Owner record](LCB-01_OWNER_DECISIONS.en.md) is the approval authority; [closure handoff](LCB-01_CLOSURE_HANDOFF.en.md) identifies the current verification receipt. Geometry/frozen source are unchanged; no production implementation is authorized by this record.
