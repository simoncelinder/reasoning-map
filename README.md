# reasoning-map

A structured format for exploring reasoning: claims, the links between them, and how strong and certain each link is.

A reasoning map is a plain JSON file. Claims are boxes that can be broken down into smaller boxes. Arrows between them say what kind of reasoning connects them (deductive, inductive, abductive or causal), how much the link matters if it is true, and how sure you are that it is. Claims that carry weight say what would change your mind.

![The worked example in the viewer](viewer/screenshot.png)

## Why use it

Thinking through a hard question with a language model is fast, fluent, and easy to get wrong in ways you cannot see. Prose lets everyone, model and human, write "A leads to B" without saying how they know, how much it matters, or how sure they are. A reasoning map does not.

- **It forces the logic into the open.** Every arrow must say what kind of reasoning it is. A deduction has to list its premises. A generalisation has to show its cases. A best-guess explanation has to name its rivals. "It follows that" stops being a free move.
- **It separates how much from how sure.** Each arrow gets two grades: *strength*, how much it would move the outcome if true, and *confidence*, how sure we are that it is true. They come apart where it matters most: a link that would be huge if real but is barely established is exactly what a single "important" or "likely" hides.
- **It keeps deductive from meaning certain.** A deduction is only as sure as its premises, so valid logic on a shaky premise is graded shaky.
- **It makes every weighty claim refutable.** Anything that carries weight says what would change your mind. A claim nobody can write a falsifier for is not ready to carry weight.
- **It shows the reasoning at every level.** Open the whole map to see the big picture, then open a box to see what it is made of and the evidence for and against it. Thick faint arrows show at a glance where the argument is big but unproven.
- **It shows where the answer actually rests.** The conclusion usually depends on one to three links that are not deductive. Typing and grading every arrow makes those impossible to miss, and that is where to spend your doubt and your research.
- **It gives a model something to be held to.** A model filling in the format has to commit, link by link, in a file you can check, diff, validate and come back to. A paragraph can be fluent and empty; a map with empty `given` fields and no falsifiers visibly is.

Use it when brainstorming or deciding with a language model, when a debate keeps going round in circles, or when you want to find out which of your beliefs are holding up the rest.

## The protocol

**[protocol/](protocol/)** is the whole spec: three JSON Schema files and one page of rules.

| Profile | What it adds |
| :-- | :-- |
| [core](protocol/core.schema.json) | Boxes, a breakdown (box inside box) and arrows. Complete on its own |
| [reasoning](protocol/reasoning.schema.json) | Inference type on each arrow, premises, evidence for and against, falsifiers |
| [grades](protocol/grades.schema.json) | Strength (how much a link moves its target if true) and confidence (how sure it exists) on each arrow |

Profiles only add fields, so a tool that knows only the core can still open any map. Start with [protocol/README.md](protocol/README.md).

## Thinking with a language model

**[skills/](skills/)** has two agent skills to copy into your own setup:

- **reasoning-map** takes a question and builds a map: an issue tree that is mutually exclusive and collectively exhaustive, branches turned into claims that can be wrong, typed and graded arrows, evidence, falsifiers. It ends with where the answer actually rests.
- **devils-advocate** attacks an existing map as a sceptic would, asking not just "is anything missing?" but "is this collectively convincing?". Run it on its own, now and then, on any map.

## Language-agnostic

The protocol is JSON and JSON Schema; any language can read, write and validate it. The validators here are optional conveniences, not part of the spec.

| Validator | |
| :-- | :-- |
| [Python](validators/python/) | `python3 validators/python/reasoning_map.py my-map.json`. Standard library only |

## Examples and viewer

- **[examples/](examples/)**: `template.json`, every field once with placeholders, to copy, and one worked example: what ended the dinosaurs. It needs every part of the format, from a deduction that is still uncertain to a piece of folklore.
- **[viewer/](viewer/)**: one example renderer, a single HTML file. Run `python3 -m http.server` in the repo root and open http://localhost:8000/viewer/. It is fully detached from the format: any other renderer can read the same files.

## What is not here

Anyone's actual reasoning. This repo holds the format and tools for it, nothing else. Keep your own maps in your own repository. See [AGENTS.md](AGENTS.md).

## Status

Early (0.x). Fields may still change; a change that breaks existing maps will be called out.

## License

[MIT](LICENSE). Use the format, the validators, the viewer and the skills however you like.
