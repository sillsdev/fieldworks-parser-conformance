# Distinct entries and both head positions

Two entries (one with two allomorphs, one with a two-segment allomorph) and two endocompounding rules, `cr1` with the head first and `cr2` with the non-head first. Covers distinct roots in each order, a root equal in spelling to a compound, and ambiguity (`ppp`, `pp`).

Synthetic forms. Source: sillsdev/PanGloss pull request 353. The expected rows are what C# HermitCrab (sillsdev/machine `1ddef2bd2f1503717de95556116df8e4a63846d6`, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
