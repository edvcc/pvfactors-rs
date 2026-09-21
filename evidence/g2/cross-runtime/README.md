# G2 Cross-Runtime Evidence

Owner Review Revision 1 was generated independently on macOS arm64 / CPython
3.12.12 and Canonical Reference Runtime R0. Both used generator commit
`75b31ff01e6ff438d0f24c8ea7d6e6f92ab6c553`, the same 45-case catalog, and the
unchanged `geometry-tolerance-v0.1`.

- macOS manifest: `9e6d23ab458dc0a7d28e325ddf01d109439881f5f06837238427547558a20c21`
- R0 manifest: `d805262560199583dad12853b422c2976bd40866cf4ff1c50133206c79b71417`
- Exact topology/key/side/source/reference/active/order/classification checks:
  23,528, all matched.
- Numerical violations: 0.
- Maximum absolute differences: angle 0, length
  `5.551115123125783e-16 m`, orientation `5.551115123125783e-17`, position
  `4.996003610813204e-16 m`.

`comparison.json` excludes only provenance/environment metadata from the
Geometry payload comparison. The environment IDs differ as expected; R0 alone
has `canonical_environment_match=true`.

Historical evidence is not overwritten: the superseded 39-case R0 manifest
`5afcc7e2...57e3f` and validation summary are under `evidence/g2/history/`.
The pre-Revision-1 macOS corpus remains retrievable from Git commit
`182dbb54d351db733ff40ba40dd4f119767b1ee4`.

All candidates remain unapproved. Candidate replacement is not promotion into
`reference/approved`.
