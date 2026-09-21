# 05｜Geometry Reimplementation Specification

## 适用域与值类型

V1 为无限轴向的二维截面：水平 ground y=0，共用 row width w、中心高度 h、pitch p=w/gcr、axis azimuth；每个时刻全阵列共用 tilt/azimuth。`Point2{x,y}`、`Vec2{x,y}`、`Segment2{a,b}`、`Interval{lo,hi}`、`SegmentSet` 足够。单位 m、degree（内部弧度仅局部）；点/方向/角不能用同一个无语义元组混传。

Rust 输入验证：N≥1；w>0；gcr>0，V1默认 gcr≤1；cut 正整数且预算内；所有有效时刻 h-w|sin(rotation)|/2>length_guard；端点处于配置 ground 范围。为保持共轴向几何与三维 AOI 一致，非零 tilt 的 surface azimuth 应是 axis±90°（mod360）；其他方向即使 Python 可运行，也不是本 V1 共轴模型已验证输入。倾角0…180°的倒置法向可表述，但 >90°需单列验证组，不借助常见0…90°测试宣称完整覆盖。

地面碰撞/几何重叠必须报参数错误。地平线太阳方向为投影奇异，先由状态策略处理；不会用巨大但有限的假阴影替代。

## 精确构造规则

设 γ=(surface_azimuth-axis_azimuth) mod360。

- γ>180°：rotation=+tilt；否则=-tilt。tilt=0 时 reference 强制 -0.0。
- row k 中心 c=(k p,h)。a=c-w/2(cos r,sin r)，b=c+w/2(cos r,sin r)。参考 b1=a、b2=b。
- front 法向 n=(-dy,dx)，back=-n；不是归一化向量，角计算必须除范数。
- 太阳截面向量 s=(sin z cos(A_s-A_axis-90°),cos z)；alpha=atan2(s_y,s_x)。s 不是单位二维向量，不要无故重定义。
- height 相等的端点，`highest_point` 取 b1，lowest 取 b2；此 tie rule 与索引稳定性相关。

来源：[geometry/base.py](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/base.py)、[pvrow.py](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvrow.py)。

### 排间直射遮挡

Reference：θ=90°-r，β=θ+alpha(deg)，δ=p[sinθ-cosθ tanβ]。暂长 lf=max(0,w-δ)、lb=max(0,w+δ)；若暂长>w，**重置0而非clip至w**。N=1时两者0。是否直射遮挡=(lf>1e-8 or lb>1e-8)。边排精确规则：row0在r>0时front shade=0、back=lb，r≤0时front=lf、back=0；rowN−1在r>0时front=lf、back=0，r≤0时front=0、back=lb。内排保留lf/lb。N1前一步已令两者0。

此写法在分母接近零时敏感。Rust 可由平行光与相邻排的交点推导长度，但 Geometry Gate 必须逐场景比对符号、极限和遮挡面，不能用普通 clamp 静默取代参考分支。平行太阳入射、N=1、90°/180°旋转、±0、临界长度±ulp 均是边界测试。

### cut 与 shade partition

每侧 cut=c，等长分成 c 段，段序从 b1→b2。每段保留 illum、shaded 两个逻辑槽；阴影从该侧低点向高点延伸。reference 使用 r>=0 判低高、r!=0判非平面；flat 时shade长度为0。设R=w/2、rs=R−shade：r>=0的shade边界为c+rs(cos(r+180°),sin(r+180°))，否则c+rs(cosr,sinr)。每段先取low/high；yshade>yhigh且非flat为全遮，yshade>ylow且非全遮/非flat为部分遮，其余无遮。shade坐标为low→shade_end，illum为shade_end→high。完整排b1参考实际用cos/sin(r+180°)求，不是浮点上直接取cos/sin(r)的负值，数学等价但最后几位可不同。不把几何零长度槽当成合法的受光面积。

稳定 `SurfaceKey={kind,row,side,segment,illumination,ground_element,cut_interval}` 与有效长度分离。ReferenceIndex 另存，不以 Vec 位置充当长期物理身份。V1 首先保留 reference 分区；允许移除当前时刻长度为0的矩阵行列，但必须保留完整key→active_index映射、输出的inactive状态、严格恢复顺序。

## ground shadow、cut、overlap

每端点投影到ground：x_shadow=x-(y-y_g)/tan(alpha)。每排投影端点排序为[l,r]。沿母地面的一维区间足够。

Reference 每排还建立切分点 x_cut=x1-(y1-y_g)/tan(r)。flat 得 ±Inf，后续 clip 使其落到有限边界；Rust 用 `CutPoint::LeftInfinity/Finite/RightInfinity` 等价表达，不能把它当普通有限坐标。这个cut用来区分某排正/背面所能看到的地面半侧，**不是辐照度为零的边界**。

N个shadow元素，N+1个illum元素。若全阵列 direct-shading flag 为真，则每个非末shadow的右端截到下一个shadow左端，避免重叠计量。之后裁到[-100,100]，illum由相邻shadow之间的补集构造。每个元素再按N个cut点分为N+1个逻辑槽，允许零长度。

默认无额外PV cut时，逻辑ground表面数=(2N+1)(N+1)，PV表面数=4N；总数 S=(2N+1)(N+1)+4N。一般PV部分=2Σ(c_front+c_back)。**逻辑S是O(N²)**，但活动ground区间数通常O(N)，这解释了未经压缩矩阵的扩张。实测N=3有S=40、活动16；N=11有S=320、活动56（仅该工况）。活跃压缩是后续经验证的优化，不能靠合并不同source/visibility的正长度区间改变模型。

地面边界是模型参数，默认[-100,100]为reference兼容配置。大型阵列必须显式更大范围并记录差异；`GroundExtent` 一处传入所有几何/VF/AOI方法，禁止复制散落全局常量。精确无限ground需另一个revision。

## 索引顺序

1. ground.shadow_elements 按排投影顺序，每个内部按cut interval；
2. ground.illum_elements 按地面顺序，每个内部按cut interval；
3. row从0至N-1，每排front后back，每侧segment顺序，每段illum后shaded；
4. sky最后，index=S。

同一批次逻辑槽保留；source/golden记录(时间,SurfaceKey,ReferenceIndex,active,coords,length)。静态 `at(idx)` 会滤空/merge，**不能用其返回顺序代替 timeseries 的矩阵索引**。参考sky不是真实地面/面板Surface。

## kernel 操作契约

| 操作 | 规则 | 退化结果 |
|---|---|---|
| projection | a+t(b-a)与q+λv交点，t=cross(q-a,v)/cross(b-a,v) | 平行不共线=None；共线=Coincident；限定segment时t∈[0,1] |
| contains | clamp参数后点到最近点距离≤τ_len，含端点 | 零长段按点距离定义 |
| collinearity | 相对方向叉积与尺度判定，另外检查位置偏移 | 不用未归一化1e-5点积作为普遍物理阈值 |
| intersection | 共线段用参数区间交；非共线可返回点 | 点交不产生正长度遮挡 |
| subtraction | [a,b]减交区间，返回0/1/2有序区间 | 完整包覆返回空；浮点小片段按策略标注 |
| overlap/merge | 同母线、同标签，排序并合并重叠/邻接 | 不跨side/normal/material/source合并 |
| clipping | 与ground范围相交，保持l≤r | 空区间保留逻辑槽，长度0 |
| length/centroid | hypot(dx,dy)、端点中点 | 空对象与零長对象区分 |

reference `contains` 是dwithin，不是Shapely严格contains。旧buffer截断会引入容差尺度的几何膨胀，不作为Rust物理目标。每个操作以独立手算fixture与上游典型case两路验收。参考projection把未归一法向叉积/点积绝对值<1e−5视为平行并返回empty（包含共线情况）；must_contain检查垂线距离<1e−8且到两端距离均≤L，若到任一端距离<1e−8则snap到该端。Rust的Coincident类型与尺度判定是显式改进，需CDR-003/006限定，而非假定参考已有这种语义。

## Geometry Gate

坐标/长度差异、分区拓扑、source标签、可见侧、索引映射分别比较；不能仅看aggregate。必须验证：每侧Σ长度=w、ground partition不重叠且覆盖extent、shade长度∈[0,w]、合并前后长度守恒、母线一致、mirror映射可逆。长度刚好落在阈值上的case保留Reference记录并建立CDR，不能为通过测试扩大容差吞掉真实片段。
