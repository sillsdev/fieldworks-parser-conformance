# The grammars

Every fixture directory under `languages/` and `edge-cases/` is listed here once, grouped by area, with
one line saying what its grammar and words exercise. Each fixture has a `grammar.xml` and a
`words.yaml`; the larger ones also have a `README.md` with their rationale.

Every grammar here is one a real FieldWorks project can produce. A grammar that FieldWorks cannot
produce does not belong in the suite, however expressible it is in the XML; see
[what FieldWorks cannot produce](fieldworks-cannot-say.md#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it).

A test fails if a fixture directory is missing from this page, listed twice, or listed here but gone.
The list has 142 fixtures: 6 languages and 136 edge cases.

## Which engines run which grammars

Engines need different amounts of phonology: what a grammar says about sounds, in segments, features and rules.

- **XAmple** works on letters: morphemes, allomorph strings, and string environments and natural classes written as lists of letters. FieldWorks' XAmple transforms write no phonological rules and no phonological features, so XAmple ignores both. It is a different algorithm (item-and-arrangement) from Hermit Crab (item-and-process, rules unapplied). It needs no phonology.
- **Hermit Crab** needs a complete phonology: every letter of every form and word is defined as a segment. An undefined letter makes the word unanalyzable, and FieldWorks' Hermit Crab loader drops allomorphs it cannot segment. It needs features only where a rule or natural class uses them.
- **PanGloss** runs grammars with no phonology, with incomplete phonology or with complete phonology. For incomplete phonology ("underdefined" in PanGloss's own terms) it supplies provisional definitions where FieldWorks' Hermit Crab loader drops material.

All 143 conformance and 16 stress grammars are Hermit Crab grammars, and PanGloss runs all of them. The suite has no grammar with incomplete phonology today; that is a gap.

### The XAmple subset

A grammar is in the XAmple subset when it has no phonological features and no phonological rules (`PhonologicalRule` or `MetathesisRule`). A grammar with rules but no features is not in it, because XAmple would ignore its rules. The subset is **50 conformance grammars and 6 stress grammars**. Each of their fixture lines on this page carries the tag `[XAmple]`. `scripts/check_grammars_md.py` recomputes the subset from every `grammar.xml` and fails if this page or the README table disagrees.

`requires: []` is not the XAmple subset. It means no phonological rules, as [PROTOCOL.md](../PROTOCOL.md) section 5 defines it, so some `requires: []` grammars still have phonological features, and some subset grammars carry `requires: [morpher-settings]` because their `words.yaml` sets a `morpher:` block. Five grammars in the subset need `morpher-settings`; they are marked below.

#### Conformance subset

All under [`languages/`](../languages/) and [`edge-cases/`](../edge-cases/).

- `edge-cases/adhoc-prohibition-affix-environment-copies`
- `edge-cases/adhoc-prohibition-affix-msa-copies`
- `edge-cases/adhoc-prohibition-allomorph-variant-control`
- `edge-cases/adhoc-prohibition-circumfix-pairings`
- `edge-cases/adhoc-prohibition-stem-msa-copies`
- `edge-cases/adhoc-prohibition-variant-enclitic-first`
- `edge-cases/adhoc-prohibition-variant-main-first-enclitic`
- `edge-cases/adhoc-prohibition-variant-msa-copies`
- `edge-cases/chained-output-feature-override-loss`
- `edge-cases/circumfix-conditioned-halves`
- `edge-cases/circumfix-cross-product-and-infix-drop`
- `edge-cases/circumfix-in-template-slot`
- `edge-cases/circumfix-infix-interior-action-precedence`
- `edge-cases/circumfix-non-first-allomorph-selection`
- `edge-cases/circumfix-reduplication-precedence`
- `edge-cases/clitic-enclitic-and-proclitic`
- `edge-cases/clitic-proclitic-after-final-template`
- `edge-cases/clitic-rule-designation`
- `edge-cases/clitic-stem-entry`
- `edge-cases/compound-max-applications` (needs `morpher-settings`)
- `edge-cases/compounding-breadth` (needs `morpher-settings`)
- `edge-cases/compounding-non-recursive`
- `edge-cases/cross-stem-material-determination`
- `edge-cases/deep-optional-affix-nesting`
- `edge-cases/diacritic-segments`
- `edge-cases/empty-required-template-slot`
- `edge-cases/feature-gating-breadth`
- `edge-cases/final-template-merge-key` (needs `morpher-settings`)
- `edge-cases/final-template-partial-discriminators` (needs `morpher-settings`)
- `edge-cases/final-template-partial-reachability`
- `edge-cases/final-template-partial-root` (needs `morpher-settings`)
- `edge-cases/final-template-partial-trace`
- `edge-cases/guesser-pattern-root-fallback`
- `edge-cases/head-ambiguous-compounding`
- `edge-cases/infix-interdigitation`
- `edge-cases/loader-pattern-shapes`
- `edge-cases/morphotactic-attribute-breadth`
- `edge-cases/non-clitic-after-final-template-layout`
- `edge-cases/optional-template-composite`
- `edge-cases/partial-rule-infixed-material`
- `edge-cases/partial-rule-truncated-material`
- `edge-cases/partial-rule-wrapped-material`
- `edge-cases/pattern-root-required-environment`
- `edge-cases/recursive-endocentric-compounding`
- `edge-cases/shared-template-unconstrained-suffix`
- `edge-cases/standalone-combining-mark`
- `edge-cases/stem-name-restricted-root-allomorph`
- `edge-cases/strrep-identity`
- `edge-cases/template-category-sharing`
- `languages/suffixing-evidential-adjacency-chain`

#### Stress subset

All under [`stress/edge-cases/`](../stress/edge-cases/).

- `stress/edge-cases/athabaskan-prefix-complex`
- `stress/edge-cases/bantu-extension-chain`
- `stress/edge-cases/bantu-extension-required-slot`
- `stress/edge-cases/derivation-chain-homophone-roots`
- `stress/edge-cases/excluded-cooccurrence`
- `stress/edge-cases/required-template-slot`

## The six languages at a glance

| Directory | Grammar name | Simulates |
|---|---|---|
| `templatic-root-modification` | TemplaticRootModification | Templatic root-and-pattern morphology, stem names, OCP co-occurrence, simultaneous rewrite |
| `metathesis-phase-isolation` | MetathesisPhaseIsolation | Infix, circumfix, reduplication, metathesis, subtractive truncation |
| `polysynthetic-stratal-derivation-chain` | PolysyntheticStratalDerivationChain | Derivation-then-inflection recursion across strata, incorporation-style compounding, guessed stems |
| `suffixing-evidential-adjacency-chain` | SuffixingEvidentialAdjacencyChain | Evidential suffix chain, morpheme-adjacency co-occurrence, in the XAmple subset (no phonological features or rules) |
| `suffixing-extension-slot-ordering` | SuffixingExtensionSlotOrdering | Verbal extension suffixes in template slots, MPR features in the loader's two groups, reduplication, post-nasal mutation, stem names on rules and root allomorphs |
| `suffixing-vowel-harmony` | SuffixingVowelHarmony | Alpha-variable vowel harmony, merges, gradation and epenthesis in one stratum, a circumfix, an infix |

Each is a dense, synthetic grammar (invented lexemes and segment inventories, no orthographic claim
about any real language) where ordinary words exercise several constructs at once, rather than a
one-mechanism probe. `edge-cases/` holds the things no shared grammar can host faithfully:
loader/XML-semantics probes, an `expect_crash` pin, a `budget_ms` pathological stress case, and
allomorphy/rewrite pins whose exact rule shape a naturalistic grammar wouldn't contain.

## The six languages

Whole-language grammars with a realistic lexicon and several interacting processes.

- `languages/metathesis-phase-isolation`: infixation, circumfixation, reduplication, metathesis and truncation, one demonstration per part of speech (26 words).
- `languages/polysynthetic-stratal-derivation-chain`: derivation then inflection across strata, with compounding, boundary markers and root guessing (24 words).
- `languages/suffixing-evidential-adjacency-chain`: [XAmple] a chain of evidential suffixes in template slots, morpheme co-occurrence exclusions and homophonous roots (32 words).
- `languages/suffixing-extension-slot-ordering`: verbal extension suffixes in template slots, MPR features in the loader's two groups, reduplication, post-nasal mutation and head-feature agreement, and rules and root allomorphs that name stem names (52 words).
- `languages/suffixing-vowel-harmony`: backness and alpha-variable harmony, vowel merges, consonant gradation and epenthesis ordered in one stratum, a circumfix whose one environment is checked at each piece, and an infix (27 words).
- `languages/templatic-root-modification`: stem names and templatic root modification, with epenthesis, prothesis, feeding and geminate rules (25 words).

## Affix shapes: circumfix, infix, null, truncation

- `edge-cases/circumfix-conditioned-halves`: [XAmple] a circumfix built as a cross product of two prefix halves and two suffix halves, each pairing conditioned on the stem edges.
- `edge-cases/circumfix-cross-product-and-infix-drop`: [XAmple] a two-prefix by two-suffix circumfix cross product, and an infix rule that drops material.
- `edge-cases/circumfix-in-template-slot`: [XAmple] a circumfix rule that sits in an affix template slot.
- `edge-cases/circumfix-infix-interior-action-precedence`: [XAmple] one allomorph that is both circumfixing and infixing in the same output.
- `edge-cases/circumfix-non-first-allomorph-selection`: [XAmple] a circumfix allomorph that is chosen after an ordinary suffix allomorph of the same rule fails.
- `edge-cases/circumfix-reduplication-precedence`: [XAmple] one allomorph that is both circumfixing and reduplicating in the same output.
- `edge-cases/copy-agreement-featureless-redup`: a first-consonant-and-vowel reduplication in a grammar with no phonological features, where the two copies must agree in spelling (19 words).
- `edge-cases/discontinuous-morph-environment`: a root environment checked on each contiguous piece of a root split by a two-infix rule.
- `edge-cases/infix-split-root-allomorph-environment`: a root allomorph conditioned on a following vowel, with an infix inside the root; infix segments are not the root's neighbours.
- `edge-cases/flex-null-affix-environments`: null prefixes whose environments look at the neighbouring prefix.
- `edge-cases/infix-interdigitation`: [XAmple] infixes inserted around a copied root, in a templatic Semitic shape.
- `edge-cases/partial-rule-infixed-material`: [XAmple] partial affix rules whose material an ordinary infix splits, under a final template.
- `edge-cases/partial-rule-truncated-material`: [XAmple] a partial suffix whose last segment an ordinary truncation rule replaces, under a final template.
- `edge-cases/partial-rule-wrapped-material`: [XAmple] partial affix rules whose material ordinary affixes and a reduplication wrap or copy, under a final template.
- `edge-cases/process-morphology-in-place-mutation`: tense expressed only by changing a segment of the root, with no affix.
- `edge-cases/truncate-morphotactic`: rules that remove a final or initial segment of the stem, matched by literal segment, with optional insertion.
- `edge-cases/truncate-morphotactic-copy-u`: the truncation grammar with explicit morpheme ids and a copying suffix rule, so one surface form has several parses with different rule histories.
- `edge-cases/truncate-morphotactic-identity`: the truncation grammar with explicit morpheme ids, so repeated signatures stay distinct rows.
- `edge-cases/truncate-morphotactic-subsumption`: a prefix rule, a leading truncation and an insertion rule over the root `ag`, so a rule can remove what an earlier rule added.

## Templates, slots and parts of speech

- `edge-cases/feature-gating-breadth`: [XAmple] a rule gated on number=pl that a lexically singular root passes only after another rule has overwritten its number, in both suffix orders (10 words).
- `edge-cases/final-template-merge-key`: [XAmple] a final template in a lower stratum, reached from two analysis orders that must merge into one parse.
- `edge-cases/final-template-partial-discriminators`: [XAmple] rules that may or may not follow a final template, depending on whether they are partial.
- `edge-cases/final-template-partial-reachability`: [XAmple] four final templates, only one of which a partial word can reach, with a partial rule and a partial entry.
- `edge-cases/final-template-partial-root`: [XAmple] a partial root with a final template, and ordinary rules blocked after the template.
- `edge-cases/final-template-partial-trace`: [XAmple] one word that both final-template refusals reject, and that parses once the partial rule is made ordinary.
- `edge-cases/morphotactic-attribute-breadth`: [XAmple] repetition caps, partial rules and entries, bound allomorphs, non-final templates, co-occurrence rules and MPR groups.
- `edge-cases/optional-template-composite`: [XAmple] optional and mandatory template slots that combine into several parses of one word.
- `edge-cases/empty-required-template-slot`: [XAmple] a required FieldWorks prefix slot with no affix rules is omitted by HCLoader, so the bare stem and an optional suffix still parse (3 words).
- `edge-cases/shared-template-unconstrained-suffix`: [XAmple] a template with a mandatory suffix shared by roots of different parts of speech.
- `edge-cases/subrule-morphosyntactic-gating`: a phonological subrule that applies only after a rule has changed the part of speech.
- `edge-cases/template-category-sharing`: [XAmple] one template used by several parts of speech.
- `edge-cases/deep-optional-affix-nesting`: [XAmple] twelve optional prefix slots that insert the same letter, so one word has many slot subsets that explain it.

## Clitics

- `edge-cases/clitic-enclitic-and-proclitic`: [XAmple] two unordered clitics, one before and one after the final template.
- `edge-cases/clitic-flex-layout-blocking-morphology`: a final template followed by an obligatory epenthesis in a stratum that holds a phonological rule.
- `edge-cases/clitic-proclitic-after-final-template`: [XAmple] a rule that is not a clitic and is refused after the final template.
- `edge-cases/clitic-rule-designation`: [XAmple] rules inside and outside the clitics stratum, checked against the final template.
- `edge-cases/clitic-stem-entry`: [XAmple] a clitic stem entry that FieldWorks loads into the clitics stratum.
- `edge-cases/non-clitic-after-final-template-layout`: [XAmple] a clitic stratum that holds only clitics, after a non-blocking stratum with a final template.

## Allomorphs, stem names and exceptions

- `edge-cases/disjunctive-recheck`: allomorphs chosen in order, where the first allomorph's right environment is re-checked against the rest of the word.
- `edge-cases/lexical-lookup-sibling-allomorphs`: a word that parses only through an entry's other allomorph than the one analysis matched (master) or not at all (machine PR 627), plus syntactic-feature homograph controls (7 words).
- `edge-cases/free-fluctuating-allomorph-pair`: two allomorphs that can both apply, so a word has one parse per allomorph.
- `edge-cases/mpr-gated-exception`: a phonological rule that a root or an affix switches off with a morphological feature.
- `edge-cases/stem-name-restricted-root-allomorph`: [XAmple] a root allomorph that is used only when a stem name matches the word's features.
- `edge-cases/pattern-root-required-environment`: [XAmple] a lexical pattern entry and a literal root that has a required environment.
- `edge-cases/guesser-pattern-root-fallback`: [XAmple] a lexical pattern entry that guesses roots only when no listed root matches.
- `edge-cases/guess-roots-settings`: root guessing turned on and off for the same words.
- `edge-cases/loader-pattern-shapes`: [XAmple] lexical entries whose shape names a natural class.

## Ad hoc prohibitions

- `edge-cases/adhoc-prohibition-affix-environment-copies`: [XAmple] a prohibition on a prefix allomorph that has two environments and two morphosyntactic analyses.
- `edge-cases/adhoc-prohibition-affix-msa-copies`: [XAmple] a prohibition on a prefix entry that has two morphosyntactic analyses.
- `edge-cases/adhoc-prohibition-allomorph-variant-control`: [XAmple] a control for the variant cases, with an allomorph prohibition between a variant stem and a prefix.
- `edge-cases/adhoc-prohibition-circumfix-pairings`: [XAmple] a prohibition that names a circumfix, which pairs with each of its prefix and suffix halves.
- `edge-cases/adhoc-prohibition-stem-msa-copies`: [XAmple] a prohibition on a stem entry that has two morphosyntactic analyses.
- `edge-cases/adhoc-prohibition-variant-enclitic-first`: [XAmple] a morpheme prohibition that starts with an enclitic, over a stem that has a variant entry.
- `edge-cases/adhoc-prohibition-variant-main-first-enclitic`: [XAmple] a morpheme prohibition that ends with an enclitic, over a stem that has a variant entry.
- `edge-cases/adhoc-prohibition-variant-msa-copies`: [XAmple] a morpheme prohibition on one analysis of a stem that has a variant entry.

## Compounding

- `edge-cases/compounding-breadth`: [XAmple] head and non-head feature requirements, a compound output part of speech that a suffix rejects, and a switched-off compounding rule (7 words, replayed under two settings variants).
- `edge-cases/compound-max-applications`: [XAmple] a recursive compounding rule capped at two applications, with the root limit raised to four (7 words).
- `edge-cases/compounding-non-recursive`: [XAmple] one non-recursive compounding rule with head and non-head lexicon subsets chosen by licence features.
- `edge-cases/head-ambiguous-compounding`: [XAmple] compounds in which either root could be the head.
- `edge-cases/recursive-endocentric-compounding`: [XAmple] a compounding rule that applies to its own output.
- `edge-cases/cross-stem-material-determination`: [XAmple] a suffix whose form depends on which prefix was chosen, not only on whether the pair is allowed.

## Phonological rules: deletion, epenthesis, merge, expansion

- `edge-cases/class-deletion-reinsertion-strrep`: a deletion whose target is a natural class, in a grammar with no phonological features.
- `edge-cases/deletion-reapplications`: hiatus resolution that deletes a run of vowels, analysed with the deletion reapplication limit.
- `edge-cases/deletion-reduplication-exception-composite`: deletion, reduplication and a feature-conferred exception in one word.
- `edge-cases/deletion-reinserted-feature-unapply`: final devoicing followed by cluster simplification, undone in the right order on analysis.
- `edge-cases/epenthesis-fed-merge`: an epenthesis whose output is merged by a later rule.
- `edge-cases/expansion-interposed-optional`: an expansion rule undone across an optional segment between its two output segments.
- `edge-cases/expansion-overlapping-targets`: an expansion whose two-segment output overlaps itself in a run of vowels.
- `edge-cases/feature-rule-before-merge`: a feature-changing rule that feeds a later merge.
- `edge-cases/geminate-under-merge`: a long consonant shortened, then fused with a vowel.
- `edge-cases/interposed-optional-multi-rhs`: a rule with several output segments and an optional segment between them.
- `edge-cases/iterative-epenthesis-cascade`: two iterative epentheses with empty targets that feed each other.
- `edge-cases/fw-metathesis-switch-indices`: a metathesis rule authored in FieldWorks with a left environment, whose two switches HCLoader names from `StrucChange`; the swap applies only after `a`.
- `edge-cases/merge-then-metathesis`: a metathesis followed by a merge, undone in order on analysis.
- `edge-cases/partial-rule-deleted-material`: partial affix rules whose inserted segment a phonological deletion rule removes from the surface form, under a final template.
- `edge-cases/simultaneous-epenthesis-cascade`: a simultaneous epenthesis that inserts a vowel after any high vowel.
- `edge-cases/simultaneous-expansion-terminates`: a simultaneous expansion that must be undone at two sites in one pass.
- `edge-cases/simultaneous-feeding`: a simultaneous feature-changing rule whose sites overlap.
- `edge-cases/simultaneous-feeding-control-iterative`: the same feature-changing rule applied iteratively, as a control.
- `edge-cases/simultaneous-subrule-genuine-overlap`: two subrules that both match one position, where the first subrule wins.
- `edge-cases/two-merges-cascade-env`: a vowel-fronting rule feeding two merges, with and without a morpheme boundary.
- `edge-cases/merge-subrules-pos-ltr-template`: a left-to-right merge with subrules gated by part of speech and a verb template.
- `edge-cases/merge-subrules-pos-rtl-template`: the same merge applied right to left.
- `edge-cases/merge-subrules-pos-simultaneous-template`: the same merge applied simultaneously.

## Boundaries, direction and string representation

- `edge-cases/boundary-first-in-narrowing-lhs`: a merge whose target starts with a morpheme boundary.
- `edge-cases/boundary-first-in-narrowing-lhs-strrep`: the same merge in a grammar with no phonological features.
- `edge-cases/boundary-leftover-in-narrowing-lhs-strrep`: a merge that absorbs a nasal and a boundary, with no phonological features.
- `edge-cases/boundary-mid-in-narrowing-lhs-strrep`: a merge with a boundary in the middle of its target, with no phonological features.
- `edge-cases/boundary-narrowing-probe`: a suffix-initial consonant that becomes a nasal after a nasal.
- `edge-cases/literal-hash-affix-context`: a literal `#` marker in an environment, which is not a word-edge anchor.
- `edge-cases/word-boundary-affix-rewrite`: a word-edge anchor in a rule that rewrites the edges of prefixes and roots.
- `edge-cases/right-to-left-anchor-environment`: a spreading rule whose reach depends on the scan direction.
- `edge-cases/right-to-left-bounded-quantifier-rewrite`: a right-to-left rewrite with a bounded repetition in its environment.
- `edge-cases/right-to-left-metathesis-reversal`: a right-to-left metathesis where the left switch names the later group, as FieldWorks writes it.
- `edge-cases/right-to-left-segments-environment`: a right-to-left iterative rewrite gated on one literal segment to its right (5 words).
- `edge-cases/unbounded-iterative-quantifier-expansion`: a rewrite with an unbounded repetition in its environment, applied iteratively.
- `edge-cases/standalone-combining-mark`: [XAmple] a tone mark defined as its own segment, written as a combining character.
- `edge-cases/diacritic-segments`: [XAmple] roots with precomposed Latin diacritics, in the middle and at the end of the stem.
- `edge-cases/strrep-identity`: [XAmple] a grammar with no phonological features, where each segment is identified by its spelling.
- `edge-cases/strrep-rewrite-unapplication`: a rewrite undone on analysis in a grammar with no phonological features.
- `edge-cases/chained-output-feature-override-loss`: [XAmple] two rules that each set an output feature, and a word that needs both.
- `edge-cases/alpha-variable-name-collision`: two vowels that flip different features under one alpha variable.

## Alpha variables in environments

These families repeat one pattern across rewrite direction and environment side. Each fixture has 16 or 17
words over a small vowel set. The names say which cell they fill: `bounded` or `unbounded` is whether the
repeated stretch has a cap, `ltr` or `rtl` is the rewrite direction, and `left` or `right` is the side
that holds the environment. `plain` means the environment holds no repeated stretch, and `zero` means
the repeated stretch may occur zero times. Each bullet says what the grammar holds.

### Nullable environment with disagreeing alpha values

- `edge-cases/nullable-disagree-bounded-ltr-left`: an optional segment, left-to-right application, environment on the left.
- `edge-cases/nullable-disagree-bounded-ltr-right`: an optional segment, left-to-right application, environment on the right.
- `edge-cases/nullable-disagree-bounded-rtl-left`: an optional segment, right-to-left application, environment on the left.
- `edge-cases/nullable-disagree-bounded-rtl-right`: an optional segment, right-to-left application, environment on the right.
- `edge-cases/nullable-disagree-plain-ltr-right`: no environment at all, left-to-right application.
- `edge-cases/nullable-disagree-unbounded-ltr-left`: a stretch of any length, including none, left-to-right application, environment on the left.
- `edge-cases/nullable-disagree-unbounded-ltr-right`: a stretch of any length, including none, left-to-right application, environment on the right.
- `edge-cases/nullable-disagree-unbounded-rtl-left`: a stretch of any length, including none, right-to-left application, environment on the left.
- `edge-cases/nullable-disagree-unbounded-rtl-right`: a stretch of any length, including none, right-to-left application, environment on the right.

Each is a back and round disagreement over a four-vowel class, with a nullable stretch in the environment
that must still allow the rewrite at the word edge, so `ia` is the one surface word.

### Partial explicit class with disagreeing alpha values

- `edge-cases/partial-class-disagree-bounded-ltr-left`: an optional segment, left-to-right application, environment on the left.
- `edge-cases/partial-class-disagree-bounded-rtl-left`: an optional segment, right-to-left application, environment on the left.
- `edge-cases/partial-class-disagree-bounded-rtl-right`: an optional segment, right-to-left application, environment on the right.
- `edge-cases/partial-class-disagree-unbounded-ltr-right`: a stretch of any length, including none, left-to-right application, environment on the right.
- `edge-cases/partial-class-disagree-unbounded-rtl-left`: a stretch of any length, including none, right-to-left application, environment on the left.
- `edge-cases/partial-class-disagree-unbounded-rtl-right`: a stretch of any length, including none, right-to-left application, environment on the right.

Each uses an explicit vowel class that omits two of the four vowels, so the engine accepts only `ia` of the 16 words.

### Ambiguous disagreement

- `edge-cases/ambiguous-disagree-feature-class-bounded-rtl`: an optional segment, right-to-left application, environment on the right.
- `edge-cases/ambiguous-disagree-feature-class-unbounded-ltr`: a stretch of any length, including none, left-to-right application, environment on the right.
- `edge-cases/ambiguous-disagree-mixed-plus-class`: no environment at all, left-to-right application.
- `edge-cases/ambiguous-disagree-repeated-minus-partial-focus`: one segment, left-to-right application, environment on the left.

Each combines a minus alpha on a complete class with an agreeing occurrence on a partial class, or on a
feature-defined class, in a bounded or unbounded environment.

### Overridden alpha

- `edge-cases/overridden-alpha-bounded-ltr-left`: 1 to 2 segments, left-to-right application, environment on the left.
- `edge-cases/overridden-alpha-bounded-rtl-left`: 1 to 2 segments, right-to-left application, environment on the left.
- `edge-cases/overridden-alpha-plain-ltr-left`: no repeated stretch, left-to-right application, environment on the left.
- `edge-cases/overridden-alpha-unbounded-ltr-left`: 1 or more segments, left-to-right application, environment on the left.

Each neutralises a feature that an alpha variable also governs, so the engine requires `ii` from `iu`.

### Quantified alpha agreement

- `edge-cases/quantified-alpha-bounded-ltr-left`: exactly 2 segments, left-to-right application, environment on the left.
- `edge-cases/quantified-alpha-bounded-ltr-right`: exactly 2 segments, left-to-right application, environment on the right.
- `edge-cases/quantified-alpha-bounded-rtl-left`: exactly 2 segments, right-to-left application, environment on the left.
- `edge-cases/quantified-alpha-bounded-rtl-right`: exactly 2 segments, right-to-left application, environment on the right.
- `edge-cases/quantified-alpha-bounded-zero-left`: up to 2 segments, including none, left-to-right application, environment on the left.
- `edge-cases/quantified-alpha-bounded-zero-right`: up to 2 segments, including none, left-to-right application, environment on the right.
- `edge-cases/quantified-alpha-unbounded-ltr-left`: 2 or more segments, left-to-right application, environment on the left.
- `edge-cases/quantified-alpha-unbounded-ltr-right`: 2 or more segments, left-to-right application, environment on the right.
- `edge-cases/quantified-alpha-unbounded-rtl-left`: 2 or more segments, right-to-left application, environment on the left.
- `edge-cases/quantified-alpha-unbounded-rtl-right`: 2 or more segments, right-to-left application, environment on the right.
- `edge-cases/quantified-alpha-unbounded-zero-left`: a stretch of any length, including none, left-to-right application, environment on the left.
- `edge-cases/quantified-alpha-unbounded-zero-right`: a stretch of any length, including none, left-to-right application, environment on the right.

Each repeats a segment in the environment with an alpha value that must agree across the repetition. In
the `zero` cells the stretch may also be empty.

## Stress grammars

The 16 grammars under `stress/` (at the repository root, beside `edge-cases/`) are timing
probes for the analysis pass, not fixtures, and no coverage ledger counts them. They follow the same rule: only
grammars a FieldWorks project can produce. All 16 carry `fieldworks_producible: true` read from the loader, and
none has a FieldWorks witness yet (issue #1). Their expected output is a parity check against an engine, not a
conformance claim. [stress/README.md](../stress/README.md) says what each really exercises and which
sillsdev/machine optimization it was built for; `scripts/check_grammars_md.py` fails if this list and that table
differ from the directory.

- `stress/edge-cases/allomorph-list-density`: five suffix rules with 30 allomorphs, each gated by the stem's final context.
- `stress/edge-cases/athabaskan-prefix-complex`: [XAmple] six prefix slots of homophonous prefixes with 51 paired-slot `exclude` rules.
- `stress/edge-cases/bantu-extension-chain`: [XAmple] seven suffix slots of homophonous suffixes with 52 `exclude` rules.
- `stress/edge-cases/bantu-extension-required-slot`: [XAmple] five free extension suffixes before a template with a required TAM prefix.
- `stress/edge-cases/bantu-tam-fusion`: the Bantu slot templates with a plain and a vowel-copying allomorph per object and subject rule.
- `stress/edge-cases/bantu-tam-templates`: 12 Bantu slot templates with required subject and TAM slots.
- `stress/edge-cases/bantu-tam-templates-shared`: the same words and templates with three trailing slots shared across templates.
- `stress/edge-cases/derivation-chain-homophone-roots`: [XAmple] seven free derivational suffixes over verb and noun roots that share shapes.
- `stress/edge-cases/early-lexicon-agglutinative`: 25 rules and a vowel-harmony rule, where the 19 words that parse start with a root.
- `stress/edge-cases/env-austronesian-nasal-prefix`: nasal-prefix allomorphs gated by the stem's first segment in the input pattern.
- `stress/edge-cases/env-bantu-concord`: concord and tense allomorphs gated by the stem's edge segments in the input pattern.
- `stress/edge-cases/env-zero-allomorphs`: zero allomorphs gated by rare segment classes, with two left environments on a lone prefix.
- `stress/edge-cases/excluded-cooccurrence`: [XAmple] six prefix slots of four fillers with 12 `exclude` rules and a zero-width filler.
- `stress/edge-cases/prefix-class-density`: four prefix rules with 20 allomorphs gated by the stem's first segment.
- `stress/edge-cases/required-template-slot`: [XAmple] a required TAM prefix and a required noun class prefix, with decoy branches.
- `stress/edge-cases/truncating-slot-chain`: five slot templates whose suffix slots each delete the vowel before them.
