# DEV-028 — View Factor 方向与有限可见域偏差候选

状态：**PROPOSED / UNAPPROVED**。日期：2026-09-22。现有 register 止于 DEV-027；新编号不修改既有批准历史。关联 CDR-008 也仍待 Owner 审阅。

## Reference 行为与触发条件

冻结 solarfactors `ecbfc863657e239817603a43898ae173c7ccad9c` 的 `pvfactors/viewfactors/vfmethods.py` 存在两类不同发现：

1. **Full F 符号缺陷。** `_vf_hottel_gnd_surf` 根据 high/low 和 cut-point side 指定 crossed/uncrossed，输出带符号差。子段舍入为等高时，顺序可能反转。408个负 PV→ground helper 结果全部出现精确 height tie。ground→PV 继承负号；sky 可能大于1，也可能在[0,1]内但仍然错误。
2. **Fast 有限可见域缺陷/局限。** `calculate_vf_to_gnd` 可能构造越出[−100,100]、端点反向且产生严重消减的边排代理；中间排代理又可能包含有限地面以外的交换量。必须在大小计算前验证实际法向和有限域。此项与 DEV-004 的有限地面背景相关，但其 Geometry 决策没有关闭 VF 聚合行为。

观察到的 Full 失败域为精确180°及180−1 ULP，随方位、排和切分变化。不能概括为“所有 >90°”或“仅精确180°”。测试的0、1e−10、1、45、89.9、90及其ULP/epsilon邻域、100、120、150、179、179.9和额外近180值，除记录的8个 case 外通过。该覆盖集固定高度/宽度/排距，不是连续域证明。一般触发条件是 VF 端点顺序假设失效，而 Geometry 仍在批准域内。Fast 有限代理差异的域更广。

## 可观察影响与正确数学行为

批准 TILT_180 的 `F[3,28]` 为 −0.2038204263767998；独立 Decimal90 为 +0.2038204263767998815712607034…，数值积分为 +0.20382042637679987。两面相向且无遮挡。该 case 有36个越界项、37个偏差字段，说明 bounds 之外也需要 differential/support 证据。row0 back 的 Fast ground helper 为 +0.5，实际有限地面可见交换为0。

正确数学对象是有限表面之间、双方相向且无遮挡射线的非负余弦加权测度。乘接收面长度后满足交换对称。端点名称和 tilt 不负责选择正负号。先显式判断 side/visibility，再在有效射线上计算大小。Sky 保留既有残差开放边界源语义，不是参与互易性的有限面。建议 Fast ground/PV 组由同一有限几何交换按长度聚合；Fast irradiance 仍为独立近似模型。

受影响字段：几何 F 的 PV→ground、ground→PV、residual sky，以及 Fast back-ground 聚合字段。本扫描未发现显著 PV→PV 或 Fast back→PV 偏差。本任务没有实现或验证 AOI G、irradiance、solver、Full/Fast 公共结果字段及生产 API。

## 兼容性与候选边界

推荐依 CDR-008 修正物理 F，保留 raw Reference 作为溯源/诊断，不把其负 F 作为合法物理结果。这会有意偏离冻结 Reference 的已识别 case。Fast 有限聚合也会改变部分其他合法输入下的 Reference Fast 数值，因此 Owner 必须明确批准兼容性影响，不能将其当成无行为变化的内部重构。

Geometry 坐标、finite extent、SurfaceKey、ReferenceIndex、active slot、normal、[0°,180°] 输入域及 front/back 身份保持不变。不需要修改 P3。拒绝整个矩阵取 abs/clamp；较窄的 helper abs 补丁虽符合当前样本，仍未证明适用于完整域。独立实现应遵循可见域语义，不逐行翻译 Python。

`reference/candidate/vf-lcb01-v0.1/manifest.json` 包含66 case/198 artifacts，以及独立的 proposed comparator profile。raw/normalized 保留，corrected 矩阵和 Fast 组提供字段级 DEV/CDR/独立 oracle provenance。这是 LCB-01 定向候选，不是完整 P4/AOI 验收集。没有晋升 candidate；Geometry Golden/tolerance 继续冻结。

回归包括 VF053（批准 TILT_180）、VF035（TILT120）、VF020（TILT90）、VF045 对照 VF063（near180切分敏感性）、VF062/VF063（两种方位）、VF064/VF065，N1/2/3/11，cut1/2/4，有/无遮挡地面，相邻PV，边排/中间排及阴影/受光地面。Synthetic 可见性/挡板样例用于独立 oracle 验证，不伪装为已批准 Geometry fixture。

## 证据与 Owner 动作

[调查报告](LCB-01_VF_INVESTIGATION_REPORT.zh-CN.md) 索引最小反例、first divergence 中间量、66-case扫描、有向分类、Decimal/线积分/双重积分、Fast差异、raw可复现性及候选哈希。无 Reference helper 的 oracle 判断可见性；独立反向/镜像/端点顺序测试补充由构造生成的 reciprocity/closure。不变量 harness 拒绝负值、>1、互易但为负、闭合但含非法项四种 mutation。

需要 Owner 集中答复：批准/修改/拒绝 DEV-028 与 CDR-008，并明确是否将 corrected Fast 组定义为有限 F 聚合。默认推荐：**批准统一有限物理语义**，审阅并批准准确 candidate manifest/profile 作为具名研究验收子集，再恢复剩余 P4–P7 closure preparation。此批准不启动实现、不决定发布。在答复前，DEV-028 未批准，LCB-01 仍是 launch blocker。
