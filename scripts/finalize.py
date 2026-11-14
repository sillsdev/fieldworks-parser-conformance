#!/usr/bin/env python3
"""Write a family's fixture files from its picked ladder, taking every expected parse from the C# oracle.

  finalize.py <family> <work-dir> <out-dir>

The oracle is hc-conformance built from sillsdev/machine 4d9b454d (the pin PanGloss uses, tag
pangloss-oracle-pin-4d9b454d), run in self-check mode with the repository's own DTD. The signature of every
analysis comes from `--propose`; each analysis's `rules` list comes from the oracle's trace, read from the
self-check's "declared N, traced M" mismatch lines; the loop runs until the self-check passes. Nothing is
typed by hand. ORACLE_DLL names the oracle (default: the scratch build).
"""
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
ORACLE = os.environ.get("ORACLE_DLL", "hc-conformance.dll")
PANGLOSS = os.environ.get("PANGLOSS", "pangloss")

CAMEL = {"deep-template-16": "CalDeepTemplate16", "redup-long-roots": "CalRedupLongRoots", "rule-cascade-32": "CalRuleCascade32",
         "infix-simulfix": "CalInfixSimulfix", "clitic-chain": "CalCliticChain", "templatic-nonconcat": "CalTemplaticNonconcat"}
REQ = {"rule-cascade-32": "phonology"}   # `requires` must equal the grammar-derived list
STRESS = {
    "deep-template-16": "16-slot template, five required slots, optional slots between them; odd slots prefix, even slots suffix",
    "redup-long-roots": "total and partial reduplication slots over long and self-repeating roots",
    "rule-cascade-32": "single-stratum cascade of 32 ordered phonological rules with metathesis and epenthesis",
    "infix-simulfix": "unanchored infix slots and ablaut simulfixes over many consonant and vowel sites",
    "clitic-chain": "homophonous proclitic and enclitic chains whose forms overlap the template suffixes",
    "templatic-nonconcat": "required root-and-pattern slot, ablaut, re-templating and affix slots over consonant skeletons",
}


def yq(s):
    return json.dumps(s, ensure_ascii=False)


def run_oracle(root, propose=False):
    cmd = ["dotnet", ORACLE, "--fixtures", str(root), "--include-pathological"] + (["--propose"] if propose else [])
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(root)).stdout


def write_draft(fx, words, parses, header):
    out = [header, f"language: {yq(CAMEL.get(fx.name, fx.name))}", "sources: []", f"requires: [{REQ.get(fx.name, '')}]",
           "fieldworks_producible: true", "budget_ms: 600000", "words:"]
    for w in words:
        entries = parses.get(w)
        if entries == []:
            out += [f"  - word: {w}", "    note: draft", "    expect_fail: true", "    blocked_by: [wasted-search]"]
            continue
        out += [f"  - word: {w}", "    note: draft", "    parses:"]
        entries = entries or [("X", ())]
        for sig, rules in entries:
            out += [f"      - signature: {yq(sig)}", f"        rules: [{', '.join(rules)}]"]
    (fx / "words.yaml").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def main():
    fam, work, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    ladder = [l.rstrip("\n").split("\t") for l in open(work / "ladder.tsv")]
    words = [l[1] for l in ladder]
    tmp = work / "oracle-root"
    shutil.rmtree(tmp, ignore_errors=True)
    fx = tmp / "edge-cases" / fam
    fx.mkdir(parents=True)
    shutil.copy(REPO / "HermitCrabInput.dtd", tmp)
    shutil.copy(REPO / "constructs.txt", tmp)
    shutil.copy(work / "grammar.xml", fx / "grammar.xml")
    header = "# kind: calibration (CALIBRATION ONLY: never run in conformance or engine test runs; see calibration/README.md)"
    write_draft(fx, words, {}, header)
    prop = run_oracle(tmp, propose=True)
    parses = {}
    cur = None
    for line in prop.splitlines():
        m = re.match(r"  - word: (\S+)", line)
        if m:
            cur = m.group(1)
            parses[cur] = []
        m = re.match(r'      - signature: "(.*)"$', line)
        if m and cur:
            parses[cur].append((m.group(1).replace('\\"', '"'), ()))
    for w in words:
        parses.setdefault(w, [])
    # a word the oracle printed with no signature has no analysis; one it did not print matched the placeholder (never)
    for rnd in range(4):
        write_draft(fx, words, parses, header)
        res = run_oracle(tmp)
        if "[PASS]" in res and "0 failed" in res:
            break
        counts = {}
        for w in words:
            counts[w] = Counter(parses[w])
        for line in res.splitlines():
            m = re.match(r"\s+word '([^']+)': (.*)", line)
            if not m:
                continue
            w = m.group(1)
            for sig, rules, declared, traced in re.findall(r"parse '([^']*)': rules \[([^\]]*)\]: declared (\d+), traced (\d+)", m.group(2)):
                key = (sig, tuple(r.strip() for r in rules.split(",") if r.strip()))
                counts[w][key] = int(traced)
        for w in words:
            parses[w] = sorted(k for k, v in counts[w].items() for _ in range(v))
    else:
        raise SystemExit("oracle self-check did not converge:\n" + res[-3000:])
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy(work / "grammar.xml", out / "grammar.xml")
    (out / "words.txt").write_text("\n".join(words) + "\n", encoding="utf-8", newline="\n")
    notes = json.load(open(work / "notes.json")) if (work / "notes.json").exists() else {}
    lines = [header, f"language: {yq(CAMEL.get(fam, fam))}", "sources: []", f"requires: [{REQ.get(fam, '')}]", "fieldworks_producible: true",
             "budget_ms: 600000",
             "# oracle-provenance: C# hc-conformance, sillsdev/machine 4d9b454d (tag pangloss-oracle-pin-4d9b454d), self-check mode; signatures from --propose, rules from the oracle trace",
             "words:"]
    for (rung, w, ln, cost, npar) in ladder:
        npp = len(parses[w])
        base = f"{rung} rung, {ln} chars, {int(cost) / 1e6:.2f}M measured parser cost, {npp} {'analysis' if npp == 1 else 'analyses'}. "
        if npp:
            extra = f"Stresses {STRESS.get(fam, fam)}; first analysis applies {len(parses[w][0][1])} rules."
        else:
            extra = f"No analysis: the search explores the {STRESS.get(fam, fam)} space and fails (dearest failing word, the cost of a wasted search)."
        note = base + extra + " " + notes.get(w, "")
        lines += [f"  - word: {w}", f"    note: {yq(note.strip())}"]
        if parses[w]:
            lines.append("    parses:")
            for sig, rules in parses[w]:
                lines += [f"      - signature: {yq(sig)}", f"        rules: [{', '.join(rules)}]"]
        else:
            lines += ["    expect_fail: true", "    blocked_by: [wasted-search]"]
    (out / "words.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    # cross-check against PanGloss: same analyses?
    raw = work / "xcheck.tsv"
    subprocess.run([PANGLOSS, "batch", str(out / "grammar.xml"), str(out / "words.txt"), str(raw), "--threads", "1", "--cost-column"], capture_output=True)
    meas = {}
    bad = 0
    for l in open(raw, encoding="utf-8"):
        f = l.rstrip("\n").split("\t")
        if len(f) >= 7 and f[3] != "STARTED":
            meas[f[1]] = (f[3], f[5], f[6])
        if len(f) >= 5 and f[3] == "ok":
            sigs = sorted(f[4].split(";")) if f[4] != "-" else []
            exp = sorted(s for s, _ in parses[f[1]])
            if sigs != exp:
                bad += 1
                print("PANGLOSS DIFFERS:", f[1], len(sigs), "vs oracle", len(exp))
    rungs = {l[1]: l[0] for l in ladder}
    (out / "ladder.tsv").write_text("word\trung\tstatus\twork_steps\tcost\n" + "".join(
        f"{w}\t{rungs[w]}\t{meas[w][0]}\t{meas[w][1]}\t{meas[w][2]}\n" for w in words), encoding="utf-8", newline="\n")
    print(f"{fam}: {len(words)} words, oracle self-check PASS, PanGloss differs on {bad}")


if __name__ == "__main__":
    main()
