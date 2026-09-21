# Geometry Tolerance Profile v0.1

- Status: **APPROVED**
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

The Repository Owner approved these exact values on 2026-09-22. The scope
remains Geometry Gate only. Comparator tolerance does not replace an algorithm
predicate, and this profile does not apply to View Factor, Perez, Radiosity, or
aggregate irradiance.
