# Reference Geometry 工作区

本目录保存冻结 Reference `pvlib/solarfactors` v1.6.1（commit
`ecbfc863657e239817603a43898ae173c7ccad9c`）的开发期证据与工具。它不是未来
Rust Core 的运行时依赖。

- `cases/`：Canonical 输入与 G2 具体案例；
- `capture/`：直接 Reference 采集入口；
- `normalize/`：语言无关的规范化入口；
- `schemas/`：JSON Schema；
- `candidate/`：等待 Owner 批准的生成产物；
- `approved/`：在 Owner 明确批准前保持为空；
- `compare/`：字节级比较与重复生成工具；
- `validate/`：Schema 与独立不变量验证；
- `tolerance/`：仅适用于 Geometry Gate 的 tolerance profile；
- `tools/`：共享实现。

raw reference 与 corrected expectation 始终分离。任何工具都不得写入
`upstream/solarfactors` 或 `reference/approved`。

