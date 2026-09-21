# Canonical Geometry Reference Runtime R0

This image is the reproducible generation environment for the G2 Geometry
Golden candidate. It is separate from ordinary pull-request CI.

- Base: Canonical Ubuntu 24.04 amd64, pinned by OCI digest.
- libc: glibc 2.39.
- Python: CPython 3.12.14 built from the python.org source archive whose
  SHA-256 is pinned in the Dockerfile.
- Python packages: `reference/requirements-linux-cp312.lock` with required
  hashes; `jsonschema==4.25.1` and its dependency graph are also version-pinned
  as validation tooling in the Dockerfile.
- Determinism variables: `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`,
  `MKL_NUM_THREADS=1`, and `PYTHONHASHSEED=0`.

Build on any Docker host with amd64 support:

```sh
docker build --platform linux/amd64 \
  --file reference/runtime/r0/Dockerfile \
  --tag pvfactors-rs-g2-r0 .
```

Run generation into a separate, initially absent output directory mounted at
`/output`. Mount the repository read-only so generation cannot mutate the
frozen reference or the current candidate:

```sh
docker run --rm --platform linux/amd64 \
  --env OPENBLAS_NUM_THREADS=1 \
  --env OMP_NUM_THREADS=1 \
  --env MKL_NUM_THREADS=1 \
  --env PYTHONHASHSEED=0 \
  --volume "$PWD:/workspace:ro" \
  --volume "/absolute/output/parent:/output" \
  pvfactors-rs-g2-r0 \
  python3.12 reference/tools/geometry_golden.py pipeline \
    --output /output/geometry-golden-v0.1
```
