import hashlib
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "upstream/solarfactors"
CRLF_CANARIES = {
    "pvfactors/tests/test_files/file_test_df_perez_luminance.csv":
        "75e2ab3e76bc297df4e436c613b33fa64daa42b2",
    "pvfactors/tests/test_files/file_test_multiprocessing_inputs.csv":
        "84720abf380804ec234c37e2f365edbb393d9a94",
}


def raw_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


class FrozenUpstreamBytePolicyTests(unittest.TestCase):
    def test_snapshot_disables_git_text_normalization(self):
        for relative_path in CRLF_CANARIES:
            repository_path = f"upstream/solarfactors/{relative_path}"
            result = subprocess.check_output(
                ["git", "check-attr", "text", "--", repository_path],
                cwd=ROOT,
                text=True,
            ).strip()
            self.assertEqual(result, f"{repository_path}: text: unset")

    def test_crlf_canaries_keep_upstream_blob_identity(self):
        for relative_path, expected_sha in CRLF_CANARIES.items():
            with self.subTest(path=relative_path):
                self.assertEqual(
                    raw_blob_sha(SNAPSHOT / relative_path),
                    expected_sha,
                )


if __name__ == "__main__":
    unittest.main()
