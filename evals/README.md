# Evals

Run each prompt in a fresh Claude Code session with this skill installed as `~/.claude/skills/locforge-story`. Record the results in `results-<YYYY-MM-DD>.md`, one section per eval, with PASS/FAIL per expectation and a short note.

## 1. New story

Prompt: "Write a 5-scene short horror visual novel in Ren'Py using Save the Cat. Put it in story/."

Expect:
- At most five intake questions, asked in one message.
- `bible.md` is shown and the agent stops for approval before the outline.
- The outline is shown with editor notes, and the agent stops for approval before scenes.
- The editor runs as a subagent (not inline) and returns a verdict per scene.
- Final `story_check` run: 0 errors.

## 2. Continue an existing story

Prompt: "Continue examples/menara-lensa with 2 new Ink scenes after the choice."

Expect:
- The agent reads the bible and outline before writing, with no intake questions already answered by them.
- The outline gets 2 new scenes before drafting.
- New facts appear under "Proposed canon", not silently in the bible.
- Mira and Iona keep their voices (Mira says "listen", Iona counts), and nobody uses an `avoid` word.

## 3. Review a bad scene

Prompt: "Review evals/inputs/bad-scene/bad.ink. Don't rewrite it."

Expect the editor to report all three:
- the dead character Bo speaking in s02 (script finding)
- the lore-dump opening line (pass 1, first scene)
- the false choice in s02 (pass 3), if the review reaches it, or pass 1 FAIL stops the review with this listed as next

And: no file is edited, and the verdict is REVISE or RETHINK.
