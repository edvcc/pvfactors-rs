# Raw Reference 与 Corrected Expectation 差异报告

- 状态：**Recommended for Approval**
- Candidate：`geometry-golden-v0.1-candidate`
- 机器可读证据：`evidence/g2/raw-vs-corrected.json`

共有 45 条机器可读修正记录。每条均包含 DEV ID、CDR ID、field-level path、raw value、
corrected value 与 explanation。没有为得到 corrected result 而修改 raw 或 normalized artifact。

| 记录数 | Path / 范围 | Raw reference | Corrected expectation | Provenance |
|---:|---|---|---|---|
| 4 | `$.result.ground.corrected_extent_m` | 硬编码 `[-100,100]` | 请求的 finite extent | DEV-004 / CDR-003 |
| 1 | `$.result.length_m` | complete-cover difference 长度 `1.0` | empty / `0.0` | DEV-016 / CDR-006 |
| 26 | `$.result.projection[*].classification` | Reference-derived `regular` 或 `parallel_ground` | 显式 direct/horizon/below-horizon state | DEV-027 / CDR-003 |
| 4 | front/back shaded-length path | Reference horizon/below-horizon direct shading | direct shaded length 为 0 | DEV-027 / CDR-003 |
| 2 | `$.result.ground` | Reference direct-shadow partition | inactive shadow slot 加完整 finite illuminated ground | DEV-027 / CDR-003 |
| 2 | `$.result.topology` | Reference projection topology | 稳定 no-direct policy topology | DEV-027 / CDR-003 |
| 2 | `$.result.surfaces` | Reference projection surface | 具体化的 no-direct policy surface | DEV-027 / CDR-003 |
| 2 | `$.result.outcome` | `captured` | `classified_state` | DEV-027 / CDR-003 |
| 2 | `$.result.state` | 不存在 | 显式 horizon/below-horizon state | DEV-027 / CDR-003 |

DEV-027 是表示层缺口，不是宣称 upstream 新增 bug。DEV-003 针对 Engine skip-mask 行为，
不能表达 Geometry 层 projection state、保留的 row geometry、inactive direct-shadow slot 或
finite ground partition。非法输入继续使用 structured non-panic error contract，不作为数值 waiver
隐藏。

本报告仍是 candidate 决策输入。`CONDITIONALLY PASS`，Awaiting Repository Owner Approval。
