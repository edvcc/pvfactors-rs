# 长任务执行合同

状态：PROPOSED；只可经 OD-10 和 Owner Launch Review 激活。日期：2026-09-22。

## 权威与终点

Owner 明确决定 > 已批准 CDR/Golden/model 合同 > 已批准 P3 设计及签署补充澄清 > 已批准 V1 完成/验收/执行合同 > 执行计划 > 私有实现选择。数学是独立正确性约束：正式数学、批准 CDR 与 Golden 无法同时满足时停止并揭示冲突；权威顺序不授权静默挑选方便答案。历史研究建议及 candidate 不是批准。EN/ZH-CN 必须一致，影响行为的差异触发 stop。

固定 P3 base：c2bc8572a976279abacbcd1d4f9c460233785bdb；冻结 Reference：ecbfc863657e239817603a43898ae173c7ccad9c；Geometry Golden manifest：efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b。三者均保留。终点为 V1 IMPLEMENTATION COMPLETE + RELEASE CANDIDATE READY FOR OWNER ACCEPTANCE，不是 master merge、tag、发布或 SemVer1.0.0 批准。

## 自主执行政策

明确启动后，Codex 可创建/修改实现文件、私有模块/helper/iterator/scratch，增加 unit/property/metamorphic/regression tests，调整独立工作顺序，重构内部 API，更新实现文档/changelog/计划，创建可恢复 commit，运行 CI 并自行修复，不逐模块询问。必要 dev dependency 须记录消费者、许可/MSRV/features 理由并锁定；normal dependency 只能在批准模块、可移植性及资源边界内增加。P3 normal dependency 保持零。后续 solver/binding 可自主评估和锁版本，不能泄漏 vendor types 或向 core 引入 Python/GEOS/BLAS。新增许可风险或平台义务变化不属于普通依赖选择。

按 M3→M4→M5→M6→M7→M8→M9→M10→M11→M12→M13 推进并遵守矩阵依赖。实际 milestone 通过后自动推进，不等待 Owner 每次说“继续”。Reference candidate approval 是 OD-08 具名停点，不静默晋升。后续缺失的 adapter 必须连同验收测试实现，不能因此标通过。保持批准语义的 adapter 接线可演进；comparator 字段、expected、tolerance 语义改变需要 Owner 审阅及新 contract digest。

## 正常反馈，不是人工停止

编译、rustfmt/Clippy、普通 unit/differential/property 失败、数值实现缺陷、内部 API 重构、性能不佳、临时 CI 故障、首个方案失败都属正常工作。observe→定位最早分歧→修复→重跑→最小 regression→继续。不能只看最终 POA。临时基础设施最多重试三次并有界退避，检查证据，可使用既有批准的等价 runner。权限/平台长期不可用才成为环境 blocker。没有先检查实现，不能把不明 mismatch 直接改称合同冲突。

## 必须停止

1. 正确实现不能同时满足数学、批准 CDR 与 Golden。
2. 必须新增 deviation、改变物理行为、输入域、公开结果/错误合同。
3. 必须改变 accepted expected、required case、exact field、tolerance 或 comparator 语义。
4. 到达 OD-08 candidate oracle/tolerance 批准停点；Agent 无批准权。
5. 发现潜在许可/provenance 问题、大段复制、attribution 缺失或依赖义务不兼容。
6. 必需环境/权限/平台没有批准替代路径，或资源预算无法容纳必需工作。

停止时：安全 checkpoint 保存工作；记录影响合同、最小反例、最早分歧字段、实际/期望值、已尝试实现修复、证据路径、默认建议、范围及准确 Owner action；更新 execution-state.json 与计划，停止依赖此决定的实现，不自行批准。等待期间可继续无关低风险诊断，不实现未决语义。不记录私有推理。

## 可信验收与开发测试

Codex 可修复开发测试错误，必须保留批准案例清单、expected 和 tolerance。不能在一次修复中同时改实现+accepted expected+tolerance 后宣告成功。原始基线与 Owner 指定 Git commit 比较，不只信任可变 hash 清单。新批准是追加的不可变版本对象。验收政策变化需明确 Owner 证据、独立 comparator mutation test、独立审阅 checkpoint。Owner 检查 diff，并从审阅过的准备/批准 commit 运行可信 harness 验收候选输出；仓库脚本无法成为对抗自身特权编辑者的安全边界。

## Git、checkpoint 与恢复

不得直接修改/推送 master、develop、release 分支，不得 force-push、merge master、正式 tag 或 publish。在 Owner 指定、同时包含 P3 与已审阅 readiness 祖先的 implementation branch 工作。feature push/CI 及向 develop 的 draft PR 只有启动授权包含时才允许；不能从 write credential 推导 merge 权。保留用户修改，不 hard reset 其他会话。

使用 feat/test/fix/docs/ci/perf scoped commit。每个 milestone 至少一个稳定通过 checkpoint，较长阶段保留中间恢复点。不得只留一个巨大最终 commit，不自动 squash；PR 前整理仍需可理解历史。先提交实现，再在 clean SHA 上验收。报告可随后提交并引用被验证的祖先 SHA，不使报告自身 hash 递归依赖自身。

持久状态：current milestone、last stable commit、验证状态及命令/artifact hash、known failures、approved blockers、next executable action。恢复时读取 AGENTS.md、本合同、EXECUTION_PLAN、execution-state.json、Owner decisions；核对 HEAD/branch/dirty 状态，检查 frozen baseline，验证 checkpoint/receipt。任务自身 dirty 修改先检查保留再恢复；异常并发编辑需协调。只重跑已过期/受影响检查；进度笔记不能证明 PASS；没有新证据不要重做已完成阶段。

## Provenance、资源与完成

独立 Rust 重建，不逐行翻译 frozen Python，不复制大段 Reference body，不移除 notice。每个重要算法模块记录 algorithm provenance、frozen behavior source、independent implementation note，无需每行引用。保留 BSD notices，包内提供必需 third-party notices/SBOM；许可疑问须停止，不能用“重写”自行豁免。

使用 OD-12 限额、实测内存、有界 property case、隔离 benchmark、任务自有 cache 清理。不建设 orchestration service、数据库、队列、dashboard。Reference Python 仅开发验证，不进入 Rust runtime。

最终必须全部 CAP01–CAP22、milestone、批准平台/包证据、真实 passed/failed/skipped/waived、性能证据、CDR/Golden/tolerance/reference 版本及 Git SHA。缺 Must Have 必须非零 FAIL/NOT_READY，不能 mostly complete。Owner 独立最终验收并决定版本/发布。本准备任务生成 CODEX_FULL_IMPLEMENTATION_TASK.md 后必须停止。
