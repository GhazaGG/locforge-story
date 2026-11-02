"""Run: python tests/test_story_check.py"""
import contextlib
import io
import json
import os
import sys
import tempfile
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import story_check  # noqa: E402

BIBLE = """
# Bible: Test

Free prose is ignored.

## Settings
- max_line: 60  # dialog box

## Characters
### Mira
- aliases: Kapten Mira, Mi
- dies_in: s02
- avoid: oke
### Iona
- max_line: 30

## Glossary
### Aetherium
- avoid: Etherium, Aeterium

## Mysteries
### Who opened the dam?
- answer: Iona
### Where is the key?
"""

OUTLINE = """
# Outline

### s01 Arrival
- chars: Mira, Iona
- setup: lens
### s02 The fall
- chars: Mi
### s03 After
- chars: Iona
"""


def story(files):
    d = tempfile.mkdtemp()
    for name, body in files.items():
        path = os.path.join(d, name)
        if isinstance(body, bytes):
            with open(path, "wb") as f:
                f.write(body)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(textwrap.dedent(body).lstrip())
    return d


def found(d, **kw):
    findings, _ = story_check.run([d], **kw)
    return sorted((f.check, os.path.basename(f.file), f.line) for f in findings)


def names(d, **kw):
    findings, _ = story_check.run([d], **kw)
    return sorted(f.check for f in findings)


# --- Task 1: bible, outline, CLI ---------------------------------------------

def test_parse_bible():
    b = story_check.parse_bible(BIBLE)
    assert b["settings"] == {"max_line": "60"}
    mira, iona = b["characters"]
    assert mira["id"] == "mira" and mira["aliases"] == ["Kapten Mira", "Mi"]
    assert mira["dies_in"] == "s02" and mira["avoid"] == ["oke"] and mira["max_line"] is None
    assert iona["max_line"] == 30 and iona["status"] == "alive"
    assert b["glossary"][0]["avoid"] == ["Etherium", "Aeterium"]
    assert [m["answer"] for m in b["mysteries"]] == ["Iona", ""]


def test_parse_outline():
    o = story_check.parse_outline(OUTLINE)
    assert [s["id"] for s in o] == ["s01", "s02", "s03"]
    assert o[0]["chars"] == ["Mira", "Iona"] and o[0]["setup"] == ["lens"]
    assert o[1]["line"] == 7


def test_missing_bible_and_outline_are_reported():
    assert names(story({})) == ["no-bible", "no-outline"]


def test_mystery_without_answer():
    assert found(story({"bible.md": BIBLE, "outline.md": OUTLINE})) == [("mystery-no-answer", "bible.md", 23)]


def test_unreadable_file_is_parse_error_and_exit_1():
    d = story({"bible.md": BIBLE, "outline.md": "", "a.ink": b"Mira: \xff\n"})
    assert ("parse", "a.ink", 0) in found(d)
    with contextlib.redirect_stdout(io.StringIO()):
        assert story_check.main([d]) == 1


def test_bom_and_json_output():
    d = story({"bible.md": "\ufeff" + BIBLE, "outline.md": OUTLINE})
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        assert story_check.main([d, "--json"]) == 0
    data = json.loads(buf.getvalue())
    assert [f["check"] for f in data["findings"]] == ["mystery-no-answer"]
    assert data["stats"] == {}


# --- Task 2: Ink -------------------------------------------------------------

INK = """
VAR lens = 0
=== s01 ===
Mira: Dengar. The roof needs one clear lens.
Iona: I can fix it.
* [Give the lens] -> s02
* Kapten Mira: Keep it. -> s03
// setup: lens
// setup: storm
~ lens = 1
= stitch
Iona: This line is far too long for the Iona box.
Narration mentions Etherium once.
=== s02 ===
Mi: Oke, I fall now. #sad
Ghost: Boo.
=== s03 ===
- Mira: I should be dead.
// payoff: lens
// payoff: key
=== s04 ===
Iona: Not planned.
=== function helper() ===
~ return 1
"""


def test_ink_findings():
    d = story({"bible.md": BIBLE, "outline.md": OUTLINE, "story.ink": INK})
    assert found(d) == [
        ("avoid-word", "story.ink", 14),
        ("dead-speaker", "story.ink", 17),
        ("long-line", "story.ink", 11),
        ("mystery-no-answer", "bible.md", 23),
        ("payoff-no-setup", "story.ink", 19),
        ("setup-no-payoff", "story.ink", 8),
        ("term-variant", "story.ink", 12),
        ("unchecked", "story.ink", 0),
        ("uninvited-speaker", "story.ink", 17),
        ("unknown-speaker", "story.ink", 15),
        ("unplanned-scene", "story.ink", 20),
    ]


def test_ink_lines_and_scenes():
    s = story_check.load_ink("x.ink", textwrap.dedent(INK).lstrip())
    assert [sid for sid, _ in s.scenes] == ["s01", "s02", "s03", "s04"]
    first = s.lines[:4]
    assert [(ln.speaker, ln.text) for ln in first] == [
        ("Mira", "Dengar. The roof needs one clear lens."),
        ("Iona", "I can fix it."),
        (None, "Give the lens"),
        ("Kapten Mira", "Keep it."),
    ]
    assert s.unchecked == 2


def test_missing_scene_and_voice_stats():
    ink = "=== s01 ===\nMira: Dengar dengar lensa.\nMi: Lensa retak.\n"
    d = story({"bible.md": BIBLE, "outline.md": OUTLINE, "a.ink": ink})
    assert ("missing-scene", "outline.md", 6) in found(d)
    assert ("missing-scene", "outline.md", 8) in found(d)
    _, stats = story_check.run([d])
    assert stats == {"Mira": {"lines": 2, "words_per_line": 2.5, "top_words": ["dengar", "lensa", "retak"]}}


def test_no_bible_skips_speaker_checks():
    d = story({"a.ink": "=== s01 ===\nAnyone: Hello there.\n"})
    assert names(d) == ["no-bible", "no-outline"]


# --- Task 3: Yarn ------------------------------------------------------------

YARN = """
title: s01
tags: intro
position: 0,0
---
Mira: Dengar. #line:a1
-> Give the lens
    <<jump s02>>
-> Mira: Keep it.
// setup: lens
<<set $lens to 1>>
Stranger: Who are you?
===
title: s02
---
Mi: I fall.
===
"""


def test_yarn_findings():
    d = story({"bible.md": BIBLE, "outline.md": OUTLINE, "story.yarn": YARN})
    assert found(d) == [
        ("missing-scene", "outline.md", 8),
        ("mystery-no-answer", "bible.md", 23),
        ("setup-no-payoff", "story.yarn", 9),
        ("unknown-speaker", "story.yarn", 11),
    ]
    s = story_check.load_yarn("x.yarn", textwrap.dedent(YARN).lstrip())
    assert [sid for sid, _ in s.scenes] == ["s01", "s02"]
    assert [(ln.speaker, ln.text) for ln in s.lines[:3]] == [
        ("Mira", "Dengar."), (None, "Give the lens"), ("Mira", "Keep it.")]


# --- Task 4: Ren'Py ----------------------------------------------------------

RPY_CHARS = """
define m = Character("Mira", color="#c8ffc8")
define i = Character(_("Iona"))
define n = Character(None, kind=nvl)
"""

RPY = """
label s01:
    m "Dengar. The roof needs a lens."
    n "The wind rises."
    "Iona" "I can fix it."
    "A plain narration line."
    x "Who am I?"
    play music "storm.ogg"
    $ lens = 1
    python:
        a = 1
        b = 2
    # setup: lens
    menu:
        "Give the lens":
            jump s02
label .inner:
    i "Still s01{w} here."
label s02:
    m "Oke."
"""


def test_renpy_findings():
    d = story({"bible.md": BIBLE, "outline.md": OUTLINE, "chars.rpy": RPY_CHARS, "script.rpy": RPY})
    assert found(d) == [
        ("avoid-word", "script.rpy", 19),
        ("missing-scene", "outline.md", 8),
        ("mystery-no-answer", "bible.md", 23),
        ("setup-no-payoff", "script.rpy", 12),
        ("unchecked", "script.rpy", 0),
        ("unknown-speaker", "script.rpy", 6),
    ]
    who = story_check.renpy_characters([RPY_CHARS])
    assert who == {"m": "Mira", "i": "Iona", "n": None}
    s = story_check.load_renpy("x.rpy", textwrap.dedent(RPY).lstrip(), who)
    assert [sid for sid, _ in s.scenes] == ["s01", "s02"]
    assert s.unchecked == 3
    assert [(ln.speaker, ln.text, ln.scene) for ln in s.lines] == [
        ("Mira", "Dengar. The roof needs a lens.", "s01"),
        (None, "The wind rises.", "s01"),
        ("Iona", "I can fix it.", "s01"),
        (None, "A plain narration line.", "s01"),
        ("x", "Who am I?", "s01"),
        (None, "Give the lens", "s01"),
        ("Iona", "Still s01 here.", "s01"),
        ("Mira", "Oke.", "s02"),
    ]


# --- Task 4 fix: attributes and screen/style/transform bodies ---------------

RPY_SCREENS = """
define m = Character("Mira")
label s01:
    m happy "Hello there."
    m happy at left "Again."
screen main_menu():
    text "Hello"
    textbutton "Start" action Start()
style say_label:
    color "#fff"
"""


def test_renpy_attributes_and_screens():
    d = story({"bible.md": BIBLE, "outline.md": OUTLINE, "script.rpy": RPY_SCREENS})
    who = story_check.renpy_characters([RPY_SCREENS])
    assert who == {"m": "Mira"}
    s = story_check.load_renpy("x.rpy", textwrap.dedent(RPY_SCREENS).lstrip(), who)
    assert [(ln.speaker, ln.text) for ln in s.lines] == [("Mira", "Hello there."), ("Mira", "Again.")]
    assert s.unchecked == 0
    assert "unknown-speaker" not in names(d)


INK_EDGE = """# title: Menara
/* Iona: block
   Mira: comment */
// setup: a, b
=== s01 ===
{ met_iona:
    Iona: Again?
- else:
    Iona: Who are you?
}
{
- met_iona: Iona: Back so soon?
- else: Iona: Hello.
}
{ visits:
- 0: Mira: First time.
}
* [Agree] Mira: Fine.
* [Give the lens] -> s02
Mira: Hi.
"""


def test_ink_global_tags_conditionals_and_choice_prefix():
    s = story_check.load_ink("x.ink", INK_EDGE)
    assert [(ln.speaker, ln.text) for ln in s.lines] == [
        ("Mira", "Fine."), (None, "Give the lens"), ("Mira", "Hi.")]
    assert s.unchecked == 12
    assert [t.name for t in s.tags] == ["a", "b"]


RPY_TRANSLATE = """translate french strings:
    old "Start"
    new "Commencer"
translate french start_a1b2:
    m "Bonjour."
label start:
    m "Hello."
"""


def test_renpy_translate_blocks_skipped():
    s = story_check.load_renpy("x.rpy", RPY_TRANSLATE, {"m": "Mira"})
    assert [(ln.speaker, ln.text) for ln in s.lines] == [("Mira", "Hello.")]
    assert s.unchecked == 0


# --- Task 5: example and templates -------------------------------------------

ROOT = os.path.join(HERE, "..")


def test_example_story_is_clean():
    findings, stats = story_check.run([os.path.join(ROOT, "examples", "menara-lensa")])
    assert findings == [], story_check.format_text(findings, stats)
    assert sorted(stats) == ["Iona", "Mira"]


def test_templates_parse():
    with open(os.path.join(ROOT, "templates", "bible.md"), encoding="utf-8") as f:
        b = story_check.parse_bible(f.read())
    assert b["settings"]["max_line"] == "120" and len(b["characters"]) == 2
    with open(os.path.join(ROOT, "templates", "outline.md"), encoding="utf-8") as f:
        assert [s["id"] for s in story_check.parse_outline(f.read())] == ["s01", "s02"]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print("%d tests passed" % len(tests))
