import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from verify_g2 import (  # noqa: E402
    APPROVED_MANIFEST_SHA256,
    approved_safety,
    p3_entry_contract,
)


class G2ApprovalClosureTests(unittest.TestCase):
    def test_approved_corpus_is_exact_immutable_promotion(self):
        report = approved_safety()
        self.assertTrue(report["pass"], report["failures"])
        self.assertTrue(report["candidate_approved_byte_identity"])
        self.assertEqual(report["approved_manifest_sha256"], APPROVED_MANIFEST_SHA256)
        self.assertEqual(report["manifest_hashes"], {
            "candidate": APPROVED_MANIFEST_SHA256,
            "approved": APPROVED_MANIFEST_SHA256,
        })
        self.assertEqual(report["case_count"], 55)
        self.assertEqual(report["artifact_count"], 165)

    def test_active_p3_contract_matches_approved_objects(self):
        report = p3_entry_contract()
        self.assertTrue(report["pass"], report["failures"])
        self.assertEqual(report["approved_case_count"], 55)


if __name__ == "__main__":
    unittest.main()
