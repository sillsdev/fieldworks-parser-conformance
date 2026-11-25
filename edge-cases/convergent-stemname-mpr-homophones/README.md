# convergent-stemname-mpr-homophones

Homophonous suffixes whose gates read state the shape does not carry: required and excluded MPR features
on the root, and a stem name whose region is a head feature a suffix assigns.

**Optimization risk.** sillsdev/machine#653 and PanGloss #481 skip a re-match of the same affix rule on the
same shape once an earlier parent path has reached it. The skip is safe only for the match: every other gate
(the root's required and excluded MPR features, the stem name region, a rule's `requiredStemName`) must still
run on each arrival. Here four homophonous `ma` rules reach one shape from two roots that differ only in MPR
features, and the stem-named root allomorph `kele` against the unnamed `keli` is chosen by `num=sg`, assigned
by a suffix. A cache keyed by rule and shape that dropped an allomorph, replayed one parent's gate result for
another, or applied the stem name before the head feature was assigned would change a row. `kele`, `kelisu`,
`kelisusu` and `kelitamasu` are negative controls.

**Why it is producible.** Required MPR features are production restrictions on derivational affixes
(`LoadDerivAffixProcessRule`, group `exceptionFeatures`). Excluded MPR features exist only on slot rules of
an affix template, as inflection-type features (`LoadAffixTemplate` 1766, group `lexEntryInflTypes`, which an
entry carries), so the two excluding `ma` rules and `ta` sit in one template while the required-feature
rules, `sg` and `sgNamed` (`requiredStemName`, 1009-1011) stay derivational in the unordered stratum.

**What changed from the staged grammar.** The staged rule `ma` had a required and an excluded subrule on
one feature, and `mbExc` excluded on a derivational rule: FieldWorks never writes either. Required and
excluded features are now distinct features (`ExcA`/`ExcB` required, `NotA`/`NotB` excluded, each root
carries one of each), so each root still passes exactly two of the four `ma` rules. A template applies after
the stratum rules, so the staged `MBEXC+MA` order and the `ma` allomorph of the ExcB root (now `maExc`, morpheme
`MAEXC`) differ from the staging rows; four words (`boluitma`, `boluitmata`, `boluitmama`, `boluitmamata`)
changed.

**Guards.** sillsdev/machine#653: these rows must stay identical after the optimization; a changed row is a
failure of the optimization, not a reason to edit the row. The rows are C# HermitCrab at machine `e63b8863`
(hc-conformance self-check). All lexemes are invented.
