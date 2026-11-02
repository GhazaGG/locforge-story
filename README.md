# LocForge Story

An open-source agent skill for writing game stories, scenarios and dialogue.

A **writer** agent drafts your story bible, outline and scenes straight into **Ink, Yarn Spinner or Ren'Py**. A separate **editor** agent reviews each scene against proven story techniques. A script checks every scene against your bible: unknown speakers, dead characters who talk, setups without payoffs, wrong term spellings, lines too long for the dialog box, and critical beats carried only by optional channels.

## What you get

- **Story bible** template: characters (want, need, lie, voice, words they never say), glossary, canon status, and mysteries with their true answers
- **Outline**: a beat sheet for the framework you pick, and scenes with goal, conflict, outcome and value shift
- **Delivery map**: for each scene, how it reaches the player (dialogue, cutscene, narration, quest, objects, barks, mechanics or UI), so no critical beat hides in an optional note
- **Scenes** in your engine's format, revised until the editor accepts them or two rounds pass
- **story_check.py**: Python 3.9+, no dependencies

## Techniques

Save the Cat, three-act, Hero's Journey, Story Circle, Kishōtenketsu, seven-point, MICE, Fichtean curve · in medias res, cold open, iceberg, mystery box, setup and payoff · scene and sequel, value shift, enter late and leave early, try-fail · want/need/lie, voice profiles, subtext, barks, VO and subtitle limits · Ashwell's branching patterns, meaningful choice, delayed consequence, storylets, ludonarrative harmony · delivery channels and environmental storytelling · localization-ready writing.

## Install

Copy this folder (or the release zip) to your agent's skills folder:

| Agent | Folder |
|---|---|
| Claude Code | `~/.claude/skills/locforge-story/` |
| Cursor, Codex CLI, Gemini CLI | the agent's skills or rules folder; point it at `SKILL.md` |

Then ask: *"Write a short visual novel in Ren'Py about a lighthouse keeper, five scenes, Save the Cat."*

## Check a story by hand

    python scripts/story_check.py examples/menara-lensa

```
No findings.
VOICE
  Iona: 7 lines, 10.6 words/line, top: your, lens, only, then, forty
  Mira: 6 lines, 7.5 words/line, top: tower, listen, wrong, this, count
```

Add `--json` for machine-readable output. The exit code is 1 when there is an error.

## Part of the LocForge family

- **LocForge Branch**: lints the whole story flow (broken jumps, dead ends, unreachable scenes) and exports a voice-over script. Story runs it automatically when it is installed next to this skill.
- **LocForge Pro**: translates game dialogue and UI with character voices and your glossary intact.

## License

MIT
