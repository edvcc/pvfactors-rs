# DEV-028 — View Factor 端点方向 / Signed-Hottel Reference 缺陷

状态：**APPROVED**。Owner 决策：2026-09-22，[Owner 记录](LCB-01_OWNER_DECISIONS.zh-CN.md)中的 OD-LCB01-01 至 OD-LCB01-05。本记录**只覆盖 Full 几何 F**；Fast 有限地面行为单独归入 [DEV-029](DEV-029_FAST_FINITE_GROUND_AGGREGATION.zh-CN.md)。

## 已确认 Reference 缺陷

冻结 pvlib/solarfactors v1.6.1、commit `ecbfc863657e239817603a43898ae173c7ccad9c` 的 `_vf_hottel_gnd_surf` 使用带符号 crossed-minus-uncrossed 表达式。其 high/low 端点构造隐含方向假设，切分及 binary64 等高 tie/reversal 会使该假设失效。由此产生的负有限物理交换是已确认兼容性缺陷，Rust V1 不得复制。

批准 TILT_180 的 receiver ReferenceIndex3/source28，Reference 为 −0.2038204263767998；独立 Decimal90 为 +0.2038204263767998815712607034…，线积分为 +0.20382042637679987。两面物理相向且无遮挡。Geometry 正确且保持不变。

## 影响域与字段

66-case 调查发现8个 Full 失败case、922个偏差字段：408 PV→ground、408 ground→PV、70 ground→residual-sky、36 PV→residual-sky。408个负 PV→ground helper 均有精确等高端点。Exact180、180−1 ULP 随方位、切分和排数而失败（N2/3/11、cut1/2/4）。不能定义成仅exact180，也不能泛化为所有tilt>90。一般触发条件是 Geometry 仍合法而 VF 端点顺序假设失效；有限覆盖集不是连续域穷举证明。

受影响字段为 Full 有限物理 F 及互易/残差后果。本扫描未发现显著 PV→PV 偏差。Fast 的53case/139字段**不归 DEV-028 管理**。

## 已批准 corrected 行为

CDR-008 规定 semantic surface identity/outward normal 和物理 line-of-sight 为权威。交换量有限、非负且有界；Hottel 是确认有效support后的解析实现。端点顺序只是局部计算构造，不定义身份、可见性或物理符号；部分遮挡须先确定可见域。Reciprocity/closure 仍必须成立，但不足以证明合法性。

P3 Geometry model、finite extent、coordinates、SurfaceKey、ReferenceIndex、ActiveIndex、activity、normals、front/back identity、Approved Geometry Golden、geometry-tolerance-v0.1 全部不变。禁止 >90 folding、side exchange、为适配Reference重排Geometry端点、global matrix abs、clamp非法值或放宽容差。

## 兼容性、oracle 与 provenance

Corrected physical F 有意偏离有缺陷的Reference。保留全部raw/normalized；corrected matrix字段引用DEV-028/CDR-008，Fast corrected字段改引DEV-029。既有66case/198artifact继续保留在 `reference/candidate/vf-lcb01-v0.1/` 以保持路径稳定，状态为 **APPROVED_TARGETED_ORACLE_SEED**。仅批准LCB-01定向corrected VF子集/P4 seed，不等于完整VF/P4 Golden或AOI覆盖。准确manifest/profile哈希由 `LCB-01_OWNER_DECISIONS.json` 绑定。

回归包括VF053、VF052/054/055、两种方位near180的VF062/063、VF064/065，以及90/120/near180通过对照。保留独立解析、角度/线积分、tensor证据及negative/reciprocal/closed-invalid mutation。[调查报告](LCB-01_VF_INVESTIGATION_REPORT.zh-CN.md)属于历史科学证据；当前验证权威是[关闭交接说明](LCB-01_CLOSURE_HANDOFF.zh-CN.md)所指向的远端提交凭证。

本批准只关闭这项语义决策。生产数值算法尚未冻结，P4–P7及完整实现均未验收或启动。
