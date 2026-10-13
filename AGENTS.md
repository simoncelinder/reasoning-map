# AGENTS.md

## This repo is the protocol only. No real reasoning goes in here.

This repository is public. It holds the **format** for reasoning maps and tools that work on that format. It must never hold anyone's actual thinking.

**Never commit, in any file, commit message, issue, test fixture or example:**

- a real reasoning map, mental model, belief, argument or analysis, whole or in part
- node labels, evidence, falsifiers, notes or conclusions taken from someone's real maps
- names, file names or folder names of private models or private repositories
- anything copied from another repository open in the same session

If you are an agent working in a session that also has private repositories open, **nothing from them comes here**. Not a sentence, not a label, not a structure "anonymised" by renaming the nodes. Reading a private map to check that a validator accepts it is fine; copying any of it here is not.

If a task would put real reasoning into this repo, stop and say so instead of doing it.

Examples, fixtures and demos use **abstract placeholders** (`a`, `b`, `Driver A`), a **plainly invented** problem, or a **well-known public question nobody here has a stake in** (like the dinosaur example: settled-enough science, no politics, no business, nothing personal). Never a topic someone in the session is actually thinking through. When unsure whether something counts as real reasoning, treat it as real and leave it out.

## What belongs here

```
protocol/      the spec: JSON Schema profiles + protocol/README.md (rules, meanings)
validators/    optional validators, one folder per language
examples/      template.json (placeholders) and one worked example
viewer/        one example renderer: a single HTML file that reads map files
skills/        agent skills for users to copy into their own setup
```

`skills/` is deliberately not `.claude/skills/` or `.agents/skills/`: those would load into every agent working on this repo, and an agent here must never build a real map. Do not move them, and do not follow them while working on this repo; edit them as documents.

Planned: a mocked research run on the example.

## The protocol is language-agnostic

- **The spec is `protocol/`**: the JSON Schema files and the rules in protocol/README.md. Nothing else.
- **Validators are optional clients.** The Python one is one implementation. A validator in another language implements the same schemas and the same numbered rules, and no validator may add a rule that is not written in protocol/README.md first.
- **Renderers are detached.** A map must read as a complete model with every renderer deleted. Nothing in the format exists only to serve a particular renderer; `kind` and edge `type` are hints a renderer may ignore.

## Changing the protocol

1. Change the schemas and protocol/README.md first, then every validator, in the same commit.
2. Profiles only add fields. Never add a required field to an existing profile; a new idea is an optional field or a new profile.
3. A change that makes an existing valid map invalid is breaking. Say so in the commit message and give the reason.
4. Every primitive must make a map easier to be wrong about. A field that only makes a map prettier or more complete stays out.

## Conventions

- **Never commit or push without asking first.** The repo is public, so a push publishes. Make the edit, show the diff, and wait for an explicit go-ahead for that change.
- Validator tests use abstract fixtures only (see validators/python/test_reasoning_map.py).
- Run `python3 -m unittest discover validators/python` before committing a change to the protocol or the validator, and validate the examples (`python3 validators/python/reasoning_map.py examples/*.json`).
- The viewer never gets a feature that requires a field the protocol does not define. If it needs one, the protocol changes first.
- Do not commit build output, packages or downloaded files (`*.whl`, `dist/`, caches).
