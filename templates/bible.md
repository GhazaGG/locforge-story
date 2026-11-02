# Bible: <Story title>

<!-- Free prose sections (Premise, World, Theme, Tone) are for people and the editor.
     story_check reads only Settings, Characters, Glossary and Mysteries.
     Structured lines are "- key: value". Text after " #" is a comment. -->

## Premise

<One paragraph: who wants what, what stands in the way, what is at stake.>

## World

<Rules of the world: what is possible and impossible. Places that matter.>

## Theme

<The question the story asks. One sentence.>

## Settings
- max_line: 120   # dialog box limit in characters; use 84 for two 42-character subtitle lines
- framework: save-the-cat   # save-the-cat | three-act | heros-journey | story-circle | kishotenketsu | seven-point | free

## Characters
### <Protagonist name>
- id: <short-lowercase-id>
- aliases: <other names the script may use, comma-separated>
- status: alive
- dies_in: <scene id, if they die>   # leave empty if they live
- max_line: <optional override of the setting>
- want: <outer goal>
- need: <inner need>
- lie: <false belief they start with>
- ghost: <past wound behind the lie>
- voice: <sentence length, vocabulary, verbal tics, register>
- avoid: <words this character never says, comma-separated>

### <Second character>
- id: <id>
- status: alive
- want: <outer goal>
- voice: <how they talk>
- avoid:

## Glossary
### <Term>
- avoid: <wrong spellings, comma-separated> # capitals match exactly; lowercase matches any case
- note: <meaning; translate or keep>

## Canon
- [established] <fact that is fixed>
- [provisional] <fact proposed and approved, may still change>
- [under-review] <fact proposed but not yet approved>

## Mysteries
### <Question the player asks>
- answer: <the true answer, even if players never learn it>
