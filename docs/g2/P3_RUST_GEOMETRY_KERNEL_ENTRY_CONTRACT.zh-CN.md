# P3 Rust Geometry Kernel Entry Contract

- 状态：**Recommended for Approval — NOT ACTIVE**
- Gate：`CONDITIONALLY PASS`，Awaiting Repository Owner Approval
- Candidate Golden：`geometry-golden-v0.1-candidate`
- Candidate manifest：`d805262560199583dad12853b422c2976bd40866cf4ff1c50133206c79b71417`
- Candidate tolerance：`geometry-tolerance-v0.1`

## 激活字段

- `approved_case_ids = []`
- `approved_golden_version = null`
- `approved_manifest_sha256 = null`
- `approved_cdrs = []`

这些字段有意保持为空。只有 Repository Owner 明确指明 CDR-003、CDR-006 与 candidate
manifest 的决定才能填入。在此之前不得开始 P3 实现。

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

## Candidate case IDs

激活决定可批准 Geometry Golden Approval Record 中列出的全部 45 个 ID，或明确子集；不得只引用
family name。最低激活集合仍须覆盖 row count 1/2/3/11；left、right、flat、正负 near-zero、
90°、120°、180°；GCR 大于 1；direct、horizon、below-horizon solar state；
no/partial/high shade；cut 1/2/8 与 3/5；finite/boundary ground extent；invalid input；
complete cover；touch/overlap；tolerance ±ULP；parallel/coincident；full mirror。

## 必须保持的不变量

每侧 illuminated length 加 shaded length 等于 row width；shade 位于 `[0,width]`；有限 ground
完整覆盖且无 positive overlap 或 unexplained gap；active endpoint finite；active length 严格大于
threshold；key/side/coordinate 一致；外部身份不依赖 vector position；full mirror 必须共同变换
row geometry、sun vector、normal、extent、row order 与 side interpretation。

## 允许的 Reference 偏差

只允许激活批准中明确命名的偏差。当前 candidate 建议 DEV-004/CDR-003（有限可配置 extent）、
DEV-016/CDR-006（complete-cover difference）与 DEV-027/CDR-003（显式 projection state 及
no-direct policy topology）。raw reference artifact 保持不可变；不得用泛化的“更稳健”waiver
接受其他差异。

## P3 精确实现范围

P3 可实现 Rust value type（`Point2`、vector、segment、interval）、输入校验与结构化 error、
rotation/row construction、solar 2D projection classification、shadow projection/clipping、
PV side partition、ground partition、稳定 topology key/order/map，以及仅 Geometry 的测试和比较器。
新增 dependency 必须有真实 consumer。

P3 不得实现 View Factor、Perez、Radiosity、irradiance aggregation、solver selection、Python
binding、serial/parallel planner、adaptive execution、SIMD 或 GPU。Rust runtime 不得依赖
Python、pvlib、Shapely 或 GEOS。

## 禁止的行为变化

不得重新解释已批准语义；不得以 `Vec` 位置作为稳定身份；不得为通过 Golden 放宽 predicate；
不得修改 raw fixture；不得跨 source/side/normal/material/visibility 合并；不得为 parallel 建立
第二套算法；不得引入未登记 Reference deviation。

## 进入前提

Owner 批准 CDR-003、CDR-006、准确 Golden manifest 与 tolerance；仅在这些记录存在后创建
P3 task。`develop` 是 integration baseline，但当前 PR 不构成批准或 merge 授权。
Canonical Runtime 差异已通过 R0 生成与 cross-runtime comparison 解决。本合同本身不授权实现。
