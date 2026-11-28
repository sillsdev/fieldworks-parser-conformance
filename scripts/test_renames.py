"""Unit tests for scripts/check_renames.py: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import unittest

import check_renames as c

H = "old_id\tnew_id\tcovered_by\twave"
LIVE = {"edge-cases/a", "edge-cases/b"}


def run(*rows, base=None, header=H):
    return c.problems_for([header, *rows], LIVE, base)


class Renames(unittest.TestCase):
    def test_second_wave_same_date_suffix(self):
        self.assertEqual(run("edge-cases/x\tretired\t\twave-2026-11-27-2"), [])
        self.assertTrue(run("edge-cases/x\tretired\t\twave-2026-11-27-1"))
        self.assertTrue(run("edge-cases/x\tretired\t\twave-2026-11-27-"))

    def test_clean(self):
        self.assertEqual(run("edge-cases/x\tretired\t\twave-2026-11-27", "edge-cases/y\tedge-cases/a\t\twave-2026-11-27"), [])

    def test_header(self):
        self.assertTrue(run(header="old_id\tnew\tcovered_by\twave"))

    def test_live_old_id(self):
        self.assertTrue(run("edge-cases/a\tretired\t\twave-2026-11-27"))

    def test_restore(self):
        retire = "edge-cases/a\tretired\t\twave-2026-11-27"
        restore = "edge-cases/a\tedge-cases/a\t\twave-2026-12-01"
        self.assertEqual(run(retire, restore), [])
        self.assertTrue(run(retire, restore, retire))  # retired again while still on disk
        self.assertTrue(run("edge-cases/x\tedge-cases/x\t\twave-2026-12-01"))  # restored but absent

    def test_reuse(self):
        self.assertTrue(run("edge-cases/a\tretired\t\twave-2026-11-27", "edge-cases/b\tedge-cases/a\t\twave-2026-11-27"))
        self.assertTrue(run("edge-cases/x\tretired\t\twave-2026-11-27", "edge-cases/y\tedge-cases/x\t\twave-2026-11-27"))

    def test_chain_resolves(self):
        rows = ("edge-cases/x\tedge-cases/y\t\twave-2026-11-27", "edge-cases/y\tedge-cases/a\t\twave-2026-11-28")
        self.assertEqual(run(*rows), [])
        last = {"edge-cases/x": "edge-cases/y", "edge-cases/y": "edge-cases/a"}
        self.assertEqual(c.resolve("edge-cases/x", last, LIVE), "edge-cases/a")
        self.assertEqual(c.resolve("edge-cases/y", last, LIVE), "edge-cases/a")
        self.assertEqual(c.resolve("edge-cases/b", last, LIVE), "edge-cases/b")

    def test_chain_ending_retired(self):
        self.assertEqual(run("edge-cases/x\tedge-cases/y\t\twave-2026-11-27", "edge-cases/y\tretired\t\twave-2026-11-28"), [])
        self.assertEqual(c.resolve("edge-cases/x", {"edge-cases/x": "edge-cases/y", "edge-cases/y": "retired"}, LIVE), "retired")

    def test_long_chain(self):
        rows = [f"edge-cases/n{i}\tedge-cases/n{i + 1}\t\twave-2026-11-27" for i in range(5)] + ["edge-cases/n5\tedge-cases/a\t\twave-2026-11-28"]
        self.assertEqual(run(*rows), [])

    def test_cycle(self):
        last = {"edge-cases/x": "edge-cases/y", "edge-cases/y": "edge-cases/x"}
        self.assertEqual(c.resolve("edge-cases/x", last, LIVE), c.CYCLE)
        self.assertTrue(run("edge-cases/x\tedge-cases/y\t\twave-2026-11-27", "edge-cases/y\tedge-cases/x\t\twave-2026-11-28"))
        self.assertEqual(c.resolve("edge-cases/x", {"edge-cases/x": "edge-cases/x2", "edge-cases/x2": "edge-cases/x3", "edge-cases/x3": "edge-cases/x2"}, LIVE), c.CYCLE)

    def test_chain_dangling_end(self):
        self.assertTrue(run("edge-cases/x\tedge-cases/y\t\twave-2026-11-27", "edge-cases/y\tedge-cases/gone\t\twave-2026-11-28"))

    def test_target_already_remapped(self):
        # y was remapped by an earlier row, so it was not live when the later row named it
        self.assertTrue(run("edge-cases/y\tedge-cases/a\t\twave-2026-11-27", "edge-cases/x\tedge-cases/y\t\twave-2026-11-28"))

    def test_short_row(self):
        self.assertTrue(run("edge-cases/x\tretired"))

    def test_dangling_targets(self):
        self.assertTrue(run("edge-cases/x\tedge-cases/gone\t\twave-2026-11-27"))
        self.assertTrue(run("edge-cases/x\tretired\tedge-cases/gone\twave-2026-11-27"))
        self.assertEqual(run("edge-cases/x\tretired\tedge-cases/a,edge-cases/b\twave-2026-11-27"), [])

    def test_wave(self):
        self.assertTrue(run("edge-cases/x\tretired\t\t"))
        self.assertTrue(run("edge-cases/x\tretired\t\t2026-11-27"))

    def test_append_only(self):
        row = "edge-cases/x\tretired\t\twave-2026-11-27"
        self.assertEqual(run(row, "edge-cases/y\tretired\t\twave-2026-11-28", base=[H, row]), [])
        self.assertTrue(run("edge-cases/y\tretired\t\twave-2026-11-28", base=[H, row]))
        self.assertTrue(run(row.replace("retired", "edge-cases/a"), base=[H, row]))


if __name__ == "__main__":
    unittest.main()
