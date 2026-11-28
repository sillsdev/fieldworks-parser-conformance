# merge-subrules-pos-template

A narrowing rule (t a becomes one fused character) with two subrules gated by requiredPartsOfSpeech (nouns fuse to F, verbs to G), and a verb AffixTemplate whose single mandatory slot adds the suffix s. TA_N becomes F; TA_V becomes ta+s then Gs; TATA (noun, two sites) becomes FF. The cells differ only in the rule's `multipleApplicationOrder`: `leftToRightIterative`, `rightToLeftIterative` or `simultaneous`. Every engine must gate the two outputs by part of speech and must still find the fused root under the template suffix.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rule, roots and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`.

The grammar declares a shared symbolic feature `cell` and every segment carries its cell's value. Without it, a feature class in one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `ltr` | `edge-cases/merge-subrules-pos-ltr-template` | `multipleApplicationOrder="leftToRightIterative"` | unchanged |
| `rtl` | `edge-cases/merge-subrules-pos-rtl-template` | `multipleApplicationOrder="rightToLeftIterative"` | `F`→`H`, `G`→`J`, `a`→`e`, `s`→`o`, `t`→`u` |
| `simultaneous` | `edge-cases/merge-subrules-pos-simultaneous-template` | `multipleApplicationOrder="simultaneous"` | `F`→`K`, `G`→`L`, `a`→`g`, `s`→`d`, `t`→`f` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv`.

Signatures were taken from the C# reference (hc-conformance self-check, `--propose`), as the members' were from the integrate-conformance-framework head. PanGloss separately keeps strategy-specific complete-identity assertions for all three orders; individual FST strategies may intentionally refuse an order that another strategy covers. Synthetic part-of-speech-gated syllabary merge, not modeling any real language.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.
