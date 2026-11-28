"""Unit tests for scripts/exceptions.py: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import exceptions

HEAD = "a" * 40
CASES = {"edge-cases/x": {"w1": True, "w2": False}}


def write(text):
    tmp = tempfile.TemporaryDirectory()
    path = Path(tmp.name) / "status.yaml"
    path.write_text(text, encoding="utf-8")
    return tmp, path


def doc(*rows):
    return "version: 1\nexceptions:\n" + "".join(rows)


CASE_ROW = ("  - case: edge-cases/x\n    kind: pending-upstream\n    ref: sillsdev/FieldWorks#1\n    ref_type: pr\n"
            f"    head: {HEAD}\n    affects: loader\n    reason: r\n")
WORD_ROW = ("  - case: edge-cases/x\n    word: w1\n    kind: reference-defect\n    ref: sillsdev/machine#2\n"
            "    ref_type: issue\n    affects: engine\n    reason: r\n    intended: R0\n")


class Problems(unittest.TestCase):
    def check(self, text):
        tmp, path = write(text)
        with tmp:
            return exceptions.problems(path, CASES)

    def test_valid_rows_have_no_problems(self):
        self.assertEqual(self.check(doc(CASE_ROW, WORD_ROW)), [])

    def test_a_stress_test_case_takes_no_exception(self):
        self.assertTrue(self.check(doc(CASE_ROW.replace("edge-cases/x", "stress/edge-cases/x"))))

    def test_a_word_row_needs_an_expect_fail_word(self):
        self.assertTrue(any("expect_fail" in p for p in self.check(doc(WORD_ROW.replace("w1", "w2")))))

    def test_a_row_must_name_a_test_case_and_a_word_of_it(self):
        self.assertTrue(any("names no test case" in p for p in self.check(doc(CASE_ROW.replace("edge-cases/x", "edge-cases/y")))))
        self.assertTrue(any("no such word" in p for p in self.check(doc(WORD_ROW.replace("w1", "w9")))))

    def test_a_word_row_needs_intended_and_a_case_row_must_not_have_it(self):
        self.assertTrue(self.check(doc(WORD_ROW.replace("    intended: R0\n", ""))))
        self.assertTrue(self.check(doc(CASE_ROW + "    intended: R0\n")))

    def test_a_pr_needs_a_head_and_an_issue_must_not_have_one(self):
        self.assertTrue(self.check(doc(CASE_ROW.replace(f"    head: {HEAD}\n", ""))))
        self.assertTrue(self.check(doc(WORD_ROW + f"    head: {HEAD}\n")))

    def test_unknown_keys_and_kinds_are_refused(self):
        self.assertTrue(self.check(doc(CASE_ROW + "    surprise: 1\n")))
        self.assertTrue(self.check(doc(CASE_ROW.replace("pending-upstream", "aspirational"))))

    def test_duplicate_rows_are_refused(self):
        self.assertTrue(any("duplicate" in p for p in self.check(doc(CASE_ROW, CASE_ROW))))


class Report(unittest.TestCase):
    def run_with(self, state, strict=True):
        rows = [{"case": "edge-cases/x", "kind": "pending-upstream", "ref": "jira:LT-1", "ref_type": "issue",
                 "affects": "loader", "reason": "r"}]
        with mock.patch("builtins.print"):
            return exceptions.report(strict=strict, rows=rows, resolver=lambda e, c: (state, "r"))

    def test_strict_fails_on_every_state_that_needs_a_human_decision(self):
        for state in ("merged", "closed-unmerged", "issue-closed", "rejected"):
            self.assertEqual(self.run_with(state), 1, state)
        for state in ("pending", "satisfied"):
            self.assertEqual(self.run_with(state), 0, state)
        self.assertEqual(self.run_with("rejected", strict=False), 0)


if __name__ == "__main__":
    unittest.main()
