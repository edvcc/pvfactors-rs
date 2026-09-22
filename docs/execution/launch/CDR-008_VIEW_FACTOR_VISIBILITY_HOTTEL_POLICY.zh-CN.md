# CDR-008 — View Factor 非负性、可见性及 Hottel 方向政策

状态：**PROPOSED — AWAITING OWNER REVIEW**。日期：2026-09-22。关联 DEV-028、LCB-01；保持 CDR-003/006 Geometry 合同。本提案不直接重写 M06/M09 或批准的 P3；批准后应先形成可追溯的规格补充，再进入生产实现。

## 请求决策

对完整批准 tilt [0°,180°] 域，在原有有限 Geometry 上，以实际法向和可见射线定义几何 F。采用不依赖端点命名方向的统一交换定义，不做角度特判。要求 corrected Fast 几何组聚合同一有限交换；保留 raw Reference，仅按准确 manifest 批准 corrected expectation，并保留 Reference differential 之外的独立验证。

默认推荐：**采用本政策，包含 Fast 有限聚合**。可选路径：(a) 仅将 raw Reference 保留为具名诊断兼容结果，不能冒充物理 F；(b) 延迟批准，保持 launch blocked，继续补充同一数学政策。拒绝收窄批准输入域、front/back交换、负值置零、global abs 或放宽容差容纳非物理值。小范围 helper abs 补丁不是普遍证明，也不能修复 Fast 的正值错误。

## 数学定义

设接收线段 i、源线段 j，p∈i、q∈j、r=q−p，Li>0，实际单位法向 ni/nj。当且仅当 `ni·r>0`、`nj·(−r)>0`，且开放连接线段不穿过其他不透明 PV 排的内部，定义 V(p,q)=1，否则为0。同一排的 front/back 是一个不透明线段的两个具名面，不是两块挡板。地面法向向上。self、同排、批准平行排几何中的同朝向面及 ground-ground 交换为0。相邻排捷径必须有几何证明，不能用来定义可见性。

```text
Eij = ∫i ∫j V(p,q) (ni·r)(−nj·r) / (2 |r|³) dsq dsp
Fij = Eij / Li
Eij = Eji; Fij >= 0
```

该核由三维漫射核沿排轴积分得到：`∫ dz/(r²+z²)² = π/(2 r³)`。接收半平面的完整角度测度归一化为1，因此任何有限可见源的 F≤1。这是物理定义，不是数值 clamp。假设仍是批准的沿轴无限、opaque、直线二维排，没有引入新三维模型。

仅有效射线贡献交换。朝反方向或被遮挡的表面，即使 Hottel 裸大小为正，也没有物理支持。>90° 保留实际 front/back 身份，包含180°的front朝下/back朝上。Tilt、`tilted_to_left`、`shadow_is_left`、high/low命名或原始负号，都不能替代法向和射线判断。

## 无遮挡交换

对整体相向、全部互相可见的直线段，端点为a/b与c/d：

```text
Fij = abs(|a-d| + |b-c| - |a-c| - |b-d|) / (2 Li)
```

这里的绝对值在确认物理支持后消除任意端点参数方向，不是 `abs(F_reference)`。反转任意一段的端点枚举，结果不变。若只部分可见，应先划分可见积分域，不能对隐藏区域与可见区域消减后的总和直接取大小。

## 遮挡交换与有效端点/字符串

对每个接收点 p，先取满足双方外向半平面的源区间，再减去不透明排遮挡的区间。穿过 blocker 端点的射线与源直线相交，形成可见区间端点。以线段相交确定可见性，不以字符串和的正负确定。源可见区间可能随 p 变化，不能普遍用一个固定裁剪后的源线段代替。

在投影端点顺序或可见性变化事件处分割接收段：包括与 source/blocker 端点对连线的交点及半平面边界。每个开放单元内，可见角区间由固定顶点（源端点或遮挡轮廓端点）界定。应由这些端点射线确定 crossed strings 的方向，而不是名义 high/low。考虑全部不透明排；只可剔除已证明不相关的排。

设可见区间边界单位射线为uA/uB，切向 `R ni = (−ni_y, ni_x)`，则点到区间的因子为：

```text
dFi(p) = 1/2 * abs((R ni) · (uB-uA))
```

它来自接收半平面内对 cos(theta)/2 的角积分；按有效角度顺序，其贡献非负。沿接收段积分并除以 Li，即本候选采用的独立数值路径。

也允许精确端点字符串路径。对单元 p(s)=p0+s*t 和固定边界顶点v，有 `d|p-v|/ds = -t·u_v`。因此每条角边界项的积分，等于从**单元端点**到**实际边界顶点**的距离差。按有效角度方向组合字符串项，得到非负单元交换，再求和。位于接收视域边界的射线方向恒定，其原函数为线性项。这是有效遮挡字符串的推导，不是把名义四端点公式无条件套到部分遮挡 pair。任何捷径/绕行表达式都必须证明与上述可见测度相等，包括端点排序和遮挡端点选择。

一次计算 Eij，反向用 `Fji=Eij/Lj`；独立反向积分仍作为验证。数值求积或稳健闭式公式可作为实现选择，前提是在批准 oracle 上证明精度。本次只构造研究 oracle，没有选定生产算法或性能方案。

## 退化、精确结构与边界源

- 保持 Geometry activity、坐标、长度、key、index、normal。余弦计算可把非零法向单位化，不能改变方向或身份；候选对 raw null 的 ground 明确使用向上法向。
- inactive/zero-length 的行列为零，不做除零；不得为了构造 VF 重新激活 slot。
- 共线的 self/同排/地面对贡献零。孤立切触和仅端点接触的角测度为零；共线 grazing 为零；接触配置按有效测度极限处理，不产生奇异0/0。批准的正离地间隙避免穿地；任意相交拓扑不在合同内。
- Topology、SurfaceKey、ReferenceIndex、可见性分类不能借 acceptance epsilon 变成“近似相等”。可用稳健/自适应 predicate 消除算术不确定性，但不能扩大可见域。若批准 Geometry 本身无法定义合法物理域，必须另报冲突，不得修改。
- physical row 保留 `F_i,sky=1−sum(physical F_i,*)`；sky row 为零，不参与长度互易。有限 ground 下，它是开放边界残差，即使接收面朝下，也包含逃逸到地面范围外的份额。本提案不把它静默改成仅天文上半球。检查非负与闭合，不能 clamp 非法残差。

## Full/Fast 兼容性与 API

Full F 使用上述定义。建议 Fast ground/PV/shaded/illuminated 几何组聚合同一有限交换；多个接收子段按长度加权。若能证明等价，也可直接计算组值。这会替代不符合有限域的最低端点代理和越域边段，不会把 Fast 的单次反射近似变为 Full solve，也不会自动关闭 CDR-007。

公共 Geometry API、身份不变；F维度、receiver/source轴、inactive slot、边界残差不变。DEV-028 case 和有限 Fast 组数值会有意改变，必须保留字段级偏差。AOI G 是独立算子，本 CDR 不对其套用几何 F 的[0,1]规则。不得声称全部 P4/P5/P6/P7 fixtures 或公共结果 availability 决策因此获批。

## Expected、容差与验收

raw/normalized Reference 为不可变证据。Owner 批准本决策、DEV-028、准确manifest和comparator后，corrected 才能进入 approved oracle。Rust输出不能生成自身expected。candidate不自动晋升。

LCB-01候选含66case/198artifacts。bounds、closure/长度互易暂拟1e−10，expected绝对比较2e−9。这是按请求求积精度建立的研究数值余量，不是算法阈值，也不改变 `geometry-tolerance-v0.1`。已观测独立误差更小，但不构成所有平台的证明。以后以生产验收预算替换研究预算，需要证据和明确批准，不能在实现失败时静默修改。

必须验证：所有active physical及residual项边界、精确support规则、仅对active接收面检查closure、physical长度互易、独立Hottel/线积分/双重积分、遮挡/完整域镜像/端点反转、Geometry不变、准确case inventory和generator/manifest完整性。Reciprocity/closure不足以证明正确，尤其不能把由构造生成的性质当成独立证据。Mutation必须抓住负值、>1、互易但为负、闭合但含非法项。缺少artifact/case或生产测试不能让milestone通过。

## Owner 关闭记录

集中审阅[调查报告](LCB-01_VF_INVESTIGATION_REPORT.zh-CN.md)、[DEV-028](DEV-028_VIEW_FACTOR_ORIENTATION_CANDIDATE.zh-CN.md)、`reference/candidate/vf-lcb01-v0.1/manifest.json`、proposed profile及 `evidence/execution/launch-closure/lcb-01/candidate-index.json`。需要答复：批准/修改/拒绝统一物理政策；明确接受/拒绝Fast有限聚合；指定批准manifest/profile哈希或要求替换证据。由Owner记录批准，不从本推荐或测试PASS推定。

此前状态保持 **PROPOSED — AWAITING OWNER REVIEW**；LCB-01可供决策，但launch仍开放，全项目closure仍BLOCKED。Owner关闭后，依据有效授权恢复剩余P4–P7研究/oracle准备。生产启动是另一个决定。本调查结束，不执行未来实现任务。
