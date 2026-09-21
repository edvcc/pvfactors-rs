# Geometry Tolerance Profile v0.1

- 状态：**APPROVED**
- 机器可读源：`reference/tolerance/geometry-tolerance-v0.1.json`
- 范围：仅 Geometry Gate

Algorithm predicate 为：active length `> 1e-8 m`；endpoint snap distance
`< 1e-8 m`；normalized orientation cross
`<= max(1e-12, 64*f64_epsilon)`；到支撑线的位置偏移
`<= max(1e-10 m, 64*f64_epsilon*max(1 m, coordinate_scale))`。

Differential comparison 使用 `|a-b| <= abs + rel*max(|a|,|b|)`：

| Profile | Absolute | Relative | Unit |
|---|---:|---:|---|
| orientation | `5e-12` | `5e-13` | dimensionless |
| position | `5e-12` | `5e-13` | m |
| length | `5e-12` | `5e-13` | m |
| angle | `5e-11` | `5e-13` | degree |

Topology、side、illumination class、logical key、source、case ID、`ReferenceIndex`、
`ActiveIndex`、active state、ordering 与 nonfinite class 必须精确相等。comparison tolerance
不能替代 algorithm predicate。本 profile 不冻结 View Factor、Perez、Radiosity 或 aggregate
irradiance tolerance。

Repository Owner 已于 2026-09-22 批准这些准确数值；适用范围仍仅为 Geometry Gate。
Comparator tolerance 不替代 algorithm predicate，且本 profile 不适用于 View Factor、Perez、
Radiosity 或 aggregate irradiance。
