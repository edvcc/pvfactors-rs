# Full-Project Launch Closure — 当前交接

完整实现保持 **INACTIVE**，全项目启动尚未就绪。Owner已批准DEV-028（Full）、DEV-029（Fast几何）、CDR-008和66-case定向oracle seed，以[Owner记录](LCB-01_OWNER_DECISIONS.zh-CN.md)为准。LCB-01关闭及研究恢复授权由[验证凭证](../../../evidence/execution/launch-closure/lcb-01/verification-summary.json)计算，见[交接说明](LCB-01_CLOSURE_HANDOFF.zh-CN.md)。本次不继续P4-P7。

原停点报告及local-only验证陈述保存在Git历史3d854a564afd44b6f50f860454c37582f1ad5302。另一33-case调查的范围已由66-case证据补足，“仅exact180”不再是政策。既有R0/平台研究仍只是证据，不构成启动批准。

## 集中决策检查点（均未批准）

| Decision | Recommended choice | Evidence status | Impact | Owner action |
|---|---|---|---|---|
| OD-01 | 正长度区间残余：扣除正长度重叠，返回有序的正长度残余连通分量闭包；点被减项为空，减点或端点相接不移除长度；不是严格集合差。 | READY_FOR_OWNER_APPROVAL | CDR-006 | 未批准；后续closure任务继续 |
| OD-02 | 先做几何/shape/有限性/非负校验：z>=90且全部源为零，z=90返回HorizonZero，z>90返回NightZero；任何非零源默认UnsupportedNoDirectDiffuse。只有显式ZeroAtOrBelowHorizon才丢弃源并返回具名零状态。z<90全零返回ZeroIrradiance；DNI=DHI=0且GHI>0返回ContradictoryIrradiance。DiffuseOnlyNoDirect留给未来model revision。 | READY_FOR_OWNER_APPROVAL | CDR-001 | 未批准；后续closure任务继续 |
| OD-03 | 单次计算并裁剪mu，mu>delta为front，mu<-delta为back，其余为grazing；delta=64*f64::EPSILON=1.4210854715202004e-14。法向反转使用-mu，不递归重算。误差界依赖归一角域、普通浮点运算及trig<=2ulp假设；16个CI配置已实测。grazing仅使direct/circumsolar投影归零，保留isotropic/horizon。 | READY_FOR_OWNER_APPROVAL | CDR-002 | 未批准；后续closure任务继续 |
| OD-04 | 采用incident形式qinc=E+FRqinc、B=I-FR、q0=Rqinc；已知sky移到b。不显式inverse；有限rho/albedo∈[0,1]且0合法。F/G分离，Gground=(1-albedo)Fground。原B,b算residual，高条件数需独立前向证据或NumericalFailure。backend/version/layout后定。LCB-01的几何F缺陷不能静默归入现有吸收/solver修正。 | READY_FOR_OWNER_APPROVAL | CDR-004 | 未批准；后续closure任务继续 |
| OD-05 | 暂拟HybridPerezTwoSidedExplicitBand-v1：按接收面水平法向选邻排，最高端点与接收面质心定义max(0,atan2(dy,abs(dx)))；h=min(1,theta/band)，H=abs(P_horizon)*(1-h)。band须显式给定且有限、在(0,90]；不宣称6.5度默认值有物理标定依据。几何/mirror探针通过，Reference对照与完整源项oracle因LCB-01停点尚未完成。 | EVIDENCE_REQUIRED_BEFORE_APPROVAL | CDR-005 | 未批准；后续closure任务继续 |
| OD-06 | Fast Isotropic采用Pps=Piso-(1-tau)*Dfront；tau=0/.5/1分别为Piso-Dfront、Piso-.5Dfront、Piso。目标修正rho_front*F_target,front_shaded*tau*Dfront在rho=0、无邻排、无可见阴影时为0。Full/Fast保持不同；完整edge/segment Reference fixtures尚未生成。 | READY_FOR_OWNER_APPROVAL | CDR-007 | 未批准；后续closure任务继续 |
| OD-07 | 保留Full q0/qinc/qabs、Fast q0/qabs unavailable、keyed ragged trace、标量广播/T=0/原始非单调顺序/dayofyear1..366。AOI成对配置、table覆盖0/180、knot严格递增、线性插值；SAPM B0..B5。不提供Python运行时callback；detach前复制owned输入，输出独立拥有内存。公共cancellation token不属于V1冻结要求，内部可选取消不改变物理模型。 | READY_FOR_OWNER_APPROVAL | Execution/API/platform | 未批准；后续closure任务继续 |
| OD-08 | 在完整实现前一次预批准P4-P7的准确oracle manifests/profiles。LCB-01定向seed已批准，完整P4-P7候选包仍未完成。不得静默换回长任务内逐包批准路线。 | EVIDENCE_REQUIRED_BEFORE_APPROVAL | Execution/API/platform | 未批准；后续closure任务继续 |
| OD-09 | Rust四目标；普通GIL CPython3.11-3.14按解释器wheel；候选NumPy>=2.3.4,<3。隔离栈锁定PyO3 .29.2、rust-numpy .29.0、maturin1.15.0；CI实测NumPy2.3.4，以及3.11上的2.4.6 /3.12-3.14上的2.5.3。最低OS仍作为release gate，现代runner通过不等于已验证下限。排除PyPy/free-threaded/abi3/universal2/musllinux/Linux或WindowsARM/WASM分发。 | READY_FOR_OWNER_APPROVAL | Execution/API/platform | 未批准；后续closure任务继续 |
| OD-10 | 终点为V1 IMPLEMENTATION COMPLETE + RELEASE CANDIDATE READY FOR OWNER ACCEPTANCE。另行启动后才授权具名实现分支修改/commit/push/CI/依赖评估/普通修复/自动推进；不授权master merge/tag/release/publish/SemVer1.0.0。当前closure停点，实施任务未激活。 | READY_FOR_OWNER_APPROVAL | Execution/API/platform | 未批准；后续closure任务继续 |
| OD-11 | master/develop需PR-only、禁止force-push/删除、要求真实CI；master另需人类review、解决conversation、过期review失效与最新commit批准。Agent不得admin/bypass/release。使用独立非admin身份、受保护refs和明确凭据能力限制；普通contents-write本身不能排除merge/tag。否则签署具名且有期限的治理风险接受。本次未改规则。 | GOVERNANCE_ACTION_REQUIRED | Execution/API/platform | 未批准；后续closure任务继续 |
| OD-12 | 保留有界资源和隔离benchmark协议。必须覆盖足够宽workload；实测存在crossover时需学习并在holdout正确选择，足够宽证据证明不存在时Serial fallback合法。未实现cost estimator而总选Serial不合法。median<=1.10*best+2ms、p95<=1.25*best+5ms为M11/M12前凭证据冻结的候选预算，不是不可修订物理语义。 | MILESTONE_DEFERRED_IMPLEMENTATION_CHOICE | Execution/API/platform | 未批准；后续closure任务继续 |
