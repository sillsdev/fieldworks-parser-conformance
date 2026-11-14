#!/usr/bin/env python3
"""Shared emitter for the structural calibration grammars (batch B).

Every construct written here is one HCLoader.cs writes (see calibration/README.md for the function per
construct). The output is HermitCrabInput XML; the repository's DTD validates it.

Inventory: five vowels and fourteen consonants over nine phonological features, every segment with a
distinct feature bundle. Natural classes are named by a dict {feature: symbol}.
"""
import os
from xml.sax.saxutils import escape

FEATURES = {
    "syl": "+-", "nas": "+-", "voice": "+-", "cont": "+-", "high": "+-", "back": "+-", "round": "+-", "lat": "+-",
    "place": ["labial", "alveolar", "velar", "glottal", "none"],
}

# segment -> (syl, nas, voice, cont, high, back, round, lat, place)
SEGS = {
    "a": "+ - + + - + - - none", "e": "+ - + + - - - - none", "i": "+ - + + + - - - none",
    "o": "+ - + + - + + - none", "u": "+ - + + + + + - none",
    "p": "- - - - - - - - labial", "t": "- - - - - - - - alveolar", "k": "- - - - - - - - velar",
    "b": "- - + - - - - - labial", "d": "- - + - - - - - alveolar", "g": "- - + - - - - - velar",
    "m": "- + + - - - - - labial", "n": "- + + - - - - - alveolar",
    "s": "- - - + - - - - alveolar", "h": "- - - + - - - - glottal",
    "l": "- - + + - - - + alveolar", "r": "- - + + - - - - alveolar",
    "w": "- - + + + + + - labial", "y": "- - + + + - - - alveolar",
}
VOWELS = "aeiou"
CONS = "ptkbdgmnshlrwy"
ORDER = ["syl", "nas", "voice", "cont", "high", "back", "round", "lat", "place"]


def sym_id(feat, sym):
    names = {"+": "p", "-": "m"}
    return f"f_{feat}_{names.get(sym, sym)}"


def fv(feat, sym):
    return f'<FeatureValue feature="f_{feat}" symbolValues="{sym_id(feat, sym)}" />'


class Grammar:
    def __init__(self, name, poss=("posV",)):
        self.name = name
        self.poss = list(poss)
        self.classes = {}      # id -> {feature: symbol}
        self.phon = []         # (id, xml)
        self.strata = []       # dict(name, mrules=[(id,xml)], templates=[xml], entries=[xml], phon=[ids])
        self.add_class("ncAny", {})
        self.add_class("ncV", {"syl": "+"})
        self.add_class("ncC", {"syl": "-"})
        self.segs = list(SEGS)
        # HCLoader writes a morpheme boundary `+` inside every form-allomorph output (prefix "form+", suffix "+form")
        self.plus = os.environ.get("CALIB_PLUS", "0") != "0"

    # -- phonology -----------------------------------------------------------------------------
    def add_class(self, cid, feats):
        self.classes[cid] = dict(feats)

    def add_phon(self, pid, xml):
        self.phon.append((pid, xml))

    def ctx(self, cid, sid=None):
        idattr = f' id="{sid}"' if sid else ""
        return f'<SimpleContext{idattr} naturalClass="{cid}" />'

    def seg(self, ch, sid=None):
        idattr = f' id="{sid}"' if sid else ""
        return f'<Segment{idattr} segment="c_{ch}" />'

    def env(self, left=None, right=None, initial=False, final=False):
        """left/right: lists of node xml strings."""
        out = "<Environment>"
        if left is not None or initial:
            ib = ' initialBoundaryCondition="true"' if initial else ""
            out += f'<LeftEnvironment><PhoneticTemplate{ib}><PhoneticSequence>{"".join(left or [])}</PhoneticSequence></PhoneticTemplate></LeftEnvironment>'
        if right is not None or final:
            fb = ' finalBoundaryCondition="true"' if final else ""
            out += f'<RightEnvironment><PhoneticTemplate{fb}><PhoneticSequence>{"".join(right or [])}</PhoneticSequence></PhoneticTemplate></RightEnvironment>'
        return out + "</Environment>"

    def rewrite(self, pid, name, inp, out, env=None, order=None):
        """inp/out: lists of node xml (empty list = empty). env: xml from env()."""
        o = f' multipleApplicationOrder="{order}"' if order else ""
        pin = f"<PhoneticInput><PhoneticSequence>{''.join(inp)}</PhoneticSequence></PhoneticInput>" if inp else "<PhoneticInput />"
        pout = f"<PhoneticOutput><PhoneticSequence>{''.join(out)}</PhoneticSequence></PhoneticOutput>" if out else "<PhoneticOutput />"
        xml = (f'<PhonologicalRule id="{pid}"{o}><Name>{name}</Name>{pin}<PhonologicalSubrules><PhonologicalSubrule>'
               f'{pout}{env or ""}</PhonologicalSubrule></PhonologicalSubrules></PhonologicalRule>')
        self.add_phon(pid, xml)

    def metathesis(self, pid, name, nodes, left_id, right_id, order=None):
        o = f' multipleApplicationOrder="{order}"' if order else ""
        xml = (f'<MetathesisRule id="{pid}" leftSwitch="{left_id}" rightSwitch="{right_id}"{o}><Name>{name}</Name>'
               f'<StructuralDescription><PhoneticTemplate><PhoneticSequence>{"".join(nodes)}</PhoneticSequence></PhoneticTemplate>'
               f'</StructuralDescription></MetathesisRule>')
        self.add_phon(pid, xml)

    # -- morphology ----------------------------------------------------------------------------
    @staticmethod
    def seq(pid, kind="one", cls="ncAny"):
        """An input part. kind: one | star (0..inf) | plus (1..inf)."""
        c = f'<SimpleContext naturalClass="{cls}" />'
        if kind == "one":
            return f'<PhoneticSequence id="{pid}">{c}</PhoneticSequence>'
        mn = {"star": 0, "plus": 1}[kind]
        return f'<PhoneticSequence id="{pid}"><OptionalSegmentSequence min="{mn}" max="-1">{c}</OptionalSegmentSequence></PhoneticSequence>'

    @staticmethod
    def copy(pid):
        return f'<CopyFromInput index="{pid}" />'

    @staticmethod
    def ins(shape):
        return f"<InsertSegments><PhoneticShape>{shape}</PhoneticShape></InsertSegments>"

    @staticmethod
    def mod(pid, cls):
        return f'<ModifyFromInput index="{pid}"><SimpleContext naturalClass="{cls}" /></ModifyFromInput>'

    def mrule(self, rid, gloss, subrules, pos="posV", outpos=None, redup=None, mprs=None):
        """subrules: list of (inputs, outputs) where inputs is a list of seq() xml and outputs a list of action xml."""
        subs = ""
        import re
        for n, (inputs, outputs) in enumerate(subrules):
            q = f"{rid}_{n}_"      # XML ids are document-unique: scope each input part to its subrule
            inputs = [re.sub(r'(<PhoneticSequence id=")', r"\1" + q, x) for x in inputs]
            outputs = [re.sub(r'(<(?:CopyFromInput|ModifyFromInput) index=")', r"\1" + q, x) for x in outputs]
            subs += (f'<MorphologicalSubrule id="sub_{rid}_{n}"><MorphologicalInput>{"".join(inputs)}</MorphologicalInput>'
                     f'<MorphologicalOutput>{"".join(outputs)}</MorphologicalOutput></MorphologicalSubrule>')
        op = f' outputPartOfSpeech="{outpos}"' if outpos else ""
        if redup:
            subs = subs.replace("<MorphologicalOutput>", f'<MorphologicalOutput redupMorphType="{redup}">')
        xml = (f'<MorphologicalRule id="{rid}" requiredPartsOfSpeech="{pos}"{op}><Name>{rid}</Name>'
               f'<MorphologicalSubrules>{subs}</MorphologicalSubrules><MorphemeId>{rid}</MorphemeId><Gloss>{gloss}</Gloss></MorphologicalRule>')
        return xml

    def suffix(self, rid, shape, gloss=None, **kw):
        return self.mrule(rid, gloss or rid, [([self.seq("s_" + rid, "plus")], [self.copy("s_" + rid), self.ins("+" + shape if self.plus else shape)])], **kw)

    def prefix(self, rid, shape, gloss=None, **kw):
        return self.mrule(rid, gloss or rid, [([self.seq("s_" + rid, "plus")], [self.ins(shape + "+" if self.plus else shape), self.copy("s_" + rid)])], **kw)

    def entry(self, eid, shape, pos="posV", gloss=None):
        return (f'<LexicalEntry id="e_{eid}" partOfSpeech="{pos}"><Allomorphs><Allomorph id="a_{eid}"><PhoneticShape>{shape}</PhoneticShape>'
                f'</Allomorph></Allomorphs><MorphemeId>{eid}</MorphemeId><Gloss>{gloss or eid}</Gloss></LexicalEntry>')

    def stratum(self, name, mrules=(), templates=(), entries=(), phon=()):
        self.strata.append(dict(name=name, mrules=list(mrules), templates=list(templates), entries=list(entries), phon=list(phon)))

    @staticmethod
    def template(name, slots, pos="posV", final=False):
        """slots: list of (name, [rule ids], optional)."""
        s = "".join(f'<Slot{" optional=\"true\"" if opt else ""} morphologicalRules="{" ".join(ids)}"><Name>{n}</Name></Slot>'
                    for n, ids, opt in slots)
        f = ' final="true"' if final else ""
        return f'<AffixTemplate requiredPartsOfSpeech="{pos}"{f}><Name>{name}</Name>{s}</AffixTemplate>'

    # -- output --------------------------------------------------------------------------------
    def xml(self):
        o = ['<?xml version="1.0" encoding="utf-8"?>', '<!DOCTYPE HermitCrabInput SYSTEM "HermitCrabInput.dtd">',
             "<HermitCrabInput>", "  <Language>", f"    <Name>{escape(self.name)}</Name>"]
        o.append("    <PartsOfSpeech>" + "".join(f'<PartOfSpeech id="{p}"><Name>{p[3:].lower()}</Name></PartOfSpeech>' for p in self.poss) + "</PartsOfSpeech>")
        o.append("    <PhonologicalFeatureSystem>")
        for f, syms in FEATURES.items():
            o.append(f'      <SymbolicFeature id="f_{f}"><Name>{f}</Name><Symbols>' + "".join(
                f'<Symbol id="{sym_id(f, s)}">{s}</Symbol>' for s in syms) + "</Symbols></SymbolicFeature>")
        o.append("    </PhonologicalFeatureSystem>")
        o.append("    <HeadFeatures />")
        o.append('    <CharacterDefinitionTable id="table1"><Name>Main</Name><SegmentDefinitions>')
        for ch in self.segs:
            vals = SEGS[ch].split()
            o.append(f'      <SegmentDefinition id="c_{ch}"><Representations><Representation>{ch}</Representation></Representations>'
                     + "".join(fv(f, v) for f, v in zip(ORDER, vals)) + "</SegmentDefinition>")
        bd = ('<BoundaryDefinitions><BoundaryDefinition id="bPlus"><Representations><Representation>+</Representation>'
              '</Representations></BoundaryDefinition></BoundaryDefinitions>') if self.plus else ""
        o.append("    </SegmentDefinitions>" + bd + "</CharacterDefinitionTable>")
        o.append("    <NaturalClasses>")
        for cid, feats in self.classes.items():
            o.append(f'      <FeatureNaturalClass id="{cid}"><Name>{cid[2:]}</Name>' + "".join(fv(f, s) for f, s in feats.items()) + "</FeatureNaturalClass>")
        o.append("    </NaturalClasses>")
        if self.phon:
            o.append("    <PhonologicalRuleDefinitions>")
            o += ["      " + x for _, x in self.phon]
            o.append("    </PhonologicalRuleDefinitions>")
        o.append("    <Strata>")
        for st in self.strata:
            a = ' characterDefinitionTable="table1" morphologicalRuleOrder="unordered"'
            if st["phon"]:
                a += f' phonologicalRules="{" ".join(st["phon"])}"'
            if st["mrules"]:
                used = " ".join(st["templates"])
                ids = [x.split('id="', 1)[1].split('"', 1)[0] for x in st["mrules"]]
                ids = [i for i in ids if f'"{i}"' not in used and f'"{i} ' not in used and f' {i}"' not in used and f' {i} ' not in used]
                if ids:
                    a += f' morphologicalRules="{" ".join(ids)}"'
            o.append(f"      <Stratum{a}><Name>{st['name']}</Name>")
            if st["mrules"]:
                o.append("        <MorphologicalRuleDefinitions>")
                o += ["          " + x for x in st["mrules"]]
                o.append("        </MorphologicalRuleDefinitions>")
            if st["templates"]:
                o.append("        <AffixTemplates>" + "".join(st["templates"]) + "</AffixTemplates>")
            if st["entries"]:
                o.append("        <LexicalEntries>")
                o += ["          " + x for x in st["entries"]]
                o.append("        </LexicalEntries>")
            o.append("      </Stratum>")
        o.append("    </Strata>")
        o.append("  </Language>")
        o.append("</HermitCrabInput>")
        return "\n".join(o) + "\n"
