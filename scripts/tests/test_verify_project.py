"""Synthetic mutations validate the gate, never manufacture production expected."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verify_project as verify


class AcceptanceHarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="readiness-selftest-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.expected = self.root / "expected"
        self.actual = self.root / "actual"
        self.expected.mkdir()
        self.actual.mkdir()
        self.ids = ["SYNTHETIC_A", "SYNTHETIC_B"]
        for case in self.ids:
            artifact = {"case_id": case, "input": {"x": 1.0}, "nonfinite_mask": [],
                        "result": {"length_m": 1.0, "classification": "direct_projection",
                                   "logical_key": {"side": "front", "row": 0},
                                   "reference_index": 0, "active": True,
                                   "active_index": 0}}
            self.write(self.expected / f"{case}.json", artifact)
            self.write(self.actual / f"{case}.json", artifact)

    @staticmethod
    def write(path, artifact):
        path.write_text(json.dumps(artifact, allow_nan=False))

    def mutate(self, field, value):
        path = self.actual / "SYNTHETIC_A.json"
        item = verify.read(path)
        item["result"][field] = value
        self.write(path, item)

    def compare(self):
        return verify.compare_geometry(self.actual, self.expected, self.ids)

    def test_unchanged_synthetic_payload_passes(self):
        self.assertEqual(self.compare()["status"], "PASS")

    def test_required_case_omission_fails(self):
        (self.actual / "SYNTHETIC_B.json").unlink()
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_extra_case_fails(self):
        self.write(self.actual / "UNREQUIRED.json", {})
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_duplicate_required_case_fails(self):
        self.ids.append(self.ids[0])
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_surface_key_mutation_fails(self):
        self.mutate("logical_key", {"side": "back", "row": 0})
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_reference_index_mutation_fails(self):
        self.mutate("reference_index", 1)
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_bool_cannot_impersonate_exact_integer_index(self):
        self.mutate("reference_index", False)
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_projection_class_mutation_fails(self):
        self.mutate("classification", "horizon_no_direct_projection")
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_active_state_is_exact(self):
        self.mutate("active", False)
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_ten_times_tolerance_fails(self):
        tol = verify.read(verify.TOLERANCE)["comparison"]["length"]
        self.mutate("length_m", 1.0 + 10 * (tol["absolute"] + tol["relative"]))
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_allowed_numeric_difference_passes(self):
        tol = verify.read(verify.TOLERANCE)["comparison"]["length"]
        self.mutate("length_m", 1.0 + 0.5 * tol["absolute"])
        self.assertEqual(self.compare()["status"], "PASS")

    def test_numeric_type_mutation_fails(self):
        self.mutate("length_m", 1)
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_missing_numeric_field_fails(self):
        path = self.actual / "SYNTHETIC_A.json"
        item = verify.read(path)
        del item["result"]["length_m"]
        self.write(path, item)
        self.assertEqual(self.compare()["status"], "FAIL")

    def test_nonstandard_nan_is_rejected(self):
        path = self.actual / "SYNTHETIC_A.json"
        path.write_text('{"result": NaN}')
        with self.assertRaises(ValueError):
            self.compare()

    def test_approved_manifest_mutation_detected(self):
        path = self.root / "manifest.json"
        path.write_text('{"approved":true}')
        lock = {"manifest.json": verify.blob(path.read_bytes())}
        self.assertEqual(verify.verify_files(self.root, lock), [])
        path.write_text('{"approved":false}')
        self.assertTrue(verify.verify_files(self.root, lock))

    def test_frozen_source_mutation_detected(self):
        path = self.root / "source.py"
        path.write_text("original source\n")
        lock = {"source.py": verify.blob(path.read_bytes())}
        path.write_text("changed source\n")
        self.assertTrue(verify.verify_files(self.root, lock))

    def test_missing_artifact_fails(self):
        (self.root / "run.json").write_text('{}')
        self.assertEqual(verify.required_artifacts(self.root, ["run.json"])["status"], "PASS")
        (self.root / "run.json").unlink()
        self.assertEqual(verify.required_artifacts(self.root, ["run.json"])["status"], "FAIL")

    def test_empty_artifact_fails(self):
        (self.root / "run.json").touch()
        self.assertEqual(verify.required_artifacts(self.root, ["run.json"])["status"], "FAIL")

    def test_zero_test_success_fails(self):
        text = "running 0 tests\ntest result: ok. 0 passed; 0 failed; 0 ignored;"
        self.assertEqual(verify.parse_tests(text)["status"], "FAIL")

    def test_geometry_approval_cannot_authorize_later_or_final_acceptance(self):
        for args in (["final"], ["milestone", "viewfactor"]):
            with self.subTest(args=args):
                output = self.root / "scope.json"
                with patch.object(sys, "argv", ["verify_project.py", *args, "--scope", "geometry",
                                               "--output", str(output)]), patch("builtins.print"):
                    self.assertEqual(verify.main(), 1)
                report = verify.read(output)
                self.assertEqual(report["status"], "FAIL")
                self.assertIn("require full-project approval", report["error"])

    def test_missing_required_test_fails(self):
        text = "test one ... ok\ntest result: ok. 1 passed; 0 failed; 0 ignored;"
        self.assertEqual(verify.parse_tests(text, ["one", "two"])["status"], "FAIL")

    def test_false_summary_fails(self):
        text = "test one ... ok\ntest result: ok. 2 passed; 0 failed; 0 ignored;"
        self.assertEqual(verify.parse_tests(text)["status"], "FAIL")

    def test_ignored_case_fails(self):
        text = "test one ... ignored\ntest two ... ok\ntest result: ok. 1 passed; 0 failed; 1 ignored;"
        self.assertEqual(verify.parse_tests(text)["status"], "FAIL")

    def test_real_named_test_format_passes(self):
        text = "test one ... ok\ntest result: ok. 1 passed; 0 failed; 0 ignored;"
        self.assertEqual(verify.parse_tests(text, ["one"])["status"], "PASS")

    def test_no_implementation_cannot_pass_milestone(self):
        m = verify.read(verify.DOCS / "acceptance-matrix.json")["milestones"][0]
        with patch.object(verify, "ROOT", self.root):
            self.assertEqual(verify.milestone(m)["status"], "NOT_READY")

    def test_unknown_comparator_cannot_pass(self):
        m = copy.deepcopy(verify.read(verify.DOCS / "acceptance-matrix.json")["milestones"][0])
        m.update(implementation_files=[], runner_file="runner.rs", checker="unapproved")
        (self.root / "runner.rs").touch()
        with patch.object(verify, "ROOT", self.root):
            self.assertEqual(verify.milestone(m)["status"], "NOT_READY")

    def test_failed_gate_cannot_execute_adapter(self):
        m = copy.deepcopy(verify.read(verify.DOCS / "acceptance-matrix.json")["milestones"][0])
        m.update(implementation_files=[], runner_file="runner.rs")
        (self.root / "runner.rs").touch()
        with patch.object(verify, "ROOT", self.root), patch.object(verify, "command") as run:
            self.assertEqual(verify.milestone(m, execute=False)["status"], "NOT_READY")
            run.assert_not_called()

    def test_golden_projection_retains_every_identity(self):
        data = verify.read(verify.GOLDEN / "corrected/C01.json")
        projected = verify.geometry_payload(data)
        self.assertEqual(projected["result"]["topology"], data["result"]["topology"])
        self.assertEqual(projected["result"]["surfaces"], data["result"]["surfaces"])

    def test_diagnostic_text_projection_does_not_remove_error_code(self):
        data = verify.read(verify.GOLDEN / "corrected/INVALID_NAN.json")
        projected = verify.geometry_payload(data)
        self.assertNotIn("message", projected["result"]["errors"][0])
        self.assertEqual(projected["result"]["errors"][0]["code"], "GEOMETRY_NONFINITE")

    def test_all_55_approved_payloads_comparator_selfcheck(self):
        # Roundtrip is comparator verification only, never evidence of Rust execution.
        for path in self.actual.glob("*.json"):
            path.unlink()
        for path in (verify.GOLDEN / "corrected").glob("*.json"):
            self.write(self.actual / path.name, verify.geometry_payload(verify.read(path)))
        report = verify.compare_geometry(self.actual)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["cases_run"], 55)


if __name__ == "__main__":
    unittest.main()
