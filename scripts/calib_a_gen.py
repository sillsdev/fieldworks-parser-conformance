#!/usr/bin/env python3
"""Generate the batch A calibration families (scale families) under calibration/.

Deterministic: every random choice comes from random.Random(seed) with a fixed seed per family.

  python3 scripts/calib_a_gen.py grammars x SCRATCH           write grammar.xml per family, candidates to SCRATCH
  python3 scripts/calib_a_gen.py select PANGLOSS SCRATCH [F]  measure candidates, pick the ladder, write words.txt
  python3 scripts/calib_a_gen.py yaml HC_DLL SCRATCH [F]      run the C# oracle on words.txt, write words.yaml

Each family function documents the HCLoader.cs function behind every construct it uses. See
calibration/README.md for the families, the ladders and the measured costs.
"""
import json
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calib_xml import *  # noqa: E402,F403

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "calibration"
CHARS = VOWELS + CONSONANTS
NCS = [("ncV", VOWELS), ("ncC", CONSONANTS), ("ncLab", "pmb"), ("ncFront", "ei"), ("ncBack", "ou"),
       ("ncVoiced", "mnlrbdg"), ("ncVless", "ptks")]


def syll(rng, n, closed=False):
    s = "".join(rng.choice(CONSONANTS) + rng.choice(VOWELS) for _ in range(n))
    return s + (rng.choice(CONSONANTS) if closed else "")


def uniq_roots(rng, n, shapes):
    seen, out = set(), []
    while len(out) < n:
        w = syll(rng, *rng.choice(shapes))
        if w not in seen:
            seen.add(w)
            out.append(w)
    return out


# Each family function returns dict(xml=, rmap={morpheme id: rule id}, cands=[dict(word, desc, kind)], pov=text)
# kind is "ok" (meant to parse) or "waste" (meant to explore and fail).

def slot_chain(rng, nslots, per_slot, forms, prefix, pos="posN", alts=None):
    """Optional slots of simple single-allomorph suffix rules. Returns (rules, slots, rmap, table) with
    table[slot] = [(rule id, form)]."""
    rules, slots, rmap, table = [], [], {}, []
    for s in range(nslots):
        ids, row = [], []
        for k, f in enumerate(rng.sample(forms, per_slot)):
            rid, mid = "%s%d_%d" % (prefix, s, k), "%s%d_%d" % (prefix.upper(), s, k)
            rules.append(rule(rid, mid, [subrule(rid + "_a", [("plus", "ncAny")], f)], pos=pos))
            rmap[mid] = rid
            ids.append(rid)
            row.append((rid, f))
        slots.append(("%sslot%d" % (prefix, s), True, ids))
        table.append(row)
    return rules, slots, rmap, table


def chain_words(rng, roots, table, n, minslots=0, maxslots=None, desc_prefix=""):
    out = []
    maxslots = len(table) if maxslots is None else maxslots
    for _ in range(n):
        r = rng.choice(roots)
        k = rng.randint(minslots, maxslots)
        used = sorted(rng.sample(range(len(table)), k))
        parts = [rng.choice(table[u]) for u in used]
        w = r + "".join(f for _, f in parts)
        out.append(dict(word=w, kind="ok", desc="%s%s+%s" % (desc_prefix, r, "+".join(p[0] for p in parts) or "-")))
    return out


def mutate_root(rng, root, roots_set):
    """A near-miss root: drop the last letter, which is a substring of a real root, so no substring prune can reject it."""
    for _ in range(20):
        m = root[:-1] if rng.random() < 0.5 else root[:-1] + rng.choice(CONSONANTS)
        if m not in roots_set and len(m) >= 2:
            return m
    return root[:-1] + "z"


# --------------------------------------------------------------------------------------------------
# Family 1: large lexicon
# --------------------------------------------------------------------------------------------------
def fam_large_lexicon():
    """5000 generated roots and a 10-slot optional suffix chain (6 rules per slot, 12 recurring forms).

    Constructs: LexicalEntry with one root allomorph (HCLoader.cs LoadLexEntry 745-760, LoadRootAllomorph 858-894);
    AffixTemplate and Slot (LoadAffixTemplate 1722-1855); slot rules with a lone suffix form allomorph
    (LoadInflAffixProcessRule 1025, LoadFormAffixProcessAllomorph 1626).
    No phonological rule: the expected rule attribution stays exact (a phonology cascade is batch B's family)."""
    rng = random.Random(24001)
    roots = uniq_roots(rng, 5000, [(2, False), (2, True), (3, False), (3, True), (4, False), (4, True)])
    forms = sorted({syll(rng, 1) for _ in range(9)} | {syll(rng, 1, True) for _ in range(3)})
    rules, slots, rmap, table = slot_chain(rng, 10, 6, forms, "s")
    entries = [entry("r%d" % i, f, "R%d" % i) for i, f in enumerate(roots)]
    xml = assemble(header("CalLargeLexicon", CHARS, NCS), [], rules, [template("nounTemplate", "posN", slots)], entries)
    cands = chain_words(rng, roots, table, 500)
    rs = set(roots)
    for _ in range(80):
        w = mutate_root(rng, rng.choice(roots), rs) + "".join(rng.choice(table[u])[1] for u in sorted(rng.sample(range(10), rng.randint(2, 10))))
        cands.append(dict(word=w, kind="waste", desc="near-miss root %s" % w))
    return dict(xml=xml, rmap=rmap, cands=cands)


# --------------------------------------------------------------------------------------------------
# Family 2: allomorph explosion
# --------------------------------------------------------------------------------------------------
NC_SEG = [("nc_" + c, c) for c in CHARS]
SEGCLASSES = [(cid, [m]) for cid, m in NC_SEG]


def suffix_text(base, ante_is_v, pen_is_v, f):
    i = CHARS.index(f)
    return base + VOWELS[i % 5] + ("" if pen_is_v else CONSONANTS[i % 11]) + ("" if ante_is_v else CONSONANTS[(i + 3) % 11])


def apply_suffix(stem, base):
    return stem + suffix_text(base, stem[-3] in VOWELS, stem[-2] in VOWELS, stem[-1])


def fam_allomorph_explosion():
    """36 suffix rules in 9 optional slots, each rule with 64 allomorphs (final segment x penultimate class x antepenultimate class),
    and 200 roots with a second, environment-conditioned root allomorph.

    Constructs: lone-suffix form allomorphs whose stem context is written in the input pattern, as
    HCLoader writes it (LoadFormAffixProcessAllomorph 1626); slot rules (LoadInflAffixProcessRule 1025); a root
    allomorph with a RequiredEnvironments right environment (LoadRootAllomorph 862-876); AffixTemplate and Slot
    (LoadAffixTemplate 1722-1855). The stress README's open item (a near-side density workload) is this."""
    rng = random.Random(24101)
    head = header("CalAllomorphExplosion", CHARS, NCS + SEGCLASSES)
    bases = []
    while len(bases) < 36:  # half vowel-initial so the elided root allomorph can apply
        b = (rng.choice(VOWELS) + rng.choice(CONSONANTS) if len(bases) % 2 else rng.choice(CONSONANTS) + rng.choice(VOWELS))
        if b not in bases:
            bases.append(b)
    rules, slots, rmap, table = [], [], {}, []
    for sl in range(9):
        ids, row = [], []
        for k in range(4):
            b = bases[sl * 4 + k]
            rid, mid = "a%d_%d" % (sl, k), "A%d_%d" % (sl, k)
            subs = []
            for av in (True, False):
                for pv in (True, False):
                    for f in CHARS:
                        items = [("star", "ncAny"), ("one", "ncV" if av else "ncC"), ("one", "ncV" if pv else "ncC"), ("one", "nc_" + f)]
                        subs.append(subrule("%s_%s%s%s" % (rid, "v" if av else "c", "v" if pv else "c", f), items, suffix_text(b, av, pv, f)))
            rules.append(rule(rid, mid, subs))
            rmap[mid] = rid
            ids.append(rid)
            row.append((rid, b))
        slots.append(("aslot%d" % sl, True, ids))
        table.append(row)
    roots = []
    seen = set()
    while len(roots) < 200:
        w = syll(rng, rng.choice([2, 3, 4]))
        if w not in seen:
            seen.add(w)
            roots.append(w)
    env = "<Environment><RightEnvironment><PhoneticTemplate><PhoneticSequence>%s</PhoneticSequence></PhoneticTemplate></RightEnvironment></Environment>" % '<SimpleContext naturalClass="ncV" />'
    entries = []
    for i, w in enumerate(roots):
        alt = '<Allomorph id="a_r%d_b"><PhoneticShape>%s</PhoneticShape><RequiredEnvironments>%s</RequiredEnvironments></Allomorph>' % (i, w[:-1], env)
        entries.append(entry("r%d" % i, w, "R%d" % i, extra_allomorphs=alt))
    xml = assemble(head, [], rules, [template("nounTemplate", "posN", slots)], entries)
    cands = []
    for n in range(500):
        r = rng.choice(roots)
        k = rng.randint(0, 9)
        used = sorted(rng.sample(range(9), k))
        for stem0, tag in ((r, "full"), (r[:-1], "elided")):
            stem, names = stem0, []
            ok = True
            for j, u in enumerate(used):
                rid, b = rng.choice(table[u])
                if j == 0 and tag == "elided" and b[0] not in VOWELS:
                    ok = False
                    break
                stem = apply_suffix(stem, b)
                names.append(rid)
            if ok:
                cands.append(dict(word=stem, kind="ok", desc="%s(%s stem)+%s" % (r, tag, "+".join(names))))
        # wasted: the last suffix text of a valid word, taken from the wrong context (matches the output, fails the input)
        stem, names = r, []
        for j, u in enumerate(used):
            rid, b = rng.choice(table[u])
            names.append(rid)
            if j == len(used) - 1:
                wrong = suffix_text(b, rng.random() < .5, rng.random() < .5, rng.choice(CHARS))
                stem = stem + wrong
            else:
                stem = apply_suffix(stem, b)
        cands.append(dict(word=stem, kind="waste", desc="%s+%s with a wrong-context allomorph last" % (r, "+".join(names))))
    return dict(xml=xml, rmap=rmap, cands=cands)


# --------------------------------------------------------------------------------------------------
# Family 3: homophone ambiguity
# --------------------------------------------------------------------------------------------------
def fam_homophone():
    """30 root forms, each shared by 4 noun and 2 verb entries; 5 noun slots, each with 3 homophonous suffix
    rules plus a distinct one; 3 verb slots whose rules reuse the same forms.

    Constructs: LexicalEntry (LoadLexEntry 745-760); two AffixTemplates, one per part of speech
    (LoadAffixTemplate 1722-1855, requiredPartsOfSpeech 1731-1733); slot rules (LoadInflAffixProcessRule 1025).
    A word with k suffixes has 4*3^k noun analyses (plus verb ones where the forms coincide)."""
    rng = random.Random(24201)
    forms = sorted({syll(rng, 1) for _ in range(12)})
    head = header("CalHomophoneAmbiguity", CHARS, NCS, parts_of_speech=(("posN", "noun"), ("posV", "verb")))
    rules, slots, rmap, table = [], [], {}, []
    for sl in range(5):
        f, g = rng.sample(forms, 2)
        ids, row = [], []
        for k in range(4):
            form = f if k < 3 else g
            rid, mid = "h%d_%d" % (sl, k), "H%d_%d" % (sl, k)
            rules.append(rule(rid, mid, [subrule(rid + "_a", [("plus", "ncAny")], form)]))
            rmap[mid] = rid
            ids.append(rid)
            row.append((rid, form))
        slots.append(("hslot%d" % sl, True, ids))
        table.append(row)
    vslots = []
    for sl in range(3):
        f = table[sl][0][1]
        ids = []
        for k in range(3):
            rid, mid = "v%d_%d" % (sl, k), "V%d_%d" % (sl, k)
            rules.append(rule(rid, mid, [subrule(rid + "_a", [("plus", "ncAny")], f)], pos="posV"))
            rmap[mid] = rid
            ids.append(rid)
        vslots.append(("vslot%d" % sl, True, ids))
    roots = uniq_roots(rng, 30, [(2, False), (3, False), (3, True), (4, False)])
    entries = []
    for i, w in enumerate(roots):
        for j in range(4):
            entries.append(entry("n%d_%d" % (i, j), w, "N%d_%d" % (i, j)))
        for j in range(2):
            entries.append(entry("v%d_%d" % (i, j), w, "W%d_%d" % (i, j), pos="posV"))
    xml = assemble(head, [], rules, [template("nounTemplate", "posN", slots), template("verbTemplate", "posV", vslots)], entries)
    cands, rs = [], set(roots)
    for n in range(300):
        r = rng.choice(roots)
        k = rng.randint(0, 5)
        used = sorted(rng.sample(range(5), k))
        tail = "".join(table[u][0][1] if rng.random() < .8 else table[u][3][1] for u in used)
        cands.append(dict(word=r + tail, kind="ok", desc="%s+%d suffixes %s" % (r, k, used)))
        if k >= 2:
            cands.append(dict(word=mutate_root(rng, r, rs) + tail, kind="waste", desc="near-miss root, %d suffixes" % k))
    return dict(xml=xml, rmap=rmap, cands=cands)


# --------------------------------------------------------------------------------------------------
# Family 4: large compounding
# --------------------------------------------------------------------------------------------------
def fam_compounding():
    """1200 noun roots and 300 verb roots of 2 to 8 syllables, two endocompound rules (noun+noun and verb+noun),
    and suffix templates on both parts of speech.

    Constructs: CompoundingRule, endocentric (HCLoader.cs LoadEndoCompoundingRule 1891-1969); slot rules
    (LoadInflAffixProcessRule 1025). The parser's root limit stays at its default of 2 (MaxRoots, PROTOCOL.md
    section 8): the batch command takes no morpher block, so a word of three or more roots would only measure the
    refusal. Cost scales with the roots squared at each split point instead."""
    rng = random.Random(24401)
    head = header("CalCompoundingLarge", CHARS, NCS, parts_of_speech=(("posN", "noun"), ("posV", "verb")))
    forms = sorted({syll(rng, 1) for _ in range(10)})
    nrules, nslots, nmap, ntable = slot_chain(rng, 5, 3, forms, "n")
    vrules, vslots, vmap, vtable = slot_chain(rng, 3, 3, forms, "w", pos="posV")
    def comp(cid, mid, hp, nhp):
        return ('<CompoundingRule id="%s" headPartsOfSpeech="%s" nonHeadPartsOfSpeech="%s" outputPartOfSpeech="%s"><Name>%s</Name>'
                '<CompoundingSubrules><CompoundingSubrule><HeadMorphologicalInput><PhoneticSequence id="%s_h">'
                '<OptionalSegmentSequence min="1" max="-1">%s</OptionalSegmentSequence></PhoneticSequence></HeadMorphologicalInput>'
                '<NonHeadMorphologicalInput><PhoneticSequence id="%s_n"><OptionalSegmentSequence min="1" max="-1">%s'
                '</OptionalSegmentSequence></PhoneticSequence></NonHeadMorphologicalInput><MorphologicalOutput>'
                '<CopyFromInput index="%s_h" /><CopyFromInput index="%s_n" /></MorphologicalOutput></CompoundingSubrule>'
                "</CompoundingSubrules></CompoundingRule>" % (cid, hp, nhp, hp, cid, cid, ANY, cid, ANY, cid, cid))
    comps = [comp("crNN", "CNN", "posN", "posN"), comp("crVN", "CVN", "posV", "posN")]
    nroots = uniq_roots(rng, 1200, [(1, True), (2, False), (2, True), (3, False), (3, True), (4, False), (5, False), (6, False), (8, False)])
    vroots = uniq_roots(rng, 300, [(2, False), (2, True), (3, False), (4, False)])
    entries = [entry("n%d" % i, w, "N%d" % i) for i, w in enumerate(nroots)] + [entry("v%d" % i, w, "V%d" % i, pos="posV") for i, w in enumerate(vroots)]
    xml = assemble(head, [], nrules + vrules, [template("nounTemplate", "posN", nslots), template("verbTemplate", "posV", vslots)],
                   entries, unslotted_ids=["crNN", "crVN"], extra_defs=comps)
    rmap = dict(nmap)
    rmap.update(vmap)
    rmap["__compound__"] = {"NN": "crNN", "VN": "crVN"}
    cands, nset = [], set(nroots)
    for _ in range(600):
        a, b = rng.choice(nroots), rng.choice(nroots)
        k = rng.randint(0, 5)
        used = sorted(rng.sample(range(5), k))
        tail = "".join(rng.choice(ntable[u])[1] for u in used)
        cands.append(dict(word=a + b + tail, kind="ok", desc="N %s + N %s, %d suffixes" % (a, b, k)))
        if rng.random() < .3:
            cands.append(dict(word=a + mutate_root(rng, b, nset) + tail, kind="waste", desc="N %s + near-miss, %d suffixes" % (a, k)))
        v, n = rng.choice(vroots), rng.choice(nroots)
        k = rng.randint(0, 3)
        used = sorted(rng.sample(range(3), k))
        cands.append(dict(word=v + n + "".join(rng.choice(vtable[u])[1] for u in used), kind="ok", desc="V %s + N %s, %d suffixes" % (v, n, k)))
    return dict(xml=xml, rmap=rmap, cands=cands)


# --------------------------------------------------------------------------------------------------
# Family 5: work cap
# --------------------------------------------------------------------------------------------------
def fam_work_cap():
    """The deep-optional shape widened: 20 optional prefix rules that all insert x and 8 optional suffix rules
    that all insert y, over four verb roots. A word x^a root y^b that fails at the lexicon is searched over every
    subset of the rules that could have fired; the subsets grow as C(20,a) * C(8,b).

    Constructs: unclassified affix process rules with a lone prefix or suffix form allomorph and a required part
    of speech (HCLoader.cs LoadUnclassifiedAffixProcessRule 1057, LoadFormAffixProcessAllomorph 1626-1653), the
    same shape edge-cases/deep-optional-affix-nesting uses."""
    rng = random.Random(24501)
    head = header("CalWorkCap", CHARS + "xy", NCS, parts_of_speech=(("posV", "verb"),))
    rules, rmap, ids = [], {}, []
    for i in range(20):
        rid, mid = "px%d" % i, "PX%d" % i
        rules.append(rule(rid, mid, [subrule(rid + "_a", [("plus", "ncAny")], "x", prefix=True)], pos="posV"))
        rmap[mid] = rid
        ids.append(rid)
    for i in range(8):
        rid, mid = "sy%d" % i, "SY%d" % i
        rules.append(rule(rid, mid, [subrule(rid + "_a", [("plus", "ncAny")], "y")], pos="posV"))
        rmap[mid] = rid
        ids.append(rid)
    roots = ["kat", "tup", "milo", "bosen"]
    entries = [entry("r%d" % i, w, "ROOT_%s" % w.upper(), pos="posV") for i, w in enumerate(roots)]
    xml = assemble(head, [], rules, [], entries, unslotted_ids=ids)
    cands = []
    for a in range(0, 21):
        for b in range(0, 9):
            for r in ("kat", "milo"):
                kind = "ok" if a + b <= 3 else "waste"
                root = r if kind == "ok" else r[:-1] + "m"
                cands.append(dict(word="x" * a + root + "y" * b, kind=kind, desc="x*%d %s y*%d" % (a, root, b)))
    return dict(xml=xml, rmap=rmap, cands=cands)


# --------------------------------------------------------------------------------------------------
# Family 6: prefilter scale
# --------------------------------------------------------------------------------------------------
def fam_prefilter(nrules=0, nslots=5, per_slot=2, nroots=700, nforms=2):
    """700 roots and a 5-slot optional suffix chain (2 rules per slot, 2 recurring forms); the word list holds 640
    words so a batch reaches the 512 words at which --prefilter auto considers a rule-admission filter.

    Constructs: as the large-lexicon family (HCLoader.cs LoadLexEntry, LoadRootAllomorph, LoadAffixTemplate,
    LoadInflAffixProcessRule, LoadFormAffixProcessAllomorph). nrules > 0 would add PhonologicalRules; the shipped
    grammar has none, because each rule adds admission units the prefilter must recover (see README)."""
    rng = random.Random(24601)
    head = header("CalPrefilterScale", CHARS, NCS + SEGCLASSES)
    forms = sorted({syll(rng, 1) for _ in range(nforms)})
    rules, slots, rmap, table = slot_chain(rng, nslots, per_slot, forms, "p")
    phon = []
    pairs = set()
    while len(phon) < nrules:
        src, dst = rng.sample(CHARS, 2)
        l1, l2 = rng.sample(CHARS, 2)
        if (src, l1, l2) in pairs:
            continue
        pairs.add((src, l1, l2))
        i = len(phon)
        phon.append(phon_rule("pr%d" % i, "sub%d" % i, src, dst, left=[("one", "nc_" + l1), ("one", "nc_" + l2)]))
    roots = uniq_roots(rng, nroots, [(2, False), (3, False), (3, True), (4, False), (5, False), (8, False), (12, False)])
    entries = [entry("r%d" % i, w, "R%d" % i) for i, w in enumerate(roots)]
    xml = assemble(head, phon, rules, [template("nounTemplate", "posN", slots)], entries)
    cands = chain_words(rng, roots, table, 3600, 0, nslots)
    rs = set(roots)
    for _ in range(600):
        w = mutate_root(rng, rng.choice(roots), rs) + "".join(rng.choice(table[u])[1] for u in sorted(rng.sample(range(nslots), rng.randint(1, nslots))))
        cands.append(dict(word=w, kind="waste", desc="near-miss root"))
    return dict(xml=xml, rmap=rmap, cands=cands)


FAMILIES = {"cal-large-lexicon": fam_large_lexicon, "cal-allomorph-explosion": fam_allomorph_explosion,
            "cal-homophone-ambiguity": fam_homophone, "cal-compounding-large": fam_compounding,
            "cal-work-cap": fam_work_cap, "cal-prefilter-scale": fam_prefilter}


# --------------------------------------------------------------------------------------------------
# Selection and oracle stages
# --------------------------------------------------------------------------------------------------
import math
import os

MINLEN, MAXLEN = 5, 40
CAP_STEPS = 200000
CAP_TXT = "cap-words.work-cap-%d.txt" % CAP_STEPS
CAP_YAML = "cap-words.work-cap-%d.yaml" % CAP_STEPS
MAX_CAP_WORDS = 3
RUNG_TOLERANCE = 2.5  # a word joins a rung only within this factor of the rung's target cost
RUNGS = [1, 4, 16, 64, 256]
# family -> (words per rung, extra top-cost words, total word target or None, extra pangloss args)
PLAN = {
    "cal-large-lexicon": (5, 0, None, []),
    "cal-allomorph-explosion": (5, 0, None, []),
    "cal-homophone-ambiguity": (5, 0, None, []),
    "cal-compounding-large": (5, 0, None, []),
    "cal-work-cap": (2, 0, None, ["--work-cap", str(CAP_STEPS)]),
    "cal-prefilter-scale": (4, 0, 640, ["--prefilter", "off"]),
}


def run_pangloss(pangloss, grammar, words, out, extra):
    subprocess.run([pangloss, "batch", str(grammar), str(words), str(out), "--cost-column", "--threads", "1"] + extra,
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def read_rows(tsv):
    rows = {}
    for line in Path(tsv).read_text(encoding="utf-8").splitlines():
        f = line.split("\t")
        if len(f) >= 7 and f[3] != "STARTED" and f[2] != "STARTED":
            rows[f[1]] = dict(status=f[3], sig=f[4], steps=int(f[5]), cost=int(f[6]))
    return rows


def select_ladder(meas, cands, per_rung, extra_top, total):
    """meas: word -> row. Return (ordered word list, word -> rung label). The 1x rung is the cheapest measured
    word of 5-40 characters; each later rung picks the words within RUNG_TOLERANCE of 4x, 16x, 64x, 256x (a rung no word reaches stays empty and the README says so), alternating
    parsing and non-parsing words so the wasted-search words are on every rung that has them."""
    kind = {c["word"]: c for c in cands}
    pool = sorted((w for w in meas if MINLEN <= len(w) <= MAXLEN and meas[w]["status"] != "SKIPPED"),
                  key=lambda w: (meas[w]["cost"], w))
    base = meas[pool[0]]["cost"]
    chosen, label = [], {}

    def take(w, lab):
        if meas[w]["status"] == "CAP" and sum(meas[x]["status"] == "CAP" for x in chosen) >= MAX_CAP_WORDS:
            return
        if w not in label:
            chosen.append(w)
            label[w] = lab

    for r in RUNGS:
        target = base * r
        by = sorted((w for w in pool if abs(math.log(max(meas[w]["cost"], 1) / target)) <= math.log(RUNG_TOLERANCE)),
                    key=lambda w: (abs(math.log(max(meas[w]["cost"], 1) / target)), w))
        parse = [w for w in by if meas[w]["sig"] != "-" and w not in label]
        nopar = [w for w in by if meas[w]["sig"] == "-" and w not in label]
        for i in range(per_rung):
            src = nopar if (i % 2 == 1 and nopar) else (parse or nopar)
            if src:
                take(src.pop(0), "%dx" % r)
    for w in sorted(pool, key=lambda w: (-meas[w]["cost"], w))[:extra_top]:
        take(w, "max")
    if total:
        band = [w for w in pool if 350000 <= meas[w]["cost"] <= 2000000 and w not in label]
        rng = random.Random(7)
        rng.shuffle(band)
        for w in band:
            if len(chosen) >= total:
                break
            take(w, "band")
        assert len(chosen) >= total, (len(chosen), total)
    return chosen, label, base


def describe(c, row, lab, base):
    ratio = row["cost"] / base
    what = "parses" if row["sig"] != "-" else "no analysis (wasted search)"
    if row["status"] == "CAP":
        return "%s. Measured: CAP at the reduced work cap of %d steps, %.0fx the family's cheapest word; the search is not finished, so no analysis is expected." % (c.get("desc", ""), CAP_STEPS, ratio)
    return "%s. Measured: %s, %.1fx the family's cheapest word (within %.1fx of the %s target)." % (c.get("desc", ""), what, ratio, RUNG_TOLERANCE, lab)


def cmd_select(pangloss, scratch, only=None):
    summary = {}
    for name in FAMILIES:
        if only and name != only:
            continue
        per_rung, extra_top, total, extra = PLAN[name]
        fd = OUT / name
        cands = json.loads((scratch / (name + ".cands.json")).read_text())
        allw = sorted({c["word"] for c in cands})
        (scratch / (name + ".all.txt")).write_text("\n".join(allw) + "\n")
        run_pangloss(pangloss, fd / "grammar.xml", scratch / (name + ".all.txt"), scratch / (name + ".all.tsv"), extra)
        meas = read_rows(scratch / (name + ".all.tsv"))
        chosen, label, base = select_ladder(meas, cands, per_rung, extra_top, total)
        capw = [w for w in chosen if meas[w]["status"] == "CAP"]
        keep = [w for w in chosen if w not in capw]
        (fd / "words.txt").write_text("\n".join(keep) + "\n", encoding="utf-8", newline="\n")
        if capw:
            (fd / CAP_TXT).write_text("\n".join(capw) + "\n", encoding="utf-8", newline="\n")
        kind = {c["word"]: c for c in cands}
        info = {w: dict(label=label[w], cost=meas[w]["cost"], steps=meas[w]["steps"], status=meas[w]["status"],
                        note=describe(kind[w], meas[w], label[w], base)) for w in chosen}
        (fd / "ladder.tsv").write_text("word\trung\tstatus\twork_steps\tcost\n" + "".join(
            "%s\t%s\t%s\t%d\t%d\n" % (w, info[w]["label"], info[w]["status"], info[w]["steps"], info[w]["cost"]) for w in chosen), encoding="utf-8", newline="\n")
        (scratch / (name + ".sel.json")).write_text(json.dumps(dict(base=base, words=info, order=chosen)))
        costs = [meas[w]["cost"] for w in chosen]
        summary[name] = (len(chosen), min(costs), max(costs), sum(costs))
        print(name, "selected", len(chosen), "min", min(costs), "max", max(costs), "sum", sum(costs))
    return summary


def cmd_table(scratch):
    """Print the README table rows and per-rung costs from the selection records."""
    print("| family | words | no-parse | min cost | max cost | span | lengths |")
    print("|---|---|---|---|---|---|---|")
    for name in FAMILIES:
        sel = json.loads((scratch / (name + ".sel.json")).read_text())
        ws = sel["order"]
        info = sel["words"]
        costs = [info[w]["cost"] for w in ws]
        base = min(costs)
        np_ = sum(1 for w in ws if "no analysis" in info[w]["note"] or info[w]["status"] == "CAP")
        print("| %s | %d | %d | %.2fM | %.1fM | %.0fx | %d-%d |" % (name, len(ws), np_, base / 1e6, max(costs) / 1e6,
              max(costs) / base, min(map(len, ws)), max(map(len, ws))))
    for name in FAMILIES:
        sel = json.loads((scratch / (name + ".sel.json")).read_text())
        by = {}
        for w in sel["order"]:
            by.setdefault(sel["words"][w]["label"], []).append(sel["words"][w]["cost"])
        print(name, {k: ["%.2fM" % (c / 1e6) for c in sorted(v)][:8] for k, v in by.items() if k != "band"})


def parse_sig(sig, rmap):
    out = []
    for a in sig.split(";"):
        morphs, _, surface = a.partition("|")
        toks = morphs.split("+")
        rules = [rmap[t] for t in toks if t in rmap and t != "__compound__"]
        roots = [t for t in toks if t[:1] in "NV" and t[1:].isdigit()]
        if len(roots) == 2 and "__compound__" in rmap:
            rules.insert(0, rmap["__compound__"][roots[0][0] + "N"])
        out.append((a, "-".join(toks), rules))
    return out


def q(s):
    return json.dumps(s, ensure_ascii=False)


def cmd_yaml(hcdll, scratch, only=None):
    for name in FAMILIES:
        if only and name != only:
            continue
        fd = OUT / name
        sel = json.loads((scratch / (name + ".sel.json")).read_text())
        rmap = json.loads((scratch / (name + ".rmap.json")).read_text())
        words = [w for w in sel["order"] if sel["words"][w]["status"] != "CAP"]
        wf = fd / "words.txt"
        script = scratch / (name + ".hc.script")
        tsv = scratch / (name + ".oracle.tsv")
        script.write_text("batch %s %s\n" % (wf, tsv))
        subprocess.run(["dotnet", hcdll, "-i", str(fd / "grammar.xml"), "-s", str(script)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        rows = {}
        for line in tsv.read_text(encoding="utf-8").splitlines():
            f = line.split("\t")
            if len(f) >= 5:
                rows[f[1]] = (f[3], f[4])
        info = sel["words"]
        capw = [w for w in sel["order"] if info[w]["status"] == "CAP"]
        out = [
            "# kind: calibration (cost-weight calibration fixture, not conformance; see calibration/README.md)",
            "# Synthetic scale grammar generated by scripts/calib_a_gen.py (family %s)." % name,
            "# Each parse's signature is the oracle's. The rules: and gloss: fields are NOT oracle output: the generator",
            "# derives them from the signature (morpheme id -> rule id, compounding rule from the root classes);",
            "# the hc-conformance self-check compares the rules against the oracle trace.",
            "# oracle-provenance: Oracle: hc.dll, Machine aab4c598 (batch command, MaxRoots 2); parses below are the oracle's signatures.",
            "language: %s" % grammar_name(fd / "grammar.xml"),
            'inspired_by: ["synthetic cost-calibration grammar"]',
            "sources:",
            '  - "PanGloss #240 parser-work cost-weight calibration"',
            "requires: []",
            "fieldworks_producible: true",
            "budget_ms: 600000",
            "words:",
        ]
        n_np = 0
        for w in words:
            st, sig = rows[w]
            assert st == "ok", (name, w, st)
            out.append("  - word: %s" % q(w))
            out.append("    note: %s" % q(info[w]["note"]))
            if sig == "-":
                out.append("    expect_fail: true")
                n_np += 1
            else:
                out.append("    parses:")
                for s_, gloss, rules in parse_sig(sig, rmap):
                    out.append("      - signature: %s" % q(s_))
                    out.append("        gloss: %s" % q(gloss))
                    out.append("        rules: [%s]" % ", ".join(rules))
                    out.append("        exercises: []")
        (fd / "words.yaml").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
        if capw:
            co = ["# kind: calibration (work-cap words; no oracle analyses are recorded for a word the engine stops)",
                  "# Run: pangloss batch grammar.xml %s out.tsv --cost-column --work-columns --work-cap %d" % (CAP_TXT, CAP_STEPS),
                  "# A CAP row ends at the cap, so its signature is partial and engine-dependent: only the status and the",
                  "# work-step bound are expected. The C# oracle has no work cap, so it supplies no row for these words.",
                  "work_cap: %d" % CAP_STEPS, "work_steps_at_most: %d" % (CAP_STEPS + CAP_STEPS // 16), "words:"]
            for w in capw:
                co += ["  - word: %s" % q(w), "    note: %s" % q(info[w]["note"]), "    expect_status: CAP",
                       "    measured_work_steps: %d" % info[w]["steps"]]
            (fd / CAP_YAML).write_text("\n".join(co) + "\n", encoding="utf-8", newline="\n")
        print(name, "yaml", len(words), "words,", n_np, "no-parse,", len(capw), "cap words")


def grammar_name(path):
    t = Path(path).read_text(encoding="utf-8")
    return t.split("<Name>")[1].split("</Name>")[0]


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    scratch = Path(sys.argv[3] if len(sys.argv) > 3 else "/tmp/calib_a")
    if cmd == "grammars":
        scratch.mkdir(parents=True, exist_ok=True)
        for name, fn in FAMILIES.items():
            d = fn()
            fd = OUT / name
            fd.mkdir(parents=True, exist_ok=True)
            (fd / "grammar.xml").write_text(d["xml"], encoding="utf-8", newline="\n")
            (scratch / (name + ".cands.json")).write_text(json.dumps(d["cands"]), encoding="utf-8")
            (scratch / (name + ".rmap.json")).write_text(json.dumps(d["rmap"]), encoding="utf-8")
            print(name, len(d["xml"]), "bytes", len(d["cands"]), "candidates")
    elif cmd == "select":
        cmd_select(sys.argv[2], scratch, sys.argv[4] if len(sys.argv) > 4 else None)
    elif cmd == "table":
        cmd_table(scratch)
    elif cmd == "yaml":
        cmd_yaml(sys.argv[2], scratch, sys.argv[4] if len(sys.argv) > 4 else None)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
