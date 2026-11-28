# Truncation identity companions

Three edge cases derive from one truncation grammar, whose original stays unchanged:
`truncate-morphotactic-identity` adds explicit `MorphemeId` labels; `truncate-morphotactic-subsumption`
uses root `ag` plus prefix rule `X` with the original leading truncation rule `B` and insertion rule
`C`; `truncate-morphotactic-copy-u` adds a copying suffix rule `U` to the explicit-ID A/B/C grammar.
These cases preserve the distinction between a parse's allomorph order in its signature and its
forward rule application order in `words.yaml`'s `rules` list. Repeated signature strings are
intentional and remain repeated rows.

The checked-in expectations were captured from the combined #500+#506 C# source state: sillsdev/machine #556
plus the #500 `ApplyRhs` relocation. The two commits are sillsdev/machine #556 head `d98d12a5d514ce589d7495c71d055830e061a418` and the #500 `ApplyRhs`
relocation `157c031ef272d07c900db41b2d4a8852b13f64b0`, as plain text. Assembly SHA-256 values: #556 `SIL.Machine.dll`
`b265a40a44292614f51f7a65afc445ae34dde685cb40ce8c2d2de5521a0c299d`; combined
`SIL.Machine.Morphology.HermitCrab.dll` `4cd980453f51fd3cf29cf38a99f342f542e631eb23be6ba87b9433aab6c3d57f`.
Reproduction: start from the truncation grammar; add the identity labels or the stated companion rule or root; use the
#556 Machine library and the #500 relocation in HermitCrab's copy/annotation transfer; parse every `words.yaml` word;
retain every returned signature and forward trace. The expected rows do not depend on a temporary staging file.

An engine without both fixes does not satisfy these complete identity rows reliably, because its
copied annotations differ. Keep the full combined-oracle multisets; do not weaken them to match the
pre-fix base output.

The corrected C# traces report the same analysis features for these rows:
`pos=[posV]`, `syntactic=[POS:v]`, `realizational=ANY`, and the default MPR feature set.
Each root token is its entry's single root XML allomorph, and each rule token is that rule's
single allomorph; every observed allomorph has index 0 and count 1. Signature token order is
the final morph occurrence order, while the tables below retain the separate forward rule
application order. All positive words have status `ok`; `bag` and `bau` have status `ok` with
zero parses, as declared by `expect_fail`. None of the test case words is skipped.

Stable source attribution is `ROOT` = `root32`/`root32_1` in the identity and copy-U test cases;
`ROOTAG` = `root32`/`root32_1` in subsumption; `A` = `mruleTruncTrail`, `B` =
`mruleTruncLead`, `C` = `mruleTruncOptIns`, `X` = `mrulePrefixX`, and `U` = `mrU`. The
corresponding `MorphemeId` is explicit in each companion grammar; runtime GUIDs are not used as
test case identities.

`truncate-morphotactic-identity` expected parses:

| Word | Signature | Forward rule order |
|---|---|---|
| `sag` | `ROOT|sag` | root |
| `sas` | `ROOT33|sas` | root |
| `a` | `ROOT+B+A|a` | B, A |
| `a` | `ROOT+A+B|a` | A, B |
| `ga` | `ROOT+B+C+A|ga` | B, A, C |
| `ga` | `ROOT+A+C+B|ga` | A, B, C |
| `ga` | `C+B+ROOT+A|ga` | B, C, A |
| `ga` | `ROOT+C+A|ga` | A, C |
| `ga` | `C+ROOT+A|ga` | C, A |
| `bag` | no parses | — |

`truncate-morphotactic-subsumption` expected parses:

| Word | Signature | Forward rule order |
|---|---|---|
| `ag` | `ROOTAG|ag` | root |
| `ag` | `ROOTAG+X+B|ag` | X, B |
| `sag` | `X+ROOTAG|sag` | X |
| `gag` | `X+C+ROOTAG|gag` | X, C |
| `gag` | `X+C+ROOTAG+B|gag` | X, B, C |
| `gag` | `X+C+ROOTAG+B|gag` | C, X, B |
| `gag` | `C+ROOTAG|gag` | C |
| `bag` | no parses | — |

`truncate-morphotactic-copy-u` expected parses (the repeated `ROOT+C+A+U|gau` identity is retained):

| Word | Signature | Forward rule order |
|---|---|---|
| `gau` | `ROOT+A+C+B+U|gau` | A, B, C, U |
| `gau` | `ROOT+B+C+A+U|gau` | B, A, C, U |
| `gau` | `B+A+C+ROOT+U|gau` | B, C, A, U |
| `gau` | `C+B+ROOT+A+U|gau` | A, B, U, C |
| `gau` | `C+A+ROOT+B+U|gau` | B, A, U, C |
| `gau` | `ROOT+U+C+A+B|gau` | A, U, B, C |
| `gau` | `ROOT+C+A+U|gau` | A, C, U |
| `gau` | `C+A+ROOT+U|gau` | C, A, U |
| `gau` | `ROOT+C+A+U|gau` | A, U, C |
| `au` | `B+ROOT+A+U|au` | A, B, U |
| `au` | `A+ROOT+B+U|au` | B, A, U |
| `au` | `ROOT+A+U+B|au` | A, U, B |
| `sagu` | `ROOT+U|sagu` | U |
| `bau` | no parses | — |

Every listed allomorph is index 0; the named roots and rules in the signatures are their explicit
`MorphemeId` values. The rules use the existing `AffixProcessRule: subtraction/truncation`
construct label; the test cases do not introduce new coverage categories. All three declare
`morphologicalRuleOrder="unordered"`, which HCLoader emits. Their words are intentionally synthetic,
but that does not make the grammar constructs FieldWorks-unproducible, so all three are correctly in scope.

The combined #500+#506 corrected-engine audit that flips those copied grammars from `unordered` to
`linear` loses analyses in all three companions; the exact changed words and signatures are recorded
in `morphological-rule-order-measurement.md` (sillsdev/machine#480). The checked-in grammars remain `unordered`,
matching HCLoader's emitted order.

The ordinary conformance runner checks signature multiplicity and the set of rule IDs associated
with each signature. It currently canonicalizes rule IDs before comparing them, so the ordered
`rules` lists preserve the observed application histories but do not independently gate their order.
