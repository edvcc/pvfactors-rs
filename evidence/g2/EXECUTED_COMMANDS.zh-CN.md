# G2 已执行命令证据

日期：2026-09-21。命令在 `research/g2-geometry-acceptance` 执行；没有命令 merge 或 push。

| 目的 | 命令（保留关键参数） | 结果 / 证据 |
|---|---|---|
| 获取 refs | `git fetch --all --prune` | 完成；仅存在 `origin/master` |
| ZIP 身份 | `shasum -a 256 Solarfactors_Phase0_1_Baseline.zip` | `2aca31b4...f5729` |
| ZIP 内部完整性 | 在解压目录执行 `shasum -a 256 -c SHA256SUMS` | 121/121 OK；`zip-integrity.json` |
| 工作分支 | `git switch -c research/g2-geometry-acceptance` | 从 `bc0b7ec...` 创建 |
| Reference 环境 | 隔离执行 `uv pip install -r reference/requirements-canonical.txt`；`jsonschema==4.25.1` | 29/29 固定包匹配；Python patch 差异已记录 |
| 案例构建 | `python reference/tools/build_g2_cases.py` | 39 个具体案例；generator-exact rebuild PASS |
| Candidate pipeline | `python reference/tools/geometry_golden.py pipeline --output reference/candidate/geometry-golden-v0.1` | PASS；39 cases / 117 artifacts |
| 可复现性 | `python reference/compare/reproduce_geometry.py --report evidence/g2/reproducibility.json` | PASS；两次生成字节级一致 |
| Candidate 比较 | fresh pipeline 后执行 `compare_geometry.py candidate fresh` | PASS；无差异；`candidate-compare.json` |
| Upstream tests | `python -m pytest pvfactors/tests -q --junitxml=evidence/g2/upstream-pytest.xml` | 102 passed / 11 warnings；保留 text/XML log |
| 最终共享验证器 | `python scripts/verify_g2.py --output evidence/g2/final-verification.json` | 必要检查 PASS；runtime 差异单独报告 |
| Branch safety | verifier 比较 branch 与 `master` / `origin/master` | PASS；两个 master ref 均保持 `bc0b7ec...` |

Terminal transcript 由上述生成的 text/XML/JSON 证据与准确命令共同表达。结构性 PASS 不会消除
CPython 3.12.14 不可用条件，也不代表 Owner 批准。
