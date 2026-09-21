# G2 Owner Review Revision 1 已执行命令证据

日期：2026-09-22。命令在 `research/g2-owner-review-closure` 执行；没有命令 merge 分支，
也未修改 `master`、`develop`、frozen upstream、tolerance 或 `reference/approved`。

| 目的 | 命令（保留关键参数） | 结果 / 证据 |
|---|---|---|
| 获取 refs | `git fetch --all --prune` | `origin/develop=ddee1f43...`，`origin/master=bc0b7ec1...` |
| 工作分支 | `git switch -c research/g2-owner-review-closure origin/develop` | 从最新 integration baseline 创建 |
| 最小迁移 | `git cherry-pick 5050091 145f4a1 cf2fd83` | 新 commit `fc86112`、`8033eff`、`76015e1`；无冲突 |
| CDR/case 冻结 | 两个聚焦的 generator commit | 最终 generator commit `75b31ff0...`；45 个具体案例；corrected-field provenance 完整 |
| R0 镜像 | `docker build --platform linux/amd64 -f reference/runtime/r0/Dockerfile -t pvfactors-rs-g2-r0:cp31214 .` | 镜像 `sha256:677db45c...45ada3`；R0 精确匹配 |
| Canonical candidate | R0 容器：`python3.12 reference/tools/geometry_golden.py pipeline` | PASS；45 cases / 135 artifacts；manifest `d8052625...1417` |
| Source/共享 verifier | R0 容器：`python3.12 scripts/verify_g2.py` | PASS；78 个 source blob、case exact rebuild、schema、54 个 invariant report、39 条 provenance、8 对文档、branch 与 approved safety |
| R0 可复现性 | R0 容器：`python3.12 reference/compare/reproduce_geometry.py` | PASS；两次完整生成字节级一致 |
| macOS 对照 corpus | 隔离 macOS arm64 / CPython 3.12.12 pipeline，两次 | PASS；每次 45/135；字节级一致；manifest `9e6d23ab...0c21` |
| Cross-runtime 比较 | `python3 reference/compare/compare_cross_runtime.py macos-candidate r0-candidate` | PASS；23,528 个 topology 精确检查；exact/numerical violation 均为 0 |
| Unit/guardrail test | `python3 -m unittest discover -s scripts/tests -v` | 14 passed，覆盖 domain revision、canonical runtime、frozen bytes 与 branch mode |
| Candidate compare | `geometry_golden.py compare checked-in-candidate independent-r0-candidate` | PASS；字节级一致 |
| 远端发布 | push branch 并新建指向 `develop` 的 PR | 本证据文件提交时待执行；最终 URL/result 在 immutable generation manifest 之外报告 |

已被取代的 39-case manifest `5afcc7e2...57e3f` 保留在 `evidence/g2/history/`。
R0 与 cross-runtime PASS 不代表 Owner 批准。
