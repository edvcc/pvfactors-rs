# G2 Cross-Runtime Evidence

The left-hand candidate was generated on macOS arm64 / CPython 3.12.12 and is
preserved here before replacement. Its complete artifact corpus remains
retrievable from Git commit `182dbb54d351db733ff40ba40dd4f119767b1ee4`; its
manifest SHA-256 is
`b51e626e19734fce0d27e7c7a85c929f16a082e34e56343617b0dc6b83e76920`.

The right-hand candidate was generated in Canonical Reference Runtime R0 from
generator commit `50500914c227aaeaf738b785eea3a20d96e8ee28`. Its manifest
SHA-256 is
`5afcc7e2cbc761ef883a422dd596e972cda603313a27f8425278dd067be57e3f`.

`comparison.json` separates algorithm/Geometry payload from the expected
provenance and environment metadata differences. It records exact topology,
key, side, index, active-state, input, classification, and nonfinite checks,
plus numerical comparisons under the unchanged `geometry-tolerance-v0.1`.

Both candidates remain unapproved. Replacement of the candidate directory is
not an approval or a promotion into `reference/approved`.
