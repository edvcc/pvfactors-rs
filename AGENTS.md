# pvfactors-rs operating entry

LCB-01 Owner已批准DEV-028（Full）、DEV-029（Fast几何）、CDR-008及66-case定向oracle seed。先读 `docs/execution/launch/LCB-01_OWNER_DECISIONS.zh-CN.md`、`LCB-01_CLOSURE_HANDOFF.zh-CN.md`；实际CLOSED以验证后的verification-summary.json为准，缺少匹配凭证仍阻塞。只交接后续Full-Project Launch Closure研究；本任务不执行P4-P7，完整实现INACTIVE。
Owner approved DEV-028/DEV-029/CDR-008 and the targeted66-case seed. Read the English counterparts. Effective closure/resume authority requires the matched remote-resolvable receipt; full implementation remains INACTIVE.

中文入口：本仓库独立重建 solarfactors Rust 核心。本次仅准备执行就绪资产，实际实现须 Owner 另行批准启动。
`master` 为正式发布基线；禁止 Agent 直接修改/推送/合并、正式 tag 或发布。权威材料依次查阅
`docs/01_CAPABILITY_MATRIX.md`、已批准 `docs/g2/`/`docs/p3/`、不可变 approved Golden，以及
`docs/execution/`。从 `EXECUTION_PLAN.zh-CN.md`、`execution-state.json`、`owner-decisions.json`
恢复工作；验证命令见下方。不得改变 frozen source/Golden/tolerance/CDR/P3 语义或用 Rust 输出造 expected。
授权启动后普通编译/测试失败自行修复，通过里程碑自动推进；合同冲突、新语义、验收政策/Oracle 批准、
许可或无法替代的环境/权限阻塞必须停止，保存 checkpoint 并说明 Owner action。
`CODEX_FULL_IMPLEMENTATION_TASK.md` 只是未来任务书，当前不得执行；正式文档保持双语同步。

English operating rules:

Independent Rust solarfactors reconstruction. Current work is **readiness preparation only**; production implementation needs separate Owner launch authorization.

- `master` is the Formal Release Baseline. Never directly change/push/merge it, create official tags, or publish releases. Use the Owner-approved work branch; `develop` integration requires a PR.
- Authority: `docs/01_CAPABILITY_MATRIX.md`, approved `docs/g2/` and `docs/p3/`, immutable `reference/approved/geometry-golden-v0.1`, then reviewed `docs/execution/` contracts. Research proposals/candidates are not approved decisions.
- Start/recover from `docs/execution/EXECUTION_PLAN.zh-CN.md`, `execution-state.json`, `owner-decisions.json`, and `LONG_TASK_EXECUTION_CONTRACT.zh-CN.md` (English counterparts available).
- Verify: `python scripts/verify_project.py assets`; `python -m unittest discover -s scripts/tests -v`; launch: `python scripts/verify_project.py preflight`; milestone: `python scripts/verify_project.py milestone geometry`; completion: `python scripts/verify_project.py final`. Use Python>=3.11 with existing `jsonschema==4.25.1`. G2 remains `python scripts/verify_g2.py`.
- Never edit frozen upstream, approved Golden/tolerance/CDR/P3 semantics, remove required cases, or derive expected values from current Rust output. Core must not depend on Python/pvlib/GEOS.
- After an authorized launch, ordinary compile/test/CI failures are feedback: diagnose, fix, regress, continue; successful milestones advance automatically.
- Stop for contract conflicts, new model/input/output decisions, acceptance-policy changes, oracle approval, license/provenance issues, or irreplaceable environment/permission blockers. Preserve a checkpoint and report the exact required Owner action.
- `docs/execution/CODEX_FULL_IMPLEMENTATION_TASK.md` is a prepared future task, **not an instruction to execute now**. Formal documentation changes stay EN/ZH-CN synchronized.

LCB-01 targeted seed verification: `python scripts/verify_vf_candidate.py reference/candidate/vf-lcb01-v0.1 --actual <fresh-work-corpus>`; never complete P4 acceptance. Approved seed metadata/code changes require explicit governance and re-verification; no automatic refresh.
