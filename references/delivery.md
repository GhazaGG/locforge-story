# Delivery: how each beat reaches the player

Use this after the outline is approved, to decide for every scene how its beat reaches the player, and when reviewing that delivery map.

## Channels

Use these ids in the outline (`channel`, `support`) and in `channel:` tags.

| Id | Channel | Best for | Avoid when | Cost and risk | Example |
|---|---|---|---|---|---|
| `dialogue` | Interactive dialogue (player picks lines) | relationships, clashing values, choices that express the player character, information that needs emotion | the content is a flat fact, or the choice is false | voice-over and translation per line; branches multiply | *Mass Effect*, *Disco Elysium* |
| `cutscene` | Linear dialogue or cutscene | big emotional beats, required plot points, introducing an antagonist, moments where taking control is fair | it runs long, comes too often, or contradicts what the player just did | expensive (animation, voice-over); players skip | *The Last of Us*, *Uncharted* |
| `narration` | Narrator or narrative text | framing, time skips, tone, inner thoughts, summing up what need not be played | it tells what could be shown or played | cheap as text, expensive when voiced | *Bastion*, *The Stanley Parable*, visual novel intros |
| `quest` | Quest or objective | beats with a verb (find, rescue, chase, pick a side), arcs with a goal | the beat is pure emotion or information with no action | needs level and system design; objective text is translated too | *The Witcher 3* (Bloody Baron) |
| `object` | Objects and environment (notes, item text, audio logs, set dressing) | backstory, "what happened here", optional lore, mysteries the player pieces together | the information is on the critical path | cheap per item; lore scatters and contradicts itself without a bible | *Dark Souls*, *Gone Home*, *BioShock* audio logs |
| `barks` | Barks and ambient chatter | the world reacting to choices and state, gameplay feedback, a living place | it carries plot the player must hear | many variants, heard again and again | *Skyrim* townsfolk, *The Last of Us* enemy barks |
| `mechanic` | Mechanics and gameplay | themes felt through action, character shown through how you play | the message is complex and needs words | expensive to design, strongest when it works | *Papers, Please*, *Brothers: A Tale of Two Sons* |
| `ui` | UI and systems (codex, journal, loading screen, map) | reference the player can reopen, "so far" summaries, glossaries | emotional beats | cheap | *Mass Effect* codex, quest journals |

`object`, `barks` and `ui` are **optional**: the player can miss them.

## Selection rules

**Sources:** Harvey Smith and Matthias Worch, "What Happened Here? Environmental Storytelling", GDC 2010; Clint Hocking, "Ludonarrative Dissonance in BioShock", 2007; Henry Jenkins, "Game Design as Narrative Architecture", 2004; Sam Kabo Ashwell, "Standard Patterns in Choice-Based Games", 2015

1. **Critical or optional.** A beat the player must understand to follow the plot never rests only on `object`, `barks` or `ui`. Carry it in dialogue, a cutscene, narration, a quest or a mechanic; optional channels may repeat it.
2. **Find the verb.** If the beat can be played, make it a quest or a mechanic. Prefer played > shown (environment, cutscene) > spoken (dialogue) > told (narration, text).
3. **Emotion needs a face.** High emotion needs faces and voices (`dialogue`, `cutscene`). Low emotion and plain facts fit `object` or `ui`.
4. **Agency.** If the player decides, use `dialogue` or a branching `quest`, never a `cutscene`.
5. **Rule of three.** Important information appears in two or three different channels: a line names it, a note explains it, the environment shows its result.
6. **Repetition.** What happens often (fights, walking through town) gets `barks` with variants, not long dialogue.
7. **Budget.** Count voice-over and translation cost per channel. Object and UI text costs far less than voiced lines. LocForge Branch can count words per scene.
8. **Lore consistency.** Every fact placed in `object` or `ui` text is recorded in the bible, because these channels contradict canon most often.

**Writer:**
- Fill `critical`, `channel`, `support`, `verb` and `cost` for every scene in the outline.
- Pick `channel` with rules 1–4, then add `support` channels with rules 5–6.
- When drafting, write each supporting text channel (`object`, `barks`, `quest`, `ui`) inside the scene, under a `channel:` tag.

**Editor asks:**
- Does any critical beat rest only on optional channels?
- Is a beat with a clear verb only talked about instead of played?
- Is a player decision delivered as a cutscene?
- Does important information reach the player through more than one channel?
- Is every fact in notes, items or codex text in the bible?
