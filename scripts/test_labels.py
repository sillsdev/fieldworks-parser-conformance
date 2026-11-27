"""Unit tests for the behaviour-label rules: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import unittest

import suite


class OneLabel(unittest.TestCase):
    def test_a_word_with_no_label_fails(self):
        self.assertIsNotNone(suite.label_problem({"word": "a", "expect_fail": True}))
        self.assertIsNotNone(suite.label_problem({"word": "a", "parses": [{"signature": "R|a", "rules": []}]}))

    def test_one_label_on_the_word_or_on_its_parses_passes(self):
        self.assertIsNone(suite.label_problem({"word": "a", "expect_fail": True, "exercises": ["x"]}))
        parses = [{"signature": "R|a", "rules": [], "exercises": ["x"]}, {"signature": "S|a", "rules": [], "exercises": ["x"]}]
        self.assertIsNone(suite.label_problem({"word": "a", "parses": parses}))
        self.assertIsNone(suite.label_problem({"word": "a", "exercises": ["x"], "parses": parses}))

    def test_a_second_label_anywhere_fails(self):
        self.assertIsNotNone(suite.label_problem({"word": "a", "exercises": ["x", "y"]}))
        self.assertIsNotNone(suite.label_problem({"word": "a", "exercises": ["x"], "parses": [{"exercises": ["y"]}]}))

    def test_word_labels_join_the_words_and_its_parses_without_repeats(self):
        word = {"exercises": ["x"], "parses": [{"exercises": ["x", "y"]}, {"exercises": ["z"]}]}
        self.assertEqual(suite.word_labels(word), ["x", "y", "z"])


class Vocabulary(unittest.TestCase):
    def test_every_child_label_names_its_parent(self):
        known = set(suite.constructs())
        for label in suite.child_labels():
            self.assertIn(label.rsplit(suite.LABEL_SEP, 1)[0], known)
            known.add(label)


if __name__ == "__main__":
    unittest.main()
