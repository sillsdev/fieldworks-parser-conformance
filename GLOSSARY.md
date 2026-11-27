# fieldworks-parser-conformance

A shared suite of grammars and words that checks a morphological parser against the C# HermitCrab reference, limited to grammars
FieldWorks can produce. The terms below are canonical in prose; file and script names keep their existing spelling.

## Language

**Test case**:
A directory holding `grammar.xml` and `words.yaml`.
_Avoid_: fixture (in prose; it remains in code and file names only)

**Grammar**:
The `grammar.xml` inside a test case.
_Avoid_: fixture (in prose)

**Word**:
An input string with its expected result.
_Avoid_: row

**Analysis**:
One parse the reference returns for a word.

**Signature**:
Morph ids plus surface form; the key for comparing analyses.

## Reference and results

**Reference**:
The C# engine; the reference commit is the pinned commit of it.
_Avoid_: oracle

**Exception**:
A tracked departure from the reference, of kind reference defect or pending upstream.
_Avoid_: known limitation, aspirational, divergence (unqualified)

**Consumer divergence**:
A difference a consumer records in its own repo.
_Avoid_: divergence (unqualified)

## Value and structure

**Behaviour label**:
A name from the hierarchical vocabulary of behaviours.
_Avoid_: construct, exercises tag

**Language profile**:
A realistic grammar representing a language type.

**Family**:
Test cases that differ in one parameter.

## Landing

**Wave**:
A batch of merges and retirements landed together, with a tag.

**Consumer**:
A pinned user of the suite, such as PanGloss or Machine.

## Supporting terms

**Witness**:
A real FieldWorks project stored with a test case as evidence that FieldWorks can produce its grammar.

**FieldWorks-producible**:
A grammar a real FieldWorks project can produce through the loader.

**Adapter**:
A program that runs an engine over a test case's words and reports its analyses in the suite's exchange format.

**Capability profile**:
The set of capabilities an engine declares; a test case needing one the engine lacks is skipped for that engine.

**Stress test case**:
A grammar kept for timing and optimisation-parity work, not for conformance.

**Ledger**:
A consumer's own record of what its test cases cover; it lives in the consumer's repo.

**XAmple subset**:
The grammars with no phonological features and no phonological rules, so XAmple loses nothing by ignoring them; a descriptive label only.
