import unittest

import tiers


class TierRules(unittest.TestCase):
    def setUp(self):
        self.all = tiers.compute(excepted={"edge-cases/zz-excepted"}, named={})

    def test_every_case_has_a_tier_and_languages_are_core(self):
        self.assertTrue(self.all)
        self.assertTrue(all(t in tiers.TIERS for t, _ in self.all.values()))
        for case, (tier, why) in self.all.items():
            if case.startswith("languages/"):
                self.assertEqual(tier, "core", case)
                self.assertIn("language profile", why)

    def test_a_consumer_naming_a_case_makes_it_core(self):
        plain = next(c for c, (t, _) in self.all.items() if t == "extended")
        named = tiers.compute(excepted=set(), named={plain: ["pangloss"]})
        self.assertEqual(named[plain], ("core", "named by pangloss"))

    def test_an_exception_makes_a_non_core_case_regression(self):
        plain = next(c for c, (t, _) in self.all.items() if t == "extended")
        got = tiers.compute(excepted={plain}, named={})
        self.assertEqual(got[plain], ("regression", "exception in status.yaml"))

    def test_each_label_has_at_most_two_carriers_by_size(self):
        found = tiers.facts()
        for label in {l for f in found.values() for l in f["labels"]}:
            holders = sorted((f["words"], c) for c, f in found.items() if label in f["labels"])
            for _, case in holders[:2]:
                self.assertEqual(self.all[case][0], "core", (label, case))

    def test_the_committed_block_is_current(self):
        text = tiers.GRAMMARS_MD.read_text(encoding="utf-8")
        self.assertEqual(tiers.current_block(text), tiers.block(tiers.compute()))


if __name__ == "__main__":
    unittest.main()
