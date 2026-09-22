# 环境、CI 与治理

证据快照：2026-09-22，准备分支基于已批准 P3。实时 API 响应见 `../../evidence/execution/github-snapshot.json`。本报告区分已具备工具、建议路径与实际执行验证。

## 实际观察

Rust/cargo1.98.1、rustfmt/clippy 已安装，Edition2024/resolver3；locked metadata/build/fmt/Clippy 通过。Core 只有 crate 级声明，**Rust 测试为零**，无 runtime dependency。本机 macOS arm64，系统 Python3.14.0 原缺 jsonschema；临时 `/tmp/pvfactors-readiness-venv` 安装仓库已有 jsonschema4.25.1 后运行 G2/治理检查。该环境不是 R0，没有新增生产依赖。

R0 由 `reference/runtime/r0/Dockerfile` 定义，锁定 Ubuntu OCI digest、CPython3.12.14 源码 SHA、29 个 wheel hash、GEOS3.13.1、确定性变量。历史 environment_id=031158a1d1be8cdb9093 有 G2 批准证据。本次 Docker CLI 存在但 daemon socket 不存在，当前 R0 执行为 **ENVIRONMENT GAP**。不得重建/刷新 Approved Golden。可在可用 Docker host 启动并按原定义构建 R0 image，再运行 preflight 实时探测；CI 替代路径需具日期、已审阅证据，历史 R0 通过不能证明今天可用。R0 environment ID 含平台/kernel，等价重建若 ID 改变须明确环境审查，不能编辑 expected ID。

Canonical lock 包含 package hash；requirements-g2.txt 固定 jsonschema，但该文件没有 hash-lock 验证工具的全部传递依赖；Dockerfile 对验证依赖做版本 pin。因此普通 PR 安装可复现性仍有限，不影响已批准 Golden payload 完整性。如有需要，后续单独审阅 tooling lock；不能为了本机安装改 canonical lock。

GitHub API：public 仓库，默认 master，Actions 启用，self-hosted runner 为0（不等于 hosted runner 不可用）。现有 G2 workflow active，最近查询的 develop run35654063756 在 fb63a96ef06cc0375fca9dbceb4f59e89e7157a7 成功。本准备分支未 push，所以没有本次新 readiness 远端执行。master/develop protected=false；两个 protection API 均404 Branch not protected；父级/仓库 ruleset=[]、匹配分支 rules=[]。这是实证不存在，不是权限推断。

## 建议平台合同（OD-09，尚未支持）

| Target | 候选 runner | 包政策及补充证据 |
|---|---|---|
| Linux x86_64 GNU | ubuntu-24.04 | Rust native；manylinux_2_28 wheel，glibc2.28 干净容器安装/audit |
| macOS arm64 | macos-14 | 原生 arm wheel；deployment11.0；仍需最低 OS smoke |
| macOS x86_64 | macos-15-intel | 原生 Intel wheel；deployment10.15；仍需最低 OS smoke |
| Windows x86_64 MSVC | windows-2022 | 原生 wheel；候选 Windows10 1809+ 下限须实际 smoke |

普通 GIL CPython3.11/3.12/3.13/3.14，per-interpreter wheel；候选 NumPy>=2.3.4,<3。采用时锁定各组合最低/当前测试版本。不承诺 PyPy/free-threaded/abi3/WASM。本机没有 maturin/PyO3 评估、wheel、Linux/macOS-Intel/Windows Rust 或干净安装证据：**ENVIRONMENT GAP**，不能 PASS。四个 hosted label 是可行路径，不代替真实打包执行。获得启动授权后可做非产品隔离 binding probe，M8 前依据实测选择准确版本/features/license 与 NumPy 所有权兼容性。

本次核查官方资料：[GitHub hosted runner](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)、[PyO3 guide](https://pyo3.rs/main/)、[NumPy2.3.4 Python 支持](https://numpy.org/devdocs/release/2.3.4-notes.html)、[maturin distribution](https://www.maturin.rs/distribution.html)。这些只支持建议路径，不证明本项目通过。PyO3 文档示例0.29.2、支持 CPython3.9+；本项目有意采用更窄范围。NumPy2.3.4 支持3.11–3.14。manylinux/OS 下限还必须满足所选依赖 wheel。

## 仓库规则准确建议（OD-11）

建立两个 active branch ruleset，分别匹配 `refs/heads/master`、`refs/heads/develop`。禁止删除/force push；必须 PR；Agent 无 bypass；所有 review conversation 解决；当前 PR head 的 required checks 通过。新 workflow 真实运行后选择 context：G2 Geometry Candidate 的 `verify` 和 Execution Readiness 的 `assets`。从 checks API 确认准确 context/app identity，不能猜 workflow 名称前缀。要求分支 up-to-date，workflow/job 名保持稳定。不要把 preflight 设为 PR required check：它在 Owner 启动批准前有意失败，不是准备资产检查。

master 另要求至少1个人类批准、旧批准失效、最新 push 后 review，Owner 决定最终 merge。Owner 自己提交的 PR 应有第二个人类 reviewer，或明确 Owner-only 紧急 bypass，不能给 Agent。develop 必须 PR+CI，baseline/contract 由 Owner review。若 token 属 admin/bypass identity，ruleset 本身不能保证 Agent 不 merge；使用非 admin 自动化身份，可行时限制可 push 分支，排除 release/package publication/organization management 权限，发布凭据只由 Owner 持有。无法技术限制 no-merge 时明确记录残余风险。

本次未修改仓库/组织规则。上述是准确配置建议，不是已应用配置。Owner 也可有期限地接受残余风险，记录到期、credential scope、manual merge control。启动时刷新 API；接受风险不改变 protected=false 实际状态。

## CI 分层

| 层 | 范围与预算 | 证据 |
|---|---|---|
| 当前 PR fast readiness | 保留 G2；新 assets job 检查 frozen integrity、文档/mapping、harness self-test、Rust toolchain/fmt/Clippy，<=15min | 上传 JSON/tests/log，不宣称生产通过 |
| 后续 PR correctness | 相关阶段 analytic/differential/invariant、每家族256 property seed、serial smoke、Native/Python 子集 | 完整 required case 计数及最早分歧 |
| 后续 nightly deep | 每家族2048 seed、边界/跨平台、内存线程 stress、有界 workload | seed/shrink、平台 trace、资源样本 |
| 后续 RC matrix | 全部 target/interpreter/NumPy 边界、干净 wheel/crate、全部 correctness/execution、许可/SBOM、隔离 benchmark | 不可变 package hash 与完整 final evidence |

本次只增加当前 readiness asset workflow，不创建未实现功能假 job，不加自动发布，不在每 commit 跑巨大矩阵。采用 read-only contents、checkout 不持久化凭据、有界 timeout/concurrency、不向不可信 PR 暴露 secrets。scheduled job 从默认分支触发；master 为 formal baseline，后续集成 nightly 时须由 Owner 决定安全 checkout develop 或 manual dispatch。本次不安装 schedule。

## 资源与证据限额

本次可用磁盘约51GiB。OD-12 建议生成物/cache 10GiB，保留10GiB free，最多4 worker 或更低 CPU 限制，solver 单线程；可执行时单进程2GiB/任务8GiB。使用任务本地 CARGO_TARGET_DIR/Python venv，不隐式改全局，不删用户 cache。G2 corpus 只读，派生产物另存。benchmark 与 build/reference capture 隔离，记录3次 warmup、10次测量、CPU/compiler/backend、median/p95/RSS。网络/安装/工具失败据实记录，缺指标就是缺口。

许可证/provenance：根 BSD-3-Clause、upstream solarfactors/SunPower notices、pvlib notices 均存在，不据此推导未来复制代码已获得许可审查。模块 provenance/独立实现说明及 package notices/SBOM 属 A11 义务；疑问按强制 stop 处理。
