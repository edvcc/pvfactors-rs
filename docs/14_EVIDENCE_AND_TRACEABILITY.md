# 14｜Evidence & Traceability

核查截止2026-09-21。以下区分亲自获取/运行的证据、官方外部说明与尚未完成的工作。source及tests链接固定SHA；动态工具链文档只说明研究时能力，不是未来版本承诺。

## 本次实际取得与运行

| 证据 | 文件 | 实际范围 |
|---|---|---|
| Repo/default branch/HEAD/tags/releases/issues | evidence/upstream-metadata.json | main；v1.6.1 HEAD；3 tags、3 releases；41条issue/PR元数据及body |
| Issue comments补查 | evidence/issue-comments.json | #6/9/10/12/13/14/37；#14有新comment，其余查询为空 |
| 逐文件source snapshot | upstream/solarfactors；evidence/source-file-manifest.json | 78文件，全部Git blob SHA吻合；完整核心代码/全部上游测试与3CSV、理论/概念/release notes/CI/LICENSE；不含完整Git历史 |
| 算法索引 | evidence/algorithm-inventory.json；source-symbol-map.json | 60算法项；356个核心class/function/method AST条目分组；不把getter算新算法 |
| 实际pvlib调用 | evidence/pvlib-call-sites.json | 50处直接调用位置；按函数去重后闭包见04 |
| Canonical依赖/平台 | reference/requirements-linux-cp312.lock；evidence/runtime.json | 29包精确pin、wheel hash；Linux CPython3.12.14；NumPy BLAS配置 |
| 原环境上游测试 | evidence/upstream-pytest.txt | 102 passed，6 warnings，3.60s |
| 全新venv复测 | evidence/clean-upstream-pytest.txt | 同lock离线安装成功后102 passed，6 warnings，2.05s |
| 主链研究探针 | reference/generator/probe_reference.py；evidence/probe-results.json | 22个simulation case＋#6递归重现；不是已批准Corpus |
| 额外边界探针 | reference/generator/probe_boundaries.py；evidence/boundary-probes.json | difference完全覆盖bug、未归一collinearity尺度效应、自定义AOI地面吸收误差 |
| nominal中间trace | evidence/nominal-trace.npz | E/rho/invrho/F/A/G/q0/qinc/coords/lengths，原始reference轴；非全层schema成品 |
| Canonical cases与schema | reference/cases；reference/schemas | 67个具体配置＋6个必须展开的派生case家族；设计产物，不伪称全部已执行 |

测试时长是运行记录，不是benchmark或性能承诺。六条warning主要是flat时ground延长线除tan0；通过上游测试不能推导其未测边界无bug。全部source blob验证见最终artifact-checks.json。

## 关键实测（W/m²）

基准参数与时间完整保存在probe-results。row1，N3，w1/h1/gcr.5，z45、sun/surface az270、tilt45、DNI600/DHI100/albedo.25：

| case | 结果/含义 |
|---|---|
| nominal Hybrid Full | front qinc744.56628054，back qinc44.4145277403；back qabs43.0820919081 |
| Isotropic Full | back qinc53.35551506 |
| Hybrid Fast | target back qinc47.0655117328；不能拿Full值作严格oracle |
| Isotropic Fast | target back qinc60.4590372981 |
| cut row1 front3/back5 | back qinc47.4100043196；不是严格cut不变 |
| all zero Hybrid | active结果可NaN；Isotropic同零输入为0 |
| night z100 | back qinc−19.42755776，虽然skip_step=True |
| circumsolar angle5/60 | 该主链case输出相同，支持调用图显示未使用参数 |
| custom f=.8 | 原F在run后被覆盖，最大条目差0.1714254150 |
| custom AOI ground | G_ground=F_ground；qabs−.75qinc最大9.788216915，违反ground常数吸收预期 |
| custom difference | [0,1]减[−1,2]返回原长度1，而数学差集应空 |
| #6重现 | RecursionError |

## Primary sources 与阅读边界

| 编号 | 来源 | 支持的事实 / 限制 |
|---|---|---|
| S01 | [README与历史](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/README.rst) | SunPower/pvfactors维护fork、pvlib用途、论文引用 |
| S02 | [pyproject](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pyproject.toml) | 当前依赖下界，不推断具体运行数值 |
| S03 | [理论问题公式](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/docs/sphinx/theory/problem_formulation.rst) | radiosity、天空分量、吸收模型；以实际engine确认矩阵方向 |
| S04 | [VF理论](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/docs/sphinx/theory/view_factors.rst) | crossed-string/无限长条带与AOI积分背景 |
| S05 | [Perez et al. 1990 原文](https://archive-ouverte.unige.ch/unige:17206) | DOI10.1016/0038-092X(90)90055-H；已下载扫描PDF，视觉核对273页ε/Δ与281页式(9)、F2可负、b=.087；不复制整篇论文到交付包 |
| S06 | [pvlib0.14 irradiance源码](https://github.com/pvlib/pvlib-python/blob/v0.14.0/pvlib/irradiance.py) | 具体1990系数、b=cos85、zero/NaN、默认isotropic；本机安装源码摘录及许可证随包 |
| S07 | [pvlib0.14 atmosphere](https://github.com/pvlib/pvlib-python/blob/v0.14.0/pvlib/atmosphere.py) | KastenYoung1989默认、z>90分支 |
| S08 | [pvlib0.14 iam](https://github.com/pvlib/pvlib-python/blob/v0.14.0/pvlib/iam.py) | SAPM polynomial/clamp；SAM数据库helper是convenience |
| S09 | [Radiation Configuration Factors C-5a](https://www.thermalradiation.net/sectionc/C-5a.html) | 两无限长板的标准交换几何背景；源码弦式另做独立推导 |
| S10 | [上游release notes](https://solarfactors.readthedocs.io/en/stable/whatsnew.html) | fork/版本维护范围；包内rst固定版本，网页stable可能变化 |
| S11 | [PyO3 parallelism](https://pyo3.rs/main/parallelism)、[multiple versions/ABI](https://pyo3.rs/main/building-and-distribution/multiple-python-versions.html) | detach与多Python/abi3取舍；未因此冻结具体版本 |
| S12 | [rust-numpy borrow](https://docs.rs/numpy/latest/numpy/borrow/index.html) | Python侧alias写入不受Rust readonly借用完全保护 |
| S13 | [maturin distribution](https://www.maturin.rs/distribution.html) | mixed/wheel/manylinux工程方向，实际wheel尚未建 |
| S14 | [faer](https://docs.rs/faer/latest/faer/)、[nalgebra分解](https://www.nalgebra.rs/docs/user_guide/decompositions_and_lapack/) | native LU/QR候选、并行feature需控制；未进行Rustbackend性能排名 |

Anoma 2017《View Factor Model and Validation for Bifacial PV and Diffuse Shade on Single-Axis Trackers》原始链接来自README，本次HTTP403；Marion等2017《A Practical Irradiance Model for Bifacial PV Modules》（NREL/CP-5J00-67847）原始PDF本次502。没有声称全文核查完成。后续物理修正可通过取得原文或独立权威证据补齐；不以错误HTTP页面作为论文内容。历史Hottel原著未直接取得，本报告用官方理论、标准configuration背景和代数/几何推导标明证据层级。

## Issue/PR审阅覆盖

`evidence/issue-triage.json`逐条列出全部41条的type/state/title/url与本项目处置。数值/几何/模型/性能相关映射DEV；CI、readme、文档网站、打包与绘图事项保留为工程/非Core范围，不因没逐项写进08就未审阅。closed PR不自动等同merged；采用修复以冻结源码和release内容为准。

## 需求到文档

| 用户要求 | 交付位置 |
|---|---|
| 上游/版本/权威分层 | 00、14、evidence |
| Capability / V1边界 | 01 |
| Algorithm Inventory及源码/tests | 02、machine JSON/AST索引 |
| 数学/Full/Fast/源项/sky | 03 |
| pvlib/Shapely闭包 | 04、pvlib-call-sites |
| 专用Rust geometry契约 | 05 |
| Golden/Case Matrix/L1–L6/Governance | 06、reference目录 |
| 独立tolerance与标定 | 07 |
| Bugs/ambiguities/CDR | 08 |
| Rust模块/solver/performance顺序 | 09 |
| Python一级能力/ABI/wheels/GIL | 10 |
| Serial/parallel/Auto/cost/resource/diagnostics | 11 |
| 全阶段Inputs/Artifacts/Tests/Entry/Exit/Gates/DoD | 12 |
| 实施前独立证据评审 | 13 |

无Rust核心算法、最终solver、SIMD、scheduler PoC在本阶段生成。Python代码仅取证、复现与schema/case组织，未引入未来core runtime依赖。
