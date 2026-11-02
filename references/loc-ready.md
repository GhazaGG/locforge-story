# Localization-ready writing

Write so the script can be translated without rework. The editor runs this as a final pass.

- [ ] Idioms and wordplay get a translator note in a comment.
- [ ] No string concatenation (`"You got " + item`). Use one full line with a named placeholder, such as `You got {item}.`
- [ ] Mark gender and plural for the player and NPCs when the line depends on them.
- [ ] Respect `max_line` (dialog box) and about 42 characters x 2 lines for subtitles.
- [ ] Names and terms live in the bible glossary. LocForge Pro can use it as a glossary.
- [ ] No text inside images.
- [ ] No sentence fragments that are assembled at runtime.
- [ ] Leave room: many languages run 20-35% longer than English.
