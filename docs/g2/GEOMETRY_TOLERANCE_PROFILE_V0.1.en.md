# Geometry Tolerance Profile v0.1

- Status: **Recommended for Approval**
- Machine-readable source: `reference/tolerance/geometry-tolerance-v0.1.json`
- Scope: Geometry Gate only

Algorithm predicates are: active length `> 1e-8 m`; endpoint snap distance
`< 1e-8 m`; normalized orientation cross
`<= max(1e-12, 64*f64_epsilon)`; positional line offset
`<= max(1e-10 m, 64*f64_epsilon*max(1 m, coordinate_scale))`.

Differential comparison uses `|a-b| <= abs + rel*max(|a|,|b|)`:

| Profile | Absolute | Relative | Unit |
|---|---:|---:|---|
| orientation | `5e-12` | `5e-13` | dimensionless |
| position | `5e-12` | `5e-13` | m |
| length | `5e-12` | `5e-13` | m |
| angle | `5e-11` | `5e-13` | degree |

Topology, side, illumination class, logical key, source, case ID,
`ReferenceIndex`, `ActiveIndex`, active state, ordering, and nonfinite class are
exact. Comparison tolerance cannot replace an algorithm predicate. This profile
does not freeze View Factor, Perez, Radiosity, or aggregate-irradiance tolerance.

The values are an initial review candidate derived from f64 operation scale,
the frozen reference branches, and same-environment capture. Cross-platform
calibration is not claimed. G2 remains `CONDITIONALLY PASS`, Awaiting Repository Owner Approval.

