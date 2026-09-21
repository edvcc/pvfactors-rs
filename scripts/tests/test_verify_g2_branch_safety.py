import os
import subprocess
import unittest
from unittest.mock import patch

import scripts.verify_g2 as verify_g2


ORIGIN_MASTER = "1111111111111111111111111111111111111111"
HEAD = "2222222222222222222222222222222222222222"


def git_result(branch: str):
    def fake_git(*args: str) -> str:
        if args == ("branch", "--show-current"):
            return branch
        if args == ("rev-parse", "HEAD"):
            return HEAD
        if args == (
            "rev-parse",
            "--verify",
            "refs/remotes/origin/master",
        ):
            return ORIGIN_MASTER
        raise AssertionError(f"unexpected git invocation: {args}")

    return fake_git


class BranchSafetyTests(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    @patch.object(verify_g2, "git", side_effect=git_result("research/g2"))
    def test_local_feature_branch(self, _git):
        result = verify_g2.branch_safety()

        self.assertTrue(result["pass"])
        self.assertEqual(result["mode"], "local")
        self.assertEqual(result["logical_branch"], "research/g2")
        self.assertEqual(result["origin_master"], ORIGIN_MASTER)

    @patch.dict(
        os.environ,
        {
            "GITHUB_ACTIONS": "true",
            "GITHUB_EVENT_NAME": "push",
            "GITHUB_REF_TYPE": "branch",
            "GITHUB_REF_NAME": "develop",
        },
        clear=True,
    )
    @patch.object(verify_g2, "git", side_effect=git_result("develop"))
    def test_github_push(self, _git):
        result = verify_g2.branch_safety()

        self.assertTrue(result["pass"])
        self.assertEqual(result["mode"], "github_push")
        self.assertEqual(result["logical_branch"], "develop")

    @patch.dict(
        os.environ,
        {
            "GITHUB_ACTIONS": "true",
            "GITHUB_EVENT_NAME": "pull_request",
            "GITHUB_HEAD_REF": "research/g2",
            "GITHUB_BASE_REF": "develop",
            "GITHUB_REF": "refs/pull/12/merge",
        },
        clear=True,
    )
    @patch.object(verify_g2, "git", side_effect=git_result(""))
    def test_github_pull_request_detached_head(self, _git):
        result = verify_g2.branch_safety()

        self.assertTrue(result["pass"])
        self.assertEqual(result["mode"], "github_pull_request")
        self.assertEqual(result["branch"], "")
        self.assertEqual(result["logical_branch"], "research/g2")
        self.assertEqual(result["base_branch"], "develop")

    @patch.dict(os.environ, {}, clear=True)
    @patch.object(verify_g2, "git", side_effect=git_result("master"))
    def test_local_master_is_rejected(self, _git):
        result = verify_g2.branch_safety()

        self.assertFalse(result["pass"])
        self.assertIn("verification is running on master", result["failures"])

    @patch.dict(os.environ, {}, clear=True)
    @patch.object(verify_g2, "git", side_effect=git_result(""))
    def test_local_detached_head_is_rejected(self, _git):
        result = verify_g2.branch_safety()

        self.assertFalse(result["pass"])
        self.assertIn(
            "detached HEAD is only supported for GitHub pull_request",
            result["failures"],
        )

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_origin_master_is_rejected(self):
        def fake_git(*args: str) -> str:
            if args == ("branch", "--show-current"):
                return "research/g2"
            if args == ("rev-parse", "HEAD"):
                return HEAD
            if args == (
                "rev-parse",
                "--verify",
                "refs/remotes/origin/master",
            ):
                raise subprocess.CalledProcessError(128, ["git", *args])
            raise AssertionError(f"unexpected git invocation: {args}")

        with patch.object(verify_g2, "git", side_effect=fake_git):
            result = verify_g2.branch_safety()

        self.assertFalse(result["pass"])
        self.assertIsNone(result["origin_master"])
        self.assertIn(
            "authoritative ref refs/remotes/origin/master is missing",
            result["failures"],
        )


if __name__ == "__main__":
    unittest.main()
