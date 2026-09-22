# 持久执行计划

状态：PREPARATION_ONLY，2026-09-22；生产实现未启动。

1. Owner 集中审阅 REMAINING_OWNER_DECISIONS 并签署准确语义，关闭 BF-01/BF-02，不编辑冻结历史。
2. 关闭 OD-08 oracle/profile 对象，或明确批准 candidate capture 后停点流程；批准 V1 完成、验收矩阵、执行及平台/资源合同。
3. 解决本次 R0/打包路径缺口，落实或明确接受分支保护/权限风险并留日期证据；启动时刷新 GitHub 状态。
4. 在 owner-decisions.json 记录 approval evidence、readiness commit、允许的 implementation branch、contract_sha256。clean checkout 上 preflight 必须实际 PASS；准备资产 PASS 不等于启动许可。
5. 只有明确启动后执行 ACCEPTANCE_MATRIX 的 M3–M13。每个里程碑实际通过即自动推进，剩余批准/合同停点按执行合同处理。
6. 最终运行 final verification，交付 candidate package、证据及 Owner 独立验收说明，不 merge master/tag/release。

## 当前状态与恢复

机器进度为 `execution-state.json`，只是可读 checkpoint，不是产品数据库。Pending decision 不是 approved blocker。恢复时确认记录的 commit 存在且为 HEAD 祖先，核对真实 branch/dirty 状态，检查上次 receipt 被验证 SHA/hash。保留用户修改，只重跑受影响检查；以证据推进，不相信状态字符串。

每个稳定 checkpoint 更新 current milestone、last completed checkpoint、verification status、known failures、approved blockers、next executable action；普通实现进度记录附相关命令、报告路径、时间，正式文档双语同步。中断在编辑中时保留文件并标未完成；先提交实现再验收，随后报告 commit 引用被验证父 commit。

## 统一命令

```sh
python scripts/verify_project.py assets --output /tmp/readiness-assets.json
python -m unittest discover -s scripts/tests -v
python scripts/verify_project.py preflight --output /tmp/preflight.json
python scripts/verify_project.py milestone geometry --output /tmp/m3.json
python scripts/verify_project.py final --output /tmp/final.json
```

使用 Python>=3.11 及仓库已有 jsonschema==4.25.1；完整 Reference 生成只用 R0。`assets` 可在编辑中执行；launch/milestone/final 要求 clean worktree。`--scope geometry` 只用于单独明确授权的限定启动，仍检查 OD-01/10/11、环境及批准，scope 参数不是授权。

当前 M3 因无 geometry 实现或验收 exporter 返回 NOT_READY；M4–M13 也缺批准 oracle/adapter，后续接线须满足 HARNESS_CONTRACT 与 OD-08。它们均未完成。
