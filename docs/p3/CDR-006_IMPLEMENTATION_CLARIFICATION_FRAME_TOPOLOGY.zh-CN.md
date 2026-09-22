# CDR-006 Implementation Clarification — Frame Topology 生命周期

- 状态：**IMPLEMENTATION CLARIFICATION — AWAITING REPOSITORY OWNER REVIEW**
- 日期：2026-09-22
- 治理决策：CDR-006（**APPROVED**）
- 相关决策：CDR-003（**APPROVED**）
- 相关偏差：DEV-013、DEV-027
- 效力：**不重新打开 CDR；不改变语义**

## 1. 需要澄清的问题

CDR-006 规定 `SurfaceKey` 与 `ReferenceIndex` 跨 frame 保持稳定。CDR-003 与 Approved
DEV-027 corrected expectation 同时定义了与普通 direct-projection topology 不同的 reduced
no-direct topology。

因此，需要明确的实现问题是：

> 当 frame 改变 projection class 并选择另一个已批准 logical surface universe 时，identity 与
> reconstruction index 的生命周期和作用域是什么？

本 clarification 只解决 implementation interpretation，不改变任何已批准决策。

## 2. 原始已批准陈述

CDR-006 要求：

```text
SurfaceKey and ReferenceIndex remain stable across frames.
Activity and ActiveIndex are derived for the requested frame.
```

它还要求准确 reconstruction order、所选 logical order 中保留 inactive logical slot，以及
实际计算请求的 nonzero frame。

CDR-003 与 DEV-027 要求，在 `horizon_no_direct_projection` 和
`below_horizon_no_direct_projection` 中：

```text
row geometry remains defined
direct shadow logical slots are retained inactive
finite ground becomes one illuminated partition
no huge or nonfinite shadow is manufactured
```

Geometry classification 与后续 Simulation skip policy 保持分离。

## 3. Approved Golden 证据

Immutable corrected expectation `SUN_90.0` 与 `SUN_BELOW_HORIZON` 已明确规定：N=3 时，
每个 case 均为：

```text
logical_surface_count = 4
active_surface_count  = 1
```

有序 topology 为：

```text
ReferenceIndex(0)  Ground Shadow element 0, inactive
ReferenceIndex(1)  Ground Shadow element 1, inactive
ReferenceIndex(2)  Ground Shadow element 2, inactive
ReferenceIndex(3)  Ground Illumination element 0, active full extent
```

Row geometry 继续存在，front/back direct-shading length 均为 0，但 PV direct-projection
surface 不 materialize 到该 topology。

`reference/tools/geometry_golden.py::no_direct_projection_result()` 明确主动构造该表示：
先生成 N 个 inactive ground shadow surface，再生成 1 个 active illuminated surface。
Owner Review validator 又独立检查 classification、finiteness、保留的 inactive shadow、完整
illuminated extent、dense index 与 one-active-surface topology。

普通 direct-projection frame materialize 完整 PV 与 ground partition topology；对 N=3、cut-1
family，通常是 40 个 logical slot。因此，Approved Golden 不支持“所有 projection class 始终
共享同一个 40-slot universe”的解释。

`MULTI_TIMESTEP_NONZERO_INDEX` 提供另一半证据：在相同 logical topology 内，请求 frame 1
必须实际计算 frame 1，同时保留 logical key 与 reconstruction index；不得复刻 frozen adapter
的 `idx -> 0` 缺陷。

## 4. 表面冲突与解决方式

如果把“remain stable across frames”解释为：

> Solar zenith 完整 `[0°, 180°]` 定义域内的每个 frame 必须包含同一个全局 logical surface
> universe 和相同 index range。

该解释将与 Approved DEV-027 冲突，因为它要求 materialize 不存在的 PV direct-projection slot，
并把 no-direct topology 改为 40 slot，违背 Approved Golden。

正确的联合解释是：稳定性作用于所选 `FrameTopology`，以及 logical topology 不变的 frame
transition。

## 5. 规范性澄清

```text
SurfaceKey
    logical surface materialize 时保持稳定的 semantic identity。

FrameTopology
    一个成功构造 frame 所选择的 projection-state-specific logical surface universe。

ReferenceIndex
    一个 FrameTopology 内的 dense reconstruction index；脱离 owning topology 不具备完整语义。

Same-topology frames
    必须保持准确的 SurfaceKey <-> ReferenceIndex reconstruction order；activity 与
    ActiveIndex 可以逐 frame 改变。

Projection-state transition
    可以合法选择另一个已批准 FrameTopology。两个 topology 都存在的 key 保持同一语义，
    但 numeric ReferenceIndex 只能在 owning topology 内比较，或先按 key 显式 remap。

ActiveIndex
    始终是 frame-local，仅对 active surface dense 编号。
```

因此，`SurfaceKey` 是跨 topology join key。`ReferenceIndex` 不是全局 identity，不得单独用来
join topology 不同的 frame。

## 6. 已批准 topology family

### 6.1 Direct-projection topology

`DirectProjection` topology 包含已批准 ground shadow 与 illumination partition slot，随后是
PV row slot。Zero-length slot 保留在 logical order 中。Layout/cuts 和 direct topology 相同的
frame，即使 coordinate、length、activity 或 `ActiveIndex` 改变，也必须保持准确
reconstruction order。

### 6.2 No-direct topology

`HorizonNoDirectProjection` 与 `BelowHorizonNoDirectProjection` topology 包含：

```text
N inactive Ground::Shadow keys
+ 1 active Ground::Illumination key spanning GroundExtent
```

PV row entity geometry 保留在 `FrameGeometry.rows` 中；PV direct-projection surface key 不进入
`FrameTopology`。同一 layout 下，两种 no-direct class 使用相同 topology 形状，因此保持其
reconstruction order。

## 7. 必须保持的 invariant

每个实现都必须保证：

- 一个 `FrameTopology` 内 `SurfaceKey` unique；
- `ReferenceIndex` 从 0 到 topology length - 1 dense；
- topology family 内保持准确 approved order；
- same-topology frame 保持 key/index order 稳定；
- 比较或聚合不同 topology family 前按 key 显式 remap；
- 每帧 `ActiveIndex` dense，`ActiveMap` 双向一致；
- 实际计算请求的 frame，包括 nonzero `FrameIndex`；
- frame 明确存储准确 projection classification。

任何 API 都不得暗示 bare `ReferenceIndex` 在 projection-state transition 中全局稳定。

## 8. API 与实现影响

`FrameTopology` 拥有 ordered `SurfaceKey` collection。`ReferenceIndex` 的值可以读取，但不
提供不受限制的 public constructor。接收 `ReferenceIndex` 的算法必须同时处于其 owning
topology context 中。

Cross-frame facility 只能选择两条安全路径之一：

1. 证明两个 frame topology 相同，再按 `ReferenceIndex` 比较；或
2. 按 `SurfaceKey` join，并显式处理任一 topology 中 absent 的 key。

第一版 P3 API 只公开 `build_frame`，不增加 public batch API 隐藏该区别。后续 Simulation
batch 设计必须保留同一规则。

## 9. Non-change 声明

本 clarification：

- 不改变或重新打开 CDR-003；
- 不改变或重新打开 CDR-006；
- 不改变 CDR-006 predicate 数值或 boundary operator；
- 不改变 DEV-013 或 DEV-027；
- 不改变 Approved Golden 及其 raw/normalized/corrected layer；
- 不改变 Geometry Tolerance Profile v0.1；
- 不重新打开 G2；
- 不改变 projection classification；
- 不授权超出单独批准任务范围的 Rust 实现。

它只说明“stable identity”与“frame-specific approved topology universe”如何在 Rust model 中
同时成立。

## 10. 被拒绝的替代方案

### 所有 N=3 frame 使用统一 40-slot topology

拒绝，因为它与 Approved no-direct 4-slot expectation 及 Owner Review 检查直接冲突。

### 把 `ReferenceIndex` 当作全局 identity

拒绝，因为 dense positional index 只有在 ordered topology 中才有语义；projection-state
transition 可以改变成员与长度。

### 删除 inactive no-direct shadow slot

拒绝，因为 Approved DEV-027 明确保留每排一个 inactive ground shadow logical slot。

### 在 no-direct frame materialize inactive PV projection surface

拒绝，因为 Approved no-direct topology 中不存在这些 surface。该变化需要新决策和 Golden
版本。

## 11. 审查效力

Repository Owner review 前，本文档是 draft implementation clarification。批准后，它将成为
下一阶段 type-skeleton 与实现任务使用的规范性解释；它不会改变已批准 G2 artifact，不会
宣称 API 已实现，也不构成 G3 PASS。
