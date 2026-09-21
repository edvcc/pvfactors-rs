# 11｜Execution & Adaptive Parallelism

## 当前上游行为与限制

`run_timeseries_engine`建立OrderedPVArray、VFCalculator、irradiance model和PVEngine，对整个T进行NumPy向量化fit/run，再callback build report。它不是严格逐timestep低内存streaming。

`run_parallel_engine`用multiprocessing，`n_processes=-1`取cpu_count；用`np.array_split`切timestamps/DNI/DHI/angles/albedo及可选GHI；每chunk重建engine，`Pool.map`运行`_run_serially`，返回chunk index与report，排序后调用`report_builder.merge`。自定义report builder必须提供合适merge，输出不一定具有通用可合并语义。

限制：复制/序列化输入与model、Python callback可pickle要求、各进程重复分配几何/F、全批zero-length判定、空chunk、进程启动开销、底层BLAS自开线程可能oversubscribe。上游parallel测试验证有限场景，不构成未来所有policy等价证明。[冻结run.py](https://github.com/pvlib/solarfactors/blob/ecbfc863657e239817603a43898ae173c7ccad9c/pvfactors/run.py)。

## 单一产品API

`ExecutionPolicy::Auto`为最终默认；`Serial`用于可复现/debug；`Parallel{max_workers?,strategy?}`为用户override。Mode::Full/Fast独立。所有策略调用同一已验证timestep kernel；不允许改变cut、model、AOI积分、输入筛选、source terms或结果字段。

| strategy | 外层 | solver | 使用条件 |
|---|---|---|---|
| Serial | 1 | 1 | 小任务、无校准保守fallback、严格debug |
| OuterParallel | 多timestep/chunk | 每solve串行 | T足够且内存可控；V1主要并行路径 |
| InnerParallel | 低并发/串行timestep | 单矩阵内部并行 | 大S、低T且backend实测有收益；V1.x候选 |
| 双层heavy | 多 | 多 | V1默认禁止；未来只有统一线程预算和benchmark可证明才开放 |

不能在每个Rayon worker里无约束调用另一个rayon/BLAS pool。solver的并行参数由ExecutionPlan显式下发；core不写全局环境变量改变同进程其他库。

## ProblemProfile与ResourceProfile

问题profile至少包含：raw_T、effective_T、zero/invalid/night分类计数、N、Slogical、active S分布/上界、matrix dimension、cuts、mode、model、AOI J/curve复杂度、output/TraceLevel、输入bytes。`effective_T`来自同一input classifier；不沿用上游未消费skip标记。若缺GHI或GHI0且DNI=DHI0的安全零值捷径可跳过solver；night/非法值按CDR-001政策先决定，不在planner擅自忽略。

资源profile：`available_parallelism`、用户max_workers、可选memory_budget_bytes、执行profile、当前context的线程预算、backend能力与校准ID。OS可用内存信息可能不可得/不准确；显式预算优先，缺失时采用记录来源的保守配置上限，不能无依据声称“检测到足够内存”。尊重容器/cgroup限制但不把logical CPU当物理核精确数。规划O(N+T)轻量扫描，不为选策略先构造全T×S²。

| execution profile | 优化目标 | 约束方向 |
|---|---|---|
| Interactive | 尾延迟和响应、少启动/竞争 | 更短chunk/cancellation latency，资源上限保守 |
| Balanced | 单任务耗时与系统可用性折中 | 默认经校准目标函数 |
| Throughput | 大批总吞吐 | 允许更大chunk/更高资源利用，仍守预算 |

不在本阶段写死“Interactive用25%线程”之类比例。

## 确定性cost model v0

对Full单时点，取active dimension n、VF候选对P、AOI bins J：

`c_full=a0+a_g·Slogical+a_v·P+a_a·P_AOI·J+a_l·n³+a_r·n²`。

Fast无全局LU：

`c_fast=b0+b_g·Slogical+b_v·P_target+b_a·P_target_AOI·J`。

可直接记`C=f(T,S,M,I)`，其中M选择Full/Fast项，I包含Isotropic/Hybrid、AOI curve/J。实际geometry部分随N、cuts和ground分区变化，不能只用row数替代S。使用按profile分桶的T与n统计而不是所有时点一律最大n；memory规划必须使用上界。

预测外层时间：`t_outer(W,K)=startup(W)+ceil(chunks/W)·overhead_chunk + Σc_t/[W·η_outer(W,K)] + t_output`，更准确实现按确定的chunk cost分配计算最大worker负载。简式只用于首版拟合；η来自benchmark，不声称完美线性。

内层候选：`t_inner(P)=Σ[c_non_solver+c_LU(n,P)]+startup_solver(P)`，从测量表插值；不假设O(n³)/P即真实收益。序列预测为Σc_t。**Outer crossover**是预计节省超过启动/排程及误差margin且内存可行；**inner crossover**只在大n校准域内启用。没有benchmark之前无法给出可信T/S阈值，Auto回退Serial并说明uncalibrated，不能把它叫优化完成。

所有a/b/η/startup都来自固定版本benchmark artifact，附CPU族、backend版本、compiler/target、OS、case域、拟合误差、有效范围和校准timestamp。运行时只确定查表/算式，不用LLM，不偷偷在线试算重复用户任务。输入/资源/校准相同则plan相同。

## 内存、worker与chunk

`M_total=M_input+M_output+M_shared+W·M_worker(n_max,K,J)+M_queue`。

worker近似项含`8·m_matrix·n² + 8·m_vec·n + geometry_scratch + AOI_scratch + K·per_timestep_buffer`；m_matrix不是固定魔数，由实际是否保留F/G/B/LU/trace计算。TraceLevel::Matrices需要输出O(T·S²)，即使逐时求解也不能忽略它的总输出内存。

约束worker≤min(可用线程预算、非空chunks、effective_T、memory可容纳worker数)。预算放不下单时点则返回ResourceLimit并提供估计/字段，而不是偷偷切Fast/降低cut。chunk K在调度开销、负载不均、memory、取消延迟间选择；至少一个有效时点，不切空chunk，输出按原raw index写回。复杂度变化大的时点可做确定cost-balanced chunks或work stealing，结果位置固定。

memory估计加入测量过的allocator/alignment余量；报告estimate而非假装精确峰值。压缩active mapping必须按timestep，避免全批is_empty造成chunk依赖。标准结果使用固定typed arrays，不允许任意Python callback决定merge算法。

## ExecutionPlan合同

```
policy_requested, profile, strategy
worker_count, chunk_size, chunk_count, solver_parallelism
raw_timesteps, effective_timesteps, status_counts
logical_surfaces, active_surfaces_min/max, matrix_dimension_max
mode, irradiance_model, aoi_sections, trace_level
estimated_memory_bytes, memory_budget_bytes, resource_limit_source
available_parallelism, requested_worker_limit
estimated_runtime, prediction_uncertainty, calibration_id
solver_backend, model_revision, deterministic_mode
reason_codes, decision_metadata, fallback_reason
```

reason codes如`SMALL_BATCH`、`UNCALIBRATED`、`OUTER_PREDICTED_FASTER`、`MEMORY_WORKER_CAP`、`USER_SERIAL`、`INNER_UNSUPPORTED`；带实际参数与候选成本。用户默认只收结果；开发者可取得plan，benchmark保存plan+实测time/peakmemory，失败日志可复原决策。

## 等价、性能与发布Gate

用L2/L3/L5验证Serial/Parallel/Auto、1/2/max workers、chunk1/prime/uneven、all-zero/mixed night、tilt变号、cut/AOI。比较原索引、mask和trace；不只均值。Python多调用并发、取消、error传播和无泄漏线程池另测。不得因性能差用容差掩盖乱序或未初始化内存。

bench轴T=1/短批/日/月/年，N/cut引出的S分层，Full/Fast，Isotropic/Hybrid，AOI on/off，TraceLevels；所有测量带warmup/repetitions/分位数与machine manifest。V1接受Serial+Outer及有依据Auto，inner与双层不作为完成V1的前提。发布前Auto在校准工作负载达到预先批准性能目标且不突破预算；具体目标必须在有测量后定义，不能现在虚构speedup。
