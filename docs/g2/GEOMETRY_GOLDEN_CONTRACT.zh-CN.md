# Geometry Golden Contract

- 状态：**Recommended for Approval**
- Candidate 版本：`geometry-golden-v0.1-candidate`
- Tolerance：`geometry-tolerance-v0.1`
- Reference：`pvlib/solarfactors` v1.6.1，`ecbfc863657e239817603a43898ae173c7ccad9c`

## 目的与权威边界

Geometry Golden 是独立 Rust 重实现的开发期 Oracle，不是 Python runtime dependency，
也不授权复制 Python/Shapely 实现结构。它记录数学输入、可观察 Reference 行为、显式
corrected expectation 与稳定 topology。Repository Owner 批准具名集合前，candidate 不具有
approved 状态。

## 三类不可混淆的数据

1. `raw_reference`：冻结 Reference 的直接观察，包括 exception、nonfinite 与已知缺陷；
2. `normalized_reference`：将观察转换为确定性、语言无关的 canonical JSON，定义 ordering、
   unit、numeric type、nonfinite mask、logical key、`ReferenceIndex` 与每帧 active map，
   但不修正行为；
3. `corrected_expectation`：只应用已命名的 CDR/DEV 决策。每个变化字段记录 raw value、
   corrected value、DEV ID、CDR ID 与 explanation。

生成器不得为使比较通过而重写 raw evidence。缺少决策 provenance 的 corrected field 会使
candidate 无效。

## Canonical representation

位置与长度是以米为单位的 f64；角度默认以 degree 表示，明确标注时才使用 radian；方向向量
是无量纲 f64。JSON object key 排序后参与 hash。NaN 与 infinity 编码为
`{"nonfinite":"..."}`，并以 JSON path 记录在 `nonfinite_mask`；禁止非标准 JSON NaN。
Python object repr 与 Shapely serialization 不属于合同数据。

每个 ordered-array artifact 包含 normalized input；rotation 与 solar 2D vector；projection
classification；row center/endpoints/normals/width/order；raw 与 clipped ground shadow；
ground cut、shaded/illuminated element；PV 与 ground logical surface；坐标、长度、side、
shade class、`SurfaceKey`、`ReferenceIndex`、active state 与 `ActiveIndex`。非法输入包含
结构化 V1 error 与 `panic=false`。

`SurfaceKey` 为
`{kind, source, row, side, segment, illumination, ground_element, cut_interval}`，
即使长度为零也保留。Reference 与 reconstruction 精确顺序由 CDR-006 定义；vector position
不是身份。

## Manifest 与 provenance

Manifest 记录 Reference version/commit、Python/NumPy/Shapely/pvlib 版本、environment
identity、generator commit/digest、generation time、case/catalog hash、field name、axes、
unit map、dtype、shape、payload hash、nonfinite mask、classification、status、transformation
与 license relevance。源 License 保存在 `reference/PVLIB_LICENSE.txt`。

## 验证与可复现性

验收必须包括：case/artifact schema validation；直接冻结 Reference capture；normalize；
candidate generation；两次独立生成对 payload、topology、key、`ReferenceIndex`、active map
和 nonfinite classification 的字节级一致；candidate compare；独立 row-side、shade-bound、
ground-coverage、finite-endpoint、active-threshold、identity 与完整 mirror 不变量；raw/corrected
差异审计；双语文档检查；branch safety 证据。

同一冻结环境内的 generation determinism 必须精确。后续 Rust 数值比较可使用
`geometry-tolerance-v0.1`；该 tolerance 不得掩盖生成不确定性或 topology 差异。

## 治理

工具只写入 `reference/candidate`；`reference/approved` 保持 `NOT APPROVED`。批准必须指明
candidate manifest hash，并同时批准 CDR-003、CDR-006 与 candidate。在此之前 G2 为
`CONDITIONALLY PASS`，Awaiting Repository Owner Approval。

