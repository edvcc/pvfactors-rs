# G2 Cross-Runtime Evidence

Owner Review Revision 2 was generated independently on macOS arm64 / CPython
3.12.12 and Canonical Reference Runtime R0. Both used generator commit
`01549e07c16bfe10a82d2889b1b62c58ef6861e7`, the same 55-case catalog, and the
unchanged `geometry-tolerance-v0.1`.

- macOS manifest: `adc63fa3594665a1a919f28fe99b0ff895642e091d9ec60e56e35b6a32c9c8cd`
- R0 manifest: `efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- Exact topology/key/side/source/reference/active/order/classification checks:
  24,391, all matched.
- Numerical violations: 0.
- Maximum absolute differences: angle 0, length
  `5.551115123125783e-16 m`, orientation `5.551115123125783e-17`, position
  `8.881784197001252e-16 m`.

`comparison.json` excludes only provenance/environment metadata from the
Geometry payload comparison. The environment IDs differ as expected; R0 alone
has `canonical_environment_match=true`.

Historical evidence is not overwritten: the superseded 39-case and 45-case R0
manifests and validation summaries are under `evidence/g2/history/`.
The pre-Revision-1 macOS corpus remains retrievable from Git commit
`182dbb54d351db733ff40ba40dd4f119767b1ee4`.

On 2026-09-22, the Repository Owner approved the exact R0 candidate manifest
`efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`.
That payload is preserved byte-for-byte at
`reference/approved/geometry-golden-v0.1`; approval metadata is recorded
separately so the generation manifest and historical cross-runtime evidence
remain unchanged.
