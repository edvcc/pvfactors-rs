# CDR-008 — View Factor 非负性、可见性及 Hottel 方向政策

状态：**APPROVED**。Owner决策2026-09-22，OD-LCB01-01..06，见[Owner记录](LCB-01_OWNER_DECISIONS.zh-CN.md)。DEV-028覆盖Full缺陷，DEV-029独立覆盖Fast有限聚合。本批准补充规定VF/Fast几何语义，不修改冻结P3/Geometry文档。生产数值算法尚未冻结。

Semantic side/outward normal、line-of-sight为权威，Hottel只是解析实现；在批准tilt域采用非负有限物理交换。禁止global matrix abs、clamp、folding、side swap、为适配Reference修改Geometry或放宽容差。

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
- physical row 保留 `F_i,sky=1−sum(physical F_i,*)`；sky row 为零，不参与长度互易。有限 ground 下，它是开放边界残差，即使接收面朝下，也包含逃逸到地面范围外的份额。本决策不把它静默改成仅天文上半球。检查非负与闭合，不能 clamp 非法残差。

## Full/Fast 兼容性与 API

Full F 使用上述定义。批准 Fast ground/PV/shaded/illuminated 几何组聚合同一有限交换；多个接收子段按长度加权。若能证明等价，也可直接计算组值。这会替代不符合有限域的最低端点代理和越域边段，不会把 Fast 的单次反射近似变为 Full solve，也不会自动关闭 CDR-007。

公共 Geometry API、身份不变；F维度、receiver/source轴、inactive slot、边界残差不变。DEV-028 Full case 和 DEV-029 有限 Fast 组数值会有意改变，必须保留字段级偏差。AOI G 是独立算子，本 CDR 不对其套用几何 F 的[0,1]规则。不得声称全部 P4/P5/P6/P7 fixtures 或公共结果 availability 决策因此获批。

## 批准 seed 与验证边界

既有66case/198artifact仅批准为 **APPROVED_TARGETED_ORACLE_SEED**：LCB-01 corrected几何F及finite Fast组，不是完整P4/VF Golden或AOI覆盖。批准不改变物理数值payload。raw/normalized Reference保留；matrix provenance引用DEV-028/CDR-008，Fast引用DEV-029/CDR-008。准确对象哈希见LCB-01_OWNER_DECISIONS.json。

Comparator状态为 **APPROVED FOR LCB-01 TARGETED ORACLE SEED**；**NOT YET FINAL P4 CROSS-PLATFORM TOLERANCE**。bounds epsilon1e-10、expected_abs2e-9、长度互易1e-10、closure1e-10保持原targeted验收预算，Geometry tolerance不变。P4正式容差须独立证据与明确批准，不能为通过实现测试静默放宽。

保留bounds、support、reciprocity、closure、高精度解析、独立角度/线积分、tensor收敛、遮挡、wrong-side/fully-blocked zero、mirror、端点反转及独立反向验证。Candidate verifier须比较全新重建结果并重算Fast有限聚合；negative-but-reciprocal、closure-pass-invalid及>1 mutation继续必需。

本批准不关闭CDR-007，不使Fast==Full，不冻结生产数值算法，不完成P4–P7或启动实现。[关闭交接说明](LCB-01_CLOSURE_HANDOFF.zh-CN.md)及对应verification receipt决定LCB-01是否CLOSED，否则仍为closure blocked。
