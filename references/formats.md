# Writing scripts that story_check can read

Scene ids in `outline.md` must match the scene names in the script exactly.

## Ink (.ink)

- Scene: a knot, `=== s01 ===`. Stitches (`= name`) belong to their knot.
- Dialogue: `Name: text` at the start of the line. Choices and gathers may come first: `* Mira: Keep it.` / `- Iona: Fine.`
- Narration: any other text line.
- Choices: `* [Choice text] -> target` or `* [Choice text]` followed by an indented block.
- Tags on their own line: `// setup: lens` and `// payoff: lens` (several tags: `// setup: lens, storm`).
- Lines starting with `~` or `{`, and function bodies, are code: skipped and counted as unchecked.
- End every ending with `-> END`.

## Yarn Spinner (.yarn)

- Scene: a node. The header has `title: s01`, then `---`, then the body, then `===`.
- Dialogue: `Name: text`. Options: `-> Option text` or `-> Name: text`.
- Commands (`<<set>>`, `<<jump>>`, `<<if>>`) are flow, not text. Line tags (`#line:abc`) are ignored.
- Tags on their own line: `// setup: lens` / `// payoff: lens`.

## Ren'Py (.rpy)

- Scene: `label s01:`. Local labels (`label .part:`) stay in their parent scene.
- Characters: `define m = Character("Mira")`. The display name ("Mira") must be a bible name, id or alias. `Character(None, ...)` is a narrator.
- Dialogue: `m "text"` or `"Mira" "text"`. Narration: `"text"`. Menu choices: `"Choice text":`.
- Tags on their own line: `# setup: lens` / `# payoff: lens`.
- `$` lines and `python:` blocks are code: skipped and counted as unchecked.

## Do not

- Write narration as `Word: text`. It is read as a speaker called "Word".
- Put a tag comment at the end of a dialogue line. Tags must be on their own line.
- Start narration with up to three words and a colon: anything of that shape before `: ` is read as a speaker.
- In Ink, expect ` #` and ` ->` to end a line's text; anything after them is not checked.
- In the bible, ` #` starts a comment; do not use it inside a value.
- Use `Character("[pname]")` in Ren'Py without adding `[pname]` as an alias of that character in the bible.
- Use single-quoted say lines in Ren'Py; they are not read (use double quotes).
