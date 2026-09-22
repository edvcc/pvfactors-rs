# DEV-029 — Fast 有限地面代理 / 有限域聚合兼容性偏差

状态：**APPROVED**。Owner决策：2026-09-22，OD-LCB01-06。关联CDR-008、DEV-004有限地面背景；与DEV-028的Full signed-Hottel缺陷分开管理。

## Reference 行为、根因与域

冻结solarfactors `ecbfc863657e239817603a43898ae173c7ccad9c` 的 `calculate_vf_to_gnd` 使用边排地面段和中间排最低端点代理。边排代理可能越出有限地面[−100,100]、端点反转并发生严重数值消减；中间排代理可能包含有限域外的交换。大小为正不能证明物理正确。

tilt180、VF053 row0 back 的 Reference back_ground=0.5，而实际朝上背面的有限地面交换为0。另有near180边排正值消减残差。覆盖集中53case/139个Fast地面字段存在差异，分布于0/45/90/100/120/150/179/179.9/near180及exact180配置，明显宽于Full的8个失败case。这是有限扫描，不是对所有尺寸/排距的普遍界。本扫描未发现显著back→PV聚合偏差。

## 已批准几何政策与兼容性影响

Fast ground/PV几何组聚合CDR-008定义的**同一有限物理交换**。多个接收segment按 `sum(Li * Fi,group) / sum(Li)` 聚合；只有证明等价后才可直接计算group。保留原有限Geometry与身份，不能用越域proxy、端点反转或消减残差定义物理组。Adaptive Planner不得改变underlying physical geometry。

修正会有意改变部分Reference Fast数值，包括原本为正及Full F已经通过的case。这是已批准几何兼容性偏差，不是容差调整。Corrected Fast provenance引用DEV-029/CDR-008；raw `back_ground`、`back_pv`、`back_shaded_pv` 仍保留为Reference观测。Seed独立提供ground及total PV group期望，不是完整Fast shaded-source/irradiance覆盖。

## 批准边界与证据

Fast irradiance、Fast simulation仍是独立近似模型。**不因此关闭CDR-007，不宣称Fast==Full，不批准全部Fast语义，不完成P4/P5/P6/P7。** AOI G仍为独立operator；生产数值算法仍可在批准语义内选择。

批准的targeted seed为 `reference/candidate/vf-lcb01-v0.1/`（66case/198artifact）。Corrected中的 `fast_group_candidate` 沿用历史schema字段名，但已承载Owner批准的几何期望；文件/字段名不代表审批状态。准确manifest及targeted comparator由 `LCB-01_OWNER_DECISIONS.json` 绑定，production跨平台容差未冻结。验证须重算有限聚合、比较重新生成的独立期望、保留raw字段，不能只检查F边界。

证据为 `fast-helper-comparison.json`、`global-abs-counterexamples.json`、单独的Full有向分类及本次重跑closure receipts。[Owner记录](LCB-01_OWNER_DECISIONS.zh-CN.md)为批准依据，[关闭交接说明](LCB-01_CLOSURE_HANDOFF.zh-CN.md)指向当前验证凭证。Geometry/frozen source保持不变，本记录不授权生产实现。
