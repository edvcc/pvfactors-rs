# Raw Reference 与 Corrected Expectation 差异报告

- 状态：**Recommended for Approval**
- Candidate：`geometry-golden-v0.1-candidate`
- 机器可读证据：`evidence/g2/raw-vs-corrected.json`

共存在 5 个字段级差异；每个差异同时具有 DEV 与 CDR 追溯。没有修改任何 raw artifact。

| Case | Field | Raw reference | Corrected expectation | Provenance |
|---|---|---|---|---|
| `GROUND_NORMAL_EXTENT` | `ground.extent` | `[-100,100]` | `[-10,10]` | DEV-004 / CDR-003 |
| `GROUND_BOUNDARY_ENDPOINT` | `ground.extent` | `[-100,100]` | `[-0.5,0.5]` | DEV-004 / CDR-003 |
| `GROUND_NEAR_BOUNDARY` | `ground.extent` | `[-100,100]` | `[-0.500000000001,0.500000000001]` | DEV-004 / CDR-003 |
| `INVALID_EXTENT_REVERSED` | `ground.extent` | `[-100,100]` | 对 `[1,-1]` 返回结构化 invalid-extent outcome | DEV-004 / CDR-003 |
| `PRIM_COMPLETE_COVER_DIFFERENCE` | `result.length_m` | `1.0` | `0.0` / empty | DEV-016 / CDR-006 |

前四项把 Reference 硬编码数值 extent 与 V1 公共 finite-extent contract 分开。最后一项依据
interval set 语义修正确认的 complete-cover subtraction 缺陷。其他 corrected artifact 或与
normalized reference geometry 相同，或应用结构化 invalid-input contract，或应用已命名的
horizon state；均不作为静默数值 waiver。

本报告仍是 candidate 决策输入。`CONDITIONALLY PASS`，Awaiting Repository Owner Approval。
