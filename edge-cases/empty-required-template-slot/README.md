# empty-required-template-slot

A FieldWorks project has a required prefix slot with no affixes and a filled optional suffix slot. HCLoader's `LoadLanguage` includes only slots that contain loaded affix rules, so the empty required slot is absent from the projected Hermit Crab grammar (see [sillsdev/machine#542](https://github.com/sillsdev/machine/issues/542) and `docs/fieldworks-cannot-say.md` row 28).

## What it pins

- `monu`: the bare stem parses after the empty required slot is omitted.
- `monua`: the optional `-a` suffix parses after the empty required slot is omitted.
- `amonu`: no analysis.

The C# loader and PanGloss both skip the empty slot. PanGloss also emits `grammar.template.slot-no-rules` for it when importing the FieldWorks project. The XML fixture alone cannot show that the source project had the slot; the witness and project-path test pin that distinction. The expected signatures and morphological-rule trace were proposed and checked by the C# founding oracle at Machine `4d9b454d`. See `words.yaml` for the exact rows.

## FieldWorks witness

`fieldworks/project.fwdata` is an authored FieldWorks project, not hand-edited. It was built with FieldWorks 9.3.10.1452 and LibLCM 11.0.0.55173. Its SHA-256 is `5f1f168d5dd133076623b6b1986e1eecef7412e6b2634c8504cf291c267236d5`; `phonology-mutations.yaml` is tied to those exact bytes. HCLoader's projection contains only the optional suffix slot. The grammar's top-level language name is normalized to `EmptyRequiredTemplateSlot`.

The `de`, `en` and `es` LDML files use the minimal versions from `deep-optional-affix-nesting`, whose writing-system definitions are equivalent to this witness. The `fr` file is kept from this witness: the `deep-optional-affix-nesting` French file adds character and collation definitions that this project does not have.
