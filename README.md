# reasoning-map

A structured format for exploring reasoning: claims, the links between them, and how strong and certain each link is.

A reasoning map is a plain JSON file. Claims are boxes that can be broken down into smaller boxes. Arrows between them say what kind of reasoning connects them (deductive, inductive, abductive or causal), how much the link matters if it is true, and how sure you are that it is. Claims that carry weight say what would change your mind.

The point is not a prettier diagram. It is a format strict enough that whoever fills it in, a person or a language model, has to commit: which kind of inference, resting on what, and what would refute it.

## The protocol

**[protocol/](protocol/)** is the whole spec: three JSON Schema files and one page of rules.

| Profile | What it adds |
| :-- | :-- |
| [core](protocol/core.schema.json) | Boxes, a breakdown (box inside box) and arrows. Complete on its own |
| [reasoning](protocol/reasoning.schema.json) | Inference type on each arrow, premises, evidence for and against, falsifiers |
| [grades](protocol/grades.schema.json) | Strength (how much a link moves its target if true) and confidence (how sure it exists) on each arrow |

Profiles only add fields, so a tool that knows only the core can still open any map. Start with [protocol/README.md](protocol/README.md).

## Language-agnostic

The protocol is JSON and JSON Schema; any language can read, write and validate it. The validators here are optional conveniences, not part of the spec.

| Validator | |
| :-- | :-- |
| [Python](validators/python/) | `python3 validators/python/reasoning_map.py my-map.json`. Standard library only |

## What is not here

Anyone's actual reasoning. This repo holds the format and tools for it, nothing else. Keep your own maps in your own repository. See [AGENTS.md](AGENTS.md).

## Status

Early (0.x). Fields may still change; a change that breaks existing maps will be called out.
