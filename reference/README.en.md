# Reference geometry workspace

This directory contains development-only evidence and tooling for the frozen
`pvlib/solarfactors` v1.6.1 reference at commit
`ecbfc863657e239817603a43898ae173c7ccad9c`. It is not a runtime dependency of
the future Rust core.

- `cases/`: canonical and G2 concrete inputs.
- `capture/`: direct reference capture entry point.
- `normalize/`: language-neutral canonicalization entry point.
- `schemas/`: JSON Schemas.
- `candidate/`: generated artifacts awaiting owner approval.
- `approved/`: intentionally empty until explicit owner approval.
- `compare/`: byte comparison and reproducibility runner.
- `validate/`: schema and independent-invariant validation.
- `tolerance/`: Geometry Gate tolerance profile only.
- `tools/`: shared implementation.

The raw reference and corrected expectation are always separate. No tool writes
to `upstream/solarfactors` or to `reference/approved`.

