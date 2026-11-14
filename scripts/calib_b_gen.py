#!/usr/bin/env python3
"""Generate the batch B structural calibration grammars and candidate word lists.

  calib_b_gen.py grammar <family> <out-dir>      write <out-dir>/grammar.xml
  calib_b_gen.py candidates <family> <n> <seed>  print n candidate words, one per line

Deterministic: the same family and seed give the same bytes. The words that ship are picked from the
candidates by pick_words.py after measuring them; they are never invented by hand.
"""
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calib_b_lib import Grammar, VOWELS, CONS  # noqa: E402

FAMILIES = {}


def family(fn):
    FAMILIES["cal-" + fn.__name__.replace("_", "-")] = fn
    return fn


def syllables(cs, vs):
    return [c + v for c in cs for v in vs]


# ===================================================================================================
# 1. deep-template-16: a 16-slot template mixing required and optional slots (HC_RSL).
# ===================================================================================================
T16_REQUIRED = {1, 4, 8, 12, 16}
T16_UNIV = syllables("ptkmns", "ai")
T16_POOL = 6
T16_ROOTS_C = "bdglrhwy"


def t16_pool(j):
    return [T16_UNIV[((j - 1) + t) % len(T16_UNIV)] for t in range(T16_POOL)]


def t16_roots():
    rnd = random.Random(1601)
    out = set()
    while len(out) < 24:
        n = rnd.choice([2, 3])
        out.add("".join(rnd.choice(T16_ROOTS_C) + rnd.choice("eou") for _ in range(n)) + rnd.choice(["", "", T16_ROOTS_C[rnd.randrange(8)]]))
    return sorted(out)


@family
def deep_template_16():
    g = Grammar("CalDeepTemplate16")
    defs, slots = [], []
    for j in range(1, 17):
        ids = []
        for syl in t16_pool(j):
            rid = f"s{j:02d}_{syl}"
            ids.append(rid)
            defs.append(g.prefix(rid, syl) if j % 2 else g.suffix(rid, syl))
        slots.append((f"slot{j:02d}", ids, j not in T16_REQUIRED))
    tpl = g.template("t16", slots)
    g.stratum("Morphology", defs, [tpl], [g.entry("r_" + r, r) for r in t16_roots()])
    g.stratum("Clitics")
    g.stratum("Surface")
    return g


def cand_deep_template_16(rnd, n_aff=None, drop_required=None):
    if drop_required is None and rnd.random() < 0.15:
        drop_required = rnd.choice(sorted(T16_REQUIRED))
    """A word: choose which slots fill (all required, plus a random set of optional), then a syllable per slot."""
    opt = [j for j in range(1, 17) if j not in T16_REQUIRED]
    k = rnd.randint(0, len(opt)) if n_aff is None else max(0, n_aff - len(T16_REQUIRED))
    filled = set(T16_REQUIRED) | set(rnd.sample(opt, min(k, len(opt))))
    if drop_required is not None:
        filled.discard(drop_required)
    pre, suf = [], []
    for j in sorted(filled):
        pool = t16_pool(j)
        syl = rnd.choice(pool) if rnd.random() < 0.5 else pool[0 if rnd.random() < 0.5 else 3]
        (pre if j % 2 else suf).append((j, syl))
    word = "".join(s for _, s in sorted(pre, reverse=True)) + rnd.choice(t16_roots()) + "".join(s for _, s in sorted(suf))
    return word


# ===================================================================================================
# 2. redup-long-roots: total and partial reduplication on 6 to 14 segment roots, under a 6-slot template.
# ===================================================================================================
RD_SYL = syllables("ptkmns", "aiu")


def rd_roots():
    rnd = random.Random(2002)
    roots = set()
    while len(roots) < 14:                      # long roots, 3 to 7 syllables, a few closed
        n = rnd.randint(3, 7)
        r = "".join(rnd.choice(RD_SYL) for _ in range(n))
        if rnd.random() < 0.4 and len(r) < 13:
            r += rnd.choice("ptkmns")
        roots.add(r)
    while len(roots) < 22:                      # roots that are themselves a repeated half (ambiguous with total reduplication)
        h = "".join(rnd.choice(RD_SYL) for _ in range(rnd.randint(2, 3)))
        roots.add(h + h)
    roots.update(["ka", "mina", "tupa", "sasi", "kakaka", "kakakaka", "mimimi", "tutu", "tutututu", "sasasasa", "mimimimi"])  # short roots a reduplicated surface can also be built from
    return sorted(roots)


RD_PRE4 = ["wo", "ye", "ho", "lu"]
RD_SUF2 = ["ka", "mi", "su", "ne"]
RD_SUF5 = ["to", "pa", "ki", "na"]
RD_PRE6 = ["ra", "de", "bi", "go"]


def rd_rules(g):
    one, plus, star = "one", "plus", "star"
    out = {}
    s = g.seq
    c, v = g.copy, None
    out["tot"] = g.mrule("rd1_tot", "RED.total", [([s("x", plus)], [c("x"), c("x")])], redup="suffix")
    out["cv1"] = g.mrule("rd1_cv", "RED.CV", [([s("c", one, "ncC"), s("v", one, "ncV"), s("r", star)], [c("c"), c("v"), c("c"), c("v"), c("r")])], redup="prefix")
    out["cvc1"] = g.mrule("rd1_cvc", "RED.CVC", [([s("c", one, "ncC"), s("v", one, "ncV"), s("d", one, "ncC"), s("r", star)], [c("c"), c("v"), c("d"), c("c"), c("v"), c("d"), c("r")])], redup="prefix")
    out["fcv1"] = g.mrule("rd1_fcv", "RED.finalCV", [([s("r", star), s("c", one, "ncC"), s("v", one, "ncV")], [c("r"), c("c"), c("v"), c("c"), c("v")])], redup="suffix")
    out["tot3"] = g.mrule("rd3_tot", "RED2.total", [([s("x", plus)], [c("x"), c("x")])], redup="suffix")
    for k in ("4", "6"):
        out["tot" + k] = g.mrule(f"rd{k}_tot", "RED" + k + ".total", [([s("x", plus)], [c("x"), c("x")])], redup="suffix")
        out["cv" + k] = g.mrule(f"rd{k}_cv", "RED" + k + ".CV", [([s("c", one, "ncC"), s("v", one, "ncV"), s("r", star)], [c("c"), c("v"), c("c"), c("v"), c("r")])], redup="prefix")
        out["fcv" + k] = g.mrule(f"rd{k}_fcv", "RED" + k + ".finalCV", [([s("r", star), s("c", one, "ncC"), s("v", one, "ncV")], [c("r"), c("c"), c("v"), c("c"), c("v")])], redup="suffix")
    out["cv3"] = g.mrule("rd3_cv", "RED2.CV", [([s("c", one, "ncC"), s("v", one, "ncV"), s("r", star)], [c("c"), c("v"), c("c"), c("v"), c("r")])], redup="prefix")
    out["fcv3"] = g.mrule("rd3_fcv", "RED2.finalCV", [([s("r", star), s("c", one, "ncC"), s("v", one, "ncV")], [c("r"), c("c"), c("v"), c("c"), c("v")])], redup="suffix")
    return out


@family
def redup_long_roots():
    g = Grammar("CalRedupLongRoots")
    r = rd_rules(g)
    defs = list(r.values())
    slots = [("redup1", ["rd1_tot", "rd1_cv", "rd1_cvc", "rd1_fcv"], True)]
    for name, forms, pre, opt in (("suf2", RD_SUF2, False, True), ("redup3", None, None, True), ("redup4", None, None, True),
                                  ("pre5", RD_PRE4, True, True), ("redup6", None, None, True), ("suf7", RD_SUF5, False, False),
                                  ("pre8", RD_PRE6, True, True)):
        if forms is None:
            k = name[-1]
            slots.append((name, [f"rd{k}_tot", f"rd{k}_cv", f"rd{k}_fcv"], opt))
            continue
        ids = []
        for f in forms:
            rid = f"{name}_{f}"
            ids.append(rid)
            defs.append(g.prefix(rid, f) if pre else g.suffix(rid, f))
        slots.append((name, ids, opt))
    g.stratum("Morphology", defs, [g.template("tred", slots)], [g.entry("r_" + x, x) for x in rd_roots()])
    g.stratum("Clitics")
    g.stratum("Surface")
    return g


def rd_apply(op, s):
    if op == "tot":
        return s + s
    if op == "cv":
        return s[:2] + s
    if op == "cvc":
        return s[:3] + s if len(s) > 2 and s[2] in CONS else None
    if op == "fcv":
        return s + s[-2:] if len(s) > 1 and s[-2] in CONS and s[-1] in VOWELS else None
    return s


def cand_redup_long_roots(rnd):
    s = rnd.choice(rd_roots() if rnd.random() < 0.3 else [r for r in rd_roots() if len(r) >= 8])
    if rnd.random() < 0.12:                     # a surface no analysis builds: the reduplicated half is altered
        s = s + s[: rnd.randint(2, 5)].replace(s[0], "w", 1)
        return s
    op1 = rnd.choice([None, "tot", "cv", "cvc", "fcv"])
    s1 = rd_apply(op1, s) if op1 else s
    if s1 is None:
        return s
    if rnd.random() < 0.6:
        s1 = s1 + rnd.choice(RD_SUF2)
    s3 = s1
    for _ in range(3):                          # the three later reduplication slots, each optional
        op3 = rnd.choice([None, None, "cv", "fcv", "tot"])
        nxt = rd_apply(op3, s3) if op3 else s3
        if nxt is None or len(nxt) > 36:
            break
        s3 = nxt
    if rnd.random() < 0.5:
        s3 = rnd.choice(RD_PRE4) + s3
    s3 = s3 + rnd.choice(RD_SUF5)
    if rnd.random() < 0.5:
        s3 = rnd.choice(RD_PRE6) + s3
    return s3


# ===================================================================================================
# 3. rule-cascade-32: 32 ordered phonological rules in one stratum (epenthesis, deletion, assimilation,
#    vowel umlaut, metathesis) under an 8-slot template.
# ===================================================================================================
CASCADE_CLASSES = {
    "ncNas": {"nas": "+"}, "ncLab": {"place": "labial", "syl": "-"}, "ncAlv": {"place": "alveolar", "syl": "-"},
    "ncStopVl": {"syl": "-", "cont": "-", "voice": "-"}, "ncStopVd": {"syl": "-", "cont": "-", "voice": "+", "nas": "-"},
    "ncLiq": {"syl": "-", "voice": "+", "cont": "+", "high": "-"}, "ncHiV": {"syl": "+", "high": "+"},
    "ncFront": {"syl": "+", "back": "-"},
}

# (kind, id, spec) in application order. Rewrites: (input class|segment, output segment|None, left, right).
CASCADE = [
    ("ep", "ep1_i_s_Tvl", ("i", ["s"], ["ncStopVl"])),
    ("sub", "su1_n_m", ("n", "m", [], ["ncLab"])),
    ("sub", "su2_t_d", ("t", "d", ["ncNas"], [])),
    ("sub", "su3_k_g", ("k", "g", ["ncNas"], [])),
    ("sub", "su4_p_b", ("p", "b", ["ncNas"], [])),
    ("vow", "vh1_a_e", ("a", "e", [], ["ncC", "i"])),
    ("del", "de1_i", ("i", None, ["ncV"], [])),
    ("sub", "su5_s_r", ("s", "r", ["ncV"], ["ncV"])),
    ("vow", "vh2_o_u", ("o", "u", [], ["ncC", "u"])),
    ("sub", "su6_l_r", ("l", "r", [], ["i"])),
    ("sub", "su7_d_r", ("d", "r", ["ncV"], ["ncV"])),
    ("vow", "vh3_e_i", ("e", "i", [], ["ncC", "i"])),
    ("sub", "su8_m_n", ("m", "n", [], ["ncAlv"])),
    ("del", "de4_y_final", ("y", None, [], "final")),
    ("ep", "ep6_o_h_C", ("o", ["h"], ["ncC"])),
    ("del", "de2_u", ("u", None, [], ["ncV"])),
    ("sub", "su9_b_w", ("b", "w", ["ncV"], ["ncV"])),
    ("vow", "vh4_a_o", ("a", "o", ["ncLab"], [])),
    ("sub", "su10_g_y", ("g", "y", ["ncFront"], [])),
    ("sub", "su11_k_h", ("k", "h", ["ncV"], ["ncV"])),
    ("sub", "su12_t_s", ("t", "s", ["ncHiV"], [])),
    ("sub", "su13_p_h", ("p", "h", ["ncV"], ["ncV"])),
    ("vow", "vh5_i_e", ("i", "e", ["ncLiq"], [])),
    ("sub", "su14_n_l", ("n", "l", ["ncV"], ["ncLiq"])),
    ("vow", "vh6_u_o", ("u", "o", ["ncLab"], [])),
    ("sub", "su15_r_l", ("r", "l", ["ncNas"], [])),
    ("sub", "su16_w_y", ("w", "y", ["ncV"], [])),
    ("sub", "su17_h_k", ("h", "k", ["ncNas"], [])),
    ("vow", "vh7_e_a", ("e", "a", ["ncAlv"], ["ncNas"])),
    ("meta", "mt1_s_Tvl", (["s", "ncStopVl"],)),
    ("meta", "mt2_N_h", (["ncNas", "h"],)),
    ("meta", "mt3_L_Tvd", (["ncLiq", "ncStopVd"],)),
    ("meta", "mt4_k_s", (["k", "s"],)),
]


def cascade_node(g, x, sid=None):
    return g.ctx(x, sid) if x.startswith("nc") else g.seg(x, sid)


def cascade_rules(g):
    for c, f in CASCADE_CLASSES.items():
        g.add_class(c, f)
    ids = []
    for kind, rid, spec in CASCADE:
        ids.append(rid)
        if kind == "meta":
            a, b = spec[0]
            g.metathesis(rid, rid, [cascade_node(g, a, rid + "_a"), cascade_node(g, b, rid + "_b")], rid + "_b", rid + "_a")
            continue
        if kind == "ep":
            out, left, right = spec
            g.rewrite(rid, rid, [], [g.seg(out)], g.env([cascade_node(g, x) for x in left], [cascade_node(g, x) for x in right]))
            continue
        inp, out, left, right = spec
        final = right == "final"
        env = g.env([cascade_node(g, x) for x in left] if left else None,
                    None if final else ([cascade_node(g, x) for x in right] if right else None), final=final)
        g.rewrite(rid, rid, [cascade_node(g, inp)], [g.seg(out)] if out else [], env)
    return ids


CAS_SLOTS = [
    ("suf1", False, ["ska", "ntu", "mbo", "lti", "hna", "iu"]),
    ("suf2", False, ["ki", "ua", "nsi", "rta", "ye", "olu"]),
    ("pre3", True, ["ans", "el", "ug", "im", "oh", "ek"]),
    ("suf4", False, ["tka", "mpi", "ngu", "hli", "ao", "ei"]),
    ("pre5", True, ["is", "unt", "ar", "om", "yu", "al"]),
    ("suf6", False, ["sku", "mtu", "gri", "ae", "nha", "kso"]),
    ("suf7", False, ["pa", "ski", "ndu", "ila", "ou", "tsa"]),
    ("pre8", True, ["wa", "tin", "ske", "uh", "ol", "an"]),
]
CAS_ROOTS = ["bikat", "tenasu", "kopami", "sulina", "hadeki", "mirota", "nakusi", "pelugo", "tasime", "gonupa",
             "lesika", "dunamo", "ritaku", "wesona", "yamiti", "bolesa", "kunari", "sitope", "mahune", "pugira"]


@family
def rule_cascade_32():
    g = Grammar("CalRuleCascade32")
    pids = cascade_rules(g)
    defs, slots = [], []
    for name, pre, forms in CAS_SLOTS:
        ids = []
        for f in forms:
            rid = f"{name}_{f}"
            ids.append(rid)
            defs.append(g.prefix(rid, f) if pre else g.suffix(rid, f))
        slots.append((name, ids, True))
    g.stratum("Morphology", defs, [g.template("tcas", slots)], [g.entry("r_" + r, r) for r in CAS_ROOTS], phon=pids)
    g.stratum("Clitics")
    g.stratum("Surface")
    return g


def cand_rule_cascade_32(rnd):
    root = rnd.choice(CAS_ROOTS)
    seq = [root]
    for name, pre, forms in CAS_SLOTS:
        if rnd.random() < 0.65:
            seq.append(f"{name}_{rnd.choice(forms)}")
    return ("GEN", "r_" + root, seq[1:])


# ===================================================================================================
# 4. infix-simulfix: anchored and unanchored infixes, a final-consonant infix, two simulfixes
#    (prefix or suffix plus a vowel change in place), plain affixes, a 60-root lexicon.
# ===================================================================================================
IX_INF1 = ["um", "in", "ar", "os"]          # "C_V"
IX_INF2 = ["ng", "ha", "ti", "lu"]          # "V_C"
IX_INF3 = ["el", "ko", "ma", "ps"]          # "V_V" and "CV_C"
IX_INF6 = ["ti", "ha", "ng", "lu"]
IX_INF7 = ["ng", "ha", "ru", "ti"]
IX_INF8 = ["ke", "wi", "do", "ru"]
IX_SIM4 = ["ta", "ki", "mo", "sa"]          # prefix + the first vowel becomes front
IX_SIM5 = ["ne", "pu", "gi", "ro"]          # suffix + the last vowel becomes high
IX_SUF6 = ["wa", "ye", "ho", "du", "bi", "lo"]
IX_PRE7 = ["ha", "he", "yu", "gi"]


def ix_roots():
    rnd = random.Random(4004)
    out = set()
    while len(out) < 60:
        n = rnd.randint(2, 6)
        r = "".join(rnd.choice("ptkmnsbdgl") + rnd.choice("aeiou") for _ in range(n))
        if rnd.random() < 0.6:
            r += rnd.choice("ptkmnsl")
        out.add(r)
    return sorted(out)


@family
def infix_simulfix():
    g = Grammar("CalInfixSimulfix")
    g.add_class("ncFrontV", {"syl": "+", "back": "-", "high": "-"})
    g.add_class("ncHighV", {"syl": "+", "high": "+"})
    g.add_class("ncFrontMod", {"back": "-"})
    g.add_class("ncHighMod", {"high": "+"})
    s, c = g.seq, g.copy
    defs, slots = [], []

    def infix(rid, form, left, right):
        """HCLoader's infix shape (LoadFormAffixProcessAllomorph, HCLoader.cs 1576-1594): input part `left` is
        any* then the left context, part `right` is the right context then any*; output is Copy left, the form
        (written +form+), Copy right. `left` and `right` are lists of natural-class ids."""
        star = '<OptionalSegmentSequence min="0" max="-1"><SimpleContext naturalClass="ncAny" /></OptionalSegmentSequence>'
        ctx = lambda cl: "".join(f'<SimpleContext naturalClass="{x}" />' for x in cl)
        lp = f'<PhoneticSequence id="left">{star}{ctx(left)}</PhoneticSequence>'
        rp = f'<PhoneticSequence id="right">{ctx(right)}{star}</PhoneticSequence>'
        shape = f"+{form}+" if g.plus else form
        return g.mrule(rid, rid, [([lp, rp], [c("left"), g.ins(shape), c("right")])])

    # Every right context is non-empty: an infix that lands at the end of the word (empty tail) is the shape on
    # which the oracle and PanGloss disagree (see README), so no word in this family depends on it.
    # The oracle parses only left contexts of two segments with a one-segment right context (VC_V, CV_C); a
    # one-segment or three-segment left context, or a two-segment right context, loses analyses in it (README).
    for slot, forms, left, right in (("inf4", IX_INF1, ["ncV", "ncC"], ["ncV"]), ("inf9", IX_INF3, ["ncC", "ncV"], ["ncC"]),
                                     ("inf5", IX_INF7, ["ncV", "ncC"], ["ncV"]), ("inf3", IX_INF2, ["ncC", "ncV"], ["ncC"]),
                                     ("inf6", IX_INF6, ["ncV", "ncC"], ["ncV"]), ("inf8", IX_INF8, ["ncC", "ncV"], ["ncC"])):
        ids = []
        for f in forms:
            rid = f"{slot}_{f}"
            ids.append(rid)
            defs.append(infix(rid, f, left, right))
        slots.append((f"infix_{slot}", ids, True))
    ids = []
    for f in IX_SIM5:
        rid = "sim5_" + f
        ids.append(rid)
        defs.append(g.mrule(rid, rid, [([s("l", "star"), s("v", "one", "ncV"), s("e", "one", "ncC")], [c("l"), g.mod("v", "ncHighMod"), c("e"), g.ins(g.plus and "+" + f or f)])]))
    slots.append(("simulfix_suffix_ablaut", ids, True))
    for name, forms, pre in (("suf6", IX_SUF6, False), ("pre7", IX_PRE7, True)):
        ids = []
        for f in forms:
            rid = f"{name}_{f}"
            ids.append(rid)
            defs.append(g.prefix(rid, f) if pre else g.suffix(rid, f))
        slots.append((name, ids, name == "pre7"))
    g.stratum("Morphology", defs, [g.template("tinf", slots)], [g.entry("r_" + x, x) for x in ix_roots()])
    g.stratum("Clitics")
    g.stratum("Surface")
    return g


def cand_infix_simulfix(rnd):
    root = rnd.choice(ix_roots())
    seq = []
    pools = [("inf4", IX_INF1), ("inf9", IX_INF3), ("inf5", IX_INF7), ("inf3", IX_INF2), ("inf6", IX_INF6), ("inf8", IX_INF8), ("sim5", IX_SIM5), ("suf6", IX_SUF6), ("pre7", IX_PRE7)]
    for name, forms in pools:
        if name == "suf6" or rnd.random() < 0.7:
            seq.append(f"{name}_{rnd.choice(forms)}")
    return ("GEN", "r_" + root, seq)


# ===================================================================================================
# 5. clitic-chain: a final template, then 8 proclitics and 12 enclitics in the Clitics stratum, with
#    homophonous clitics and enclitic forms that are also template suffixes (clitic-vs-affix ambiguity).
# ===================================================================================================
CL_PRO = ["wa", "ye", "ho", "lu", "de", "bi"]
CL_ENC = ["ka", "ti", "mi", "su", "ne", "lo"]
CL_SUF1 = ["ka", "ti", "mi", "su", "pa", "ra"]
CL_SUF2 = ["ne", "lo", "ka", "ti", "ga", "ba"]
CL_SUF3 = ["su", "mi", "do", "re"]
CL_ROOTS = ["bakul", "tomis", "gurad", "helon", "sirak", "dolem", "paran", "kemun", "lobit", "rasog",
            "mutek", "nabid", "wegal", "yosun", "hahip", "midor", "yaluk", "denab", "witor", "samed"]


@family
def clitic_chain():
    g = Grammar("CalCliticChain")
    defs, slots = [], []
    for name, forms in (("suf1", CL_SUF1), ("suf2", CL_SUF2), ("suf3", CL_SUF3)):
        ids = []
        for f in forms:
            rid = f"{name}_{f}"
            ids.append(rid)
            defs.append(g.suffix(rid, f))
        slots.append((name, ids, True))
    g.stratum("Morphology", defs, [g.template("tcl", slots, final=True)], [g.entry("r_" + x, x) for x in CL_ROOTS])
    cdefs = []
    for f in CL_PRO:
        for h in "ab":
            cdefs.append(g.prefix(f"pro_{f}_{h}", f))
    for f in CL_ENC:
        for h in "ab":
            cdefs.append(g.suffix(f"enc_{f}_{h}", f))
    g.stratum("Clitics", cdefs)
    g.stratum("Surface")
    return g


def cand_clitic_chain(rnd):
    root = rnd.choice(CL_ROOTS)
    seq = []
    for name, forms in (("suf1", CL_SUF1), ("suf2", CL_SUF2), ("suf3", CL_SUF3)):
        if rnd.random() < 0.6:
            seq.append(f"{name}_{rnd.choice(forms)}")
    pro = [f"pro_{rnd.choice(CL_PRO)}_a" for _ in range(rnd.randint(0, 4))]
    enc = [f"enc_{rnd.choice(CL_ENC)}_a" for _ in range(rnd.randint(0, 5))]
    return ("GEN", "r_" + root, seq + enc + pro)


# ===================================================================================================
# 6. templatic-nonconcat: root-and-pattern morphology as FieldWorks can write it: consonant-skeleton roots
#    (3 and 4 consonants) interdigitated with vowels by MoAffixProcess-style rules (copy each consonant,
#    insert vowels, copy a consonant twice for gemination), plus in-place vowel mutation (ModifyFromInput).
# ===================================================================================================
TM_TRI = {   # pattern id -> output spec over c1 c2 c3; strings are inserted segments
    "p01": ["c1", "a", "c2", "a", "c3"], "p02": ["c1", "a", "c2", "c2", "a", "c3"], "p03": ["c1", "u", "c2", "i", "c3"],
    "p04": ["c1", "a", "c2", "i", "c3"], "p05": ["ni", "c1", "c2", "a", "c3"], "p06": ["c1", "a", "c2", "c2", "i", "c3"],
    "p07": ["ta", "c1", "a", "c2", "a", "c3"], "p08": ["c1", "i", "c2", "a", "c3"], "p09": ["ma", "c1", "c2", "a", "c3"],
    "p10": ["c1", "aa", "c2", "a", "c3"], "p11": ["i", "c1", "c2", "a", "c3"], "p12": ["c1", "a", "c2", "c2", "u", "c3"],
    "p13": ["c1", "u", "c2", "c2", "i", "c3"], "p14": ["sta", "c1", "c2", "a", "c3"], "p15": ["c1", "a", "c2", "a", "c3", "a"],
}
TM_QUAD = {
    "q01": ["c1", "a", "c2", "c3", "a", "c4"], "q02": ["c1", "a", "c2", "c3", "i", "c4"], "q03": ["ta", "c1", "a", "c2", "c3", "a", "c4"],
    "q04": ["c1", "u", "c2", "c3", "i", "c4"], "q05": ["mu", "c1", "c2", "i", "c3", "c4"],
}
TM_PRE3 = ["ya", "ta", "na", "ha", "bi", "lu"]
TM_SUF4 = ["tu", "ta", "ti", "na", "un", "in"]
TM_PRE5 = ["wa", "ba", "ka", "sa"]
TM_SUF6 = ["ni", "hu", "ha", "ki"]


def tm_roots():
    rnd = random.Random(6006)
    cs = "ptkbdgmnslrh"
    tri, quad = set(), set()
    while len(tri) < 100:
        tri.add("".join(rnd.choice(cs) for _ in range(3)))
    while len(quad) < 20:
        quad.add("".join(rnd.choice(cs) for _ in range(4)))
    return sorted(tri), sorted(quad)


@family
def templatic_nonconcat():
    g = Grammar("CalTemplaticNonconcat")
    g.add_class("ncHighMod", {"high": "+"})
    g.add_class("ncFrontMod", {"back": "-"})
    s, c = g.seq, g.copy
    defs, pat_ids = [], []

    def spec_out(spec, n):
        out = []
        for t in spec:
            out.append(c(t) if t.startswith("c") and t[1:].isdigit() else g.ins(t))
        return out

    for pid, spec in TM_TRI.items():
        defs.append(g.mrule("tri_" + pid, "PATTERN." + pid, [([s(f"c{i}", "one", "ncC") for i in (1, 2, 3)], spec_out(spec, 3))]))
        pat_ids.append("tri_" + pid)
    for pid, spec in TM_QUAD.items():
        defs.append(g.mrule("quad_" + pid, "PATTERN." + pid, [([s(f"c{i}", "one", "ncC") for i in (1, 2, 3, 4)], spec_out(spec, 4))]))
        pat_ids.append("quad_" + pid)
    slots = [("pattern", pat_ids, False)]
    defs.append(g.mrule("ablaut_last", "ABL.last", [([s("l", "star"), s("v", "one", "ncV"), s("e", "one", "ncC")], [c("l"), g.mod("v", "ncHighMod"), c("e")])]))
    defs.append(g.mrule("ablaut_first", "ABL.first", [([s("a", "one", "ncC"), s("v", "one", "ncV"), s("r", "star")], [c("a"), g.mod("v", "ncFrontMod"), c("r")])]))
    slots.append(("ablaut", ["ablaut_last", "ablaut_first"], True))
    cv = lambda: [s(f"c{i}", "one", "ncC") if i % 2 else s(f"v{i}", "one", "ncV") for i in range(1, 6)]
    parts = ("c1", "v2", "c3", "v4", "c5")
    t2 = {"t1": [parts[0], parts[1], parts[2], parts[2], parts[3], parts[4]], "t2": ["ta", *parts], "t3": [*parts, "at"],
          "t4": [parts[0], parts[1], parts[2], parts[3], parts[4], parts[3], parts[4]]}
    ids = []
    for k, spec in t2.items():
        rid = "retemplate_" + k
        ids.append(rid)
        defs.append(g.mrule(rid, rid, [(cv(), [c(t) if t in parts else g.ins(t) for t in spec])]))
    slots.append(("retemplate", ids, True))
    for name, forms, pre in (("pre3", TM_PRE3, True), ("suf4", TM_SUF4, False), ("pre5", TM_PRE5, True), ("suf6", TM_SUF6, False),
                             ("suf7", TM_SUF4, False), ("pre8", TM_PRE3, True)):
        ids = []
        for f in forms:
            rid = f"{name}_{f}"
            ids.append(rid)
            defs.append(g.prefix(rid, f) if pre else g.suffix(rid, f))
        slots.append((name, ids, True))
    tri, quad = tm_roots()
    g.stratum("Morphology", defs, [g.template("ttm", slots)], [g.entry("r_" + x, x) for x in tri + quad])
    g.stratum("Clitics")
    g.stratum("Surface")
    return g


def cand_templatic_nonconcat(rnd):
    tri, quad = tm_roots()
    if rnd.random() < 0.7:
        root, pat = rnd.choice(tri), "tri_" + rnd.choice(sorted(TM_TRI))
    else:
        root, pat = rnd.choice(quad), "quad_" + rnd.choice(sorted(TM_QUAD))
    seq = [pat]
    if rnd.random() < 0.5:
        seq.append(rnd.choice(["ablaut_last", "ablaut_first"]))
    if rnd.random() < 0.5:
        seq.append("retemplate_" + rnd.choice(["t1", "t2", "t3", "t4"]))
    for name, forms in (("pre3", TM_PRE3), ("suf4", TM_SUF4), ("pre5", TM_PRE5), ("suf6", TM_SUF6), ("suf7", TM_SUF4), ("pre8", TM_PRE3)):
        if rnd.random() < 0.75:
            seq.append(f"{name}_{rnd.choice(forms)}")
    return ("GEN", "r_" + root, seq)


# ---------------------------------------------------------------------------------------------------
def generate(grammar, root, rules):
    import subprocess
    r = subprocess.run([PANGLOSS, "generate", str(grammar), root] + list(reversed(rules)), capture_output=True, text=True)
    out = r.stdout.split()
    return out[0] if out else None


PANGLOSS = os.environ.get("PANGLOSS", "pangloss")


def main(argv):
    cmd = argv[1]
    fam = argv[2].removeprefix("cal-")
    if cmd == "grammar":
        out = Path(argv[3])
        out.mkdir(parents=True, exist_ok=True)
        (out / "grammar.xml").write_text(FAMILIES["cal-" + fam]().xml(), encoding="utf-8", newline="\n")
    elif cmd == "candidates":
        n, seed = int(argv[3]), int(argv[4])
        rnd = random.Random(seed)
        fn = globals()["cand_" + fam.replace("-", "_")]
        seen = []
        gram = None
        tries = 0
        while len(seen) < n and tries < n * 20:
            tries += 1
            w = fn(rnd)
            if isinstance(w, tuple):                 # a morpheme list: realise it with the engine's own generator
                w = generate(Path(argv[5]) / "grammar.xml", w[1], w[2])
            if w and w not in seen and 5 <= len(w) <= 40:
                seen.append(w)
        print("\n".join(seen))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
