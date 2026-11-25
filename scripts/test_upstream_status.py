"""--strict must fail on every state that needs a human decision, including rejected."""
import unittest
from unittest import mock

import upstream_status


class Strict(unittest.TestCase):
    def run_with(self, state, strict=True):
        entry = {"ref": "jira:LT-1", "kind": "issue", "affects": "loader", "note": "n"}
        with mock.patch.object(upstream_status, "fixture_dirs", return_value=[upstream_status.ROOT / "edge-cases" / "x"]), \
             mock.patch.object(upstream_status, "load_words", return_value={"upstream": [entry]}), \
             mock.patch.object(upstream_status, "resolve", return_value=(state, "r")), \
             mock.patch("builtins.print"):
            return upstream_status.main(["--strict"] if strict else [])

    def test_strict(self):
        for state in ("merged", "closed-unmerged", "issue-closed", "rejected"):
            self.assertEqual(self.run_with(state), 1, state)
        for state in ("pending", "satisfied"):
            self.assertEqual(self.run_with(state), 0, state)
        self.assertEqual(self.run_with("rejected", strict=False), 0)


if __name__ == "__main__":
    unittest.main()
