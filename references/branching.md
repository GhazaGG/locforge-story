# Branching and choice design

Use these when planning the structure of choices at intake and when drafting choice text.

## Standard patterns of choice-based games

**Source:** Sam Kabo Ashwell, *Standard Patterns in Choice-Based Games*, 2015

Eight common shapes for branching narratives:

- **Time Cave:** branches never rejoin; every path is unique.
- **Gauntlet:** one main line with side failures or short deviations.
- **Branch and Bottleneck:** branches split and rejoin at key points.
- **Quest:** a hub with several locations or tasks, in any order.
- **Open Map:** free movement between nodes, with state tracked.
- **Sorting Hat:** an early choice sorts the player onto a long route.
- **Floating Modules:** self-contained pieces that can occur in any order.
- **Loop and Grow:** a repeating structure that unlocks more each cycle.

**Use in games when:** you are choosing structure at intake. The pattern sets the content budget. Three binary choices give 8 paths, 5 give 32, and 10 give 1,024, so a Time Cave becomes unaffordable fast.

**Writer:**
- Choose one pattern at intake and write it in the bible.
- Estimate path count and word count from the pattern before outlining.
- If the budget is tight, pick Branch and Bottleneck or Quest rather than a Time Cave.

**Editor asks:**
- Is a pattern chosen and does the outline follow it?
- Is the number of unique paths realistic for the stated scope?

## Meaningful choice

**Source:** Sid Meier ("a series of interesting decisions"); a four-part test

A choice is meaningful when it passes four checks: the options are distinct, the consequences are perceivable, the choice cannot be undone at once, and it expresses character.

**Use in games when:** you are deciding which choices are worth writing. A false choice (every option leads to the same result with no trace) feels like a trick.

**Writer:**
- For each choice, write what the player sees change afterward.
- Make the options differ in values, not only in tone.
- Avoid a free undo; make the choice stick for at least a scene.

**Editor asks:**
- Do the options lead to different, visible consequences?
- Does any choice reduce to a false choice with all options rejoining without a mark?

## Delayed consequence and callback

**Source:** Telltale games; *The Witcher* series

A flag set now changes a line, a character's reaction or an ending later. Players feel their choices are remembered.

**Use in games when:** you want choice to carry across chapters. The Branch lint's `unused-var` check hints at a forgotten callback: a variable that is set but never read.

**Writer:**
- For every flag set, name where it is read.
- Keep callbacks small: a line, a look, a prop.
- Reserve large changes for flags worth the cost of writing them.

**Editor asks:**
- Is every flag that is set read somewhere later?
- Does each callback appear in all routes that could set the flag?

## Foldback and bottlenecks

**Source:** Branch and Bottleneck pattern (Ashwell); common practice

Branches rejoin at key beats so the writer can keep control of the main line and budget. Vary the texture (lines, mood, small details) so the player still feels the difference.

**Use in games when:** you need to bring several routes back to one story beat, such as a boss or a reveal.

**Writer:**
- Mark each bottleneck beat in the outline.
- Write route-specific lines at the start of the bottleneck, so the join does not feel like a reset.
- Carry at least one trace of the branch past the join.

**Editor asks:**
- Are bottleneck beats named in the outline?
- Does the scene after the join reflect the player's earlier route?

## Storylets and quality-based narrative

**Source:** Emily Short; Failbetter Games, *Fallen London*

Content is built from small pieces that unlock by state, not by a fixed path. A storylet becomes available when its conditions (qualities) are met.

**Use in games when:** the game is systemic, open or long-running, and a fixed script cannot cover every situation.

**Writer:**
- Write each storylet with its conditions, one clear hook, and its state changes.
- Keep each one self-contained so it reads well in any order.
- Track which qualities each storylet reads and writes.

**Editor asks:**
- Does each storylet state when it is available?
- Does it read well when it appears out of the planned order?

## Choice wording

**Source:** Dialogue wheel practice (the "paraphrase problem" in *Mass Effect*-style wheels)

Option text must show the intent of what the character will say, so the player is not surprised by the actual line.

**Use in games when:** the game shows a short label and then a longer spoken line. The label must match the line.

**Writer:**
- Write the choice text and the spoken line together and check that the tone matches.
- State intent, for example "Refuse, politely", rather than a vague word.
- Keep labels short and parallel in form.

**Editor asks:**
- Does the spoken line match the tone and intent of its label?
- Are the labels parallel and clear without context?

## Ludonarrative harmony

**Source:** Clint Hocking, 2007 essay on *BioShock*

Story and mechanics should say the same thing. When a game rewards a behavior its story condemns, the player feels a dissonance.

**Use in games when:** the player's main actions are repetitive, such as combat or looting, and the story has a stance about them.

**Writer:**
- List the player's main verbs and check that the story's values agree with them.
- If they disagree on purpose, make the contrast part of the theme.
- Let characters react to what the player actually does.

**Editor asks:**
- Do the player's main actions agree with the character and theme?
- If not, is the conflict deliberate and acknowledged in the story?

## Player character type

**Source:** Game narrative practice

The player character can be a silent protagonist, a blank slate, or a defined character. The type changes how choice text is written and how much the character speaks for the player.

**Use in games when:** you are choosing the voice of the choices. A defined character allows full lines; a silent or blank-slate protagonist needs short, neutral options.

**Writer:**
- Pick the type at intake and record it in the bible.
- For a defined character, write the player options in that voice.
- For a blank slate, avoid backstory the player did not choose.

**Editor asks:**
- Does the choice text fit the stated player character type?
- Does the story avoid contradicting the type, such as backstory for a blank slate?
