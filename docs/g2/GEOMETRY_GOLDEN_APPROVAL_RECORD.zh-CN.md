# Geometry Golden Approval Record

- 记录状态：**Recommended for Approval**
- Golden 状态：**CANDIDATE — NOT APPROVED**
- Candidate：`geometry-golden-v0.1-candidate`
- Manifest SHA-256：`efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- Generator commit：`01549e07c16bfe10a82d2889b1b62c58ef6861e7`
- Reference：`pvlib/solarfactors` v1.6.1，`ecbfc863657e239817603a43898ae173c7ccad9c`
- Tolerance：`geometry-tolerance-v0.1`

## Candidate 集合

集合包含 55 个具体案例与 165 个 artifact：每个案例各有一个 `raw_reference`、
`normalized_reference` 和 `corrected_expectation`。

`C01`、`C02`、`C03`、`C04`、`TILT_LEFT`、`TILT_FLAT`、`TILT_1e-10`、
`TILT_NEAR_LEFT`、`TILT_90.0`、`SHADING_NONE_CANDIDATE`、
`SHADING_PARTIAL_CANDIDATE`、`SHADING_HIGH_CANDIDATE`、`SUN_90.0`、
`SUN_ALONG_AXIS`、`CUT_2`、`CUT_8`、`CUT_ASYMMETRIC`、`UNDERGROUND`、
`CUT_ZERO`、`TILT_120`、`TILT_180`、`GCR_GT_1`、`SUN_BELOW_HORIZON`、
`INVALID_TILT_NEGATIVE`、`INVALID_TILT_GT_180`、`GROUND_NORMAL_EXTENT`、
`GROUND_BOUNDARY_ENDPOINT`、`GROUND_NEAR_BOUNDARY`、`MIRROR_BASE`、
`MIRROR_IMAGE`、`INVALID_AXIS_AZIMUTH`、`INVALID_SURFACE_AZIMUTH`、
`INVALID_NAN`、`INVALID_INF`、`INVALID_EXTENT_REVERSED`、
`PRIM_COMPLETE_COVER_DIFFERENCE`、`PRIM_ENDPOINT_TOUCH`、`PRIM_POINT_TOUCH`、
`PRIM_POSITIVE_OVERLAP`、`PRIM_ZERO_LENGTH`、`PRIM_PARALLEL_PROJECTION`、
`PRIM_COINCIDENT_PROJECTION`、`PRIM_ACTIVE_TOL_MINUS_ULP`、
`PRIM_ACTIVE_TOL_EXACT`、`PRIM_ACTIVE_TOL_PLUS_ULP`、
`MULTI_TIMESTEP_NONZERO_INDEX`、`PRIM_ENDPOINT_SNAP_MINUS_ULP`、
`PRIM_ENDPOINT_SNAP_EXACT`、`PRIM_ENDPOINT_SNAP_PLUS_ULP`、
`PRIM_ORIENTATION_MINUS_ULP`、`PRIM_ORIENTATION_EXACT`、
`PRIM_ORIENTATION_PLUS_ULP`、`PRIM_LINE_OFFSET_MINUS_ULP`、
`PRIM_LINE_OFFSET_EXACT`、`PRIM_LINE_OFFSET_PLUS_ULP`。

## 实际执行结果

- 冻结 source snapshot：78 个 Git blob hash 全部通过；
- Canonical Reference Runtime R0：PASS；Linux x86_64 / glibc 2.39 /
  CPython 3.12.14、29 个固定 package、GEOS 3.13.1 与四个确定性环境变量全部匹配；
  environment ID 为 `031158a1d1be8cdb9093`；
- Case 与 artifact schema：PASS；
- 独立不变量：PASS；65 个 report 已包括 structured invalid-input、primitive expectation、
  corrected-extent、mirror、`TILT_120`、`TILT_180`、`GCR_GT_1`、horizon 与
  below-horizon 检查；
- Reproducibility：PASS；两次独立完整 R0 生成字节级一致；
- 与 macOS arm64 / CPython 3.12.12 的 cross-runtime comparison：PASS；24,391 个
  topology/key/side/index/active-state 检查精确一致。角度最大绝对差为 0 degree，长度为
  `5.551115123125783e-16 m`，orientation 为 `5.551115123125783e-17`，position 为
  `8.881784197001252e-16 m`，均满足未修改的 `geometry-tolerance-v0.1`；violation 为 0；
- Raw/corrected 审计：PASS；47 条 deviation record 均含 DEV、CDR、field-level path、
  raw value、corrected value 与 explanation。DEV-004 为 4 条 extent 记录，DEV-013 为 1 条
  nonzero-index 记录，DEV-016 为 1 条 complete-cover 记录，DEV-027 为 41 条显式
  projection state/no-direct 记录；没有隐藏的无依据修正；
- Approved 目录安全：PASS；仅含 `NOT APPROVED` README。

## 已记录条件

Canonical Runtime 条件保持关闭。当前 candidate 在 R0 中生成，
`canonical_environment_match=true`，并通过扩展后的 cross-runtime payload comparison。
macOS arm64 / CPython 3.12.12 的 manifest、validation、verification、reproducibility 与
comparison 记录保留在 `evidence/g2/cross-runtime/`。

已被取代的 39-case 与 45-case R0 manifest 保留在 `evidence/g2/history/`，不再是当前
approval hash。closure 分支
`research/g2-owner-review-closure` 从最新 `origin/develop` commit
`ddee1f43d78dc4060c7f20f0b9d3777b07ddc914` 创建；`182dbb54...` 之后未集成的 3 个
canonical-runtime commit 按拓扑顺序 cherry-pick。本任务未修改 `master` 或 `develop`，
也未 merge PR。

## 推荐与 Owner 决策

本 candidate **Recommended for Approval**。批准必须指明本 manifest hash，并分别批准
CDR-003 与 CDR-006。

- CDR-003 Owner 决策：Pending
- CDR-006 Owner 决策：Pending
- Geometry Golden Owner 决策：Pending
- Reviewer 身份/证据：Pending

在这些决策形成前：`CONDITIONALLY PASS`，Awaiting Repository Owner Approval。
