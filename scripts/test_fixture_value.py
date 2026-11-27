import tempfile
import unittest
from pathlib import Path

import fixture_value as fv


class IdsTests(unittest.TestCase):
    def test_qualified_and_bare_ids(self):
        ids = fv._ids_in("Machine #480 and machine#653, PanGloss #240, LT-22922, FieldWorks#1263, also #615")
        self.assertEqual(ids, {"machine#480", "machine#653", "pangloss#240", "LT-22922", "fieldworks#1263", "?#615"})

    def test_divergence_file(self):
        self.assertEqual(fv._ids_in("docs/divergences/058-x.md"), {"pangloss-divergence-058"})


class CoverageTests(unittest.TestCase):
    def test_summarise_unique_and_marginal(self):
        per = {"a": ({"f:1", "f:2", "f:3"}, {"f:1:0"}), "b": ({"f:1", "f:2"}, set()), "c": ({"f:1", "f:9"}, {"f:9:0"})}
        rows = {r[0]: r for r in fv.summarise(per)}
        self.assertEqual(rows["a"][3], 1)  # f:3 is hit by a alone
        self.assertEqual(rows["c"][3], 1)  # f:9
        self.assertEqual(rows["b"][3], 0)
        self.assertEqual(rows["b"][5:7], (0, 0))  # b adds nothing once a is taken
        self.assertEqual(rows["a"][7], 1)

    def test_parse_cobertura_keeps_engine_files_only(self):
        xml = (
            '<coverage><packages><package><classes>'
            '<class filename="/x/src/SIL.Machine.Morphology.HermitCrab/Morpher.cs"><lines>'
            '<line number="1" hits="2"/><line number="2" hits="0"/>'
            '<line number="3" hits="1" branch="true"><conditions><condition number="0" coverage="50%"/>'
            '<condition number="1" coverage="0%"/></conditions></line></lines></class>'
            '<class filename="/x/src/SIL.Machine.Morphology.HermitCrab.Conformance/Runner.cs"><lines>'
            '<line number="1" hits="5"/></lines></class>'
            '</classes></package></packages></coverage>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "c.xml"
            path.write_text(xml)
            lines, branches = fv.parse_cobertura(path)
        self.assertEqual(lines, {"SIL.Machine.Morphology.HermitCrab/Morpher.cs:1", "SIL.Machine.Morphology.HermitCrab/Morpher.cs:3"})
        self.assertEqual(branches, {"SIL.Machine.Morphology.HermitCrab/Morpher.cs:3:0"})


class DetectionTests(unittest.TestCase):
    def test_render_marks_last_detector(self):
        text = fv.render_detection({"machine#1": {"citing": ["a", "b"], "detectors": {"a": ["w"]}, "also": {}}, "_baseline_failing": {}})
        self.assertIn("LAST DETECTOR", text)


if __name__ == "__main__":
    unittest.main()
