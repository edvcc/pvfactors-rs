# 00｜Reference Baseline

版本：v1.0；核查日期：2026-09-21。本文冻结本次研究的上游参照，后续不得随 main 漂移。

## 结论与证据等级

选用 **solarfactors v1.6.1，commit `ecbfc863657e239817603a43898ae173c7ccad9c`**。查询时默认分支为 `main`，HEAD 与该发布标签相同。选择依据是已发布、修复 pvlib 0.14 输出字段变化、已兼容 Shapely 2，并且本次实际取得全部核心源码、全部测试及测试输入，跑通测试；不是因为它恰好是 HEAD。

核查来源：[冻结提交](https://github.com/pvlib/solarfactors/commit/ecbfc863657e239817603a43898ae173c7ccad9c)、[release](https://github.com/pvlib/solarfactors/releases/tag/v1.6.1)、[项目说明](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/README.rst)。GitHub API 查询结果、文件 blob SHA、运行日志保存在 evidence。Git 克隆未完成，实际采用 GitHub 逐文件获取，不能把这份源码快照称为完整 Git 历史克隆。

| 标签 | commit | 判断 |
|---|---|---|
| v1.5.3 | c8411bfd7199f029e75a7e15cd21219df873ff70 | fork 首发；移除 pvlib 上界，旧 Shapely 路线 |
| v1.6.0 | 18b72e55be7f505a406b587579377edbc1b944db | Shapely 2 迁移，非当前默认 |
| v1.6.1 | ecbfc863657e239817603a43898ae173c7ccad9c | 本次冻结 |

v1.6.1 发布于 2026-01-15。当前 API issue 集合取得 41 条（含 PR），已区分问题与 PR。2026-09-07 新增的 PR #41 仍未合并，不能把它的正面 horizon 修正当作 v1.6.1 行为。

## 历史与维护目标

SunPower 的 vf_model 后演变为 pvfactors；solarfactors 是 SunPower/pvfactors 的维护分叉，目的是继续支撑 pvlib 中已有的 pvfactors 功能。发行名称是 `solarfactors`，导入名称仍是 `pvfactors`。这不是 NASA 算法包，也不是 pvlib 全库。新 Python 扩展应采用独立导入名称，避免与参照包覆盖同一个 namespace。上游许可为 BSD-3-Clause，源码与派生代码须携带相应 notice。

## Reference Authority Hierarchy

| 层 | 权威范围 | 遇到冲突 |
|---|---|---|
| A：物理/数学规格 | 视因子定义、能量交换、明确的模型假设、论文公式 | 作为独立检查；经验模型也有适用范围，论文不是所有软件默认参数的来源 |
| B：冻结行为 | 指定依赖与输入下的可观察输出、分区、分量和异常 | Golden 记录事实；确认 bug 可通过 CDR 偏离 |
| C：实现细节 | ndarray 形状、DataFrame 对齐、Shapely 容器、进程池、matrix inverse | 不自动成为 Rust 要求；改变算法近似则必须回到 A/B 审查 |

数值兼容、Python API 兼容、bitwise 兼容是三件事。项目只承诺文档规定的数值/物理行为与明确批准的修正。

## Canonical Runtime R0

| 项 | 冻结值 | 理由 |
|---|---|---|
| CPython | 3.12.14，Clang 22.1.3 构建 | 本机实际可用，清洁环境复测；无需追逐最新 minor |
| OS/架构 | Linux x86_64，glibc 2.39；实际 kernel 6.18.44 | 初始 Golden 唯一产出平台，非 Rust 平台约束 |
| solarfactors | 上述 commit，源码直接导入 | 防止 PyPI 与 Git 源混用 |
| pvlib | 0.14.0 | 对应 v1.6.1 字段兼容修复；冻结实现及系数 |
| NumPy | 2.3.5 | 实际测试通过；记录 wheel hash 与 BLAS |
| Pandas | 2.2.3 | 日期/dayofyear、索引、concat 语义影响参考 |
| Shapely / GEOS | 2.1.2 / 3.13.1 | 满足 >=2.0，冻结几何判定行为 |
| SciPy | 1.17.0 | pvlib 传递依赖；主 radiosity 实际用 NumPy.linalg |
| Matplotlib | 3.10.8 | 上游导入和绘图测试需要，Rust Core 不需要 |
| pytest / pytest-mock / mock | 8.4.2 / 3.15.1 / 5.2.0 | 复现测试 harness |
| BLAS | NumPy wheel 的 OpenBLAS 0.3.30 ILP64 | 三类线程环境变量固定 1；完整配置见 runtime.json |

其他 20 个运行/测试依赖均在 29 包的 `requirements-linux-cp312.lock` 固定并提供 wheel SHA-256。锁文件是本 Linux CPython 3.12 环境专用；不能声称同一 wheel hash 可跨平台安装。日期与时区规则另见 03/10。

本次在原环境及全新 venv 均实际运行上游全套测试；详细结果见 evidence 日志。最终冻结还需 Golden 阶段完成环境重建检查、产物重复生成与跨平台误差标定。本包未提供容器 digest，也未取得 macOS/Windows 实测；不把同机 venv 复测冒充跨平台复现。

## 复现入口

`reference/generator/reproduce_reference.py` 先验证附带快照的 Git blob SHA，再运行上游测试。使用随包 `upstream/solarfactors` 源码，无需在本阶段实现 Rust。建议新建 Python 3.12.14 venv，按 lock 下载/安装 Linux wheel，再设置 BLAS 线程为 1、MPLBACKEND=Agg、PYTHONHASHSEED=0 后执行。`requirements-canonical.txt` 只用于阅读，安装 Gate 以含 hash 的 lock 为准。

## 来源边界

已实际阅读全部核心 Python 文件、102 个上游测试、理论 rst、全部 release note；Perez 1990 原文已下载并视觉核对关键公式页。Anoma 2017 / Marion 2017 的原始全文本次分别遭遇 403 / 502，不能声称已逐式审读；其模型关系通过上游官方理论文档、公式推导及源码交叉分析。此缺口登记在 08，不阻塞已经明确的基础几何，不允许用它给新的物理修正背书。

论文、软件依赖和技术选型来源集中列于 `14_EVIDENCE_AND_TRACEABILITY.md`，各专题同时有直接链接。
