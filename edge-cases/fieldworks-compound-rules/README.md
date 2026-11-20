# fieldworks-compound-rules

Pins the compound rules a FieldWorks project can write, for Motif's compose-author-compound-rule composer
(sillsdev/motif #248). A project with NoDefaultCompounding=true has no compound rule unless it lists one, so a
compound of two stems has no analysis until the rule exists.

| Rule | Shape | Words |
|---|---|---|
| crE1 | endocentric, HeadLast=true, OverridingMsa without a part of speech | bagokesu, bagokesure, bagokesupa |
| crE2 | endocentric, HeadLast=false, OverridingMsa without a part of speech | mitalonu, mitalonuvi, mitalonuzo |
| crE3 | endocentric, HeadLast=true, OverridingMsa with part of speech R | tabedisi, tabedisifu, tabedisizu |
| crE4 | endocentric, HeadLast=false, OverridingMsa with part of speech R | nukagelo, nukagelofu, nukagelowa |
| crX1, crX2 | exocentric, ToMsa part of speech S (the loader emits one rule per head choice) | solutamo, solutamohu |
| none | category mismatch (A+C) | bagomita |
| none | disabled rule (the loader skips it) | demubonu, bonudemu |

Producibility is read from `HCLoader.cs`, not witnessed by a project (see `words.yaml`). Rows come from the C#
HermitCrab at machine 1ddef2bd (`hc-conformance --propose`); PanGloss 0.27.0 returns the same 36 rows, including the
repeated signature for `bagokesure` (suffix on the head stem or on the compound) and the two analyses of the exocentric
words (one per head choice).
