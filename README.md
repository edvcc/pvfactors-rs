# pvfactors-rs — Phase 0–1 Baseline and P2 / G2 Candidate

日期：2026-09-21；Reference：solarfactors v1.6.1，commit ecbfc863657e239817603a43898ae173c7ccad9c。

`pvfactors-rs` 是参考 pvlib/solarfactors 与 pvfactors 行为进行的独立 Rust 重实现项目。
本仓库当前包含研究、算法重建、工程基线、P2 / G2 Geometry Acceptance tooling 与
candidate，不含 Rust Geometry Core 实现。Phase 0–1 结论为 **CONDITIONALLY READY**；
G2 状态见 [G2 Geometry Acceptance Review](docs/g2/G2_GEOMETRY_ACCEPTANCE_REVIEW.zh-CN.md)。
CDR 与 Geometry Golden 均须 Repository Owner 人工批准。

- docs/00–13：要求的14份文档；14为额外证据/追踪索引。
- upstream/solarfactors：78个原始文件的冻结快照，带BSD许可证；不是完整Git历史克隆。
- evidence：实际运行日志、源文件hash、22个主链探针、额外边界探针、nominal中间trace、issues与机器索引。
- reference：29包lock、研究复现脚本、67个 Phase 0–1 case、39个 G2 concrete case、
  capture/normalize/schema/compare/invariant tooling；`candidate/` 不等于 `approved/`。

## 重现研究环境

需要Linux x86_64 CPython3.12.14。下述lock针对该平台wheel，其他平台需另建manifest，不可宣称同一个hash lock通用。

```bash
python3.12 -m venv .venv-reference
.venv-reference/bin/python -m pip install --require-hashes -r reference/requirements-linux-cp312.lock
.venv-reference/bin/python reference/generator/reproduce_reference.py --verify-only
.venv-reference/bin/python reference/generator/reproduce_reference.py --output-dir reference/candidates/replay-01 --probes
.venv-reference/bin/python reference/generator/probe_boundaries.py --output-file reference/candidates/boundaries-01.json
```

output目录/文件必须是新的，防止覆盖取证结果。重现脚本不自动安装软件、不改冻结源码、不更新approved Golden。测试日志与probe输出写入指定candidate路径。canonical运行时更详细的BLAS、GEOS、Python构建信息见evidence/runtime.json。

当前generator是研究复现入口，不是06所设计的全层Golden capture/comparator成品；请按G2实现并审核后才批准Corpus。

本包自撰规格与第三方源文件分别保留来源。solarfactors许可证在upstream/solarfactors/LICENSE；pvlib源码摘录许可证在reference/PVLIB_LICENSE.txt。论文链接只用于证据，不把全文复制进包。SHA256SUMS列出包内文件完整性摘要。
