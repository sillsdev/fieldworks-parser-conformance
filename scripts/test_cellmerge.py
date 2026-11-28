"""Unit tests for scripts/cellmerge.py: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import os
import shutil
import subprocess
import tempfile
import unittest

import yaml

import cellmerge as c

GRAMMAR = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE HermitCrabInput SYSTEM "HermitCrabInput.dtd">
<HermitCrabInput>
  <Language>
    <Name>L</Name>
    <PartsOfSpeech><PartOfSpeech id="posN"><Name>noun</Name></PartOfSpeech></PartsOfSpeech>
    <Strata><Stratum morphologicalRules="r1"/></Strata>
  </Language>
  <MorphologicalRuleDefinitions>
    <MorphologicalRule id="r1"><Name>r1</Name><MorphemeId>{mid}</MorphemeId></MorphologicalRule>
  </MorphologicalRuleDefinitions>
  <LexicalEntries>
    <LexicalEntry id="e1"><Allomorphs><Allomorph id="a1"><PhoneticShape>{ch}</PhoneticShape></Allomorph></Allomorphs>
      <MorphemeId>{ent}</MorphemeId></LexicalEntry>
  </LexicalEntries>
</HermitCrabInput>
"""


def write_member(suite, name, ch, mid, ent, words):
    d = os.path.join(suite, "edge-cases", name)
    os.makedirs(d)
    with open(os.path.join(d, "grammar.xml"), "w", encoding="utf-8") as f:
        f.write(GRAMMAR.format(ch=ch, mid=mid, ent=ent))
    with open(os.path.join(d, "words.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump({"language": "L", "words": words}, f)


def word(w, sig, rule="r1"):
    return {"word": w, "parses": [{"signature": sig, "rules": [rule]}]}


class CellMerge(unittest.TestCase):
    def merge(self, surv_words, surv_mid="m1", absorbed_mid="m1", absorbed_ent="s1"):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        suite, out = os.path.join(tmp, "suite"), os.path.join(tmp, "out")
        write_member(suite, "surv", "a", surv_mid, "s1", surv_words)
        write_member(suite, "abs", "a", absorbed_mid, absorbed_ent, [word("a", f"{absorbed_ent}+{absorbed_mid}|a")])
        c.main([suite, out, "L", "surv:one", "abs:two"])
        with open(os.path.join(out, "words.yaml"), encoding="utf-8") as f:
            words = yaml.safe_load(f)["words"]
        with open(os.path.join(out, "grammar.xml"), encoding="utf-8") as f:
            return words, f.read()

    def test_survivor_signatures_unchanged(self):
        before = [word("a", "s1+m1|a")]
        words, xml = self.merge(before)
        self.assertEqual(words[0]["parses"], before[0]["parses"])
        self.assertIn("<MorphemeId>m1</MorphemeId>", xml)
        self.assertIn('id="r1"', xml)

    def test_absorbed_ids_suffixed(self):
        words, xml = self.merge([word("a", "s1+m1|a")])
        parse = words[1]["parses"][0]
        self.assertEqual(parse["signature"], "s1_two+m1_two|" + words[1]["word"])
        self.assertEqual(parse["rules"], ["r1_two"])
        self.assertIn('id="r1_two"', xml)

    def test_suffixed_id_avoids_survivor_id(self):
        words, _ = self.merge([word("a", "s1+m1_two|a")], surv_mid="m1_two")
        self.assertEqual(words[0]["parses"][0]["signature"], "s1+m1_two|a")
        absorbed_sig = words[1]["parses"][0]["signature"]
        self.assertNotIn("m1_two+", absorbed_sig)
        self.assertEqual(absorbed_sig.split("+")[1].split("|")[0], "m1_two_")


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The parent of the wave-10 merge (PR #92): the members of wave 10 still exist as test cases there.
BEFORE_WAVE10 = "43a3324^1"
SURVIVOR = "spelling-coverage-compound-depth-prefix-zone"
ABSORBED = "spelling-coverage-compound-depth-asymmetric"
OTHER = "spelling-coverage-compound-depth-medial-suffix"


def history_suite(tmp):
    """The edge-cases tree at BEFORE_WAVE10, or None when git history lacks it (a shallow clone)."""
    try:
        tar = subprocess.run(["git", "-C", ROOT, "archive", BEFORE_WAVE10, "edge-cases"], capture_output=True, check=True).stdout
        subprocess.run(["tar", "-x", "-C", tmp], input=tar, check=True)
    except (subprocess.CalledProcessError, OSError):
        return None
    return tmp


def read_words(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)["words"]


class RealMembers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        if history_suite(self.tmp) is None:
            self.skipTest("git history before wave 10 is not available")
        self.suite = self.tmp

    def edge(self, name, *rest):
        return os.path.join(self.suite, "edge-cases", name, *rest)

    def test_dry_run_keeps_survivor_results_and_maps_absorbed(self):
        out = os.path.join(self.tmp, "out")
        c.main([self.suite, out, "X", f"{SURVIVOR}:prefix-zone", f"{ABSORBED}:asymmetric"])
        old, new = read_words(self.edge(SURVIVOR, "words.yaml")), read_words(os.path.join(out, "words.yaml"))
        self.assertGreater(len(new), len(old))
        self.assertEqual([w.get("parses") for w in old], [w.get("parses") for w in new[:len(old)]])
        self.assertTrue(all(w["note"].startswith("[cell asymmetric]") for w in new[len(old):]))

    def test_mpr_groups_merge_into_one(self):
        from lxml import etree
        out = os.path.join(self.tmp, "out")
        c.main([self.suite, out, "X", "spelling-coverage-compound-orders-pos:pos", "spelling-coverage-compound-orders:orders"])
        groups = list(etree.parse(os.path.join(out, "grammar.xml")).iter("MorphologicalPhonologicalRuleFeatureGroup"))
        self.assertEqual([g.find("Name").text for g in groups], ["exceptionFeatures"])

    def test_repeat_merge_into_same_survivor_has_no_collision(self):
        from lxml import etree
        first = os.path.join(self.tmp, "first")
        c.main([self.suite, first, "X", f"{SURVIVOR}:prefix-zone", f"{ABSORBED}:asymmetric"])
        os.makedirs(self.edge("merged"))
        for f in ("grammar.xml", "words.yaml"):
            shutil.copy(os.path.join(first, f), self.edge("merged", f))
        second = os.path.join(self.tmp, "second")
        c.main([self.suite, second, "X", "merged:one", f"{OTHER}:asymmetric"])
        ids = [e.get("id") for e in etree.parse(os.path.join(second, "grammar.xml")).iter() if e.get("id")]
        self.assertEqual(len(ids), len(set(ids)))
        old, new = read_words(self.edge("merged", "words.yaml")), read_words(os.path.join(second, "words.yaml"))
        self.assertEqual([w.get("parses") for w in old], [w.get("parses") for w in new[:len(old)]])


if __name__ == "__main__":
    unittest.main()
