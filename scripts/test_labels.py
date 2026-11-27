"""Unit tests for the behaviour-label rules: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import unittest

import suite


class Labelled(unittest.TestCase):
    def test_a_rejection_needs_its_own_label(self):
        self.assertTrue(suite.unlabelled({"word": "a", "expect_fail": True}))
        self.assertFalse(suite.unlabelled({"word": "a", "expect_fail": True, "exercises": ["x"]}))

    def test_a_skip_needs_its_own_label(self):
        self.assertTrue(suite.unlabelled({"word": "a", "expect_skip": True, "parses": []}))

    def test_every_analysis_needs_a_label_of_its_own_or_the_words(self):
        parses = [{"signature": "R|a", "rules": [], "exercises": ["x"]}, {"signature": "S|a", "rules": []}]
        self.assertTrue(suite.unlabelled({"word": "a", "parses": parses}))
        self.assertFalse(suite.unlabelled({"word": "a", "parses": parses, "exercises": ["y"]}))
        self.assertFalse(suite.unlabelled({"word": "a", "parses": parses[:1]}))

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
