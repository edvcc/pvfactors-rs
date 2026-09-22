# Full-Project Launch Closure：停点报告

**2026-09-22 更新：** 已按后续授权完成 LCB-01 调查，可供 Owner 决策，见[当前调查报告](LCB-01_VF_INVESTIGATION_REPORT.zh-CN.md)。DEV-028/CDR-008 及66-case corrected candidate仍未批准，全项目closure仍BLOCKED。以下原停点报告保留为历史checkpoint；其中“等待调查授权”和“VF候选为零”的状态由本更新替代。

**FULL-PROJECT LAUNCH CLOSURE — BLOCKED**。本次不是完整 Launch Review 的交付成功；这是任务第40条触发后的可恢复 checkpoint。没有批准任何决定或Oracle，也没有开始生产实现。

## 必须先处理的 LCB-01

已批准 Geometry 的 `TILT_180` 输入（3排、宽/高1m、gcr0.5、z45°、太阳/面方位270°）在冻结Reference中给出负的几何F。接收面 ReferenceIndex3、源面28：Reference `-0.2038204263767998`；独立80位Decimal无遮挡Hottel诊断为 `+0.20382042637679988157…`。该case共有36个active项违反[0,1]，包括sky>1。两次R0捕获逐字节相同，surface记录与已批准Geometry payload完全一致。row closure与reciprocity仍接近零，说明仅检查这两项会漏检。

这不是Geometry输入非法、inactive槽、G吸收近似或微小舍入差异。当前CDR没有覆盖此VF缺陷；不能把Reference负值作为expected，也不能abs/clip矩阵、放宽tolerance或偷偷收窄已批准[0,180]域。[最小证据](../../../evidence/execution/launch-closure/NEW_LAUNCH_BLOCKER_LCB-01.json) · [完整矩阵](../../../evidence/execution/launch-closure/vf-domain-probe.json)。

默认推荐：明确授权新增具名VF deviation/CDR候选调查，在保留已批准Geometry数据、域、SurfaceKey与front/back身份的前提下，研究端点/可见性边界并建立独立corrected oracle。只请求恢复closure研究，不请求生产实现授权。尚未擅自编号为正式DEV/CDR或生成修正expected。

## 已保存的有效进展

- R0已恢复，environment_id准确匹配`031158a1d1be8cdb9093`，依赖未改。
- 隔离栈PyO3 0.29.2 / rust-numpy 0.29.0 / maturin 1.15.0，独立Cargo.lock；四平台×CPython3.11–3.14共16个CI job全部成功，32份NumPy测试报告、544个ownership/import检查。
- NumPy最低2.3.4；上端样本3.11为2.4.6，3.12–3.14为2.5.3。最低OS只标TARGET / NOT YET VERIFIED，生产binding未实现。
- Grazing每环境413项，4个平台/16个CI配置的最大样本误差5.551115123125783e-16；候选delta=64eps有条件传播界与80位高精度证据支撑，尚未获批。441项区间真值表、190项horizon几何检查通过，但OD-05完整Reference对照未完成。
- master/develop仍未保护，ruleset为空，当前身份admin/push；未修改规则或权限。

CI：[实际成功run](https://github.com/edvcc/pvfactors-rs/actions/runs/35684741799)。准确环境、报告与wheel哈希见ENVIRONMENT_LAUNCH_STATUS.json及证据目录。

## 集中决策检查点（均未批准）

| Decision | Recommended choice | Evidence status | Impact | Owner action |
|---|---|---|---|---|
| OD-01 | 正长度区间残余：扣除正长度重叠，返回有序的正长度残余连通分量闭包；点被减项为空，减点或端点相接不移除长度；不是严格集合差。 | READY_FOR_OWNER_APPROVAL | CDR-006 | 未批准；LCB-01后恢复完整闭环 |
| OD-02 | 先做几何/shape/有限性/非负校验：z>=90且全部源为零，z=90返回HorizonZero，z>90返回NightZero；任何非零源默认UnsupportedNoDirectDiffuse。只有显式ZeroAtOrBelowHorizon才丢弃源并返回具名零状态。z<90全零返回ZeroIrradiance；DNI=DHI=0且GHI>0返回ContradictoryIrradiance。DiffuseOnlyNoDirect留给未来model revision。 | READY_FOR_OWNER_APPROVAL | CDR-001 | 未批准；LCB-01后恢复完整闭环 |
| OD-03 | 单次计算并裁剪mu，mu>delta为front，mu<-delta为back，其余为grazing；delta=64*f64::EPSILON=1.4210854715202004e-14。法向反转使用-mu，不递归重算。误差界依赖归一角域、普通浮点运算及trig<=2ulp假设；16个CI配置已实测。grazing仅使direct/circumsolar投影归零，保留isotropic/horizon。 | READY_FOR_OWNER_APPROVAL | CDR-002 | 未批准；LCB-01后恢复完整闭环 |
| OD-04 | 采用incident形式qinc=E+FRqinc、B=I-FR、q0=Rqinc；已知sky移到b。不显式inverse；有限rho/albedo∈[0,1]且0合法。F/G分离，Gground=(1-albedo)Fground。原B,b算residual，高条件数需独立前向证据或NumericalFailure。backend/version/layout后定。LCB-01的几何F缺陷不能静默归入现有吸收/solver修正。 | READY_FOR_OWNER_APPROVAL | CDR-004 | 未批准；LCB-01后恢复完整闭环 |
| OD-05 | 暂拟HybridPerezTwoSidedExplicitBand-v1：按接收面水平法向选邻排，最高端点与接收面质心定义max(0,atan2(dy,abs(dx)))；h=min(1,theta/band)，H=abs(P_horizon)*(1-h)。band须显式给定且有限、在(0,90]；不宣称6.5度默认值有物理标定依据。几何/mirror探针通过，Reference对照与完整源项oracle因LCB-01停点尚未完成。 | EVIDENCE_REQUIRED_BEFORE_APPROVAL | CDR-005 | 未批准；LCB-01后恢复完整闭环 |
| OD-06 | Fast Isotropic采用Pps=Piso-(1-tau)*Dfront；tau=0/.5/1分别为Piso-Dfront、Piso-.5Dfront、Piso。目标修正rho_front*F_target,front_shaded*tau*Dfront在rho=0、无邻排、无可见阴影时为0。Full/Fast保持不同；完整edge/segment Reference fixtures尚未生成。 | READY_FOR_OWNER_APPROVAL | CDR-007 | 未批准；LCB-01后恢复完整闭环 |
| OD-07 | 保留Full q0/qinc/qabs、Fast q0/qabs unavailable、keyed ragged trace、标量广播/T=0/原始非单调顺序/dayofyear1..366。AOI成对配置、table覆盖0/180、knot严格递增、线性插值；SAPM B0..B5。不提供Python运行时callback；detach前复制owned输入，输出独立拥有内存。公共cancellation token不属于V1冻结要求，内部可选取消不改变物理模型。 | READY_FOR_OWNER_APPROVAL | Execution/API/platform | 未批准；LCB-01后恢复完整闭环 |
| OD-08 | 在完整实现前一次预批准P4-P7的准确oracle manifests/profiles。因LCB-01阻塞，目前没有完整候选包，更没有晋升。不得静默换回长任务内逐包批准路线。 | EVIDENCE_REQUIRED_BEFORE_APPROVAL | Execution/API/platform | 未批准；LCB-01后恢复完整闭环 |
| OD-09 | Rust四目标；普通GIL CPython3.11-3.14按解释器wheel；候选NumPy>=2.3.4,<3。隔离栈锁定PyO3 .29.2、rust-numpy .29.0、maturin1.15.0；CI实测NumPy2.3.4，以及3.11上的2.4.6 /3.12-3.14上的2.5.3。最低OS仍作为release gate，现代runner通过不等于已验证下限。排除PyPy/free-threaded/abi3/universal2/musllinux/Linux或WindowsARM/WASM分发。 | READY_FOR_OWNER_APPROVAL | Execution/API/platform | 未批准；LCB-01后恢复完整闭环 |
| OD-10 | 终点为V1 IMPLEMENTATION COMPLETE + RELEASE CANDIDATE READY FOR OWNER ACCEPTANCE。另行启动后才授权具名实现分支修改/commit/push/CI/依赖评估/普通修复/自动推进；不授权master merge/tag/release/publish/SemVer1.0.0。当前closure停点，实施任务未激活。 | READY_FOR_OWNER_APPROVAL | Execution/API/platform | 未批准；LCB-01后恢复完整闭环 |
| OD-11 | master/develop需PR-only、禁止force-push/删除、要求真实CI；master另需人类review、解决conversation、过期review失效与最新commit批准。Agent不得admin/bypass/release。使用独立非admin身份、受保护refs和明确凭据能力限制；普通contents-write本身不能排除merge/tag。否则签署具名且有期限的治理风险接受。本次未改规则。 | GOVERNANCE_ACTION_REQUIRED | Execution/API/platform | 未批准；LCB-01后恢复完整闭环 |
| OD-12 | 保留有界资源和隔离benchmark协议。必须覆盖足够宽workload；实测存在crossover时需学习并在holdout正确选择，足够宽证据证明不存在时Serial fallback合法。未实现cost estimator而总选Serial不合法。median<=1.10*best+2ms、p95<=1.25*best+5ms为M11/M12前凭证据冻结的候选预算，不是不可修订物理语义。 | MILESTONE_DEFERRED_IMPLEMENTATION_CHOICE | Execution/API/platform | 未批准；LCB-01后恢复完整闭环 |

8项具有政策候选，2项仍需证据（其中OD-08受LCB-01直接阻塞），1项需治理动作，1项为里程碑延后选择。此分类不表示12项完整approval package已经完成。BF-01只有解析证据与候选语义；BF-02只有按任务修正的政策候选；其正式补充、corrected fixtures及完整批准对象尚未完成。

P4–P7候选manifest均未生成（0 case/0 artifact）；Geometry既有批准不变。Comparator扩展、全量policy同步、统一activation实现均未进行。旧任务书保持PREPARED / INACTIVE，恢复后必须按本次OD-02/07/12方向同步修订，再供完整Review。本次STOP优先于机械补齐缺失文件。

分支research/full-project-launch-closure；base2347b1d16c9c18b795182714a3925db7e1dda53c。Final SHA以Git HEAD为准；证据记录各自测试SHA。下一步只需要决定是否授权上述新VF偏差调查；当前不能做完整Launch Approval。

## Checkpoint verification

干净被测checkpoint `905792533459170104946a43e803a75e5967cd92`：assets PASS；既有加新增门禁测试50/50 PASS；preflight NOT_READY/exit2，其中R0 PASS，Owner批准与LCB-01未关闭。详见 `../../../evidence/execution/launch-closure/verification-summary.json`。验证工具只增加LCB门禁，没有把未实现的完整closure inventory/comparator当成PASS。
