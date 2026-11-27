"""Unit tests for the generated_no_parse expander: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import unittest

import suite

NOTE = "n"


def case(rules, listed=()):
    return {"words": [dict(w) for w in listed], "generated_no_parse": rules}


class Expand(unittest.TestCase):
    def test_order_is_length_then_alphabet_order(self):
        words = suite.expand_words(case([{"alphabet": ["b", "a"], "max_length": 2, "note": NOTE}]))
        self.assertEqual([w["word"] for w in words], ["b", "a", "bb", "ba", "ab", "aa"])

    def test_generated_words_are_only_no_parse(self):
        word = suite.expand_words(case([{"alphabet": ["a"], "max_length": 1, "note": NOTE, "exercises": ["x"]}]))[0]
        self.assertEqual(word, {"word": "a", "note": NOTE, "expect_fail": True, "exercises": ["x"]})

    def test_listed_words_win_and_come_first(self):
        listed = [{"word": "ab", "note": "own", "parses": [{"signature": "R|ab", "rules": []}]}]
        words = suite.expand_words(case([{"alphabet": ["a", "b"], "max_length": 2, "note": NOTE}], listed))
        self.assertEqual(words[0], listed[0])
        self.assertEqual([w["word"] for w in words], ["ab", "a", "b", "aa", "ba", "bb"])

    def test_min_length_and_overlapping_rules_do_not_repeat_a_word(self):
        words = suite.expand_words(case([
            {"alphabet": ["a"], "max_length": 2, "note": NOTE},
            {"alphabet": ["a", "+"], "min_length": 2, "max_length": 2, "note": "m"},
        ]))
        self.assertEqual([(w["word"], w["note"]) for w in words], [("a", NOTE), ("aa", NOTE), ("a+", "m"), ("+a", "m"), ("++", "m")])

    def test_a_huge_rule_is_refused(self):
        with self.assertRaises(ValueError):
            suite.expand_words(case([{"alphabet": list("abcdefghij"), "max_length": 6, "note": NOTE}]))


if __name__ == "__main__":
    unittest.main()
