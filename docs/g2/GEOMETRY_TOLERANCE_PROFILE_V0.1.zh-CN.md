# Geometry Tolerance Profile v0.1

- 状态：**Recommended for Approval**
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

这些数值是依据 f64 运算尺度、冻结 Reference 分支与同环境采集形成的初始审查候选；
不宣称已完成跨平台标定。G2 保持 `CONDITIONALLY PASS`，Awaiting Repository Owner Approval。

