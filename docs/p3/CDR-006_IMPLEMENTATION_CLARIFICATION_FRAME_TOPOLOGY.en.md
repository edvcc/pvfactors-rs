# CDR-006 Implementation Clarification — Frame Topology Lifetime

- Status: **IMPLEMENTATION CLARIFICATION — APPROVED**
- Date: 2026-09-22
- Governing decision: CDR-006 (**APPROVED**)
- Related decision: CDR-003 (**APPROVED**)
- Related deviations: DEV-013, DEV-027
- Effect: **NOT A CDR REOPEN; NOT A SEMANTIC CHANGE**

## 1. Question being clarified

CDR-006 states that `SurfaceKey` and `ReferenceIndex` remain stable across
frames. CDR-003 and the Approved DEV-027 corrected expectations also define a
reduced no-direct topology that differs from normal direct-projection topology.

The implementation question is therefore:

> What is the lifetime and scope of identity and reconstruction index when a
> frame changes projection class and selects a different approved logical
> surface universe?

This clarification resolves the implementation interpretation only. It does
not alter either approved decision.

## 2. Original approved statements

CDR-006 requires:

```text
SurfaceKey and ReferenceIndex remain stable across frames.
Activity and ActiveIndex are derived for the requested frame.
```

It also requires exact reconstruction order, inactive logical slots within the
selected logical order, and actual evaluation of a requested nonzero frame.

CDR-003 and DEV-027 require that, in
`horizon_no_direct_projection` and
`below_horizon_no_direct_projection`:

```text
row geometry remains defined
direct shadow logical slots are retained inactive
finite ground becomes one illuminated partition
no huge or nonfinite shadow is manufactured
```

Geometry classification remains distinct from later Simulation skip policy.

## 3. Approved Golden evidence

The immutable corrected expectations for `SUN_90.0` and
`SUN_BELOW_HORIZON` are explicit. For N=3, each contains:

```text
logical_surface_count = 4
active_surface_count  = 1
```

The ordered topology is:

```text
ReferenceIndex(0)  Ground Shadow element 0, inactive
ReferenceIndex(1)  Ground Shadow element 1, inactive
ReferenceIndex(2)  Ground Shadow element 2, inactive
ReferenceIndex(3)  Ground Illumination element 0, active full extent
```

Row geometry remains present and both direct-shading lengths are zero, but PV
direct-projection surfaces are not materialized in this topology.

`reference/tools/geometry_golden.py::no_direct_projection_result()` constructs
this representation deliberately: N inactive ground shadow surfaces followed
by one active illuminated surface. The Owner Review validator separately checks
the classification, finiteness, retained inactive shadows, complete illuminated
extent, dense indices, and one-active-surface topology.

Normal direct-projection frames materialize the full PV and ground partition
topology. For the N=3, cut-1 family this is ordinarily 40 logical slots. The
Approved Golden therefore does not support an interpretation in which all
projection classes always share one 40-slot universe.

`MULTI_TIMESTEP_NONZERO_INDEX` supplies the other half of the evidence: within
the same logical topology, requesting frame 1 must evaluate frame 1 while
preserving logical keys and reconstruction indices. The frozen adapter's
`idx -> 0` defect is not reproduced.

## 4. Apparent conflict and resolution

The phrase “remain stable across frames” would conflict with Approved DEV-027
if interpreted as:

> Every frame in the complete `[0°, 180°]` solar-zenith domain must contain the
> same global logical surface universe and identical index range.

That interpretation is rejected because it would require materializing absent
PV direct-projection slots and a 40-slot no-direct topology contrary to the
Approved Golden.

The approved statements are jointly satisfied by scoping stability to the
selected `FrameTopology` and to transitions that retain the same logical
topology.

## 5. Normative clarification

```text
SurfaceKey
    Stable semantic identity whenever a logical surface is materialized.

FrameTopology
    The projection-state-specific logical surface universe selected for one
    successfully constructed frame.

ReferenceIndex
    Dense reconstruction index within one FrameTopology. It is not meaningful
    without the topology that owns it.

Same-topology frames
    Must preserve the exact SurfaceKey <-> ReferenceIndex reconstruction order.
    Activity and ActiveIndex may change per frame.

Projection-state transition
    May legally select another approved FrameTopology. Keys that exist in both
    topologies keep their semantic meaning, but numeric ReferenceIndex values
    are compared only within their owning topology or through explicit key
    remapping.

ActiveIndex
    Always frame-local and dense over active surfaces only.
```

Thus, `SurfaceKey` is the cross-topology join key. `ReferenceIndex` is not a
global identity and must never be used alone to join frames with different
topologies.

## 6. Approved topology families

### 6.1 Direct-projection topology

For `DirectProjection`, the topology contains the approved ground shadow and
illumination partition slots followed by PV row slots. Zero-length slots remain
in the logical order. Frames with the same layout/cuts and direct topology must
preserve exact reconstruction order even when coordinates, lengths, activity,
or `ActiveIndex` change.

### 6.2 No-direct topology

For `HorizonNoDirectProjection` and `BelowHorizonNoDirectProjection`, the
topology contains:

```text
N inactive Ground::Shadow keys
+ 1 active Ground::Illumination key spanning GroundExtent
```

PV row entity geometry remains in `FrameGeometry.rows`; PV direct-projection
surface keys are not present in `FrameTopology`. The two no-direct classes use
the same topology shape for the same layout and therefore preserve their
reconstruction order.

## 7. Required invariants

Every implementation must enforce:

- `SurfaceKey` uniqueness inside one `FrameTopology`;
- dense `ReferenceIndex` values from zero to topology length minus one;
- exact approved order within a topology family;
- stable key/index order for same-topology frames;
- explicit key-based remapping before comparing or aggregating different
  topology families;
- per-frame dense `ActiveIndex` and bidirectional `ActiveMap` consistency;
- requested-frame evaluation, including nonzero `FrameIndex`; and
- exact projection classification stored with the frame.

No API may imply that a bare `ReferenceIndex` is globally stable across a
projection-state transition.

## 8. API and implementation consequences

`FrameTopology` owns the ordered `SurfaceKey` collection. `ReferenceIndex` has
a readable value but no unrestricted public constructor. Algorithms receiving
a `ReferenceIndex` must also operate in the context of its owning topology.

Cross-frame facilities may use one of two safe paths:

1. assert/evidence that both frames have the same topology and compare by
   `ReferenceIndex`; or
2. join by `SurfaceKey` and explicitly handle keys absent from either topology.

The first P3 API exposes only `build_frame`; it does not add a public batch API
to hide this distinction. Later Simulation batch design must preserve the same
rule.

## 9. Non-change statement

This clarification:

- does not change or reopen CDR-003;
- does not change or reopen CDR-006;
- does not change CDR-006 predicate values or boundary operators;
- does not change DEV-013 or DEV-027;
- does not change the Approved Golden or its raw/normalized/corrected layers;
- does not change Geometry Tolerance Profile v0.1;
- does not reopen G2;
- does not change projection classification; and
- does not authorize Rust implementation beyond the separately approved task.

It only defines how “stable identity” and “frame-specific approved topology
universe” coexist in the Rust model.

## 10. Rejected alternatives

### One universal 40-slot topology for all N=3 frames

Rejected because it contradicts the explicit 4-slot Approved no-direct
expectations and Owner Review checks.

### Treat `ReferenceIndex` as global identity

Rejected because a dense positional index is meaningful only in an ordered
topology; projection-state transitions can change membership and length.

### Remove inactive no-direct shadow slots

Rejected because Approved DEV-027 explicitly retains one inactive ground
shadow logical slot per row.

### Materialize inactive PV projection surfaces in no-direct frames

Rejected because they are absent from the Approved no-direct topology. Such a
change requires a new decision and Golden version.

## 11. Review effect

Repository Owner approval is complete. This clarification is the normative P3
implementation interpretation of CDR-006 stable identity and `FrameTopology`
lifetime. It does not alter approved G2 artifacts, reopen CDR-006, change
CDR-003 or the Approved Golden, declare the API implemented, or constitute G3
PASS.
