# fieldworks-parser-conformance

A shared suite of grammars and words that checks a morphological parser against the C# HermitCrab reference, limited to grammars
FieldWorks can produce. The terms below are canonical in prose; file and script names keep their existing spelling.

## Language

**Test case**:
A directory holding `grammar.xml` and `words.yaml`. Its id is its directory path.
_Avoid_: fixture (in prose; it remains in file and script names), row, case

**Grammar**:
The `grammar.xml` inside a test case.
_Avoid_: fixture

**Word**:
An input string with its expected result.
_Avoid_: row, entry

**Analysis**:
One parse the reference returns for a word.
_Avoid_: parse result, row

**Signature**:
Morph ids plus surface form; the key for comparing analyses.
_Avoid_: fingerprint, key

## Reference and results

**Reference**:
The C# HermitCrab engine, the only source of expected results.
_Avoid_: oracle, ground truth

**Reference commit**:
The pinned commit of the reference.
_Avoid_: oracle build

**Exception**:
A tracked departure from the reference, of kind reference defect or pending upstream.
_Avoid_: known limitation, aspirational, oracle limitation, divergence (unqualified)

**Consumer divergence**:
A difference a consumer records in its own repo.
_Avoid_: divergence (unqualified), exception

## Value and structure

**Behaviour label**:
A name from the hierarchical vocabulary of behaviours.
_Avoid_: construct, exercises tag

**Language profile**:
A realistic grammar representing a language type.
_Avoid_: language fixture

**Family**:
Test cases that differ in one parameter.
_Avoid_: group, series

## Landing

**Wave**:
A batch of merges and retirements landed together, with a tag.
_Avoid_: batch, release

**Consumer**:
A pinned user of the suite, such as PanGloss or Machine.
_Avoid_: client, downstream
