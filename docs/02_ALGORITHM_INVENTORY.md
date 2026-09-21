# 02｜Algorithm Inventory

共 **60 个算法/行为项**。每项列出所需字段；同一Python class可映射多个Rust模块，反之亦然。共同数学完整式见03，专用几何合同见05。覆盖核心执行路径、辅助静态几何、未进入主链的circumsolar helper和当前执行机制；getter/plot/容器样板不是隐藏物理算法。现有测试链接说明覆盖关联，不宣称其覆盖全部登记边界。

物理来源A与B/C明确区分：Perez原文、Hottel/半球积分与依赖官方源码索引见14；软件近似不能因列出物理背景就升级为论文规定。

| ID | Name | Purpose | Rust module |
|---|---|---|---|
| MATH-01 | Degree trigonometry | 统一度/弧度原语 | math |
| MATH-02 | Rotation convention | 确定截面排朝向 | math/geometry |
| MATH-03 | Solar vector | 把日光投影至截面 | math |
| MATH-04 | Tolerance predicates | 复原分支语义 | math/numerics |
| GEO-01 | Point/Vec/Segment | 建立有限线性几何值 | geometry/kernel |
| GEO-02 | PVSurface | 面身份与几何/光学关联 | geometry/surface |
| GEO-03 | PVSegment | 维护同线明暗分区 | geometry/partition |
| GEO-04 | ShadeCollection | 同阴影语义的面分组 | geometry/partition |
| GEO-05 | PVRow & normals | 构造等宽排两侧 | geometry/layout |
| GEO-06 | OrderedPVArray | 构造有序等距阵列 | geometry/layout |
| GEO-07 | Timeseries geometry | 保持跨时点稳定身份 | geometry/frame |
| GEO-08 | Surface indexing | 定义矩阵对应关系 | geometry/index |
| GEO-09 | PV cut/discretization | 细分面与分配阴影 | geometry/partition |
| GEO-10 | Inter-row direct shading | 计算正背遮长 | geometry/shading |
| GEO-11 | Ground shadow projection | 沿光线投影PV端点 | geometry/shading |
| GEO-12 | Ground cut projection | 划分row可见半地面 | geometry/ground |
| GEO-13 | Overlap & complement | 构造无重叠明暗覆盖 | geometry/ground |
| GEO-14 | Ground per-cut slots | 创建VF可见分区 | geometry/ground |
| GEO-15 | Containment | 判定点容差内在线段上 | geometry/kernel |
| GEO-16 | Collinearity | 验证同线分区 | geometry/kernel |
| GEO-17 | Line difference | 共线线段相减 | geometry/kernel |
| GEO-18 | Projection/intersection | 沿向量投影至线 | geometry/kernel |
| GEO-19 | Cast/cut/merge | 静态面分区辅助操作 | geometry/partition |
| GEO-20 | Ground snapshot/degeneracy | 按指定时点提取活跃面 | geometry/frame |
| VF-01 | Hottel crossed-string | 无限条带几何交换 | viewfactor/hottel |
| VF-02 | PV→PV | 填邻排相向VF | viewfactor/ordered |
| VF-03 | Obstructed strings | 遮挡下有效弦长 | viewfactor/obstruction |
| VF-04 | PV→Ground | 半地面与邻排挡光交换 | viewfactor/ordered |
| VF-05 | Reciprocity / ground→PV | 一致反向交换 | viewfactor/matrix |
| VF-06 | Sky / VF matrix | 补齐边界源与顺序 | viewfactor/matrix |
| VF-07 | AOI quadrature basis | 预计算切线角吸收积分 | viewfactor/aoi |
| VF-08 | AOI wedge / obstruction | PV接收面吸收VF | viewfactor/aoi |
| VF-09 | AOI sky | 吸收加权天空项 | viewfactor/aoi |
| VF-10 | AOI matrix | 隔离几何与吸收核 | viewfactor/matrix |
| VF-11 | Effective reflectivity | 吸收曲线推均匀ρ | irradiance/optics |
| VF-12 | Fast grouped VF | 分组环境可见因子 | viewfactor/fast |
| IRR-01 | Input normalization | 建立输入时间轴 | simulation/input |
| IRR-02 | Extraterrestrial radiation | Perez太阳通量归一化 | irradiance/primitives |
| IRR-03 | Relative airmass | Perez亮度指标 | irradiance/primitives |
| IRR-04 | AOI / hemisphere | 确定正背受光 | irradiance/primitives |
| IRR-05 | Perez decomposition | 三diffuse分量 | irradiance/perez |
| IRR-06 | Luminance/back conversion | Perez标量映射到各面 | irradiance/perez |
| IRR-07 | IsotropicOrdered | 各向同性源项 | irradiance/isotropic |
| IRR-08 | HybridPerezOrdered | 混合天空模型源项 | irradiance/hybrid |
| IRR-09 | Transmission/albedo/rho | 经验透射和漫反射参数 | irradiance/optics |
| IRR-10 | Horizon band shading | 地平线diffuse遮挡 | irradiance/shading |
| IRR-11 | Circumsolar disk/Gaussian | 解释非主链辅助能力 | irradiance/shading(扩展候选) |
| IRR-12 | Absorbed source/AOI | 源分量吸收 | irradiance/absorption |
| IRR-13 | SAPM convenience | 拆解可选pvlib数据库依赖 | irradiance/optics |
| ENG-01 | Transform to surfaces | 将类别源映射到面 | simulation/frame |
| ENG-02 | Irradiance/rho matrices | 装配radiosity输入 | radiosity/assembly |
| ENG-03 | Full radiosity solve | 多次反射系统求解 | radiosity/solve |
| ENG-04 | Incident decomposition | 分离sky与反射 | radiosity/output |
| ENG-05 | qabs/surface update | 总吸收与面结果 | radiosity/output |
| ENG-06 | Fast/row/segment selection | 背面环境单次反射近似 | simulation/fast |
| ENG-07 | Weighted aggregation | 面→segment→side→row | simulation/report |
| ENG-08 | Skip/input status | 明确有效时点与捷径 | simulation/input |
| EXEC-01 | Serial execution | 时序Reference主流程 | execution/serial |
| EXEC-02 | Multiprocessing split | 解释上游并行分块 | execution/outer |
| EXEC-03 | Report merge | 恢复原时序顺序 | execution/output |

## MATH-01｜Degree trigonometry

| Field | Specification |
|---|---|
| Purpose | 统一度/弧度原语 |
| Python source | [pvfactors/geometry/base.py::_coords_from_center_tilt_length](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/base.py#L40) |
| Mathematical / physical source | A：欧氏向量/三角函数；B：pvlib角约定与源码阈值。03 M01、07。 |
| Input | degree角度 |
| Output | sin/cos值 |
| Formula / rule | 乘π/180后sin/cos；轴值不随意截断 |
| Dependencies | 无 |
| Edge cases | 周期/负零/near90 |
| Tolerance behavior | angle/geometry predicate分开；参考阈值见MATH-04；验收用07 named profiles。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_base.py::test_coords_from_center_tilt_length_vec](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L285) |
| Known ambiguity | libm ULP差异 |
| Proposed Rust module | math |
| Expected validation | L1解析方向/周期/边界；L2参考primitive；L4 biased near-zero/near90。 |

## MATH-02｜Rotation convention

| Field | Specification |
|---|---|
| Purpose | 确定截面排朝向 |
| Python source | [pvfactors/geometry/base.py::_get_rotation_from_tilt_azimuth](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/base.py#L97) |
| Mathematical / physical source | A：欧氏向量/三角函数；B：pvlib角约定与源码阈值。03 M01、07。 |
| Input | tilt/surface az/axis az |
| Output | signed rotation |
| Formula / rule | 差mod360>180取+tilt，否则−tilt；flat−0 |
| Dependencies | MATH-01 |
| Edge cases | 180等号/flat/wrap |
| Tolerance behavior | angle/geometry predicate分开；参考阈值见MATH-04；验收用07 named profiles。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_base.py::test_coords_from_center_tilt_length_float](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L266) |
| Known ambiguity | 任意方位与2D轴可能不一致DEV-018 |
| Proposed Rust module | math/geometry |
| Expected validation | L1解析方向/周期/边界；L2参考primitive；L4 biased near-zero/near90。 |

## MATH-03｜Solar vector

| Field | Specification |
|---|---|
| Purpose | 把日光投影至截面 |
| Python source | [pvfactors/geometry/base.py::_get_solar_2d_vectors](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/base.py#L128) |
| Mathematical / physical source | A：欧氏向量/三角函数；B：pvlib角约定与源码阈值。03 M01、07。 |
| Input | sun z/az/axis |
| Output | s2与alpha |
| Formula / rule | M01公式；alpha=atan2(y,x) |
| Dependencies | MATH-01 |
| Edge cases | 沿轴/地平线/night |
| Tolerance behavior | angle/geometry predicate分开；参考阈值见MATH-04；验收用07 named profiles。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_base.py::test_solar_2d_vectors](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L307) |
| Known ambiguity | night skip未执行 |
| Proposed Rust module | math |
| Expected validation | L1解析方向/周期/边界；L2参考primitive；L4 biased near-zero/near90。 |

## MATH-04｜Tolerance predicates

| Field | Specification |
|---|---|
| Purpose | 复原分支语义 |
| Python source | [pvfactors/config.py](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/config.py#L1) |
| Mathematical / physical source | A：欧氏向量/三角函数；B：pvlib角约定与源码阈值。03 M01、07。 |
| Input | 长度/方向差 |
| Output | 分类布尔值 |
| Formula / rule | distance1e−8、collinear1e−5；各调用<与>独立 |
| Dependencies | MATH-01 |
| Edge cases | 等阈值/ULP两侧 |
| Tolerance behavior | angle/geometry predicate分开；参考阈值见MATH-04；验收用07 named profiles。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_base.py::test_pvsurface_difference_precision_error](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L146) |
| Known ambiguity | 不等于验收误差；尺度敏感 |
| Proposed Rust module | math/numerics |
| Expected validation | L1解析方向/周期/边界；L2参考primitive；L4 biased near-zero/near90。 |

## GEO-01｜Point/Vec/Segment

| Field | Specification |
|---|---|
| Purpose | 建立有限线性几何值 |
| Python source | [pvfactors/geometry/timeseries.py::TsLineCoords](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/timeseries.py#L259) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | 两个端点 |
| Output | length/centroid/high/low |
| Formula / rule | hypot、均值，最高点y>=时选b1 |
| Dependencies | MATH-01 |
| Edge cases | 重合点/最高点tie |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_timeseries.py::test_ts_pvrow](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_timeseries.py#L13) |
| Known ambiguity | Shapely容器非物理需求 |
| Proposed Rust module | geometry/kernel |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-02｜PVSurface

| Field | Specification |
|---|---|
| Purpose | 面身份与几何/光学关联 |
| Python source | [pvfactors/geometry/base.py::PVSurface](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/base.py#L328) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | segment/shade/index/normal |
| Output | surface |
| Formula / rule | normal=(-dy,dx)或显式normal；保存params |
| Dependencies | GEO-01 |
| Edge cases | empty/反法向/零长 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_base.py::test_add_pvsurface_shadecollection](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L113) |
| Known ambiguity | 可变Python dict是C层 |
| Proposed Rust module | geometry/surface |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-03｜PVSegment

| Field | Specification |
|---|---|
| Purpose | 维护同线明暗分区 |
| Python source | [pvfactors/geometry/base.py::PVSegment](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/base.py#L657) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | illum与shade collections |
| Output | segment/shaded length |
| Formula / rule | 两组同线，length相加，参数按长度聚合 |
| Dependencies | GEO-02 GEO-04 |
| Edge cases | 空一侧/重复覆盖 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_base.py::test_segment_shaded_length](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L65) |
| Known ambiguity | 静态buffer路径非主kernel需求 |
| Proposed Rust module | geometry/partition |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-04｜ShadeCollection

| Field | Specification |
|---|---|
| Purpose | 同阴影语义的面分组 |
| Python source | [pvfactors/geometry/base.py::ShadeCollection](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/base.py#L361) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | 同shade surfaces |
| Output | ordered pieces/weighted param |
| Formula / rule | uniform shading检查，ΣLq/ΣL |
| Dependencies | GEO-02 |
| Edge cases | 空集合/零权重 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_base.py::test_shade_collection](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L18) |
| Known ambiguity | merge不能跨params或logical身份 |
| Proposed Rust module | geometry/partition |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-05｜PVRow & normals

| Field | Specification |
|---|---|
| Purpose | 构造等宽排两侧 |
| Python source | [pvfactors/geometry/pvrow.py::TsPVRow.from_raw_inputs](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvrow.py#L45) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | center/w/r/cuts/shade |
| Output | front/back sides |
| Formula / rule | M01端点，front/back同坐标相反normal |
| Dependencies | GEO-01 MATH-02 |
| Edge cases | 地下/tilt90/flat |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_timeseries.py::test_ts_pvrow](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_timeseries.py#L13) |
| Known ambiguity | clearance验证缺失DEV-002 |
| Proposed Rust module | geometry/layout |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-06｜OrderedPVArray

| Field | Specification |
|---|---|
| Purpose | 构造有序等距阵列 |
| Python source | [pvfactors/geometry/pvarray.py::OrderedPVArray.fit](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvarray.py#L130) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | N/w/h/gcr/axis/angles |
| Output | rows/ground/index |
| Formula / rule | pitch=w/gcr；center=(kpitch,h)；共同r |
| Dependencies | GEO-05 MATH-03 |
| Edge cases | N1/非法gcr/extent越界 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_pvarray.py::test_ordered_pvarray_from_dict](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_pvarray.py#L10) |
| Known ambiguity | 不支持任意terrain/非等距排 |
| Proposed Rust module | geometry/layout |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-07｜Timeseries geometry

| Field | Specification |
|---|---|
| Purpose | 保持跨时点稳定身份 |
| Python source | [pvfactors/geometry/timeseries.py::TsSurface](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/timeseries.py#L112) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | coords[T]/params/index |
| Output | 每时点surface |
| Formula / rule | logical槽持久；at过滤短面；is_empty为全批nansum长度 |
| Dependencies | GEO-02 GEO-06 |
| Edge cases | 有时为空/NaN/切chunk |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_timeseries.py::test_ts_pvrow_to_geometry](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_timeseries.py#L87) |
| Known ambiguity | 全批empty产生批次依赖DEV-018/025 |
| Proposed Rust module | geometry/frame |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-08｜Surface indexing

| Field | Specification |
|---|---|
| Purpose | 定义矩阵对应关系 |
| Python source | [pvfactors/geometry/base.py::BasePVArray._index_all_ts_surfaces](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/base.py#L1323) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | 全部ground/row槽 |
| Output | index/key映射 |
| Formula / rule | ground shade→illum；row front→back；segment illum→shade；sky末尾 |
| Dependencies | GEO-06 GEO-07 |
| Edge cases | 零长/cut不等 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_pvarray.py::test_ts_surface_indices_order](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_pvarray.py#L332) |
| Known ambiguity | 压缩需保留logical映射 |
| Proposed Rust module | geometry/index |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-09｜PV cut/discretization

| Field | Specification |
|---|---|
| Purpose | 细分面与分配阴影 |
| Python source | [pvfactors/geometry/pvrow.py::TsSide.from_raw_inputs](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvrow.py#L246) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | w/r/cut/shade |
| Output | 每segment两槽 |
| Formula / rule | 等分线段与自最低点起shade区间求交 |
| Dependencies | GEO-05 GEO-10 |
| Edge cases | cut0/1/shade0/w/flat |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_pvarray.py::test_discretization_ordered_pvarray](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_pvarray.py#L81) |
| Known ambiguity | 重新求解cut不严格等价DEV-019 |
| Proposed Rust module | geometry/partition |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-10｜Inter-row direct shading

| Field | Specification |
|---|---|
| Purpose | 计算正背遮长 |
| Python source | [pvfactors/geometry/pvarray.py::OrderedPVArray._calculate_interrow_shading](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvarray.py#L228) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | alpha/r/pitch/w/N |
| Output | shade lengths/flag |
| Formula / rule | M02δ；max(0,w∓δ)，>w重置0；边排消除无邻居遮挡 |
| Dependencies | MATH-02 MATH-03 |
| Edge cases | N1/tan极点/遮长端点 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_pvarray.py::test_ordered_pvarray_direct_shading](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_pvarray.py#L543) |
| Known ambiguity | 不可把>w reset静默改clamp |
| Proposed Rust module | geometry/shading |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-11｜Ground shadow projection

| Field | Specification |
|---|---|
| Purpose | 沿光线投影PV端点 |
| Python source | [pvfactors/geometry/pvground.py::TsGround.from_ts_pvrows_and_angles](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvground.py#L73) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | PV endpoints/alpha |
| Output | raw shadows |
| Formula / rule | x'=x−(y−yg)/tan(alpha)，左右排序 |
| Dependencies | GEO-05 MATH-03 |
| Edge cases | 水平光/night/extent外 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_pvarray.py::test_coords_ground_shadows](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_pvarray.py#L429) |
| Known ambiguity | 地平线不能直接进入奇异除法 |
| Proposed Rust module | geometry/shading |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-12｜Ground cut projection

| Field | Specification |
|---|---|
| Purpose | 划分row可见半地面 |
| Python source | [pvfactors/geometry/pvground.py::TsGround.from_ts_pvrows_and_angles](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvground.py#L73) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | b1/r/yg |
| Output | cutpoints |
| Formula / rule | xcut=x1−(y1−yg)/tan(r) |
| Dependencies | GEO-05 |
| Edge cases | flat负零/inf |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_pvarray.py::test_coords_cut_points](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_pvarray.py#L465) |
| Known ambiguity | flat warning不是物理定义 |
| Proposed Rust module | geometry/ground |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-13｜Overlap & complement

| Field | Specification |
|---|---|
| Purpose | 构造无重叠明暗覆盖 |
| Python source | [pvfactors/geometry/pvground.py::TsGround.from_ordered_shadows_coords](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvground.py#L132) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | shadows/overlap flag/extent |
| Output | shadow/illum elements |
| Formula / rule | 重叠时前shadow右=后shadow左，再clip并取补集 |
| Dependencies | GEO-10 GEO-11 |
| Edge cases | 出界/端点接触/全遮 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_timeseries.py::test_ts_ground_overlap](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_timeseries.py#L168) |
| Known ambiguity | 仅ordered假设；非通用polygon union |
| Proposed Rust module | geometry/ground |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-14｜Ground per-cut slots

| Field | Specification |
|---|---|
| Purpose | 创建VF可见分区 |
| Python source | [pvfactors/geometry/pvground.py::TsGroundElement._create_all_ts_surfaces](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvground.py#L898) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | element/N cuts |
| Output | N+1 slots per element |
| Formula / rule | left/right clipping；Sg=(2N+1)(N+1) |
| Dependencies | GEO-12 GEO-13 |
| Edge cases | 重复cut/空槽 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_timeseries.py::test_ts_ground_elements_surfaces](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_timeseries.py#L301) |
| Known ambiguity | O(N²)logicalslots DEV-006 |
| Proposed Rust module | geometry/ground |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-15｜Containment

| Field | Specification |
|---|---|
| Purpose | 判定点容差内在线段上 |
| Python source | [pvfactors/geometry/utils.py::contains](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/utils.py#L74) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | segment/point/tol |
| Output | bool |
| Formula / rule | dwithin含端点；不是topological contains |
| Dependencies | GEO-01 MATH-04 |
| Edge cases | 端点/微偏线/零长 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_utils.py::test_contains_on_side](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_utils.py#L113) |
| Known ambiguity | GIS同名函数语义不同 |
| Proposed Rust module | geometry/kernel |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-16｜Collinearity

| Field | Specification |
|---|---|
| Purpose | 验证同线分区 |
| Python source | [pvfactors/geometry/utils.py::are_2d_vecs_collinear](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/utils.py#L110) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | normals/elements |
| Output | bool/error |
| Formula / rule | 参考未归一normal叉积/点积判定；Rust应加支撑线offset检查 |
| Dependencies | GEO-01 MATH-04 |
| Edge cases | 平行不同线/反向/零normal |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_base.py::test_baseside](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L11) |
| Known ambiguity | normal相同不足以证明共线 |
| Proposed Rust module | geometry/kernel |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-17｜Line difference

| Field | Specification |
|---|---|
| Purpose | 共线线段相减 |
| Python source | [pvfactors/geometry/utils.py::difference](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/utils.py#L10) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | u/v |
| Output | 0/1/2segments |
| Formula / rule | 数学上参数区间差；参考端点分支逐项比对 |
| Dependencies | GEO-15 GEO-16 |
| Edge cases | v全盖u/反向/接触 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_utils.py::test_difference](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_utils.py#L43) |
| Known ambiguity | 全覆盖分支已重现DEV-016 |
| Proposed Rust module | geometry/kernel |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-18｜Projection/intersection

| Field | Specification |
|---|---|
| Purpose | 沿向量投影至线 |
| Python source | [pvfactors/geometry/utils.py::projection](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/utils.py#L117) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | point/vector/segment/must_contain |
| Output | point或empty |
| Formula / rule | P+tV=A+uD；cross比求解；contain检查u∈[0,1] |
| Dependencies | GEO-15 GEO-16 |
| Edge cases | parallel/collinear/zero vector |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_utils.py::test_projection](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_utils.py#L6) |
| Known ambiguity | 参考2×2inverse无需复制 |
| Proposed Rust module | geometry/kernel |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-19｜Cast/cut/merge

| Field | Specification |
|---|---|
| Purpose | 静态面分区辅助操作 |
| Python source | [pvfactors/geometry/base.py::PVSegment.cast_shadow](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/base.py#L759) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | segment/shadow/cutpoint |
| Output | updated collections |
| Formula / rule | buffer(tol)防舍入相交，illum差集，shade并入；同线相邻linemerge |
| Dependencies | GEO-17 GEO-18 GEO-04 |
| Edge cases | touch/多段/不同params |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_base.py::test_cast_shadow_segment_precision_error](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L155)；[pvfactors/tests/test_geometry/test_base.py::test_merge_shadecollection](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L182)；[pvfactors/tests/test_geometry/test_base.py::test_shadecol_cut_at_point](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_base.py#L223) |
| Known ambiguity | 不是要求重写GEOS topology |
| Proposed Rust module | geometry/partition |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## GEO-20｜Ground snapshot/degeneracy

| Field | Specification |
|---|---|
| Purpose | 按指定时点提取活跃面 |
| Python source | [pvfactors/geometry/pvground.py::TsGround.non_point_shaded_surfaces_at](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvground.py#L510) |
| Mathematical / physical source | A：欧氏线段、射线与区间集合；B：Ordered阵列与分区规则。03 M01–M02、05。 |
| Input | idx/elements |
| Output | nonempty surfaces |
| Formula / rule | 参考两个helper错误传idx0；正确按idx并保留keys |
| Dependencies | GEO-07 GEO-14 |
| Edge cases | idx>0活动集合变化 |
| Tolerance behavior | position/length/angle分别比较；参考1e−8 active/contains与1e−5方向语义保留原比较符；index与partition精确。 |
| Existing upstream tests | [pvfactors/tests/test_geometry/test_timeseries.py::test_ts_ground_to_geometry](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_geometry/test_timeseries.py#L186) |
| Known ambiguity | DEV-013无针对该bug专项测试 |
| Proposed Rust module | geometry/frame |
| Expected validation | L1几何解析与集合关系；L2分区/坐标/keys；L3长度/阴影守恒；L4边界；L5镜像/切块。 |

## VF-01｜Hottel crossed-string

| Field | Specification |
|---|---|
| Purpose | 无限条带几何交换 |
| Python source | [pvfactors/viewfactors/vfmethods.py::VFTsMethods._vf_surface_to_surface](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/vfmethods.py#L585) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | two segments/Lreceiver |
| Output | Fij |
| Formula / rule | M06 crossed−uncrossed弦长差绝对值/(2L) |
| Dependencies | GEO-01 |
| Edge cases | 相向性由caller保证/smallL |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_timeseries.py::test_vf_pvrow_to_gnd_surf_obstruction_hottel](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_timeseries.py#L5) |
| Known ambiguity | 近等弦长相消 |
| Proposed Rust module | viewfactor/hottel |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-02｜PV→PV

| Field | Specification |
|---|---|
| Purpose | 填邻排相向VF |
| Python source | [pvfactors/viewfactors/vfmethods.py::VFTsMethods.vf_pvrow_to_pvrow](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/vfmethods.py#L185) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | rows/tilt |
| Output | pair matrix entries |
| Formula / rule | r>0连leftback-rightfront，否则leftfront-rightback；互易回填 |
| Dependencies | VF-01 GEO-08 |
| Edge cases | edge/zero slots/flat |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_calculator.py::test_ts_view_factors](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_calculator.py#L99) |
| Known ambiguity | 不适用非平行任意阵列 |
| Proposed Rust module | viewfactor/ordered |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-03｜Obstructed strings

| Field | Specification |
|---|---|
| Purpose | 遮挡下有效弦长 |
| Python source | [pvfactors/viewfactors/vfmethods.py::VFTsMethods._hottel_string_length](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/vfmethods.py#L540) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | ground/PV/obstruction/side |
| Output | string length |
| Formula / rule | 左alphaPV>alphaOb或右<时经障碍点两段，否则直线 |
| Dependencies | GEO-01 MATH-03 |
| Edge cases | 视线共线/missingneighbor |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_timeseries.py::test_vf_pvrow_to_gnd_surf_obstruction_hottel](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_timeseries.py#L5) |
| Known ambiguity | obstruction用最低端非最高端 |
| Proposed Rust module | viewfactor/obstruction |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-04｜PV→Ground

| Field | Specification |
|---|---|
| Purpose | 半地面与邻排挡光交换 |
| Python source | [pvfactors/viewfactors/vfmethods.py::VFTsMethods.vf_pvrow_surf_to_gnd_surf_obstruction_hottel](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/vfmethods.py#L105) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | PVslot/groundslot/row/tilt |
| Output | Fpv,gnd |
| Formula / rule | 边排直Hottel；内排M06 signed弦式；front/back×left/right mask |
| Dependencies | VF-01 VF-03 GEO-14 |
| Edge cases | finiteextent/flat/smallfaces |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_timeseries.py::test_vf_pvrow_to_gnd_surf_obstruction_hottel](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_timeseries.py#L5) |
| Known ambiguity | extent模型DEV-004 |
| Proposed Rust module | viewfactor/ordered |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-05｜Reciprocity / ground→PV

| Field | Specification |
|---|---|
| Purpose | 一致反向交换 |
| Python source | [pvfactors/viewfactors/vfmethods.py::VFTsMethods.vf_pvrow_surf_to_gnd_surf_obstruction_hottel](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/vfmethods.py#L105) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | Fij/Li/Lj |
| Output | Fji |
| Formula / rule | Fji=FijLi/Lj，Lj>tol否则0 |
| Dependencies | VF-04 |
| Edge cases | Lj0/巨大长度比 |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_calculator.py::test_ts_view_factors](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_calculator.py#L99) |
| Known ambiguity | sky不适用互易 |
| Proposed Rust module | viewfactor/matrix |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-06｜Sky / VF matrix

| Field | Specification |
|---|---|
| Purpose | 补齐边界源与顺序 |
| Python source | [pvfactors/viewfactors/calculator.py::VFCalculator.build_ts_vf_matrix](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/calculator.py#L69) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | physical F/lengths |
| Output | F(S+1)² |
| Formula / rule | active Fisky=1−ΣFij；zero slots sky0；sky row0 |
| Dependencies | VF-02 VF-04 GEO-08 |
| Edge cases | smallnegative residual/zeroslots |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_calculator.py::test_ts_view_factors](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_calculator.py#L99) |
| Known ambiguity | 不得为满足bounds盲clip |
| Proposed Rust module | viewfactor/matrix |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-07｜AOI quadrature basis

| Field | Specification |
|---|---|
| Purpose | 预计算切线角吸收积分 |
| Python source | [pvfactors/viewfactors/aoimethods.py::AOIMethods.fit](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/aoimethods.py#L52) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | f_front/back/J |
| Output | bins/integrands |
| Formula / rule | 0…180 J等分，f(mid)·.5abs(coslo−coshi) |
| Dependencies | MATH-01 |
| Edge cases | J0/f越界/非有限 |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_aoi_methods.py::test_vf](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_aoi_methods.py#L83)；[pvfactors/tests/test_viewfactors/test_aoi_methods.py::test_calculate_aoi_angles](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_aoi_methods.py#L95) |
| Known ambiguity | f为吸收修正而非自动绝对IAM |
| Proposed Rust module | viewfactor/aoi |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-08｜AOI wedge / obstruction

| Field | Specification |
|---|---|
| Purpose | PV接收面吸收VF |
| Python source | [pvfactors/viewfactors/aoimethods.py::AOIMethods._calculate_vf_aoi_wedge_level](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/aoimethods.py#L468) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | centroid/tangent/target/obstruction |
| Output | Gpv,pv/Gpv,gnd |
| Formula / rule | acos切线角；障碍角裁剪；wedge触格计整格，M07 |
| Dependencies | VF-07 VF-03 |
| Edge cases | wedge端点/zeroarea/bin touch |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_aoi_methods.py::test_vf_aoi_pvrow_gnd_benchmark_with_obstruction](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_aoi_methods.py#L168) |
| Known ambiguity | DEV-011近似，G≤F非严格成立 |
| Proposed Rust module | viewfactor/aoi |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-09｜AOI sky

| Field | Specification |
|---|---|
| Purpose | 吸收加权天空项 |
| Python source | [pvfactors/viewfactors/aoimethods.py::AOIMethods.vf_aoi_pvrow_to_sky](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/aoimethods.py#L84) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | rowhighs/extent/tilt |
| Output | Gpv,sky |
| Formula / rule | 邻排最高端与边界ground构造sky proxies再积分 |
| Dependencies | VF-08 GEO-05 |
| Edge cases | N1/flat/edges |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_aoi_methods.py::test_vf_aoi_pvrow_to_sky](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_aoi_methods.py#L276) |
| Known ambiguity | 不是简单1−ΣG |
| Proposed Rust module | viewfactor/aoi |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-10｜AOI matrix

| Field | Specification |
|---|---|
| Purpose | 隔离几何与吸收核 |
| Python source | [pvfactors/viewfactors/calculator.py::VFCalculator.build_ts_vf_aoi_matrix](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/calculator.py#L116) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | F/rho/fAOI |
| Output | G |
| Formula / rule | default (1−rho_receiver)F；custom替换PVrows |
| Dependencies | VF-06 VF-08 VF-09 |
| Edge cases | onecallback/albedo0/groundrows |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_calculator.py::test_vfcalculator_aoi_methods](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_calculator.py#L35)；[pvfactors/tests/test_viewfactors/test_calculator.py::test_vfcalculator_no_aoi_functions](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_calculator.py#L72) |
| Known ambiguity | DEV-009/010/017 |
| Proposed Rust module | viewfactor/matrix |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-11｜Effective reflectivity

| Field | Specification |
|---|---|
| Purpose | 吸收曲线推均匀ρ |
| Python source | [pvfactors/viewfactors/aoimethods.py::AOIMethods.rho_from_faoi_fn](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/aoimethods.py#L614) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | f/bins |
| Output | rho_front/back |
| Formula / rule | 1−Σf(mid)weight；显式初始化才选该ρ |
| Dependencies | VF-07 |
| Edge cases | f0/f1/越界 |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_aoi_methods.py::test_rho_from_faoi_fn](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_aoi_methods.py#L315) |
| Known ambiguity | 不是所有构造器自动初始化 |
| Proposed Rust module | irradiance/optics |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## VF-12｜Fast grouped VF

| Field | Specification |
|---|---|
| Purpose | 分组环境可见因子 |
| Python source | [pvfactors/viewfactors/calculator.py::VFCalculator.get_vf_ts_pvrow_element](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/calculator.py#L183) |
| Mathematical / physical source | A：Hottel条带交换/互易、半球积分；B：ordered遮挡、AOI近似。03 M06–M07/M09。 |
| Input | targetback/rows/shadows |
| Output | Fgshade/Fgillum/Fpvshade/Fpvillum/Fsky |
| Formula / rule | M09ground代理段与shadowHottel；邻排shade；剩余illum/sky |
| Dependencies | VF-01 VF-03 GEO-11 |
| Edge cases | edge/segment/zerolength |
| Tolerance behavior | 几何F用独立absolute+relative，长度≤tol归零；AOI整格近似误差与舍入误差分开，不统一clip。 |
| Existing upstream tests | [pvfactors/tests/test_engine.py::test_run_fast_mode_segments](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L230)；[pvfactors/tests/test_engine.py::test_run_fast_mode_back_shading](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L281) |
| Known ambiguity | 与Full不同近似层 |
| Proposed Rust module | viewfactor/fast |
| Expected validation | L1解析条带/常数吸收；L2逐矩阵；L3几何bounds/reciprocity/closure（G按M07前提）；L5镜像/求积收敛。 |

## IRR-01｜Input normalization

| Field | Specification |
|---|---|
| Purpose | 建立输入时间轴 |
| Python source | [pvfactors/engine.py::PVEngine.fit](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/engine.py#L109) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | scalar/arrays/timestamps/GHI |
| Output | normalized vectors/T |
| Formula / rule | 参考DNI scalar分支、albedo广播；Rust显式shape合同 |
| Dependencies | 无 |
| Edge cases | NaN/空T/错长度/timezone |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_engine.py::test_pvengine_float_inputs_iso](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L12)；[pvfactors/tests/test_engine.py::test_pvengine_ts_inputs_perez](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L97) |
| Known ambiguity | DEV-018 |
| Proposed Rust module | simulation/input |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-02｜Extraterrestrial radiation

| Field | Specification |
|---|---|
| Purpose | Perez太阳通量归一化 |
| Python source | [pvfactors/irradiance/utils.py::perez_diffuse_luminance](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/utils.py#L15) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | dayofyear |
| Output | I0 W/m² |
| Formula / rule | M03 Spencer1366.1、365分母，pvlib default |
| Dependencies | MATH-01 IRR-01 |
| Edge cases | leapday/timezone跨日 |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_utils.py::test_perez_diffuse_luminance](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_utils.py#L7) |
| Known ambiguity | 上游无primitive独立测试 |
| Proposed Rust module | irradiance/primitives |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-03｜Relative airmass

| Field | Specification |
|---|---|
| Purpose | Perez亮度指标 |
| Python source | [pvfactors/irradiance/utils.py::perez_diffuse_luminance](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/utils.py#L15) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | z |
| Output | m |
| Formula / rule | M03 KastenYoung1989；z>90 NaN |
| Dependencies | MATH-01 |
| Edge cases | 90边界/night |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_utils.py::test_perez_diffuse_luminance](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_utils.py#L7) |
| Known ambiguity | 不是压力修正absoluteairmass |
| Proposed Rust module | irradiance/primitives |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-04｜AOI / hemisphere

| Field | Specification |
|---|---|
| Purpose | 确定正背受光 |
| Python source | [pvfactors/irradiance/models.py::HybridPerezOrdered._calculate_luminance_poa_components](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/models.py#L950) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | sun/surface angles |
| Output | mu/AOIf/AOIb |
| Formula / rule | M01 dotclip；back=180−front；≤90为受光 |
| Dependencies | MATH-01 MATH-02 |
| Edge cases | near90/roundoff |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_models.py::test_hybridperez_ordered_back](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_models.py#L454) |
| Known ambiguity | DEV-001递归与CDR-002 |
| Proposed Rust module | irradiance/primitives |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-05｜Perez decomposition

| Field | Specification |
|---|---|
| Purpose | 三diffuse分量 |
| Python source | [pvfactors/irradiance/utils.py::perez_diffuse_luminance](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/utils.py#L15) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | DNI/DHI/I0/m/angles |
| Output | ε/Δ/bin/F1/F2/POA |
| Formula / rule | M04八bins表；F1≥0，F2带符号，b≥cos85，总量clamp与清零 |
| Dependencies | IRR-02 IRR-03 IRR-04 |
| Edge cases | DHI0/both0/F1>1/binthreshold |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_utils.py::test_perez_diffuse_luminance](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_utils.py#L7) |
| Known ambiguity | 论文0.087vs软件cos85；DEV-012/024 |
| Proposed Rust module | irradiance/perez |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-06｜Luminance/back conversion

| Field | Specification |
|---|---|
| Purpose | Perez标量映射到各面 |
| Python source | [pvfactors/irradiance/utils.py::perez_diffuse_luminance](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/utils.py#L15) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | POA/geometricdivisors |
| Output | Liso/Lcirc/Lhor/backcirc |
| Formula / rule | M04分量除对应VF；背面递归取Lcirc，backcirc除cosz |
| Dependencies | IRR-05 |
| Edge cases | 零分母/flat/backlowSun |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_models.py::test_hybridperez_ordered_back](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_models.py#L454) |
| Known ambiguity | DEV-001/012 |
| Proposed Rust module | irradiance/perez |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-07｜IsotropicOrdered

| Field | Specification |
|---|---|
| Purpose | 各向同性源项 |
| Python source | [pvfactors/irradiance/models.py::IsotropicOrdered.fit](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/models.py#L84) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | weather/angles/rho/tau/GHI |
| Output | E/Lsky/Penv |
| Formula / rule | M03/M05；skyDHI；litdirect与shadeτdirect |
| Dependencies | IRR-01 IRR-04 IRR-09 |
| Edge cases | zero光/frontback |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_models.py::test_isotropic_model_front](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_models.py#L33)；[pvfactors/tests/test_irradiance/test_models.py::test_isotropic_model_back](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_models.py#L153) |
| Known ambiguity | Fastshadeτ缺项DEV-015 |
| Proposed Rust module | irradiance/isotropic |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-08｜HybridPerezOrdered

| Field | Specification |
|---|---|
| Purpose | 混合天空模型源项 |
| Python source | [pvfactors/irradiance/models.py::HybridPerezOrdered.fit](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/models.py#L480) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | weather/angles/optics |
| Output | direct/circ/horizon/E/Lsky |
| Formula / rule | M05逐面表；horizon取abs；Penv实际isotropic |
| Dependencies | IRR-05 IRR-06 IRR-09 |
| Edge cases | nearhorizon/负分量 |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_models.py::test_hybridperez_ordered_front](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_models.py#L273)；[pvfactors/tests/test_irradiance/test_models.py::test_hybridperez_ordered_back](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_models.py#L454) |
| Known ambiguity | DEV-012/015 |
| Proposed Rust module | irradiance/hybrid |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-09｜Transmission/albedo/rho

| Field | Specification |
|---|---|
| Purpose | 经验透射和漫反射参数 |
| Python source | [pvfactors/irradiance/models.py::HybridPerezOrdered.fit](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/models.py#L480) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | spacing/transparency/albedo/rho |
| Output | tau/rho arrays |
| Formula / rule | τ=s+(1−s)t；groundρ=albedo，front.01/back.03默认 |
| Dependencies | IRR-01 |
| Edge cases | ρ0/1、τ0/1、seriesalbedo |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_models.py::test_isotropic_ordered_transparency_spacing](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_models.py#L854)；[pvfactors/tests/test_irradiance/test_models.py::test_hybridperez_ordered_transparency_spacing_back](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_models.py#L804) |
| Known ambiguity | ρ与fAOI语义需一致 |
| Proposed Rust module | irradiance/optics |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-10｜Horizon band shading

| Field | Specification |
|---|---|
| Purpose | 地平线diffuse遮挡 |
| Python source | [pvfactors/irradiance/models.py::HybridPerezOrdered._calculate_horizon_shading_pct_ts](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/models.py#L848) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | surfacecentroid/neighborhigh/r/band |
| Output | hshade/Hback |
| Formula / rule | atan(abs(dy/dx))，clip(angle/band)，无邻居0，仅back |
| Dependencies | GEO-05 IRR-08 |
| Edge cases | dx0/front未遮/cut变化 |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_models.py::test_hybridperez_horizon_shading_ts](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_models.py#L651) |
| Known ambiguity | confirmedDEV-005 |
| Proposed Rust module | irradiance/shading |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-11｜Circumsolar disk/Gaussian

| Field | Specification |
|---|---|
| Purpose | 解释非主链辅助能力 |
| Python source | [pvfactors/irradiance/utils.py::calculate_circumsolar_shading](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/utils.py#L176) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | percentdistance/model |
| Output | percentarea遮挡 |
| Formula / rule | M05圆缺面积或截断±3σ erf归一CDF |
| Dependencies | MATH-01 |
| Edge cases | <0/>100/未知model |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_utils.py::test_calculate_circumsolar_shading](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_utils.py#L28) |
| Known ambiguity | DEV-014未用于fit/transform；neighborNone私有helper缺赋值 |
| Proposed Rust module | irradiance/shading(扩展候选) |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-12｜Absorbed source/AOI

| Field | Specification |
|---|---|
| Purpose | 源分量吸收 |
| Python source | [pvfactors/irradiance/models.py::HybridPerezOrdered._calculate_faoi_modifiers](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/models.py#L1021) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | AOI/tilt/f/rho/Ecomponents |
| Output | Eabs |
| Formula / rule | direct/circ乘f(abs90−AOI)，horizon乘f(tilt)，ground1albedo |
| Dependencies | IRR-04 IRR-08 IRR-09 |
| Edge cases | onecallback/f越界 |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_engine.py::test_engine_w_faoi_fn_in_irradiance_vfcalcs](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L622) |
| Known ambiguity | 不等于最终qabs乘IAM |
| Proposed Rust module | irradiance/absorption |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## IRR-13｜SAPM convenience

| Field | Specification |
|---|---|
| Purpose | 拆解可选pvlib数据库依赖 |
| Python source | [pvfactors/viewfactors/aoimethods.py::faoi_fn_from_pvlib_sandia](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/viewfactors/aoimethods.py#L647) |
| Mathematical / physical source | A：Perez 1990与经验primitive；B：pvlib0.14默认与Hybrid/Isotropic组装。03 M03–M05；04实际调用边界。 |
| Input | B0…B5/angle或modulename |
| Output | f曲线 |
| Formula / rule | tangent转abs90−angle，五次poly clip0..1；retrieve_sam仅取数 |
| Dependencies | MATH-01 |
| Edge cases | NaN/90+ |
| Tolerance behavior | 输入shape/bin/状态精确；角、无量纲primitive、W/m²分量分别absolute+relative；NaN分类登记。 |
| Existing upstream tests | [pvfactors/tests/test_viewfactors/test_aoi_methods.py::test_faoi_fn_from_pvlib](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_viewfactors/test_aoi_methods.py#L9) |
| Known ambiguity | Core接coeff不携整库数据库 |
| Proposed Rust module | irradiance/optics |
| Expected validation | L1公式/系数/边界；L2逐分量/primitive；L3限定域非负/吸收；L4 bins/零光；L6模型选择。 |

## ENG-01｜Transform to surfaces

| Field | Specification |
|---|---|
| Purpose | 将类别源映射到面 |
| Python source | [pvfactors/irradiance/models.py::HybridPerezOrdered.transform](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/models.py#L626) |
| Mathematical / physical source | A：短波线性能量交换与面积加权；B：source映射/Full/Fast近似。03 M05、M08–M10。 |
| Input | modelvectors/pvarray |
| Output | surface params |
| Formula / rule | ground明暗分类；PV逐面horizon与absorbed更新；sky不重复加 |
| Dependencies | GEO-08 IRR-07 IRR-08 IRR-10 IRR-12 |
| Edge cases | 零长/同排多cut |
| Tolerance behavior | system residual、q0/qinc/qabs与aggregate分别预算；shape/index/status精确；bug字段仅CDR限定waiver。 |
| Existing upstream tests | [pvfactors/tests/test_irradiance/test_models.py::test_hybridperez_transform](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_irradiance/test_models.py#L690) |
| Known ambiguity | Python mutation非Core要求 |
| Proposed Rust module | simulation/frame |
| Expected validation | L1小系统/代数恒等；L2中间/最终向量；L3残差/能量；L5分块/透射极限；L6接口。 |

## ENG-02｜Irradiance/rho matrices

| Field | Specification |
|---|---|
| Purpose | 装配radiosity输入 |
| Python source | [pvfactors/irradiance/base.py::BaseModel.get_ts_modeling_vectors](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/irradiance/base.py#L49) |
| Mathematical / physical source | A：短波线性能量交换与面积加权；B：source映射/Full/Fast近似。03 M05、M08–M10。 |
| Input | surfaceparams/sky |
| Output | E/rho/invrho/Eabs |
| Formula / rule | M08索引顺序；skyρ1和E=Lsky |
| Dependencies | ENG-01 VF-06 |
| Edge cases | rho0/sky索引 |
| Tolerance behavior | system residual、q0/qinc/qabs与aggregate分别预算；shape/index/status精确；bug字段仅CDR限定waiver。 |
| Existing upstream tests | [pvfactors/tests/test_engine.py::test_pvengine_float_inputs_perez](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L51) |
| Known ambiguity | DEV-008逆ρ奇异 |
| Proposed Rust module | radiosity/assembly |
| Expected validation | L1小系统/代数恒等；L2中间/最终向量；L3残差/能量；L5分块/透射极限；L6接口。 |

## ENG-03｜Full radiosity solve

| Field | Specification |
|---|---|
| Purpose | 多次反射系统求解 |
| Python source | [pvfactors/engine.py::PVEngine.run_full_mode](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/engine.py#L177) |
| Mathematical / physical source | A：短波线性能量交换与面积加权；B：source映射/Full/Fast近似。03 M05、M08–M10。 |
| Input | E/F/R |
| Output | q0/qinc |
| Formula / rule | 参考inv(diag1ρ−F)E；Rust解(I−FR)qin=b后q0=Rqin |
| Dependencies | ENG-02 |
| Edge cases | rho0/near1/singular/emptyactive |
| Tolerance behavior | system residual、q0/qinc/qabs与aggregate分别预算；shape/index/status精确；bug字段仅CDR限定waiver。 |
| Existing upstream tests | [pvfactors/tests/test_engine.py::test_pvengine_ts_inputs_perez](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L97) |
| Known ambiguity | inverse是C层；DEV-008 |
| Proposed Rust module | radiosity/solve |
| Expected validation | L1小系统/代数恒等；L2中间/最终向量；L3残差/能量；L5分块/透射极限；L6接口。 |

## ENG-04｜Incident decomposition

| Field | Specification |
|---|---|
| Purpose | 分离sky与反射 |
| Python source | [pvfactors/engine.py::PVEngine.run_full_mode](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/engine.py#L177) |
| Mathematical / physical source | A：短波线性能量交换与面积加权；B：source映射/Full/Fast近似。03 M05、M08–M10。 |
| Input | solution/E/Fsky/Lsky |
| Output | qinc/isotropic/reflection |
| Formula / rule | qinc=E+Fq0；iso=FskyL；reflection=qinc−E−iso |
| Dependencies | ENG-03 |
| Edge cases | 全零/nearzero相减 |
| Tolerance behavior | system residual、q0/qinc/qabs与aggregate分别预算；shape/index/status精确；bug字段仅CDR限定waiver。 |
| Existing upstream tests | [pvfactors/tests/test_engine.py::test_pvengine_float_inputs_iso](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L12) |
| Known ambiguity | direct/circ/horizon不能重复加sky |
| Proposed Rust module | radiosity/output |
| Expected validation | L1小系统/代数恒等；L2中间/最终向量；L3残差/能量；L5分块/透射极限；L6接口。 |

## ENG-05｜qabs/surface update

| Field | Specification |
|---|---|
| Purpose | 总吸收与面结果 |
| Python source | [pvfactors/engine.py::PVEngine.run_full_mode](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/engine.py#L177) |
| Mathematical / physical source | A：短波线性能量交换与面积加权；B：source映射/Full/Fast近似。03 M05、M08–M10。 |
| Input | G/q0/Eabs |
| Output | qabs与面字段 |
| Formula / rule | qabs=Gq0+Eabs；发布q0/qinc/isotropic/reflection/qabs |
| Dependencies | ENG-03 VF-10 IRR-12 |
| Edge cases | customAOIground/Falias |
| Tolerance behavior | system residual、q0/qinc/qabs与aggregate分别预算；shape/index/status精确；bug字段仅CDR限定waiver。 |
| Existing upstream tests | [pvfactors/tests/test_engine.py::test_engine_w_faoi_fn_in_irradiance_vfcalcs](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L622) |
| Known ambiguity | DEV-009/010 |
| Proposed Rust module | radiosity/output |
| Expected validation | L1小系统/代数恒等；L2中间/最终向量；L3残差/能量；L5分块/透射极限；L6接口。 |

## ENG-06｜Fast/row/segment selection

| Field | Specification |
|---|---|
| Purpose | 背面环境单次反射近似 |
| Python source | [pvfactors/engine.py::PVEngine.run_fast_mode](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/engine.py#L267) |
| Mathematical / physical source | A：短波线性能量交换与面积加权；B：source映射/Full/Fast近似。03 M05、M08–M10。 |
| Input | targetrow/segment/Penv/Fgroups |
| Output | selectedqinc/isotropic/reflection |
| Formula / rule | M09四环境源加sky与Eback；不求Fullq0/qabs |
| Dependencies | VF-12 IRR-07 IRR-08 |
| Edge cases | 非法selection/未求字段 |
| Tolerance behavior | system residual、q0/qinc/qabs与aggregate分别预算；shape/index/status精确；bug字段仅CDR限定waiver。 |
| Existing upstream tests | [pvfactors/tests/test_engine.py::test_run_fast_mode_isotropic](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L134)；[pvfactors/tests/test_engine.py::test_run_fast_mode_perez](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L183)；[pvfactors/tests/test_engine.py::test_run_fast_mode_segments](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L230) |
| Known ambiguity | Fast与Full不是严格等价 |
| Proposed Rust module | simulation/fast |
| Expected validation | L1小系统/代数恒等；L2中间/最终向量；L3残差/能量；L5分块/透射极限；L6接口。 |

## ENG-07｜Weighted aggregation

| Field | Specification |
|---|---|
| Purpose | 面→segment→side→row |
| Python source | [pvfactors/geometry/pvrow.py::TsSide.get_param_weighted](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/geometry/pvrow.py#L419) |
| Mathematical / physical source | A：短波线性能量交换与面积加权；B：source映射/Full/Fast近似。03 M05、M08–M10。 |
| Input | Li/qi/keys |
| Output | weightedmean/weighted sum |
| Formula / rule | ΣLi qi/ΣLi；保留length及sum供汇总 |
| Dependencies | GEO-09 ENG-04 ENG-05 |
| Edge cases | zero totals/活跃NaN |
| Tolerance behavior | system residual、q0/qinc/qabs与aggregate分别预算；shape/index/status精确；bug字段仅CDR限定waiver。 |
| Existing upstream tests | [pvfactors/tests/test_run.py::test_run_timeseries_engine](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_run.py#L8) |
| Known ambiguity | 任意callback报告不是Corecontract |
| Proposed Rust module | simulation/report |
| Expected validation | L1小系统/代数恒等；L2中间/最终向量；L3残差/能量；L5分块/透射极限；L6接口。 |

## ENG-08｜Skip/input status

| Field | Specification |
|---|---|
| Purpose | 明确有效时点与捷径 |
| Python source | [pvfactors/engine.py::PVEngine.fit](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/engine.py#L109) |
| Mathematical / physical source | A：短波线性能量交换与面积加权；B：source映射/Full/Fast近似。03 M05、M08–M10。 |
| Input | z/DNI/DHI/GHI/geometry |
| Output | status/effectiveT |
| Formula / rule | 参考mask未消费；Core按M10/CDR-001前置分类 |
| Dependencies | IRR-01 |
| Edge cases | z90/night/全零但GHI>0 |
| Tolerance behavior | system residual、q0/qinc/qabs与aggregate分别预算；shape/index/status精确；bug字段仅CDR限定waiver。 |
| Existing upstream tests | [pvfactors/tests/test_engine.py::test_check_tilt_zero_discontinuity](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_engine.py#L565) |
| Known ambiguity | 无skip专项；DEV-003/007 |
| Proposed Rust module | simulation/input |
| Expected validation | L1小系统/代数恒等；L2中间/最终向量；L3残差/能量；L5分块/透射极限；L6接口。 |

## EXEC-01｜Serial execution

| Field | Specification |
|---|---|
| Purpose | 时序Reference主流程 |
| Python source | [pvfactors/run.py::run_timeseries_engine](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/run.py#L19) |
| Mathematical / physical source | C：Python批处理/进程/报告机制，不是新物理模型。11与run.py。 |
| Input | inputs/config/reportfn |
| Output | report |
| Formula / rule | construct→fit→Full/Fast→callback；整批数组驻留 |
| Dependencies | ENG-01 ENG-03 ENG-06 ENG-07 |
| Edge cases | largeT/callbackmutation |
| Tolerance behavior | 结果沿用物理输出各profile，时间顺序/shape/status精确一致；同kernel优先固定归约。 |
| Existing upstream tests | [pvfactors/tests/test_run.py::test_run_timeseries_engine](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_run.py#L8)；[pvfactors/tests/test_run.py::test_run_timeseries_engine_fast_mode](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_run.py#L41) |
| Known ambiguity | 不是逐时低内存streaming |
| Proposed Rust module | execution/serial |
| Expected validation | L5 Serial/Parallel/chunk等价和原序；L6错误/选择/合并；11资源诊断与memory Gate。 |

## EXEC-02｜Multiprocessing split

| Field | Specification |
|---|---|
| Purpose | 解释上游并行分块 |
| Python source | [pvfactors/run.py::run_parallel_engine](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/run.py#L117) |
| Mathematical / physical source | C：Python批处理/进程/报告机制，不是新物理模型。11与run.py。 |
| Input | batch/nprocess/config |
| Output | process reports |
| Formula / rule | array_split全部输入；Pool.map；chunk独立engine |
| Dependencies | EXEC-01 |
| Edge cases | nproc>T/emptychunk/pickle/GHI |
| Tolerance behavior | 结果沿用物理输出各profile，时间顺序/shape/status精确一致；同kernel优先固定归约。 |
| Existing upstream tests | [pvfactors/tests/test_run.py::test_run_parallel_engine_with_ghi](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_run.py#L155)；[pvfactors/tests/test_run.py::test_run_parallel_faoi_fn](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_run.py#L309) |
| Known ambiguity | DEV-025；Rust不复制双API |
| Proposed Rust module | execution/outer |
| Expected validation | L5 Serial/Parallel/chunk等价和原序；L6错误/选择/合并；11资源诊断与memory Gate。 |

## EXEC-03｜Report merge

| Field | Specification |
|---|---|
| Purpose | 恢复原时序顺序 |
| Python source | [pvfactors/run.py::_run_serially](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/run.py#L261) |
| Mathematical / physical source | C：Python批处理/进程/报告机制，不是新物理模型。11与run.py。 |
| Input | chunkindex/reports |
| Output | orderedreport |
| Formula / rule | 排序chunkindex后builder.merge；Rust直接按原index写回 |
| Dependencies | EXEC-02 ENG-07 |
| Edge cases | 非结合merge/重复timestamp |
| Tolerance behavior | 结果沿用物理输出各profile，时间顺序/shape/status精确一致；同kernel优先固定归约。 |
| Existing upstream tests | [pvfactors/tests/test_run.py::test_run_parallel_engine_with_irradiance_params](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/tests/test_run.py#L100) |
| Known ambiguity | callback格式outofscope |
| Proposed Rust module | execution/output |
| Expected validation | L5 Serial/Parallel/chunk等价和原序；L6错误/选择/合并；11资源诊断与memory Gate。 |

## 非数值代码边界

plot.py及所有plot/plot_at_idx方法仅可视化；config绘图颜色、Matplotlib轴与index标注不纳入Core。property/getter、字典更新、DataFrame列名与wrapper异常归为C层，相关数学行为已映射到上述条目。BaseModel抽象方法不是额外模型；run callback不是计算权威。角度辅助、Gaussian工具、Fast组VF均已登记。

evidence/algorithm-inventory.json为本表机器可读副本；evidence/source-symbol-map.json列出核心源码所有class/function/method与负责的算法组或样板分类。映射是人工规格+AST索引，不冒充形式化程序覆盖证明。
