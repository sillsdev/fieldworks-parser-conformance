"""Unit tests for scripts/upstream.py: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import upstream

HEAD40 = "a" * 40


def fake_gh(stdout=None, code=0, stderr="", exc=None):
    def run(cmd, **kw):
        if cmd[0] == "git":
            return subprocess.run(cmd, **kw)
        if exc:
            raise exc
        return SimpleNamespace(returncode=code, stdout=json.dumps(stdout) if stdout is not None else "", stderr=stderr)
    return run


def git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *a],
                          check=True, capture_output=True, text=True).stdout.strip()


class Resolve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.repo = Path(cls.tmp.name)
        git(cls.repo, "init", "-q")
        git(cls.repo, "commit", "-q", "--allow-empty", "-m", "one")
        cls.first = git(cls.repo, "rev-parse", "HEAD")
        git(cls.repo, "commit", "-q", "--allow-empty", "-m", "two")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def pr(self, affects="engine", head=None):
        return {"ref": "sillsdev/machine#615", "kind": "pr", "head": head or HEAD40, "affects": affects}

    def test_ancestry_satisfies_without_gh(self):
        def boom(cmd, **kw):
            if cmd[0] == "gh":
                raise AssertionError("gh must not be called")
            return subprocess.run(cmd, **kw)
        state, _ = upstream.resolve(self.pr(head=self.first), self.repo, run=boom)
        self.assertEqual(state, "satisfied")

    def test_unknown_head_falls_to_gh_open(self):
        state, reason = upstream.resolve(self.pr(), self.repo, run=fake_gh({"state": "OPEN"}))
        self.assertEqual((state, reason), ("pending", "open"))

    def test_merged_and_contained(self):
        out = {"state": "MERGED", "mergeCommit": {"oid": self.first}}
        self.assertEqual(upstream.resolve(self.pr(), self.repo, run=fake_gh(out))[0], "satisfied")

    def test_merged_not_contained_or_no_checkout(self):
        out = {"state": "MERGED", "mergeCommit": {"oid": "b" * 40}}
        self.assertEqual(upstream.resolve(self.pr(), self.repo, run=fake_gh(out))[0], "merged")
        self.assertEqual(upstream.resolve(self.pr("loader"), None, run=fake_gh(out))[0], "merged")

    def test_closed_pr(self):
        self.assertEqual(upstream.resolve(self.pr(), None, run=fake_gh({"state": "CLOSED"}))[0], "closed-unmerged")

    def test_issues(self):
        e = {"ref": "sillsdev/FieldWorks#9", "kind": "issue", "affects": "loader"}
        self.assertEqual(upstream.resolve(e, run=fake_gh({"state": "OPEN"}))[0], "pending")
        state, reason = upstream.resolve(e, run=fake_gh({"state": "CLOSED", "stateReason": "COMPLETED"}))
        self.assertEqual(state, "issue-closed")
        self.assertIn("COMPLETED", reason)

    def test_gh_missing_unauthenticated_offline(self):
        for run in (fake_gh(exc=FileNotFoundError()), fake_gh(code=4, stderr="auth required"),
                    fake_gh(exc=subprocess.TimeoutExpired("gh", 30))):
            state, reason = upstream.resolve(self.pr("loader"), None, run=run)
            self.assertEqual(state, "pending")
            self.assertIn("pending", reason)

    def test_bad_ref(self):
        with self.assertRaises(ValueError):
            upstream.parse_ref("machine#615")

    def test_never_shape_gate(self):
        loader = {"ref": "sillsdev/FieldWorks#1263", "kind": "pr", "head": HEAD40, "affects": "loader"}
        self.assertEqual(upstream.allows_never_shape([loader], run=fake_gh({"state": "OPEN"})), (True, ""))
        self.assertFalse(upstream.allows_never_shape([loader], run=fake_gh({"state": "CLOSED"}))[0])
        allowed, note = upstream.allows_never_shape([loader], run=fake_gh(exc=FileNotFoundError()))
        self.assertTrue(allowed)
        self.assertIn("not confirmed open", note)
        self.assertFalse(upstream.allows_never_shape([self.pr()], run=fake_gh({"state": "OPEN"}))[0])
        self.assertFalse(upstream.allows_never_shape([])[0])


if __name__ == "__main__":
    unittest.main()
