import json
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "reference/tools"))

from build_g2_cases import build  # noqa: E402


class Cdr006OwnerRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {case["id"]: case for case in build()["cases"]}
        cls.tolerance = json.loads(
            (ROOT / "reference/tolerance/geometry-tolerance-v0.1.json").read_text(encoding="utf-8")
        )["algorithm_predicates"]

    def test_predicate_values_and_operators_are_unchanged(self):
        self.assertEqual(self.tolerance["active_length_m"], 1e-8)
        self.assertEqual(self.tolerance["endpoint_snap_m"], 1e-8)
        self.assertEqual(self.tolerance["orientation_normalized_cross_abs"], 1e-12)
        self.assertEqual(self.tolerance["position_offset_abs_m"], 1e-10)
        self.assertEqual(self.tolerance["scale_roundoff_factor"], 64.0)
        self.assertEqual(self.tolerance["boundary_operators"], {
            "active": "length > active_length_m",
            "endpoint_snap": "distance < endpoint_snap_m",
            "orientation": (
                "normalized_abs_cross <= max(orientation_normalized_cross_abs, "
                "scale_roundoff_factor*f64_epsilon)"
            ),
            "position_offset": "distance <= scale_aware_position_offset",
        })

    def test_each_added_predicate_has_minus_exact_plus_ulp_cases(self):
        families = {
            "ENDPOINT_SNAP": (1e-8, "snapped", (True, False, False)),
            "ORIENTATION": (1e-12, "parallel", (True, True, False)),
            "LINE_OFFSET": (1e-10, "within", (True, True, False)),
        }
        value_keys = {
            "ENDPOINT_SNAP": "distance_m",
            "ORIENTATION": "normalized_abs_cross",
            "LINE_OFFSET": "offset_m",
        }
        for family, (threshold, decision, expected_decisions) in families.items():
            values = []
            decisions = []
            for label in ("MINUS_ULP", "EXACT", "PLUS_ULP"):
                case = self.cases[f"PRIM_{family}_{label}"]
                values.append(case["expected"][value_keys[family]])
                decisions.append(case["expected"][decision])
            self.assertEqual(values, [
                math.nextafter(threshold, 0.0),
                threshold,
                math.nextafter(threshold, math.inf),
            ])
            self.assertEqual(tuple(decisions), expected_decisions)

    def test_dev013_case_is_multi_timestep_and_requests_index_one(self):
        case = self.cases["MULTI_TIMESTEP_NONZERO_INDEX"]
        self.assertIn("DEV-013", case["tags"])
        self.assertEqual(case["expected"]["requested_frame_index"], 1)
        self.assertEqual(case["expected"]["v1_nonzero_index_policy"], "evaluate_requested_frame")
        for name in ("solar_zenith", "solar_azimuth", "surface_tilt", "surface_azimuth"):
            self.assertEqual(len(case["inputs"][name]), 2)


if __name__ == "__main__":
    unittest.main()
