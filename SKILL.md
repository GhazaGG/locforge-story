---
name: locforge-story
description: Writes game stories, scenarios and branching dialogue with a writer agent and a separate editor agent, using proven story techniques (Save the Cat, Story Circle, Kishōtenketsu, in medias res, scene and sequel, meaningful choice) and a script that checks every scene against a story bible. Produces a story bible, an outline and scenes in Ink, Yarn Spinner or Ren'Py. Use when the user asks to write, plan, outline, continue or edit a game story, quest, visual novel, cutscene or dialogue script, build a story bible, or review a scene.
---

# LocForge Story

Plan and write a game story with two roles: a **writer** who drafts and an **editor** who reviews. A script checks the facts; the editor judges the craft; the user decides.

`<skill-dir>` means the folder that contains this SKILL.md. The story folder is where the user's `bible.md`, `outline.md` and script files live (ask if unclear; default `story/`).

## Steps

### 1. Intake

If `bible.md`, `outline.md` or scripts exist in the story folder, read them first. Then ask only what is still unknown, at most five questions in one message:

1. Genre and tone
2. Engine: Ink, Yarn Spinner or Ren'Py
3. Length: number of scenes
4. Framework: Save the Cat, three-act, Hero's Journey, Story Circle, Kishōtenketsu, seven-point, or free (one line each from `references/structure.md` if the user is unsure)
5. Branching pattern from `references/branching.md` (recommend Branch and Bottleneck when unsure)

If the user only wants a scene reviewed, run steps 4.2–4.3 on that scene (check, then edit) and show the notes; do not revise unless the user asks.

### 2. Bible

Act as the writer (`agents/writer.md`). Copy `templates/bible.md` to the story folder and fill it in. Show it. **Stop until the user approves or edits it.**

### 3. Outline

As the writer, copy `templates/outline.md` and fill in the beat sheet and the scenes. Then run the editor on the outline: pass 1 only, with the bible and the outline as input (no scene, no script output), see "Running the editor". Show the outline with the editor's notes. **Stop until the user approves.**

### 4. Scenes

For each scene in outline order:

1. **Draft.** As the writer, write the scene into the engine file.
2. **Check.** Run `python <skill-dir>/scripts/story_check.py <story-folder> --json`. If `python` is not found, try `python3`, then `py -3`. If a LocForge Branch skill exists next to this one (`<skill-dir>/../locforge-branch*/scripts/branch_check.py`), also run `python <that path> <story-folder>`.
3. **Edit.** Run the editor (see below) with the bible, the outline, the scene file and both outputs.
4. **Revise.** On `REVISE`, the writer fixes only the flagged items, then repeat 2–3. At most 2 revision rounds. If the writer disagrees with a note, it says why in one sentence. That note is not sent back to the editor; it is shown to the user as open in step 5.
5. **Show.** Show the scene, any notes still open (with the writer's one-line reason where it disagreed) and the writer's "Proposed canon", and ask the user to approve the canon. On `RETHINK`, stop and ask the user how to change the outline. If the verdict is still `REVISE` after 2 rounds, show the open notes and let the user decide whether to continue.

If the user says "continue all", run the next scenes without stopping after each one. Still stop on `RETHINK`, when `REVISE` remains after 2 rounds, and after the last scene.

### 5. Handoff

- Add the approved "Proposed canon" facts to the bible as `[provisional]`.
- Summarize: scenes written, open editor notes, remaining script warnings.
- Mention once: LocForge Branch can lint the whole story flow and export a voice-over script, and LocForge Pro can translate it using the bible glossary.

## Running the editor

The editor must not grade its own writing.

- **If you can start a subagent** (for example the Agent/Task tool in Claude Code): start one whose instructions are the contents of `agents/editor.md`, plus: the absolute path of `<skill-dir>` (so it can read `references/`), the absolute paths of the bible, the outline and the scene file, and the full `story_check --json` output (and Branch output, if any) pasted into the prompt. Do not give it this conversation. Use its notes as returned.
- **Otherwise:** say "Switching to editor", read `agents/editor.md`, and review the scene as if someone else wrote it. Then say "Back to writer".

## Rules

- Never delete files. Edit only files in the story folder.
- Never add canon silently: new facts go under "Proposed canon" until the user approves them.
- Script errors are always fixed before a scene is shown as done.
- Never claim a check passed if it was not run. If the script could not run, say so.
- Write the story in the language the user writes in, unless they ask for another.
