#!/usr/bin/env python3
"""Rebuild-merge member test cases into one grammar of disjoint cells.

usage: cellmerge.py SUITE OUTDIR LANGNAME member1:suffix1 member2:suffix2 ...
Cell 1 is the survivor: it keeps its letters and its XML ids, morpheme ids and rule ids, so its signatures do not change.
Later (absorbed) cells take letters no cell uses, and every XML id, morpheme id and rule id of one gets _suffix
(underscores are added when the result is already an id of an earlier cell).
Writes OUTDIR/grammar.xml, OUTDIR/words.yaml and OUTDIR/cellmap.json (the cell map used for replay checking).
"""
import sys, json, copy, re, os
from lxml import etree
import yaml

LOWER_POOL = "bdfghjklmnopqrsvwxz" + "àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ" + "aceituy"
UPPER_POOL = "HJKLMNPQRWXYZVUBDE"
TEXT_TAGS = ("Representation", "PhoneticShape")
CONTAINERS = ("BoundaryDefinitions", "PartsOfSpeech", "PhonologicalFeatureSystem", "SegmentDefinitions", "NaturalClasses",
              "MorphologicalPhonologicalRuleFeatures", "PhonologicalRuleDefinitions", "MorphologicalRuleDefinitions", "AffixTemplates", "LexicalEntries",
              "MorphemeCoOccurrenceRules", "AllomorphCoOccurrenceRules")


class Ind(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def load(suite, member):
    tree = etree.parse(os.path.join(suite, "edge-cases", member, "grammar.xml"))
    words = yaml.safe_load(open(os.path.join(suite, "edge-cases", member, "words.yaml"), encoding="utf-8"))
    return tree.getroot(), words


KEEP = set(os.environ.get("KEEP", ""))


def used_chars(root):
    s = set()
    for e in root.iter(*TEXT_TAGS):
        s.update(c for c in (e.text or "") if c.isalpha() and c not in KEEP)
    return s


def rename(old, suffix, taken):
    """old + _suffix, with underscores added until the result is not in taken; taken gains the result."""
    new = old + "_" + suffix
    while new in taken:
        new += "_"
    taken.add(new)
    return new


def make_cell(root, words, suffix, charmap, survivor=False, taken_ids=None, taken_mids=None):
    root = copy.deepcopy(root)
    taken_ids = set() if taken_ids is None else taken_ids
    taken_mids = set() if taken_mids is None else taken_mids
    ids = {e.get("id") for e in root.iter() if e.get("id")}
    shared = set() if os.environ.get("SEPB") else {e.get("id") for e in root.iter("BoundaryDefinition")}
    ids -= shared
    mids = set()
    for e in root.iter("MorphemeId"):
        mids.add(e.text)
    if survivor:
        taken_ids |= ids | shared
        taken_mids |= mids
        idmap = {i: i for i in ids}
        midmap = {m: m for m in mids}
    else:
        idmap = {i: rename(i, suffix, taken_ids) for i in sorted(ids)}
        midmap = {m: rename(m, suffix, taken_mids) for m in sorted(mids)}
    for e in root.iter():
        for k, v in list(e.attrib.items()):
            toks = v.split()
            if toks and any(t in ids for t in toks) and not all(t in ids or t in shared for t in toks):
                raise SystemExit(f"mixed id/non-id attribute {k}={v}")
            if toks and all(t in ids for t in toks):
                e.set(k, " ".join(idmap[t] for t in toks))
    for e in root.iter("MorphemeId"):
        e.text = midmap[e.text]
    if not survivor:
        for e in root.iter("MorphologicalPhonologicalRuleFeature"):
            e.text = idmap.get(e.text, e.text + "_" + suffix)
        for e in root.iter("Name"):
            if e.getparent().tag not in ("Language", "MorphologicalPhonologicalRuleFeatureGroup"):
                e.text = e.text + "_" + suffix
    for e in root.iter(*TEXT_TAGS):
        e.text = "".join(charmap.get(c, c) for c in (e.text or ""))
    return root, idmap, midmap


def map_word(w, idmap, midmap, suffix, charmap, survivor=False):
    w = copy.deepcopy(w)

    def nid(x):
        return idmap.get(x, x if survivor else x + "_" + suffix)

    w["word"] = "".join(charmap.get(c, c) for c in w["word"])
    for p in w.get("parses", []) or []:
        sig = p["signature"]
        pre, _, post = sig.partition("|")
        toks = pre.split("+")
        new = []
        for t in toks:
            if t == "":
                new.append(t)
            elif t in midmap:
                new.append(midmap[t])
            else:
                raise SystemExit(f"unknown morph id {t!r} in {sig}")
        post = "".join(charmap.get(c, c) for c in post)
        p["signature"] = "+".join(new) + "|" + post
        if "rules" in p:
            p["rules"] = [nid(r) for r in p["rules"]]
    for k in ("blocked_by", "neutralizes"):
        if k in w:
            w[k] = [nid(x) for x in w[k]]
    for k in w:
        if k not in ("word", "note", "parses", "exercises", "expect_fail", "provenance", "blocked_by", "neutralizes", "expect_skip"):
            raise SystemExit(f"unhandled word key {k}")
    note = w.get("note", "")
    w["note"] = f"[cell {suffix}] " + str(note)
    return w


def merge_stratum(tgt, ch):
    for k in ("phonologicalRules", "morphologicalRules"):
        if ch.get(k):
            tgt.set(k, (tgt.get(k, "") + " " + ch.get(k)).strip())
    merge(tgt, ch)


def merge(a, b):
    for ch in list(b):
        if not isinstance(ch.tag, str):
            continue
        if ch.tag in ("HeadFeatures", "FootFeatures"):
            if len(ch) or (ch.text or "").strip():
                raise SystemExit("non-empty " + ch.tag)
            continue
        if ch.tag in CONTAINERS:
            tgt = a.find(ch.tag)
            if tgt is None and ch.tag == "MorphologicalPhonologicalRuleFeatures":
                before = ("Name", "PartsOfSpeech", "PhonologicalFeatureSystem", "HeadFeatures", "FootFeatures")
                idx = max(i for i, x in enumerate(a) if x.tag in before) + 1
                tgt = etree.Element(ch.tag)
                a.insert(idx, tgt)
            if tgt is None and ch.tag in ("MorphemeCoOccurrenceRules", "AllomorphCoOccurrenceRules"):
                tgt = etree.Element(ch.tag)
                if ch.tag == "MorphemeCoOccurrenceRules" and a.find("AllomorphCoOccurrenceRules") is not None:
                    a.insert(list(a).index(a.find("AllomorphCoOccurrenceRules")), tgt)
                else:
                    pos = a.find("MorphemeCoOccurrenceRules")
                    if pos is None:
                        pos = a.find("Strata")
                    a.insert(list(a).index(pos) + 1, tgt)
            if tgt is None and a.tag == "Stratum" and ch.tag in ("MorphologicalRuleDefinitions", "AffixTemplates", "LexicalEntries"):
                order = ["Name", "MorphologicalRuleDefinitions", "AffixTemplates", "LexicalEntries"]
                idx = max([i for i, x in enumerate(a) if order.index(x.tag) < order.index(ch.tag)] + [-1]) + 1
                tgt = etree.Element(ch.tag)
                a.insert(idx, tgt)
            if tgt is None:
                raise SystemExit(f"structure differs at {ch.tag}")
            for x in list(ch):
                if x.tag == "BoundaryDefinition" and any(
                        y.get("id") == x.get("id") for y in tgt):
                    old = [y for y in tgt if y.get("id") == x.get("id")][0]
                    if etree.tostring(old) != etree.tostring(x):
                        if not os.environ.get("UNIONB"):
                            raise SystemExit("boundary %s differs between cells" % x.get("id"))
                        have = {r.text for r in old.iter("Representation")}
                        reps = old.find("Representations")
                        for r in x.iter("Representation"):
                            if r.text not in have:
                                reps.append(r)
                    continue
                tgt.append(x)
        elif ch.tag == "Strata":
            tgt = a.find("Strata")
            tl = list(tgt.findall("Stratum"))
            bsl = list(ch.findall("Stratum"))
            n_extra = max(len(bsl) - len(tl), 0)
            ctab = tl[0].get("characterDefinitionTable")
            for k, st in enumerate(bsl[:n_extra]):
                st.set("characterDefinitionTable", ctab)
                tgt.insert(k, st)
            rest = bsl[n_extra:]
            off = len(tl) - len(rest)
            for k, st in enumerate(rest):
                merge_stratum(tl[off + k], st)
        elif ch.tag in ("Language", "Strata", "Stratum"):
            tgt = a.find(ch.tag)
            if ch.tag == "Stratum":
                for k in ("phonologicalRules", "morphologicalRules"):
                    if ch.get(k):
                        tgt.set(k, (tgt.get(k, "") + " " + ch.get(k)).strip())
            merge(tgt, ch)
        elif ch.tag in ("Name",):
            pass
        elif ch.tag == "XXXX":
            pass
        elif ch.tag == "CharacterDefinitionTable":
            tgt = a.find(ch.tag)
            merge(tgt, ch)
        else:
            raise SystemExit(f"unmerged tag {ch.tag}")


def main(argv=None):
    suite, out, lang, *members = sys.argv[1:] if argv is None else argv
    specs = [s.split(":") for s in members]
    roots = []
    all_used = set()
    for m, _ in specs:
        r, w = load(suite, m)
        roots.append((r, w))
        all_used |= used_chars(r)
    word_only = []
    for r, w in roots:
        g = used_chars(r)
        wo = {c for x in w["words"] for c in x["word"] if c.isalpha() and c not in g and c not in KEEP}
        word_only.append(sorted(wo))
        all_used |= wo
    pool_l = [c for c in LOWER_POOL if c not in all_used]
    pool_u = [c for c in UPPER_POOL if c not in all_used]
    MAPP = set(os.environ.get("MAPPUNCT", ""))
    punct_used = set()
    for r, w in roots:
        for e in r.iter(*TEXT_TAGS):
            punct_used.update(c for c in (e.text or "") if not c.isalpha())
        for x in w["words"]:
            punct_used.update(c for c in x["word"] if not c.isalpha())
    pool_p = [c for c in "~#%&*/;!<>@$|" if c not in punct_used]
    merged = None
    words_out = []
    cellmap = []
    front = None
    seg_cell = {}
    taken_ids, taken_mids = set(), set()
    for i, ((m, suffix), (r, w)) in enumerate(zip(specs, roots)):
        chars = sorted(used_chars(r))
        if i == 0:
            cm = {}
        else:
            cm = {}
            for c in chars:
                if c.isupper():
                    cm[c] = pool_u.pop(0)
                else:
                    cm[c] = pool_l.pop(0)
            for c in word_only[i]:
                cm[c] = pool_u.pop(0) if c.isupper() else pool_l.pop(0)
            for e in r.iter(*TEXT_TAGS):
                for c in (e.text or ""):
                    if c in MAPP and c not in cm:
                        cm[c] = pool_p.pop(0)
        cell, idmap, midmap = make_cell(r, w, suffix, cm, i == 0, taken_ids, taken_mids)
        for el in cell.iter("SegmentDefinition", "FeatureNaturalClass"):
            seg_cell[el.get("id")] = suffix
        # Fixed point: pool letters used by earlier cells are now consumed (pool_l pops) but the same
        # letter must not be reused by a later cell: pop already removes it.
        mapped = [map_word(x, idmap, midmap, suffix, cm, i == 0) for x in w["words"]]
        words_out += mapped
        cellmap.append({"member": m, "suffix": suffix, "chars": cm, "ids": sorted(idmap), "morphemeIds": sorted(midmap), "idMap": idmap, "morphemeIdMap": midmap})
        if merged is None:
            merged = cell
            front = {k: v for k, v in w.items() if k != "words"}
        else:
            for k, v in w.items():
                if k == "words" or k == "language":
                    continue
                if k == "generated_no_parse":
                    for rule in v:
                        rule = copy.deepcopy(rule)
                        rule["alphabet"] = [cm.get(c, c) for c in rule["alphabet"]]
                        rule["note"] = f"[cell {suffix}] " + str(rule.get("note", ""))
                        front.setdefault("generated_no_parse", []).append(rule)
                    continue
                if k not in front:
                    front[k] = v
                elif k == "morpher":
                    if front[k] != v:
                        raise SystemExit("morpher differs: %s vs %s" % (front[k], v))
                elif isinstance(v, list) and isinstance(front[k], list):
                    for x in v:
                        if x not in front[k]:
                            front[k].append(x)
                elif front[k] != v:
                    front[k] = str(front[k]) + " | " + str(v) if isinstance(v, str) else front[k]
            if "morpher" in front and "morpher" not in w and front["morpher"] != {"MaxRoots": 2}:
                raise SystemExit("cell %s has no morpher but earlier cells do" % suffix)
            if "morpher" in w and "morpher" not in front:
                if w["morpher"] != {"MaxRoots": 2}:
                    raise SystemExit("late morpher %s" % w["morpher"])
                front["morpher"] = w["morpher"]
            merge(merged, cell)
    fs = merged.find("Language/PhonologicalFeatureSystem")
    if fs is not None and not os.environ.get("NOCELL"):
        # Unspecified features match anything, so a class of one cell would accept another cell's segments.
        # One shared feature gives every segment its cell's own value, and no class or segment crosses cells.
        # A survivor that already holds a cell feature (an earlier merge) keeps it; this merge's feature is outercell.
        fid = "cell"
        allids = {x.get("id") for x in merged.iter() if x.get("id")}
        while any(i == fid or i.startswith(fid + "_") for i in allids):
            fid = "outer" + fid
        f = etree.SubElement(fs, "SymbolicFeature", id=fid)
        etree.SubElement(f, "Name").text = fid
        syms = etree.SubElement(f, "Symbols")
        for _, suffix in specs:
            etree.SubElement(syms, "Symbol", id=fid + "_" + suffix).text = fid + " " + suffix
        for nc in merged.iter("FeatureNaturalClass"):
            etree.SubElement(nc, "FeatureValue", feature=fid, symbolValues=fid + "_" + seg_cell[nc.get("id")])
        for sd in merged.iter("SegmentDefinition"):
            etree.SubElement(sd, "FeatureValue", feature=fid, symbolValues=fid + "_" + seg_cell[sd.get("id")])
    mpr = merged.find("Language/MorphologicalPhonologicalRuleFeatures")
    if mpr is not None:
        kids = list(mpr)
        groups = {}
        for k in list(kids):
            if k.tag == "MorphologicalPhonologicalRuleFeatureGroup":
                nm = k.find("Name").text
                if nm in groups:
                    groups[nm].set("features", groups[nm].get("features") + " " + k.get("features"))
                    kids.remove(k)
                else:
                    groups[nm] = k
        for k in list(mpr):
            mpr.remove(k)
        for k in [k for k in kids if k.tag == "MorphologicalPhonologicalRuleFeature"] + [k for k in kids if k.tag != "MorphologicalPhonologicalRuleFeature"]:
            mpr.append(k)
    lang_el = merged.find("Language/Name")
    if lang != "-":
        lang_el.text = lang
        front["language"] = lang
    else:
        front["language"] = lang_el.text
    etree.indent(merged, space="  ")
    os.makedirs(out, exist_ok=True)
    xml = etree.tostring(merged, encoding="unicode")
    open(os.path.join(out, "grammar.xml"), "w", encoding="utf-8", newline="\n").write(
        '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE HermitCrabInput SYSTEM "HermitCrabInput.dtd">\n' + xml + "\n")
    doc = dict(front)
    doc["words"] = words_out
    open(os.path.join(out, "words.yaml"), "w", encoding="utf-8", newline="\n").write(
        yaml.dump(doc, Dumper=Ind, sort_keys=False, allow_unicode=True, width=1000, default_flow_style=False))
    json.dump(cellmap, open(os.path.join(out, "cellmap.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
