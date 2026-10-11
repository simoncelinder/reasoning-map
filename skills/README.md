# Skills

Two agent skills for thinking in the format with a language model. Each is a folder with a `SKILL.md`, the common skill format, so they work with any agent that reads skills.

| Skill | What it does |
| :-- | :-- |
| [reasoning-map](reasoning-map/SKILL.md) | Takes a question and builds a map: an issue tree that is mutually exclusive and collectively exhaustive, branches turned into claims that can be wrong, typed and graded arrows, evidence, falsifiers. Ends with where the answer actually rests |
| [devils-advocate](devils-advocate/SKILL.md) | Attacks an existing map as a sceptic would: missing branches, weak premises, rival explanations, over-graded arrows, folklore. Proposes concrete edits. Use it on its own, now and then, on any map |

## Install

Copy the folders to where your agent looks for skills. For Claude Code:

```
cp -r skills/reasoning-map skills/devils-advocate ~/.claude/skills/
```

or into `.claude/skills/` in the repository where you keep your maps.

They are kept here in `skills/` on purpose, not in a folder agents load automatically, so that an agent working on this repo never starts building maps in it. Your maps belong in your own repository.
