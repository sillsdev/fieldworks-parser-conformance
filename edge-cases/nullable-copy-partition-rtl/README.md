# nullable-copy-partition-rtl

Test case of the staged PanGloss family `nullable-copy-partition-*` (PanGloss#189), admitted as two test cases: one per rule direction. It holds two **cells**, each a root with one obligatory nasal deletion (applied right to left) and one suffix rule whose input is two parts that may each be empty (`OptionalSegmentSequence`) and whose output copies part 0, part 1, part 0, part 1 and then inserts a segment. A word such as `ttp` is accepted only when the reference finds a partition of the root across the two nullable parts that is copied twice and then loses its nasal.

What it pins: which capture partition of a nullable repeated copy reaches root lookup. PanGloss's unlanded capture-pruning candidate (commit `eee7a171`) filtered capture histories before canonicalisation, lost the accepted `ttp` of the `accept` cell and accepted the rejected `ttp`-shaped word of the `reject` cell. That is a PanGloss defect and the reference is right, so this test case records no exception; it is kept because no other test case copies a nullable input part more than once (label `MorphologicalOutputAction: CopyFromInput/InsertSegments > repeated copy of a nullable part`).

## Cells

| Cell | What differs | Letters (nasal, stop, suffix) |
|---|---|---|
| `accept` | root `tn`, parts of up to two segments, so `tn` + `tntnp` loses its nasal and `ttp` parses as ROOT+SUFFIX | `n`, `t`, `p` |
| `reject` | root `mk` (nasal first), parts of at most one segment, so no partition of the root copies the stop twice and `kkb` has no analysis | `m`, `k`, `b` |

Every id, morpheme id and rule id ends in `_<cell>`, each word's `note` starts with `[cell <name>]`, and the grammar has one shared symbolic feature `cell`: every segment carries its cell's value and each natural class is restricted to it, so a class of one cell matches no segment of the other. The `reject` cell is the mutation control of the `accept` cell: changing the root order and the bound of the parts (`accept` to `reject`) flips the detecting word from one analysis to none, and the control words (`t`/`k`) keep their one analysis.

Two cells and not four: the staged family has the same two cells in each direction, and one grammar holding all four took more than three minutes in the reference's analysis (each added cell's deletion rule is unapplied against every other cell's words), so the directions are two test cases (cannot-merge reason: interaction in analysis cost, not in results).

## Words

Per cell: the detecting word (`ttp` shape), the bare root (the deletion alone), a short copied neighbour and the same material on the wrong side. Expected results are what C# HermitCrab returned on `hc-conformance --propose` at `reference.commit`; the second run prints no patch. `rules:` is the trace the same run verified.

## Producibility

Read from `HCLoader.cs` (not witnessed by a `fieldworks/` project):

- `LoadCharacterDefinitionTable` and `LoadFeatureSystem` write the segments, the features and the `cell` feature; `TryLoadNaturalClass` writes the feature-defined classes.
- `LoadRewriteRule` (2051) writes the nasal deletion, with `Direction` right-to-left at 2064-2078.
- `LoadInflAffixProcessRule` (1025) and `LoadAffixProcessAllomorph` (1383) write the suffix rule: each input context is loaded by `LoadPatternNode`, whose `PhIterationContext` case builds `Quantifier(Minimum, Maximum, ...)` (2387-2392), and the output copies are the `MoCopyFromInput` mappings (1428).

The staged `-alpha-` cells (an alpha variable on each input part) are not admitted: the loader reads affix process input without a variable table (docs/fieldworks-cannot-say.md row 31).
