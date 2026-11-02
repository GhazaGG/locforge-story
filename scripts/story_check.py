#!/usr/bin/env python3
"""LocForge Story checker: compares Ink, Yarn Spinner and Ren'Py scripts with a story bible and outline.

Usage: python story_check.py <story-folder-or-files...> [--bible PATH] [--outline PATH] [--json]

Prints findings grouped by severity, one per line: <file>:<line>  [<check>]  <message>,
then voice stats per character. Exit code 1 if any finding is an error.
Python 3.9+ standard library only.
"""
import argparse
import collections
import json
import os
import re
import sys

Finding = collections.namedtuple("Finding", "severity check file line message")
Line = collections.namedtuple("Line", "file line scene speaker text")
Tag = collections.namedtuple("Tag", "file line kind name")

SEVERITIES = ("error", "warning", "info")
EXTS = (".ink", ".yarn", ".rpy")
DEFAULT_MAX_LINE = 120


class Script:
    def __init__(self, path):
        self.path = path
        self.scenes = []  # (scene_id, line)
        self.lines = []  # Line
        self.tags = []  # Tag
        self.unchecked = 0


def read_text(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def _csv(value):
    return [x.strip() for x in value.split(",") if x.strip()]


def _int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


# --- bible and outline -------------------------------------------------------

H2 = re.compile(r"^##\s+(.+?)\s*$")
H3 = re.compile(r"^###\s+(.+?)\s*$")
KV = re.compile(r"^\s*[-*]\s+([A-Za-z_]+)\s*:\s*(.*?)\s*$")


def _value(raw):
    return re.sub(r"\s+#.*$", "", raw).strip()


def parse_bible(text):
    bible = {"settings": {}, "characters": [], "glossary": [], "mysteries": []}
    section, entry = None, None
    for n, raw in enumerate(text.splitlines(), 1):
        m = H3.match(raw)
        if m:
            name = m.group(1)
            entry = None
            if section == "characters":
                entry = {"name": name, "id": name.lower(), "aliases": [], "status": "alive",
                         "dies_in": None, "avoid": [], "max_line": None, "line": n}
                bible["characters"].append(entry)
            elif section == "glossary":
                entry = {"term": name, "avoid": [], "line": n}
                bible["glossary"].append(entry)
            elif section == "mysteries":
                entry = {"question": name, "answer": "", "line": n}
                bible["mysteries"].append(entry)
            continue
        m = H2.match(raw)
        if m:
            section, entry = m.group(1).lower(), None
            continue
        m = KV.match(raw)
        if not m:
            continue
        key, val = m.group(1).lower(), _value(m.group(2))
        if section == "settings" and entry is None:
            bible["settings"][key] = val
        elif section == "characters" and entry is not None:
            if key in ("aliases", "avoid"):
                entry[key] = _csv(val)
            elif key == "max_line":
                entry[key] = _int(val)
            elif key in ("id", "status"):
                entry[key] = val.lower()
            elif key == "dies_in":
                entry[key] = val or None
        elif section == "glossary" and entry is not None and key == "avoid":
            entry["avoid"] = _csv(val)
        elif section == "mysteries" and entry is not None and key == "answer":
            entry["answer"] = val
    return bible


OUTLINE_SCENE = re.compile(r"^###\s+(\S+)")


def parse_outline(text):
    scenes, current = [], None
    for n, raw in enumerate(text.splitlines(), 1):
        m = OUTLINE_SCENE.match(raw)
        if m:
            current = {"id": m.group(1), "line": n, "chars": [], "setup": [], "payoff": []}
            scenes.append(current)
            continue
        if raw.startswith("#"):
            current = None
            continue
        m = KV.match(raw)
        if current is not None and m and m.group(1).lower() in ("chars", "setup", "payoff"):
            current[m.group(1).lower()] = _csv(_value(m.group(2)))
    return scenes


# --- script loaders ----------------------------------------------------------

TAG_SLASH = re.compile(r"^//\s*(setup|payoff)\s*:\s*(.+?)\s*$", re.I)
TAG_HASH = re.compile(r"^#\s*(setup|payoff)\s*:\s*(.+?)\s*$", re.I)
SPEAKER = re.compile(r"^([^\s:{}\[\]<>\"][^:{}\[\]<>\"]{0,40}?)\s*:\s+(\S.*)$")


def _add_tags(script, n, m):
    for name in _csv(m.group(2)):
        script.tags.append(Tag(script.path, n, m.group(1).lower(), name.lower()))


def _add_line(script, n, scene, speaker, text):
    text = text.strip()
    if text:
        script.lines.append(Line(script.path, n, scene, speaker, text))


def _add_text(script, n, scene, text):
    m = SPEAKER.match(text)
    if m and len(m.group(1).split()) <= 3:
        _add_line(script, n, scene, m.group(1).strip(), m.group(2))
    else:
        _add_line(script, n, scene, None, text)


INK_KNOT = re.compile(r"^={2,}\s*(function\s+)?(\w+)")
INK_STITCH = re.compile(r"^=\s*\w+\s*$")
INK_SKIP = re.compile(r"^(?:VAR|CONST|INCLUDE|EXTERNAL|LIST|TODO)\b|^->|^<-")
INK_MARKERS = re.compile(r"^(?:(?:[*+]|-(?!>))\s*)+(?:\(\w+\)\s*)?")


def load_ink(path, text):
    s = Script(path)
    scene, in_func, in_block = None, False, False
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if in_block:
            in_block = "*/" not in line
            continue
        if line.startswith("/*"):
            in_block = "*/" not in line
            continue
        m = TAG_SLASH.match(line)
        if m:
            _add_tags(s, n, m)
            continue
        if not line or line.startswith("//"):
            continue
        m = INK_KNOT.match(line)
        if m:
            in_func = bool(m.group(1))
            scene = None if in_func else m.group(2)
            if scene:
                s.scenes.append((scene, n))
            continue
        if INK_STITCH.match(line):
            continue
        if in_func or line.startswith("~") or line.startswith("{"):
            s.unchecked += 1
            continue
        if INK_SKIP.match(line):
            continue
        body = INK_MARKERS.sub("", line)
        body = re.sub(r"\s*//.*$", "", body)
        body = re.sub(r"\s*->.*$", "", body)
        body = re.sub(r"\s#.*$", "", body)
        body = body.replace("[", "").replace("]", "")
        _add_text(s, n, scene, body)
    return s


def load_yarn(path, text):
    s = Script(path)
    scene, in_body = None, False
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not in_body:
            if line == "---":
                in_body = True
                continue
            m = re.match(r"^title\s*:\s*(\S+)", line, re.I)
            if m:
                scene = m.group(1)
                s.scenes.append((scene, n))
            continue
        if line == "===":
            in_body, scene = False, None
            continue
        m = TAG_SLASH.match(line)
        if m:
            _add_tags(s, n, m)
            continue
        if not line or line.startswith("//") or re.match(r"^<<.*>>$", line):
            continue
        body = re.sub(r"^->\s*", "", line)
        body = re.sub(r"<<.*?>>", "", body)
        body = re.sub(r"\s*//.*$", "", body)
        body = re.sub(r"(^|\s)#\S+", "", body)
        _add_text(s, n, scene, body)
    return s


RPY_CHAR = re.compile(r"""^define\s+(\w+)\s*=\s*Character\(\s*(?:_\(\s*)?(["'])(.*?)\2""")
RPY_CHAR_NONE = re.compile(r"^define\s+(\w+)\s*=\s*Character\(\s*None\b")
RPY_LABEL = re.compile(r"^label\s+([\w.]+)\s*(?:\(.*\))?\s*:")
RPY_PY = re.compile(r"^(?:init\s+)?(?:-?\d+\s+)?python\b.*:\s*$")
STR = r'"((?:[^"\\]|\\.)*)"'
RPY_NAMED = re.compile(r"^" + STR + r"\s+" + STR)
RPY_SAY = re.compile(r"^(\w+)(?:\s+[\w@.]+)*\s+" + STR)
RPY_UI = re.compile(r"^(?:screen|style|transform)\b.*:\s*$")
RPY_CHOICE = re.compile(r"^" + STR + r"\s*(?:if\s.*)?:\s*$")
RPY_NARR = re.compile(r"^" + STR + r"\s*(?:with\s.*|nointeract)?$")
RPY_NARRATOR = {"narrator", "centered", "extend", "nvl"}
RPY_KEYWORDS = {"show", "scene", "hide", "play", "stop", "queue", "voice", "jump", "call", "return",
                "with", "pause", "image", "define", "default", "label", "menu", "if", "elif", "else",
                "while", "python", "init", "transform", "screen", "style", "translate", "window",
                "camera", "at", "renpy"}


def renpy_characters(texts):
    who = {}
    for text in texts:
        for raw in text.splitlines():
            line = raw.strip()
            m = RPY_CHAR.match(line)
            if m:
                who[m.group(1)] = m.group(3)
            elif RPY_CHAR_NONE.match(line):
                who[RPY_CHAR_NONE.match(line).group(1)] = None
    return who


def _rpy_text(text):
    return re.sub(r"\{[^{}]*\}", "", text.replace('\\"', '"'))


def load_renpy(path, text, who):
    s = Script(path)
    scene, skip_indent, skip_counts = None, None, True
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        indent = len(raw) - len(raw.lstrip())
        if skip_indent is not None:
            if line and indent <= skip_indent:
                skip_indent = None
            else:
                if skip_counts:
                    s.unchecked += bool(line)
                continue
        m = TAG_HASH.match(line)
        if m:
            _add_tags(s, n, m)
            continue
        if not line or line.startswith("#") or line.startswith("define "):
            continue
        if RPY_PY.match(line):
            skip_indent, skip_counts = indent, True
            continue
        if RPY_UI.match(line):
            skip_indent, skip_counts = indent, False
            continue
        if line.startswith("$"):
            s.unchecked += 1
            continue
        m = RPY_LABEL.match(line)
        if m:
            if not m.group(1).startswith("."):
                scene = m.group(1)
                s.scenes.append((scene, n))
            continue
        m = RPY_NAMED.match(line)
        if m:
            _add_line(s, n, scene, m.group(1), _rpy_text(m.group(2)))
            continue
        m = RPY_SAY.match(line)
        if m and m.group(1) not in RPY_KEYWORDS:
            var = m.group(1)
            speaker = None if var in RPY_NARRATOR or (var in who and who[var] is None) else who.get(var, var)
            _add_line(s, n, scene, speaker, _rpy_text(m.group(2)))
            continue
        m = RPY_CHOICE.match(line) or RPY_NARR.match(line)
        if m:
            _add_line(s, n, scene, None, _rpy_text(m.group(1)))
    return s


def load_script(path, text, who):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".ink":
        return load_ink(path, text)
    if ext == ".yarn":
        return load_yarn(path, text)
    return load_renpy(path, text, who)


# --- checks ------------------------------------------------------------------

def _index(bible):
    index = {}
    for c in (bible or {}).get("characters", []):
        for key in [c["id"], c["name"]] + c["aliases"]:
            index[key.lower()] = c
    return index


def _word(phrase):
    return re.compile(r"(?<!\w)%s(?!\w)" % re.escape(phrase), re.I)


def check(bible, bible_path, outline, outline_path, scripts):
    out = []

    def add(severity, name, path, line, message):
        out.append(Finding(severity, name, path, line, message))

    index = _index(bible)
    max_line = _int((bible or {}).get("settings", {}).get("max_line")) or DEFAULT_MAX_LINE
    order = {sc["id"]: i for i, sc in enumerate(outline or [])}
    cast = {sc["id"]: {index[x.lower()]["id"] if x.lower() in index else x.lower() for x in sc["chars"]}
            for sc in outline or []}
    terms = [(g["term"], a, _word(a)) for g in (bible or {}).get("glossary", []) for a in g["avoid"]]
    avoid = {c["id"]: [(a, _word(a)) for a in c["avoid"]] for c in (bible or {}).get("characters", [])}

    for s in scripts:
        if s.unchecked:
            add("info", "unchecked", s.path, 0, "%d line(s) of code or logic were not checked." % s.unchecked)
        for ln in s.lines:
            char = index.get(ln.speaker.lower()) if ln.speaker else None
            if ln.speaker and bible is not None and char is None:
                add("error", "unknown-speaker", ln.file, ln.line,
                    "Speaker '%s' is not in the bible (name, id or alias)." % ln.speaker)
            limit = (char and char["max_line"]) or max_line
            if len(ln.text) > limit:
                add("warning", "long-line", ln.file, ln.line,
                    "Line is %d characters; the limit is %d." % (len(ln.text), limit))
            for term, wrong, rx in terms:
                if rx.search(ln.text):
                    add("warning", "term-variant", ln.file, ln.line,
                        "'%s' is a wrong spelling of '%s'." % (wrong, term))
            if char is None:
                continue
            for phrase, rx in avoid[char["id"]]:
                if rx.search(ln.text):
                    add("warning", "avoid-word", ln.file, ln.line,
                        "%s never says '%s' (bible: avoid)." % (char["name"], phrase))
            dies = char["dies_in"]
            if dies in order and ln.scene in order and order[ln.scene] > order[dies]:
                add("warning", "dead-speaker", ln.file, ln.line,
                    "%s dies in %s but speaks in %s." % (char["name"], dies, ln.scene))
            if cast.get(ln.scene) and char["id"] not in cast[ln.scene]:
                add("info", "uninvited-speaker", ln.file, ln.line,
                    "%s speaks in %s but is not in its outline chars." % (char["name"], ln.scene))

    if outline is not None and scripts:
        found = {}
        for s in scripts:
            for sid, n in s.scenes:
                found.setdefault(sid, (s.path, n))
        for sc in outline:
            if sc["id"] not in found:
                add("warning", "missing-scene", outline_path, sc["line"],
                    "Outline scene '%s' has no matching knot, node or label." % sc["id"])
        for sid, (path, n) in found.items():
            if sid not in order:
                add("info", "unplanned-scene", path, n, "Scene '%s' is not in the outline." % sid)

    setups, payoffs = {}, {}
    for s in scripts:
        for t in s.tags:
            (setups if t.kind == "setup" else payoffs).setdefault(t.name, t)
    for name, t in setups.items():
        if name not in payoffs:
            add("warning", "setup-no-payoff", t.file, t.line, "Setup '%s' is never paid off." % name)
    for name, t in payoffs.items():
        if name not in setups:
            add("warning", "payoff-no-setup", t.file, t.line, "Payoff '%s' has no setup." % name)

    for m in (bible or {}).get("mysteries", []):
        if not m["answer"]:
            add("warning", "mystery-no-answer", bible_path, m["line"],
                "Mystery '%s' has no answer." % m["question"])
    return out


def voice_stats(bible, scripts):
    index, acc = _index(bible), {}
    for s in scripts:
        for ln in s.lines:
            if not ln.speaker:
                continue
            c = index.get(ln.speaker.lower())
            a = acc.setdefault(c["name"] if c else ln.speaker,
                               {"lines": 0, "words": 0, "counter": collections.Counter()})
            words = re.findall(r"\w+", ln.text.lower())
            a["lines"] += 1
            a["words"] += len(words)
            a["counter"].update(w for w in words if len(w) >= 4 and not w.isdigit())
    return {name: {"lines": a["lines"], "words_per_line": round(a["words"] / a["lines"], 1),
                   "top_words": [w for w, _ in a["counter"].most_common(5)]}
            for name, a in sorted(acc.items())}


# --- running -----------------------------------------------------------------

def discover(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs.sort()
                files += [os.path.join(root, n) for n in sorted(names) if n.lower().endswith(EXTS)]
        else:
            files.append(p)
    return files


def _read(path, findings):
    try:
        return read_text(path)
    except (OSError, UnicodeDecodeError) as e:
        findings.append(Finding("error", "parse", path, 0, "Cannot read file: %s" % e))
        return None


def run(paths, bible_path=None, outline_path=None):
    findings = []
    base = paths[0] if os.path.isdir(paths[0]) else (os.path.dirname(paths[0]) or ".")
    loaded = {}
    for kind, path, parse in (("bible", bible_path, parse_bible), ("outline", outline_path, parse_outline)):
        if path is None and os.path.isfile(os.path.join(base, kind + ".md")):
            path = os.path.join(base, kind + ".md")
        loaded[kind] = (path, None)
        if path is None:
            findings.append(Finding("info", "no-" + kind, base, 0,
                                    "No %s.md found; checks that need it were skipped." % kind))
            continue
        text = _read(path, findings)
        loaded[kind] = (path, parse(text) if text is not None else None)

    texts = []
    for f in discover(paths):
        if not f.lower().endswith(EXTS):
            findings.append(Finding("error", "parse", f, 0, "Unsupported file type (use .ink, .yarn or .rpy)."))
            continue
        text = _read(f, findings)
        if text is not None:
            texts.append((f, text))
    who = renpy_characters(t for f, t in texts if f.lower().endswith(".rpy"))
    scripts = [load_script(f, t, who) for f, t in texts]

    (bpath, bible), (opath, outline) = loaded["bible"], loaded["outline"]
    findings += check(bible, bpath, outline, opath, scripts)
    return findings, voice_stats(bible, scripts)


def format_text(findings, stats):
    out = []
    for sev in SEVERITIES:
        group = sorted((f for f in findings if f.severity == sev), key=lambda f: (f.file, f.line, f.check))
        if group:
            out.append("%s (%d)" % (sev.upper(), len(group)))
            out += ["  %s:%d  [%s]  %s" % (f.file, f.line, f.check, f.message) for f in group]
    if not findings:
        out.append("No findings.")
    if stats:
        out.append("VOICE")
        for name, st in stats.items():
            out.append("  %s: %d lines, %.1f words/line, top: %s"
                       % (name, st["lines"], st["words_per_line"], ", ".join(st["top_words"]) or "-"))
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(description="Check game story scripts against a story bible and outline.")
    p.add_argument("paths", nargs="+", help="story folder(s) or .ink / .yarn / .rpy files")
    p.add_argument("--bible", help="bible file (default: bible.md in the first folder)")
    p.add_argument("--outline", help="outline file (default: outline.md in the first folder)")
    p.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = p.parse_args(argv)
    findings, stats = run(args.paths, args.bible, args.outline)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.json:
        print(json.dumps({"findings": [f._asdict() for f in findings], "stats": stats},
                         ensure_ascii=False, indent=2))
    else:
        print(format_text(findings, stats))
    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
