# 07｜Numerical Tolerance Strategy

本阶段不冻结一个随意的全局1e−6。下列是误差模型、测试域与标定程序；正式数值阈值由Golden/cross-platform实验生成经审查的`tolerance-profile-v1.json`。原源码阈值属于参考**分支语义**，与验收误差不是同一个概念。

## 比较规则

标量一般使用 `|x−y| ≤ a + r·max(|x|,|y|)`；x,y接近0时绝对项主导。向量同时报告max norm、RMS与最坏case；不得只以平均误差掩盖局部错误。相对误差报告时分母用文档规定floor，不能除以0。NaN/Inf须匹配分类并命中已登记例外；正常Rust输出不允许因reference NaN就无条件pass。矩阵的索引/topology/shape/单位/模型revision精确比较。

| profile | 单位 / 比较对象 | 如何确定a/r | 边界策略 |
|---|---|---|---|
| geometry_orientation | 无量纲/叉积归一化 | fp误差随向量长度及坐标尺度传播，独立解析predicate样本标定 | 共线分类带宽与结果distance tolerance分离 |
| geometry_position | m，端点/投影 | a由坐标尺度×machine ε×实际运算界，r用于大坐标 | 近水平投影条件差，不能任意扩大阈值吞掉拓扑 |
| length | m，面长/遮长/守恒 | a随w/extent与求和面数，r控制较大长度 | 0/非0 active分类用命名模型阈值 |
| angle | degree/radian分别 | circular distance与acos near±1误差分别标定 | signed zero不强制bitwise；90°半球CDR另判定 |
| view_factor | 无量纲 | a处理本应为0；r处理非零F；Hottel差分相消按长度比标注 | small L与大端点距离可能放大误差，单独case家族 |
| AOI_quadrature | 无量纲 | 参考J300软件兼容误差与J收敛近似误差分开 | 不能把整格算法偏差归入floating tolerance |
| Perez_components | W/m²及中间无量纲各一组 | F1/F2/epsilon/bin先检查，POA按分量尺度 | bin必须精确归属；threshold邻域单独case不能放宽误差跨bin |
| solver_residual | 无量纲scaled backward error | `η=||Bq−b||∞/(||B||∞||q||∞+||b||∞)`，参考machineε、n与pivoting稳定性 | 分母0且残差0定义η0；估计κ，识别接近奇异 |
| q0/qinc/qabs | W/m²，逐面 | 分开a/r，结合source误差与κ(B)传播；q0近0主要a | 不以solver残差替代forward误差；高κ警告/错误政策明确 |
| aggregate_irradiance | W/m²，side/row | 由ΣLq和length误差传播的预算，再用corpus验证 | 正长度面不允许NaN；避免平均掩盖局部异常 |
| execution_equivalence | 同上述 | 同一solver/归约顺序应最紧；跨backend使用已标定输出组 | 线程变化不得改变input mask/topology/model |

IEEE f64机器epsilon约2.22e−16。理论估计可用`γ_k=kε/(1−kε)`提供舍入预算，k为实际求和/操作数；它是推导起点，不是所有几何/solver误差的固定倍数保证。将算法近似、离散化误差、模型偏差与浮点误差分别记录。

## 参考常量审计

`DISTANCE_TOLERANCE=1e−8`（长度/contains/active相关分支）；`TOL_COLLINEAR=1e−5`（参考未归一化向量的点积/叉积判定）；`THRESHOLD_DISTANCE_TOO_CLOSE=1e−10`在本冻结快照仅定义、没有调用，不应据此设计一层精度。参考不同方法出现 `<tol`、`>tol`、`≤tol`，恰好等于tol须专门golden，不能用一个通用epsilon helper悄然统一。

Rust早期可以显式`ReferenceGeometryPolicy`保留这些B层阈值，再通过CDR决定scale-aware predicate。比较tolerance不能充当predicate；例如把length1e−9误差判定为“都差不多”会改变表面数与矩阵维度。

## 最终冻结流程

1. 在R0对每case重复生成，找出环境内确定性与nonfinite基线；使用高精度/解析小例作为独立真值。
2. 运行Rust f64原型后比较最早分歧层，不以终值调参。LU与inverse差分仅用于验证代数等价；本次nominal类探针incident solve差异最大约4.55e−13 W/m²，不足以据此冻结全库阈值。
3. Linux x86_64、macOS arm64/x86_64、Windows x86_64分别记录CPU、compiler/target flags、math/solver backend，建立跨平台误差分布。未实测平台不得宣称通过。
4. 每profile提出阈值=解析误差预算与实测可信上界的审查结果；报告p50/p95/p99/max、最坏输入、条件数、物理规模。安全余量写明理由，不按“让所有当前测试绿”倒推。
5. 领域审查确认不会吞掉source/index/model错误，冻结版本；有重大新增硬件/solver/model变更重新审查，不自动放宽。

Bitwise复现不作为跨平台承诺。可提供同构建、同backend、固定归约顺序的deterministic模式；禁用fast-math作为初始正确性基线。SIMD/FMA、并行分解和重排引入的差异要在相同误差预算内验证。
