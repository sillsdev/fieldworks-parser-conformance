# metathesis-allomorph-env-after-swap

Prefix `s` before roots `ta` (required right environment: word-final) and `taa` (required right environment: a
segment follows the root), with the obligatory rule `s t -> t s`. After the swap the root's morph range runs
from `t` to its last segment and wraps the prefix; C# `AllomorphEnvironment.IsMatch` reads `morph.Range.End.Next`
of that range, so `tsa` and `t+sa` parse and `tsaa` is rejected. PanGloss #380: Rust HC ended the root at the
segment before the prefix, so it found no parse for `tsa` and `t+sa` and accepted `tsaa`.

`tsa` fails on an engine that ends the root at `t` (the prefix follows it, so word-final fails). `tsaa` fails on
C# only because `taa` requires a following segment: with that environment removed `taa` and `tsaa` both parse.

**FieldWorks-producible.** A prefix process, a metathesis rule and root-allomorph required environments
(`HCLoader.LoadRootAllomorph`, 862-876). The staged grammar excluded the word-final environment on `taa`;
`ExcludedEnvironments` is never written (row 20 of
[docs/fieldworks-cannot-say.md](../../docs/fieldworks-cannot-say.md)), so `taa` now requires a following segment.
`taa` therefore never parses in C#; it is a negative control. All lexemes are synthetic. Rows come from the C#
self-check (`hc-conformance --propose`) at sillsdev/machine `ba6dfa10`; no row was filled from PanGloss output.
`rules:` copies the attribution of the sibling `metathesis-boundary-between-switches-prefix` rows.
