"""Unit tests for scripts/check_renames.py: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import unittest

import check_renames as c

H = "old_id\tnew_id\tcovered_by\twave"
LIVE = {"edge-cases/a", "edge-cases/b"}


def run(*rows, base=None, header=H):
    return c.problems_for([header, *rows], LIVE, base)


class Renames(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(run("edge-cases/x\tretired\t\twave-2026-11-27", "edge-cases/y\tedge-cases/a\t\twave-2026-11-27"), [])

    def test_header(self):
        self.assertTrue(run(header="old_id\tnew\tcovered_by\twave"))

    def test_live_old_id(self):
        self.assertTrue(run("edge-cases/a\tretired\t\twave-2026-11-27"))

    def test_dangling_targets(self):
        self.assertTrue(run("edge-cases/x\tedge-cases/gone\t\twave-2026-11-27"))
        self.assertTrue(run("edge-cases/x\tretired\tedge-cases/gone\twave-2026-11-27"))
        self.assertEqual(run("edge-cases/x\tretired\tedge-cases/a,edge-cases/b\twave-2026-11-27"), [])

    def test_wave(self):
        self.assertTrue(run("edge-cases/x\tretired\t\t"))
        self.assertTrue(run("edge-cases/x\tretired\t\t2026-11-27"))

    def test_duplicate_old_id(self):
        row = "edge-cases/x\tretired\t\twave-2026-11-27"
        self.assertTrue(run(row, row))

    def test_append_only(self):
        row = "edge-cases/x\tretired\t\twave-2026-11-27"
        self.assertEqual(run(row, "edge-cases/y\tretired\t\twave-2026-11-28", base=[H, row]), [])
        self.assertTrue(run("edge-cases/y\tretired\t\twave-2026-11-28", base=[H, row]))
        self.assertTrue(run(row.replace("retired", "edge-cases/a"), base=[H, row]))


if __name__ == "__main__":
    unittest.main()
