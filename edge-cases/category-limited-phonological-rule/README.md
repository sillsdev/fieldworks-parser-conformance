# category-limited-phonological-rule

Pins sillsdev/motif#468. A FieldWorks regular rule can be limited to a category on its right-hand side
("Category", `PhSegRuleRHS.InputPOSes`; Black, Conceptual Introduction 6.1.2.2.1). `HCLoader.cs` (`LoadRewriteRule`,
lines 2102-2103 at FieldWorks `origin/main`) copies the category and its subcategories into the subrule's
`RequiredSyntacticFeatureStruct`; FieldWorks stores no excluded category. The XML says it as
`requiredPartsOfSpeech` on a `PhonologicalSubrule`.

One rule `prVerbUI` (u becomes i between a and n) has one subrule that requires Verb. Roots:

- `kaun` as a verb: the rule fires, the surface form is `kain`.
- `kaun` as a noun: same segments, same context, but not a verb, so the surface form stays `kaun`. The trace
  lists the rule because it is tried; `kain` has no noun parse and `kaun` has no verb parse.
- `kaut` and `pun` (verbs): controls outside the context, unchanged.

Without the category gate `kain` also parses as the noun and `kaun` has no parse (checked on `e63b8863`). The XML
cannot nest parts of speech, so a Verb-subcategory variant is not expressible here.
