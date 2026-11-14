"""Small XML writer shared by the calibration generators of batch A.

Every construct it can emit is one the stress or edge-case fixtures already use and that
fieldworks-writable-shapes.tsv lists as written by HCLoader.cs; the callers name the loader function.
Standard library only. Output is deterministic: no timestamps, no unordered iteration.
"""
from xml.sax.saxutils import escape

VOWELS = "aeiou"
CONSONANTS = "ptksmnlrbdg"
ANY = '<SimpleContext naturalClass="ncAny" />'


def seg_id(ch):
    return "c_" + ch


def header(name, chars, natural_classes=(), parts_of_speech=(("posN", "noun"),), comment=""):
    out = ['<?xml version="1.0" encoding="utf-8"?>', '<!DOCTYPE HermitCrabInput SYSTEM "HermitCrabInput.dtd">',
           "<HermitCrabInput>", "  <Language>", "    <Name>%s</Name>" % name]
    if comment:
        out.append("    <!--\n%s\n    -->" % comment.replace("--", "- -"))
    out.append("    <PartsOfSpeech>")
    for pid, pname in parts_of_speech:
        out.append('      <PartOfSpeech id="%s"><Name>%s</Name></PartOfSpeech>' % (pid, pname))
    out.append("    </PartsOfSpeech>")
    out.append('    <CharacterDefinitionTable id="table1">')
    out.append("      <Name>Main</Name>")
    out.append("      <SegmentDefinitions>")
    for ch in chars:
        out.append('        <SegmentDefinition id="%s"><Representations><Representation>%s</Representation>'
                   "</Representations></SegmentDefinition>" % (seg_id(ch), escape(ch)))
    out.append("      </SegmentDefinitions>")
    out.append("    </CharacterDefinitionTable>")
    out.append("    <NaturalClasses>")
    out.append('      <FeatureNaturalClass id="ncAny"><Name>Any</Name></FeatureNaturalClass>')
    for cid, members in natural_classes:
        out.append('      <SegmentNaturalClass id="%s"><Name>%s</Name>%s</SegmentNaturalClass>'
                   % (cid, cid, "".join('<Segment segment="%s" />' % seg_id(m) for m in members)))
    out.append("    </NaturalClasses>")
    return out


def pattern(pid, items):
    """items: ('star', nc) zero or more, ('plus', nc) one or more, ('one', nc) exactly one."""
    parts = []
    for kind, nc in items:
        ctx = '<SimpleContext naturalClass="%s" />' % nc
        if kind == "star":
            parts.append('<OptionalSegmentSequence min="0" max="-1">%s</OptionalSegmentSequence>' % ctx)
        elif kind == "plus":
            parts.append('<OptionalSegmentSequence min="1" max="-1">%s</OptionalSegmentSequence>' % ctx)
        else:
            parts.append(ctx)
    return '<PhoneticSequence id="%s">%s</PhoneticSequence>' % (pid, "".join(parts))


def subrule(sid, items, text, prefix=False, env=""):
    """One allomorph of an affix rule: a stem pattern and a prefix or suffix text.

    HCLoader writes the stem-side context of a lone affix into the input pattern (README, "what the XML can
    say"), so conditions go in `items`; `env` is a RequiredEnvironments body, allowed only on a lone prefix
    (left environment) or a lone suffix (right environment): HCLoader.cs LoadFormAffixProcessAllomorph.
    """
    pid = sid + "_s"
    ins = "<InsertSegments><PhoneticShape>%s</PhoneticShape></InsertSegments>" % escape(text) if text else ""
    cp = '<CopyFromInput index="%s" />' % pid
    out = (ins + cp) if prefix else (cp + ins)
    req = "<RequiredEnvironments>%s</RequiredEnvironments>" % env if env else ""
    return ('<MorphologicalSubrule id="%s"><MorphologicalInput>%s</MorphologicalInput>'
            "<MorphologicalOutput>%s</MorphologicalOutput>%s</MorphologicalSubrule>" % (sid, pattern(pid, items), out, req))


def rule(rid, morph_id, subrules, pos="posN", out_pos=None, gloss=None):
    """A MorphologicalRule. Slot rules (inflectional, LoadInflAffixProcessRule) carry no outputPartOfSpeech;
    unslotted derivational rules do (LoadDerivAffixProcessRule)."""
    attrs = 'id="%s" requiredPartsOfSpeech="%s"' % (rid, pos)
    if out_pos:
        attrs += ' outputPartOfSpeech="%s"' % out_pos
    return ("<MorphologicalRule %s><Name>%s</Name><MorphologicalSubrules>%s</MorphologicalSubrules>"
            "<MorphemeId>%s</MorphemeId><Gloss>%s</Gloss></MorphologicalRule>"
            % (attrs, rid, "".join(subrules), morph_id, gloss or morph_id))


def entry(eid, form, morph_id, pos="posN", extra_allomorphs=""):
    return ('<LexicalEntry id="e_%s" partOfSpeech="%s"><Allomorphs><Allomorph id="a_%s"><PhoneticShape>%s</PhoneticShape>'
            "</Allomorph>%s</Allomorphs><MorphemeId>%s</MorphemeId><Gloss>%s</Gloss></LexicalEntry>"
            % (eid, pos, eid, escape(form), extra_allomorphs, morph_id, morph_id))


def template(name, pos, slots):
    """slots: list of (slot name, optional, [rule ids]). HCLoader.cs LoadAffixTemplate."""
    body = "".join('<Slot%s morphologicalRules="%s"><Name>%s</Name></Slot>'
                   % (' optional="true"' if opt else "", " ".join(rids), sname) for sname, opt, rids in slots)
    return '<AffixTemplate requiredPartsOfSpeech="%s"><Name>%s</Name>%s</AffixTemplate>' % (pos, name, body)


def phon_rule(rid, name, src, dst, left=None, right=None, order="leftToRightIterative"):
    """A PhonologicalRule with one subrule (HCLoader.cs LoadRewriteRule / LoadPhonologicalRule, 2052-2146).
    left/right are lists of pattern items ('one', nc) / ('star', nc)."""
    def tmpl(tag, items):
        parts = []
        for kind, nc in items:
            ctx = '<SimpleContext naturalClass="%s" />' % nc
            parts.append('<OptionalSegmentSequence min="0" max="-1">%s</OptionalSegmentSequence>' % ctx
                         if kind == "star" else ctx)
        return "<%s><PhoneticTemplate><PhoneticSequence>%s</PhoneticSequence></PhoneticTemplate></%s>" % (tag, "".join(parts), tag)
    env = ""
    if left or right:
        env = "<Environment>%s%s</Environment>" % (tmpl("LeftEnvironment", left) if left else "",
                                                   tmpl("RightEnvironment", right) if right else "")
    return ('<PhonologicalRule id="%s" multipleApplicationOrder="%s"><Name>%s</Name><PhoneticInput><PhoneticSequence>'
            '<Segment segment="%s" /></PhoneticSequence></PhoneticInput><PhonologicalSubrules><PhonologicalSubrule>'
            '<PhoneticOutput><PhoneticSequence><Segment segment="%s" /></PhoneticSequence></PhoneticOutput>%s'
            "</PhonologicalSubrule></PhonologicalSubrules></PhonologicalRule>"
            % (rid, order, name, seg_id(src), seg_id(dst), env))


def assemble(head, phon_rules, rules, templates, entries, unslotted_ids=(), extra_defs=(), cooccurrence=""):
    """One Main stratum. unslotted_ids are rules the stratum lists in morphologicalRules (derivational and
    compounding rules); slot rules are reached through the templates only."""
    phon_ids = [r.split('id="')[1].split('"')[0] for r in phon_rules]
    attrs = 'characterDefinitionTable="table1" morphologicalRuleOrder="unordered"'
    if phon_ids:
        attrs += ' phonologicalRules="%s"' % " ".join(phon_ids)
    if unslotted_ids:
        attrs += ' morphologicalRules="%s"' % " ".join(unslotted_ids)
    out = list(head)
    if phon_rules:
        out.append("    <PhonologicalRuleDefinitions>")
        out.extend("      " + r for r in phon_rules)
        out.append("    </PhonologicalRuleDefinitions>")
    out.append("    <Strata>")
    out.append("      <Stratum %s>" % attrs)
    out.append("        <Name>Main</Name>")
    out.append("        <MorphologicalRuleDefinitions>")
    out.extend("          " + r for r in list(rules) + list(extra_defs))
    out.append("        </MorphologicalRuleDefinitions>")
    if templates:
        out.append("        <AffixTemplates>")
        out.extend("          " + t for t in templates)
        out.append("        </AffixTemplates>")
    out.append("        <LexicalEntries>")
    out.extend("          " + e for e in entries)
    out.append("        </LexicalEntries>")
    out.append("      </Stratum>")
    out.append("    </Strata>")
    out.append(cooccurrence) if cooccurrence else None
    out.append("  </Language>")
    out.append("</HermitCrabInput>")
    return "\n".join(out) + "\n"
