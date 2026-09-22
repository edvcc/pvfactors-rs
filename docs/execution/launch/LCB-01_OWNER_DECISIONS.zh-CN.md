# LCB-01 Owner 决策记录

日期：2026-09-22。依据 Repository Owner 明确提供的 **Owner Decision Propagation + Evidence Provenance Repair Task v1.0**，原文保留于 `evidence/execution/launch-closure/lcb-01/owner-decision/source-request.txt` 并计算哈希。这是Owner决定，不是Agent建议或推定批准。[LCB-01_OWNER_DECISIONS.json](LCB-01_OWNER_DECISIONS.json)保存机器可读权威记录和准确批准对象哈希。

| 决策 | 已批准政策 |
|---|---|
| OD-LCB01-01 | Full端点方向/signed-Hottel Reference行为为已确认兼容性缺陷，Rust V1不复制；DEV-028只覆盖此项。 |
| OD-LCB01-02 | P3 Geometry、coordinates、finite extent、SurfaceKey、ReferenceIndex、ActiveIndex、front/back身份、Approved Geometry Golden、Geometry tolerance不变。 |
| OD-LCB01-03 | Semantic identity/outward normal、物理line-of-sight、非负有限交换为权威；Hottel只是解析实现，端点顺序只是局部构造。 |
| OD-LCB01-04 | 适用active physical/residual F须在[0,1]；reciprocity/closure必要但不充分，保留非法矩阵mutation。 |
| OD-LCB01-05 | 禁止global matrix abs、clamp非法F、tilt folding、side swap、为适配Reference改变Geometry，以及放宽容差吸收非物理值。 |
| OD-LCB01-06 | Fast几何组按接收长度聚合同一有限交换，或使用已证明等价的直接计算；DEV-029独立覆盖。Fast simulation保持独立，CDR-007未关闭。 |

[DEV-028](DEV-028_VIEW_FACTOR_ENDPOINT_ORIENTATION_DEFECT.zh-CN.md)、[DEV-029](DEV-029_FAST_FINITE_GROUND_AGGREGATION.zh-CN.md)、[CDR-008](CDR-008_VIEW_FACTOR_VISIBILITY_HOTTEL_POLICY.zh-CN.md)均为 **APPROVED**。生产数值算法未冻结；本批准不启动实现、不验收P4，也不批准其他项目决定。

既有corpus仅批准为 **LCB-01 Targeted Corrected VF Oracle Subset / P4 Oracle Seed**：66case/198artifact，覆盖几何F及finite Fast几何组。路径继续为 `reference/candidate/vf-lcb01-v0.1/`，目录名不能覆盖明确的targeted批准状态。Raw/normalized字节、科学数值及Geometry payload保持不变，只更新状态/provenance元数据和必要verifier绑定。Full matrix修正引用DEV-028，Fast引用DEV-029，两者都引用CDR-008。

Comparator为 **APPROVED FOR LCB-01 TARGETED ORACLE SEED**、**NOT YET FINAL P4 CROSS-PLATFORM TOLERANCE**。原预算不变：bounds1e−10、expected_abs2e−9、长度互易1e−10、closure1e−10。后续P4正式容差仍需独立证据与批准，不能因实现失败静默调大；AOI G仍是独立operator。

LCB-01关闭须在clean真实commit重新验证，并保证content/receipt两个commit均可远端解析。旧 `8b0208b4ae471bf81d70e4358e8cdc22a38e0384` 凭证仅作历史证据；本次GitHub返回HTTP422。初始远端 `3d854a564afd44b6f50f860454c37582f1ad5302` 可正常解析。见初始远端审计及[关闭交接说明](LCB-01_CLOSURE_HANDOFF.zh-CN.md)。

原OD-01..OD-12、其他CDR、完整P4–P7 oracle包及平台/治理决定不因此获批。LCB-01最终状态从verification receipt读取，不重复硬编码多个状态副本。本任务在传播、修复、验证及push后停止。
