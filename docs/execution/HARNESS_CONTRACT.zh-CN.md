# 验收 Harness 合同

状态：供 Owner 审阅的 PROPOSED 验收接口，准备 tooling 已实现。Python>=3.11，新代码仅 stdlib，复用现有 G2 jsonschema4.25.1，不引入生产算法或 Rust runtime dependency。

## 命令与状态

```sh
python scripts/verify_project.py assets --output /tmp/assets.json
python scripts/verify_project.py preflight --output /tmp/preflight.json
python scripts/verify_project.py milestone geometry --output /tmp/geometry.json
python scripts/verify_project.py final --output /tmp/final.json
python -m unittest discover -s scripts/tests -p 'test_verify_project*.py' -v
```

exit0=PASS；exit1=FAIL（非法/变更/格式错误/失败证据）；exit2=NOT_READY（缺实现/批准/oracle/环境）。同时存在失败及未完成时优先 FAIL，报告保留每项状态。`assets` 只验证当前准备资产、基线、工具、G2，不授权启动。`preflight` 另要求 clean 具名分支、绑定当前 contract SHA 的 Owner 批准、environment/governance receipt、真实 R0 执行、harness self-test；PASS 只表示允许开始，不表示项目完成。报告通常写仓库外或 ignored reference/work；写入 tracked evidence 会使下次 launch dirty。

原491个冻结文件与 c2bc8572a976279abacbcd1d4f9c460233785bdb 的 Git blob 比对；lock 清单本身从该 commit 重建，所以同时修改 source 与本地 manifest 也不能通过。原 verify_g2.py 不变，直接组合 source/cases/schema/invariant/provenance 检查，不复制 G2 物理判定。P3 双语批准文本也受保护。实时检查 Rust/Cargo、locked metadata、workspace Edition/resolver、组件及 Python tooling。

## Geometry 可执行 adapter

`--scope geometry` 仅允许限定 preflight 或 M3，仍须具名 Owner 授权；M4–M13 和 final 必须使用全项目批准。工具拒绝用 Geometry-only 批准绕过后续决策。

里程碑要求存在生产 math/geometry 模块及未来 test-only target `crates/solarfactors-core/tests/acceptance_geometry.rs`，执行：

```sh
cargo test --locked -p solarfactors-core --test acceptance_geometry -- --nocapture --test-threads=1
```

Harness 提供全新空的 PVFACTORS_ACCEPTANCE_OUTPUT 目录。Rust test target 必须真实调用 public/core 代码，运行全部55个 approved case 及 acceptance-matrix.json 中具名独立测试，写出：

- `run.json`：schema_version1、git_commit（被测 clean HEAD）、producer=`solarfactors-core`、milestone=`M3`。
- `results/<case_id>.json`：准确对应不可变 APPROVAL.json 的55个 ID；对象准确包含 case_id/input/result/nonfinite_mask。可读 fixture input/metadata，但 computational result 必须来自 Rust，禁止把 expected/result 复制成 actual。
- Harness 写 `test.log`，校验真实具名 test record、非零且匹配的计数，重算 artifact hash，并把输出保留在 ignored `reference/work/acceptance/M3-*` 供审阅/CI 上传。不单独消费旧 receipt。

Expected projection 为 `geometry_payload`：只去掉 result.warnings、result.reference_length_m、result.ground.reference_extent_m（Reference 历史注解）以及 result.errors[*].message（P3 §8 明确非协议诊断文本）。其余 result、input、key、index、classification、order、active、nonfinite_mask 全部保留。Actual exporter 输出该 projected shape。这个投影是明确 Owner 审阅对象，改变排除字段属于验收政策变化。Golden 字节不变。Trace-only intermediate 位于 test adapter，不进入生产公开 API。

比较复用既有 Geometry Comparison 并加精确 JSON type 校验，False 不能冒充 index0。数值使用冻结 quantity-specific geometry-tolerance-v0.1；alpha rad 按原 comparator 转换。topology exact 字段无 numeric tolerance。漏/多案例、key/index/class 改变、shape/type/nonfinite 不符、缺产物均 FAIL。即使 subprocess exit0，零测试、ignored test、summary 计数不符仍 FAIL。独立测试必须覆盖 interval residual、验证顺序、partition/coverage、identity/active map、projection、predicate、mirror、请求帧。结果差分不能代替独立测试。

## 后续里程碑与 final adapter

M4–M13 当前没有批准的 executable binding/oracle。矩阵已定义 scope/tests/oracle/tolerance/artifact/CI，但执行返回 NOT_READY。这是真实扩展边界，不是 PASS placeholder。采用前按 OD-08 打包 concrete expanded IDs、独立 expected/推导、Reference capture manifest、profile、测试命令、comparator mutation test；再实现 adapter 与有类型的证据校验。语义清单/profile 变化须 Owner 批准并更新审阅 digest；不改语义的接线是普通实现。

Final 当前枚举11个 milestone、22个必需 CAP、10个排除项、逐平台状态、packages/performance（缺失时空）、计数、CDR/Golden/tolerance/reference/Git SHA。真实 package hash/干净安装、平台/interpreter/NumPy 笛卡尔覆盖、provenance/version、OD-12 raw benchmark validator 未建立前，release evidence 保持 NOT_READY。不得换成“文件存在”或用户自报 pass=true。Final 必须重跑本地 Gate，并按被测 SHA、CI run URL/conclusion、环境身份、下载 artifact hash 校验远端证据；平台不能互相替代。Adapter 须暴露单个 case 结果、failed/skipped/waived 及完整性；初版 harness 不接受隐式 waiver。

## 信任边界与 Owner 独立验收

可修改脚本不能证明作者自身可信。Owner 固定已审阅 preparation/approval commit 与 digest，独立审查 harness/expected/tolerance diff，可在另一 checkout 运行可信 harness 比较候选输出。真实 CI log/package digest 补充本地测试；分支保护/凭据限制属 OD-11。伪造 pass receipt、复制 expected、删测试或伪造批准证据均违反执行合同，即使有权限的 Agent 能编辑文件逃避检查。

`contract_sha256` 固定规范文本、矩阵、baseline lock、审计、任务书及入口，不包含进度、报告、批准状态或验证程序字节。每份运行报告另记准确 `verification_tool_sha256` 与 `verification_self_tests_sha256`，并绑定 Git SHA。这样在已批语义内新增 adapter/修复接线不要求每次重新批准启动；语义变化仍须 Owner 决定并更新合同摘要。程序哈希只提供追溯，不证明语义未变。Owner 在最终验收前须审查相对已审阅 commit 的工具 diff，采用可信版本独立重跑；不得把修改后的程序自报 PASS 当成独立验收。

Self-test 在临时目录使用 synthetic fixture，approved payload roundtrip 仅验证 tooling，不声称 Rust compatibility。变异覆盖漏案例、SurfaceKey/ReferenceIndex/ProjectionClass、10倍阈值、合法差异、manifest/source 字节改变、缺失/空 artifact、零/ignored/缺测试、JSON 类型不符、未知 comparator、缺实现。还须运行全部既有 G2 tests。Self-test FAIL 阻止启动；实际计数和日志执行后归档 evidence/execution。

Owner 独立比较命令（在可信审阅 checkout；仅比较，不证明 Rust 执行或 milestone）：

```sh
python scripts/verify_project.py compare-geometry --actual /absolute/candidate/results --output /tmp/owner-comparison.json
```
