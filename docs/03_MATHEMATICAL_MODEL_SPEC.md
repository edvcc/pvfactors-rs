# 03｜Mathematical Model Specification

## 3.1 计算域、约定与单位

二维截面表示沿 tracker 轴无限延伸的平行 PV 排。坐标 x 水平、y 向上；地面 y=0，默认 x∈[-100,100] m。第 k 排中心 `(k w/gcr,h)`，k=0…N−1。输入 solar zenith z 从天顶量起；所有 azimuth 为 pvlib 的北0°、东90°、顺时针；tilt β 从水平面量起。内部几何 rotation r 有正负，与 β 不是同一变量。时间由输入给定，**不负责太阳位置、天气生成、跟踪器控制或电功率模型**。

长度 m；角度对外 degree、三角函数内部 radian；DNI/DHI/GHI、E、q0/qinc/qabs 均 W/m²。F、吸收因子、反射率无量纲。上游称 `luminance_*` 的量在本模型是经几何因子还原的辐照度标量，不能标成 cd/m² 或 W/(m²·sr)。τ 表示 spacing/transparency 的经验直通比例，不是各向异性 BSDF。

本节编号 Mxx 供 Inventory 引用。公式中的判断、截断和系数也属于规格，不能仅复刻主公式。

## M01｜角度、太阳与排

令 A 为 surface azimuth，Aₐ 为 axis azimuth：

- `r=+β` 若 `(A−Aₐ) mod 360 >180`，否则 `r=−β`；β=0 时参考保存 −0.0。
- `s₂=(sin(z) cos(A_s−Aₐ−90°), cos(z))`；`α=atan2(s₂.y,s₂.x)`。
- `b₁=c−(w/2)(cos r,sin r)`，`b₂=c+(w/2)(cos r,sin r)`；front 法向 `(-dy,dx)`、back 相反。无需把这个长度为 w 的法向当作单位向量。
- 入射投影 `μ=cosβ cosz+sinβ sinz cos(A_s−A)`；先 clip 至[-1,1]，AOI_front=acos μ，AOI_back=180°−AOI_front。

二维几何的轴向假设与三维 AOI 必须一致。正式输入要求非平放时面方位与轴方向正交；参考没有充分验证这种约束。见 05 的域与 CDR-003。

## M02｜阴影与分段

相邻中心距 p=w/gcr，θ=90°−r，δ=p[sinθ−cosθ tan(θ+α)]。参考临时正面遮长 `max(0,w−δ)`、背面 `max(0,w+δ)`；若结果大于 w 则重新置0，**不是 min(w,…)**。N=1 两侧均0。边排根据 r>0 与受光侧移除不存在邻排的遮挡。PV 每侧按 cut 等长切段，再按整排自最低端起的遮长切为 illuminated/shaded 两个固定槽；零长度槽仍有 logical index。

地面投影 `x_shadow=x_pv−y_pv/tanα`；排延长线与地面交点 `x_cut=x₁−y₁/tan r`。有排间遮挡时相邻投影重叠区被裁成相接边界；再 clip 地面区间，取照亮补集。所有 shadow / illum element 都进一步被 N 个排 cut 分成 N+1 个槽。零倾角的无限 cut 是待显式处理的极限情形。完整几何判定见 05。

## M03｜pvlib-compatible primitives

`B=2π(doy−1)/365`，Spencer 默认日外辐射：

`I0=1366.1 [1.00011+0.034221 cosB+0.00128 sinB+0.000719 cos(2B)+0.000077 sin(2B)]`。

闰年 doy 可366，但分母仍365。日期按传入 DatetimeIndex 的当地日序数取值，不自动转 UTC。Kasten–Young 1989 相对大气质量：

`m=1/[cos z+0.50572(96.07995−z)^(-1.6364)]`，z 用 degree；z>90° 为 NaN。

普通 isotropic 平面总入射：

`P_iso=DNI max(μ,0)+DHI(1+cosβ)/2+albedo·GHI(1−cosβ)/2`。

若未提供 GHI，参考用 `GHI=DNI cosz+DHI`。提供 GHI 时它影响 Fast 的地面/邻排近似源，不替代 Full 的 DNI/DHI 源。见 [pvlib 0.14 irradiance](https://github.com/pvlib/pvlib-python/blob/v0.14.0/pvlib/irradiance.py) 与 [atmosphere](https://github.com/pvlib/pvlib-python/blob/v0.14.0/pvlib/atmosphere.py)。

## M04｜Perez 1990 与 solarfactors 分解

令 zᵣ 为 z 的弧度，`Δ=DHI·m/I0`，

`ε=[(DHI+DNI)/DHI+1.041 zᵣ³]/[1+1.041 zᵣ³]`。

ε bins 上界依次1.065、1.23、1.5、1.95、2.8、4.5、6.2、∞；使用 pvlib `digitize([0,1.065,…,6.2], right=False)−1` 的等号归属。NaN 使用附加 NaN 系数行。`F₁=max(0,f₁₁+f₁₂Δ+f₁₃zᵣ)`，`F₂=f₂₁+f₂₂Δ+f₂₃zᵣ`。

| bin | f11 | f12 | f13 | f21 | f22 | f23 |
|---|---:|---:|---:|---:|---:|---:|
|1|−.008|.588|−.062|−.060|.072|−.022|
|2|.130|.683|−.151|−.019|.066|−.029|
|3|.330|.487|−.221|.055|−.064|−.026|
|4|.568|.187|−.295|.109|−.152|−.014|
|5|.873|−.392|−.362|.226|−.462|.001|
|6|1.132|−1.237|−.412|.288|−.823|.056|
|7|1.060|−1.600|−.359|.264|−1.127|.131|
|8|.678|−.327|−.250|.156|−1.377|.251|

该表为 pvlib `allsitescomposite1990` 的实际系数，应以依赖源码 SHA 核对。定义 `a=max(μ,0)`、`b=max(cosz,cos85°)`：

- `P_iso,diff=DHI(1−F₁)(1+cosβ)/2`
- `P_circ=DHI F₁ a/b`
- `P_hor=DHI F₂ sinβ`
- `P_sky=max(0,P_iso,diff+P_circ+P_hor)`；pvlib 对 airmass NaN 将总量置0，对总量等于0再把分量置0。

solarfactors 再除以 `(1+cosβ)/2`、`a/b`、`sinβ`，得到 `L_iso,L_circ,L_hor`；若总 diffuse 为0，三者置0。其他零分母可能留下 NaN。太阳落在背面时以反转法向递归求 L_circ：`β'=180−β,A'=(A−180)mod360`。两次投影都因舍入略小于0时会无限递归（DEV-001）。数学上应单次确定受光半球，无需递归。

**A/B 冲突须保留：**原文式(9)把 horizon 项允许为负，分母下限写0.087；pvlib 使用 cos85°≈0.0871557。solarfactors 对用于模型的 horizon POA 取绝对值。背面 circumsolar 使用 `L_circ cos(AOI_back)/cosz`，没有 pvlib 的85°下限。前两者是软件模型选择，后一项造成低太阳高度的非对称放大，不能靠“Perez”这个名称掩盖。原文实际核对页273、281；[Perez et al. 1990](https://archive-ouverte.unige.ch/unige:17206)，DOI 10.1016/0038-092X(90)90055-H。

## M05｜各 surface 的 source terms

`τ=spacing_ratio+(1−spacing_ratio)·module_transparency`；二者均为[0,1]输入。

| surface | Direct D | Circumsolar C（Hybrid） | Horizon H（Hybrid） |
|---|---|---|---|
| ground illum | DNI cosz | L_circ | 0 |
| ground shaded | τ·D_ground | τ·L_circ | 0 |
| front illum | DNI cos(AOI_front)，AOI≤90°，否则0 | P_circ，正面受光时，否则0 | abs(P_hor) |
| front shaded | τ·D_front | τ·C_front | abs(P_hor) |
| back illum | DNI cos(AOI_back)，AOI_back≤90°，否则0 | L_circ cos(AOI_back)/cosz，背面受光时，否则0 | abs(P_hor)(1−h_back) |
| back shaded | τ·D_back | τ·C_back | abs(P_hor)(1−h_back) |

`h_back=clip(γ/horizon_band,0,1)`，默认 band6.5°；γ 为 surface 质心到相邻排最高端的遮挡仰角。参考用 `atan(abs(Δy/Δx))`；按倾斜方向选择邻排，无邻排则0。每个细分面单独算，所以改变 cut 会改变采样。正面不应用此遮挡（DEV-005）。Isotropic 只有 D，`L_sky=DHI`；Hybrid `E_i=D_i+C_i+H_i`，`L_sky=L_iso`。各向同性天空项通过 F 耦合，不再重复加入 E_phys。

常数吸收时 `Eabs_i=(1−ρ_i)E_i`，ground `ρ=albedo`、front .01、back .03 为默认。自定义 AOI 时 direct/circ 乘各侧 `f(abs(90°−AOI))`，horizon 乘 `f(β)`，ground 仍乘1−albedo。f 是该软件采用的吸收修正语义；归一化 IAM 与绝对吸收率不能无说明互换。`with_rho_initialization` 可通过半球积分从 f 求均匀有效ρ；普通构造器不会自动使两者一致。初始化优先级是已给scalar ρ > 由f算出的scalar ρ > default；因此默认.01/.03仍为scalar时不会被计算值覆盖，要显式选择由f初始化（参考传ρ=None）。

圆盘/高斯 circumsolar 部分遮挡工具存在，但 fit→transform 主链没有调用它们。主模型通过直射阴影分区对 C 用同一个 τ；调整 `circumsolar_angle` 不改变所测 Full 输出。辅助 uniform disk 覆盖高度 d∈[0,2r]：小于半径时 `θ=2 acos((r−d)/r)`，面积比例 `(θ−sinθ)/(2π)`；大于半径用未遮面积的补集。Gaussian 使用截断 ±3σ、σ=1/√2，通过 `0.5(erf(x)−erf(y))` 归一化。这些不是当前 Full 主源项中的隐藏步骤。

## M06｜View Factor 的方向、索引与遮挡

`F_ij` 是从面 i 看到面 j 的几何视因子；用于面 i 接收入射时 `Σ_j F_ij q0_j`。无限长条带用长度替代面积。`i` 是接收行、`j` 是源列；不要因几何定义的“i→j”字面而转置矩阵。

未遮挡线段 i=(a,b)、j=(c,d)：

`F_ij=| |a−d|+|b−c|−|a−c|−|b−d| |/(2L_i)`。

仅在相向且可见时使用；长度≤参考距离阈值时置0。正背面、左右半地面由旋转符号和排 cut 判定。仅邻排相向表面直接耦合，ground-ground 为0。PV→ground 有邻排时用该邻排最低端 o 作为绕行点。对 ground端 g、PV端 p，若左侧 `atan2(p−g)>atan2(o−g)`，或右侧反向不等式，则 string length 改为 `|g−o|+|o−p|`。左地面取 `d1=l(high,right),d2=l(low,left),l1=l(high,left),l2=l(low,right)`；右地面对换 left/right。`F=(d1+d2−l1−l2)/(2L_i)`，此遮挡式不再取 abs。

由互易性 `L_iF_ij=L_jF_ji` 回填 ground→PV 和反向 PV。所有 physical row 的 sky 列为 `1−Σphysical F_ij`；零长 row 的 sky 为0。Sky **row全0**，包括 F_sky,sky。附加 sky 是边界源，不是一个有限面积、参与互易性的物理面。

顺序：ground shaded elements 的全部 cut slots → ground illum elements 的全部 slots → row0 front segments(illum,shaded)→back→row1…→sky。参考 F shape `(S+1,S+1,T)`；Rust artifact 标准化为 `[T,receiver,source]`。S 是 logical slots，包括零长；主动压缩须保存双向映射。

## M07｜AOI-adjusted VF

无自定义 f 时 `G_ij=(1−ρ_i)F_ij`，是接收面吸收加权。自定义 f 时用面质心看目标两端的切线夹角 θ∈[0,180°]。半球条带积分基本权重 `dF=0.5 sinθ dθ`，区间权重 `0.5|cosθ_low−cosθ_high|`。

参考将0…180°均分 J=300格，格中点评估 f；只要 wedge 与格满足 `wedge_low≤bin_high && wedge_high>bin_low` 就计入**整格**，不截断交叠边界。PV→ground 根据邻排最低端裁可见角；PV→PV 用对向面；sky 使用地面边界到边排最高端、邻排最高端之间的代理天空线段。`ρ_eff=1−Σbins f(mid)·weight`。

因此 G 的计算是面中心与整格求积近似；不可把 `G≤F`、精确互易性或不同 cut 下结果严格相同作为当前近似的硬条件。参考还存在原位覆盖 F 和 ground receiving rows 未乘吸收率的问题，见 DEV-009/010。Rust 必须让 F 与 G 分开存储，确认修正由 CDR-004 管理。

## M08｜Full radiosity

对每个 timestep，n=S+1，E∈Rⁿ，R=diag(ρ)；sky E_n=L_sky、ρ_n=1。参考求解：

`(R⁻¹−F)q0=E`；`qinc=R⁻¹q0`。

- q0：面向外反射的短波辐照度密度；这里不含热发射模型。
- qinc：总入射；满足 `qinc=E+Fq0`。
- sky：由最后一行得到 q0_sky=E_sky=L_sky。
- `isotropic_i=F_i,sky L_sky`。
- `reflection_i=qinc_i−E_i−isotropic_i`。
- `qabs_i=Eabs_i+Σ_j G_ij q0_j`。

参考采用 batched `np.linalg.inv(A)` 后做矩阵向量乘。源码没有说明必须求 inverse 的物理理由；“便于批量向量化”只是工程推断，不能冒充作者意图。显式 inverse 会增加计算/存储，也让ρ=0出现 inf×0。探针中 albedo=0 时 PV 量可以有限，而 ground qinc 出现 NaN；不能说所有结果都 NaN。

Rust 推荐去掉已知 sky 未知量，在 active physical surfaces 上解：

`b=E_phys+F_phys,sky L_sky`

`B qinc=b`，`B=I−F_phys,phys R_phys`

`q0=R_phys qinc`。

这是对有限非零ρ时原系统的代数等价形式，并自然扩展至ρ=0。它不是新的反射物理模型。输入合法且谱半径(FR)<1时可逆；ρ<1及有效对外泄漏通常提供稳定性，但ρ接近1/封闭腔体仍需残差与条件检查。B一般不对称，禁止默认 Cholesky。使用带主元 LU 的直接 solve；QR 作为显式诊断/回退策略，不能静默 least-squares 或正则化改变问题。

注意 AOI 本身只改变吸收 qabs；Full qinc 的反射系统仍使用均匀ρ。将角度依赖反射带入 radiosity 是新的模型，V1 不隐含实施。

## M09｜Fast Mode

Fast 不解全局反射系统；只更新选择排的背面，可进一步选择 segment。它用目标面到 ground shaded/illum、邻排 front shaded/illum、sky 的分组 VF：

`qinc_back=E_back+F_sky L_sky+albedo(F_gs P_gs+F_gi P_gi)+ρ_front(F_ps P_ps+F_pi P_pi)`。

其中 `P_pi=P_iso`（M03）。尽管变量名 `total_perez`，两种模型调用 get_total_irradiance 都没有指定 model，实际默认 isotropic。Hybrid `P_ps=P_iso−D_front−C_front+τD_front+τC_front`；Isotropic `P_ps=P_iso−D_front`，未补 τD_front（DEV-015）。地面 `P_gi=GHI`；Hybrid `P_gs=DHI−L_circ+τL_circ+τD_ground`；Isotropic `P_gs=DHI+τD_ground`。

F_g_total 由边排有限地面或相邻排最低端构成代理段；F_gs 按真实 ground shadow 的可见部分求和，F_gi=F_g_total−F_gs。F_p_total 为该背面面对的邻排，F_ps 对邻排 front shade segment 求，F_pi=F_p_total−F_ps。F_sky=1−F_g_total−F_p_total。Fast 返回 qinc/isotropic/reflection 及源项，**没有求出 Full q0/qabs**，不应伪造它们。Fast 与 Full 可有模型误差，Auto 只能改变执行策略，绝不能自动把 Full 换成 Fast。

## M10｜聚合、跳过与异常

面结果通过 `Σ L_i q_i / Σ L_i` 聚合到段/侧/排。空槽不参与长度权重；活跃面出现 NaN 必须报错或标为无效，不能 `nansum` 掩盖。参考的 `skip_step=(z>90)|(DNI<0)|(DHI<0)|((DNI==0)&(DHI==0))` 在 fit 最后计算，但 Full/Fast 未用它屏蔽计算；night 探针能产生负 qinc。前置有效性与零光照策略必须显式修正。

拟议 Rust V1：非有限输入、负 DNI/DHI、非法几何返回带 timestep 的错误；夜间策略可明确为 `ZeroAtNight`（默认模型政策，CDR-001）或 `RejectNight`，不得混入隐式裁剪；有效域内 DNI=DHI=0 且 GHI 为0/未提供可直接输出0与 ZeroIrradiance 状态。若 GHI>0 则不满足全零捷径，应报输入矛盾或按显式 GHI 政策处理。z=90°先进入边界政策，不走奇异除法。冻结政策前不实现物理计算入口。
