# Geometry Golden Approval Record

- 记录状态：**Recommended for Approval**
- Golden 状态：**CANDIDATE — NOT APPROVED**
- Candidate：`geometry-golden-v0.1-candidate`
- Manifest SHA-256：`bcbe113c5c6ce189ba0d5c2ec4f3750e58e2b7652403282eed0691bbbf717799`
- Generator commit：`5e864bf2d466191155dfe930b1c8e5de88cfccb1`
- Reference：`pvlib/solarfactors` v1.6.1，`ecbfc863657e239817603a43898ae173c7ccad9c`
- Tolerance：`geometry-tolerance-v0.1`

## Candidate 集合

集合包含 39 个具体案例与 117 个 artifact：每个案例各有一个 `raw_reference`、
`normalized_reference` 和 `corrected_expectation`。

`C01`、`C02`、`C03`、`C04`、`TILT_LEFT`、`TILT_FLAT`、`TILT_1e-10`、
`TILT_NEAR_LEFT`、`TILT_90.0`、`SHADING_NONE_CANDIDATE`、
`SHADING_PARTIAL_CANDIDATE`、`SHADING_HIGH_CANDIDATE`、`SUN_90.0`、
`SUN_ALONG_AXIS`、`CUT_2`、`CUT_8`、`CUT_ASYMMETRIC`、`UNDERGROUND`、
`CUT_ZERO`、`GROUND_NORMAL_EXTENT`、`GROUND_BOUNDARY_ENDPOINT`、
`GROUND_NEAR_BOUNDARY`、`MIRROR_BASE`、`MIRROR_IMAGE`、
`INVALID_AXIS_AZIMUTH`、`INVALID_SURFACE_AZIMUTH`、`INVALID_NAN`、
`INVALID_INF`、`INVALID_EXTENT_REVERSED`、
`PRIM_COMPLETE_COVER_DIFFERENCE`、`PRIM_ENDPOINT_TOUCH`、`PRIM_POINT_TOUCH`、
`PRIM_POSITIVE_OVERLAP`、`PRIM_ZERO_LENGTH`、`PRIM_PARALLEL_PROJECTION`、
`PRIM_COINCIDENT_PROJECTION`、`PRIM_ACTIVE_TOL_MINUS_ULP`、
`PRIM_ACTIVE_TOL_EXACT`、`PRIM_ACTIVE_TOL_PLUS_ULP`。

## 实际执行结果

- 输入 ZIP SHA-256 为 `2aca31b43080431a026f421e7d28ae86a814430fe27d60c0cf6e1aef2f4f5729`；
  内部 manifest 121 项全部通过；
- 冻结 source snapshot：78 个 Git blob hash 全部通过；
- Upstream suite：本次 macOS capture 为 102 passed / 11 warnings；其中 6 个是 baseline 已出现的
  divide-by-zero Reference 行为，5 个是非交互绘图 warning；无失败；
- Case 与 artifact schema：PASS；
- 独立不变量：PASS；43 个 report 已包括 structured invalid-input、primitive expectation、
  corrected-extent 与 mirror 检查；
- Reproducibility：PASS；两个独立完整生成目录字节级一致；
- Candidate 与另一份 fresh generation 比较：PASS，无差异；
- Raw/corrected 审计：PASS；DEV-004 影响 4 个 extent 案例，DEV-016 影响 complete-cover
  difference；没有隐藏的无依据修正；
- Approved 目录安全：PASS；仅含 `NOT APPROVED` README。

## 已记录条件

29 个固定包版本全部匹配。本次 capture 使用 CPython 3.12.12 macOS arm64，而 Phase 0–1
包声称 CPython 3.12.14；当前执行环境无法获得该 patch 版本。批准前，Owner 必须修正/替换
canonical runtime 声明并重新生成，或明确接受新的 canonical runtime。

Fetch 后不存在远端 `develop`，仅有 `origin/master`。因此工作分支从未变化的
`origin/master` commit `bc0b7ec1cb17938be9f4d53c83e1fb80a1abd9ba` 创建。进入新建或
Owner 指定的 `develop` 仍是人工治理动作。

## 推荐与 Owner 决策

本 candidate **在两个已记录基线条件被解决或明确接受后，Recommended for Approval**。
批准必须指明本 manifest hash，并分别批准 CDR-003 与 CDR-006。

- CDR-003 Owner 决策：Pending
- CDR-006 Owner 决策：Pending
- Geometry Golden Owner 决策：Pending
- Reviewer 身份/证据：Pending

在这些决策形成前：`CONDITIONALLY PASS`，Awaiting Repository Owner Approval。
