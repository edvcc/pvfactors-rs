# P3 Rust Geometry Kernel Entry Contract

- 状态：**ACTIVE**
- Gate：**G2 PASS**
- P3 Implementation：**NOT STARTED**
- Approved Golden：`geometry-golden-v0.1`
- Source candidate：`geometry-golden-v0.1-candidate`
- Approved manifest：`efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- Approved tolerance：`geometry-tolerance-v0.1`
- 批准日期：2026-09-22

## 激活字段

- `approved_case_ids =` “Approved case IDs”章节中的全部 55 个 ID
- `approved_golden_version = geometry-golden-v0.1`
- `approved_manifest_sha256 = efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- `approved_cdrs = [CDR-003, CDR-006]`
- `approved_tolerance = geometry-tolerance-v0.1`

Repository Owner 已通过日期为 2026-09-22 的 `G2 Approval Closure Task v1.0` 填充这些
字段。此决定激活 Entry Contract，但本身不开始或实现 P3。

## 激活后冻结的语义

有限闭区间 ground extent，Reference 兼容默认值 `[-100,100]`；row 位于 extent 内/边界；
ground projection clipping；严格大于 `1e-10 m` 的 clearance；有限且 modulo-normalized
azimuth；非 flat surface azimuth 为 axis±90°；tilt `[0°,180°]` 且不折叠、不交换 side；
exact-flat 区分；solar zenith 表示域 `[0°,180°]`，具名 `direct_projection`、
`horizon_no_direct_projection`、`below_horizon_no_direct_projection`；GCR finite 且严格大于 0，
不以 `<=1` 代理限制，真实 geometry 冲突按自身规则检查；具名 parallel、coincident geometric
projection；结构化 non-panic error；正确 interval subtraction；
严格 active/snap threshold；scale-aware orientation/offset predicate；稳定 `SurfaceKey`；
单独的 `ReferenceIndex` 与每帧 `ActiveIndex`；包含 inactive slot 的精确 reconstruction order。
所有按帧选择的 lookup 必须使用请求的 index，不得复刻冻结 Reference 的 DEV-013 `idx -> 0`
ground-adapter 缺陷。

## Approved case IDs

激活决定批准以下全部 55 个 ID：

`C01`、`C02`、`C03`、`C04`、`TILT_LEFT`、`TILT_FLAT`、`TILT_1e-10`、
`TILT_NEAR_LEFT`、`TILT_90.0`、`SHADING_NONE_CANDIDATE`、
`SHADING_PARTIAL_CANDIDATE`、`SHADING_HIGH_CANDIDATE`、`SUN_90.0`、
`SUN_ALONG_AXIS`、`CUT_2`、`CUT_8`、`CUT_ASYMMETRIC`、`UNDERGROUND`、
`CUT_ZERO`、`TILT_120`、`TILT_180`、`GCR_GT_1`、`SUN_BELOW_HORIZON`、
`INVALID_TILT_NEGATIVE`、`INVALID_TILT_GT_180`、
`MULTI_TIMESTEP_NONZERO_INDEX`、`GROUND_NORMAL_EXTENT`、
`GROUND_BOUNDARY_ENDPOINT`、`GROUND_NEAR_BOUNDARY`、`MIRROR_BASE`、
`MIRROR_IMAGE`、`INVALID_AXIS_AZIMUTH`、`INVALID_SURFACE_AZIMUTH`、
`INVALID_NAN`、`INVALID_INF`、`INVALID_EXTENT_REVERSED`、
`PRIM_COMPLETE_COVER_DIFFERENCE`、`PRIM_ENDPOINT_TOUCH`、`PRIM_POINT_TOUCH`、
`PRIM_POSITIVE_OVERLAP`、`PRIM_ZERO_LENGTH`、`PRIM_PARALLEL_PROJECTION`、
`PRIM_COINCIDENT_PROJECTION`、`PRIM_ACTIVE_TOL_MINUS_ULP`、
`PRIM_ACTIVE_TOL_EXACT`、`PRIM_ACTIVE_TOL_PLUS_ULP`、
`PRIM_ENDPOINT_SNAP_MINUS_ULP`、`PRIM_ENDPOINT_SNAP_EXACT`、
`PRIM_ENDPOINT_SNAP_PLUS_ULP`、`PRIM_ORIENTATION_MINUS_ULP`、
`PRIM_ORIENTATION_EXACT`、`PRIM_ORIENTATION_PLUS_ULP`、
`PRIM_LINE_OFFSET_MINUS_ULP`、`PRIM_LINE_OFFSET_EXACT`、
`PRIM_LINE_OFFSET_PLUS_ULP`。

Approved set 覆盖 row count 1/2/3/11；left、right、flat、正负 near-zero、
90°、120°、180°；GCR 大于 1；direct、horizon、below-horizon solar state；
no/partial/high shade；cut 1/2/8 与 3/5；finite/boundary ground extent；invalid input；
complete cover；touch/overlap；tolerance ±ULP；parallel/coincident；full mirror。
最低集合还必须覆盖 endpoint snap、normalized orientation、line-offset 的 ±ULP 边界，以及
multi-timestep nonzero-index lookup。

## 必须保持的不变量

每侧 illuminated length 加 shaded length 等于 row width；shade 位于 `[0,width]`；有限 ground
完整覆盖且无 positive overlap 或 unexplained gap；active endpoint finite；active length 严格大于
threshold；key/side/coordinate 一致；外部身份不依赖 vector position；full mirror 必须共同变换
row geometry、sun vector、normal、extent、row order 与 side interpretation。

## 允许的 Reference 偏差

只允许激活批准中明确命名的偏差。当前 candidate 建议 DEV-004/CDR-003（有限可配置 extent）、
DEV-013/CDR-006（按请求 frame 执行 ground lookup）、
DEV-016/CDR-006（complete-cover difference）与 DEV-027/CDR-003（显式 projection state 及
no-direct policy topology）。raw reference artifact 保持不可变；不得用泛化的“更稳健”waiver
接受其他差异。

## P3 精确实现范围

P3 可实现 Rust value type（`Point2`、vector、segment、interval）、geometry input validation 与结构化 error、
rotation/row construction、solar 2D projection classification、shadow projection/clipping、
PV side partition、ground partition、稳定 `SurfaceKey` / `ReferenceIndex` / `ActiveIndex`，
以及仅 Geometry 的测试和 differential comparison。
新增 dependency 必须有真实 consumer。

P3 不得实现 View Factor、Perez、Radiosity、irradiance aggregation、solver selection、Python
binding、serial/parallel planner、Adaptive Planner、SIMD 或 GPU。Rust runtime 不得依赖
Python、pvlib、Shapely 或 GEOS。

## 禁止的行为变化

不得重新解释已批准语义；不得以 `Vec` 位置作为稳定身份；不得为通过 Golden 放宽 predicate；
不得修改 raw fixture；不得跨 source/side/normal/material/visibility 合并；不得为 parallel 建立
第二套算法；不得引入未登记 Reference deviation。

## 进入前提

进入前提已全部满足：CDR-003、CDR-006、准确 Golden manifest 与 Geometry-only tolerance
均已批准，Canonical Runtime R0 与 cross-runtime comparison 均通过。本合同为 `ACTIVE`，可供
单独获得授权的 P3 implementation task 使用。`develop` 是 integration baseline，但当前 PR
不构成 merge 授权。本 G2 closure 未开始 P3 implementation。
