# 04｜Dependency Decomposition

以下为对源码实际 import/call 的审计。直接调用范围与 pvlib 传递实现不同，tests/教程里用于产生天气/太阳角的 pvlib 调用不属于 Core。

## pvlib：必须独立实现的最小闭包

| 直接调用 | solarfactors 位置 | 物理语义 | Rust 处理与版本敏感性 |
|---|---|---|---|
| tools.sind / cosd | geometry/base,pvrow；vfmethods,aoimethods；irradiance | degree trig | 小 helper；实现 deg→rad，保留临界符号决策 |
| irradiance.aoi_projection | irradiance/utils.py | 太阳方向与正面法向点积 | 实现 clamp[-1,1]；近零符号见 CDR-002 |
| irradiance.aoi | irradiance/models.py | 法向入射角 | acos 投影，背面=180-front；表面切线角另定义 |
| irradiance.get_extra_radiation | irradiance/utils.py | Perez 的法向大气外辐照度 | 只需默认 Spencer、常数1366.1、dayofyear；不需要 SPA/ephemeris |
| atmosphere.get_relative_airmass | irradiance/utils.py | Perez brightness 中相对气团质量 | 只需默认 Kasten–Young 1989，无 pressure 修正 |
| irradiance.perez(return_components=True) | irradiance/utils.py | 1990 allsitescomposite diffuse | 必须实现系数、分箱、F1截断、总量和分量掩码；0.14字段变化只是 C 层 |
| irradiance.get_total_irradiance | 两个 model 的 fit | Fast 环境入射量 | **未传 model，实际默认 isotropic**；仅闭包中的 sky isotropic + ground diffuse + direct |
| pvsystem.retrieve_sam('SandiaMod') | aoimethods.faoi_fn_from_pvlib_sandia | 读组件参数数据库 | convenience；Core 不携带/访问 SAM，用户显式提供 B0…B5 |
| iam.sapm(upper=1) | 同上返回的 closure | SAPM AOI polynomial | 支持参数化 polynomial 时需实现 clamp[0,1]，入射角<0→0；非基本 Full 路径依赖 |

传递闭包：get_total_irradiance→get_sky_diffuse(default isotropic)、get_ground_diffuse、aoi、poa_components；perez→_get_perez_coefficients；get_extra_radiation→day angle helper。其他模型分支不纳入。`reference/pvlib_primitives.py` 保存所审读函数的版本化源码摘录，仅为可读证据，不能当独立可执行模块。

公式见 03。使用 `luminance_*` 变量不意味着 cd/m²：这些量是 W/m² 模型强度，不是人眼光度学亮度。天气、location、tracking、clear sky、单二极管等出现在测试准备或用户系统，不因此变成重写任务。

依据：[irradiance/models.py](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/models.py)、[utils.py](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/utils.py)、[AOI helper](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/aoimethods.py)、[pvlib 0.14.0 irradiance](https://github.com/pvlib/pvlib-python/blob/v0.14.0/pvlib/irradiance.py)。

## Shapely：实际调用语义

| 类型/操作 | 位置与用途 | 必需能力 | 替代方式 |
|---|---|---|---|
| Point；x/y/coords/distance | utils 投影与端点比较 | 是，二维点 | Point2/Vec2，hypot |
| LineString；boundary.geoms/coords/length/centroid | base、pvrow、pvground，静态快照 | 是，线段本体；容器否 | Segment2，端点对、长度、中点 |
| GeometryCollection；geoms/is_empty/length | 空结果与表面集合 | 集合语义是 | Option/enum、Vec<Segment2>，显式 Empty |
| MultiLineString | 自定义 difference 返回两个片段 | 是，最多两段 | SegmentSet，沿母线有序 |
| dwithin(point,tol) | 自定义 contains | 是，但不是拓扑 contains | 点到闭线段最短距离≤tol，**含端点** |
| distance/intersects | base/side 透传 | 限定线段域是 | 最近点与区间相交，排除通用多边形 |
| interpolate(normalized=True) | side 等分 | 是 | p(t)=a+t(b-a) |
| buffer(DISTANCE_TOLERANCE).intersects | ShadeCollection.remove_linestring | 容差接触判定 | 共线检查+沿线区间判断，不生成 buffer 多边形 |
| buffer(tol).intersection(linestring) | PVSegment.cast_shadow | 静态遮挡裁切 | 专用投影/裁切；记录与 buffer 扩长的差别 |
| linemerge | ShadeCollection、PVRow 静态呈现 | 连续共线线段合并 | 排序区间合并，标签不同不合并 |
| unary_union | PVRow.geometry | 静态组合 | Surface list/拓扑快照，不需要 GIS union |
| bounds/xy | plot.py | 绘图辅助 | Out of Scope V1 |
| geos_version / geos_capi_version | pvfactors.__init__ | 安装自检 | Core 不需要 |

没有发现运行核心需要 polygon overlay、CRS、空间索引、地理投影。timeseries Ordered 主流程本身主要是 NumPy 坐标运算；Shapely 主要承担静态对象、快照及旧几何便利 API。**专用 geometry kernel 足够且推荐**，但必须以其受限输入域证明；不能声称能替代全部 Shapely。

自定义 `geometry.utils.difference` 并非 Shapely difference，其完整包覆分支已由最小探针确认错误。Rust 使用明确定义的区间差，偏差登记 DEV-016。投影中的 2×2 inverse 用叉积公式替代，平行/共线是显式结果。

## 其他依赖

NumPy：向量化、broadcast、线代与掩码；Rust 不复制整批三维矩阵，也不能忽略 NaN/Inf 的差异。Pandas：时间索引及结果组织，binding 只搬运日期/数值。multiprocessing：执行实现细节，不进入 Core。Matplotlib：绘图，不进入 Core。SciPy：在该包核心中无直接算法调用，pvlib 导入所需不等于 Rust 物理依赖。math.erf 只用于遗留 Gaussian 遮挡工具，主 V1 不因此强制外部特殊函数库。

工程依赖与物理依赖分别管理；Python Binding 可依赖 NumPy/PyO3，但 core 的 Cargo 依赖闭包不得出现 Python/GEOS/pvlib。
