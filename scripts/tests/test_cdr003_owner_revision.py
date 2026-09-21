import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reference/tools"))

from build_g2_cases import build  # noqa: E402
from geometry_golden import projection_policy_state, validate_v1  # noqa: E402


class Cdr003OwnerRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {case["id"]: case for case in build()["cases"]}

    def test_concrete_owner_review_cases_are_present(self):
        self.assertEqual(len(self.cases), 45)
        for case_id in (
            "TILT_120", "TILT_180", "GCR_GT_1", "SUN_BELOW_HORIZON",
            "INVALID_TILT_NEGATIVE", "INVALID_TILT_GT_180",
        ):
            self.assertIn(case_id, self.cases)

    def test_expanded_tilt_and_gcr_domain_is_not_proxy_rejected(self):
        for case_id in ("TILT_120", "TILT_180", "GCR_GT_1"):
            self.assertEqual(validate_v1(self.cases[case_id]), [], case_id)

    def test_tilt_outside_closed_domain_is_structured_error(self):
        for case_id in ("INVALID_TILT_NEGATIVE", "INVALID_TILT_GT_180"):
            errors = validate_v1(self.cases[case_id])
            self.assertTrue(errors, case_id)
            self.assertEqual(errors[0]["code"], "GEOMETRY_TILT_UNSUPPORTED")

    def test_solar_projection_states_cover_closed_representation_domain(self):
        self.assertEqual(projection_policy_state(0.0), "direct_projection")
        self.assertEqual(projection_policy_state(89.999), "direct_projection")
        self.assertEqual(projection_policy_state(90.0), "horizon_no_direct_projection")
        self.assertEqual(projection_policy_state(100.0), "below_horizon_no_direct_projection")
        self.assertEqual(projection_policy_state(180.0), "below_horizon_no_direct_projection")


if __name__ == "__main__":
    unittest.main()
