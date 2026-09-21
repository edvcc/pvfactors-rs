import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reference/tools"))
sys.path.insert(0, str(ROOT / "reference/compare"))

from compare_cross_runtime import METADATA_FIELDS, payload  # noqa: E402
from geometry_golden import CANONICAL_RUNTIME  # noqa: E402


class CanonicalRuntimeContractTests(unittest.TestCase):
    def test_r0_contract_is_not_silently_redefined(self):
        self.assertEqual(
            CANONICAL_RUNTIME,
            {
                "implementation": "CPython",
                "python": "3.12.14",
                "system": "Linux",
                "machine": "x86_64",
                "libc": {"name": "glibc", "version": "2.39"},
                "geos": "3.13.1",
                "thread_environment": {
                    "OPENBLAS_NUM_THREADS": "1",
                    "OMP_NUM_THREADS": "1",
                    "MKL_NUM_THREADS": "1",
                    "PYTHONHASHSEED": "0",
                },
            },
        )

    def test_cross_runtime_payload_excludes_only_metadata(self):
        artifact = {
            "reference": {"python": "3.12.12"},
            "generator": {"version": "0.1.0"},
            "provenance": {"generated_at": "example"},
            "case_id": "C01",
            "result": {"topology": {"active": [True]}},
        }

        self.assertEqual(
            payload(artifact),
            {
                "case_id": "C01",
                "result": {"topology": {"active": [True]}},
            },
        )
        self.assertEqual(METADATA_FIELDS, {"reference", "generator", "provenance"})


if __name__ == "__main__":
    unittest.main()
