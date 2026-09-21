# G2 已执行命令证据

日期：2026-09-21。命令在 `research/g2-geometry-acceptance` 执行；没有命令 merge；分支 push
仅用于 PR 验证。

| 目的 | 命令（保留关键参数） | 结果 / 证据 |
|---|---|---|
| 获取 refs | `git fetch --all --prune` | 完成；仅存在 `origin/master` |
| ZIP 身份 | `shasum -a 256 Solarfactors_Phase0_1_Baseline.zip` | `2aca31b4...f5729` |
| ZIP 内部完整性 | 在解压目录执行 `shasum -a 256 -c SHA256SUMS` | 121/121 OK；`zip-integrity.json` |
| 工作分支 | `git switch -c research/g2-geometry-acceptance` | 从 `bc0b7ec...` 创建 |
| 保留的旧环境 | macOS arm64 / CPython 3.12.12 隔离运行 | manifest、summary、verifier、reproducibility 记录保存在 `evidence/g2/cross-runtime/` |
| R0 镜像 | `docker build --platform linux/amd64 -f reference/runtime/r0/Dockerfile -t pvfactors-rs-g2-r0:cp31214 .` | 镜像 `sha256:677db45c...45ada3`；R0 精确匹配，29/29 package |
| 案例构建 | `python reference/tools/build_g2_cases.py` | 39 个具体案例；generator-exact rebuild PASS |
| Canonical candidate pipeline | R0 容器：`python3.12 reference/tools/geometry_golden.py pipeline --output /output/geometry-golden-v0.1` | PASS；39 cases / 117 artifacts；manifest `5afcc7e2...57e3f` |
| R0 可复现性 | R0 容器：`python3.12 reference/compare/reproduce_geometry.py --report /output/reproducibility-r0.json` | PASS；两次生成字节级一致 |
| Cross-runtime 比较 | `python3 reference/compare/compare_cross_runtime.py old-macos-candidate new-r0-candidate` | PASS；19,511 个 topology 精确检查；无数值 tolerance 失败 |
| Upstream tests | `python -m pytest pvfactors/tests -q --junitxml=evidence/g2/upstream-pytest.xml` | 102 passed / 11 warnings；保留 text/XML log |
| 最终共享验证器 | R0 容器：`python3.12 scripts/verify_g2.py --candidate /output/geometry-golden-v0.1` | PASS；source integrity、rebuild、schema、43 invariants、audit、docs、branch 与 approved safety |
| Branch safety | verifier 以 `origin/master` 为 authoritative remote ref | PASS；`origin/master` 保持 `bc0b7ec...` |
| 最终远端状态 | `git ls-remote origin refs/heads/master refs/heads/develop refs/heads/research/g2-geometry-acceptance` | master `bc0b7ec...`；develop `ddee1f4...` 来自更早的外部 PR #1 merge；本任务只 push research |

Terminal transcript 由上述生成的 text/XML/JSON 证据与准确命令共同表达。R0 与
cross-runtime PASS 已关闭 runtime 条件，但不代表 Owner 批准。
