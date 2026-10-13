# reasoning-map

A structured format for building and examining a mental model of a hard question: claims, the causal and logical links between them, the evidence on each side, and how strong and certain each link is.

A reasoning map is a plain JSON file. Claims are boxes that can be broken down into smaller boxes. Arrows between them say what kind of reasoning connects them (deductive, inductive, abductive or causal), how much the link matters if it is true, and how sure you are that it is. Claims that carry weight say what would change your mind.

![The worked example in the viewer](viewer/screenshot.png)

## What it is for

Questions you want to think about longer and harder than a conversation allows, and come back to: a big challenge in society, a decision that will shape years of your life, a belief you suspect you hold because of who you are rather than what you know. The kind of question where the answer is a web of causes, the evidence is mixed, and the honest state is "probably, depending on two things I have not checked".

For those, a map does what careful thinkers do by habit and the rest of us skip, and it does it every time:

- **It makes gaps visible.** In prose, a missing premise or an unstated assumption is simply a sentence that is not there. In a map it is an empty `given` field, and a validator flags it. Fluent writing hides what it leaves out; a schema cannot.
- **It separates how much from how sure.** Each link gets two grades: *strength*, how much it would move the outcome if real, and *confidence*, how sure we are that it is real. A single word like "important" or "likely" blurs them. The link that would be huge if true but is barely established is exactly the one you need to see, and it is the one prose hides best.
- **It shows where the answer rests.** Type every link and the conclusion usually turns out to hang on one to three that are not deductive. Those are where to spend your doubt and your research, and they are rarely where you expected.
- **It treats every side the same.** Your claims and your opponents' go through the same fields, the same grades and the same falsifier requirement. A map cannot be stricter with the claims it dislikes without that showing, which is as close to a cure for motivated reasoning as a format can get.
- **It persists and compounds.** A prompt's rigour lasts one conversation. A map is a file: diff it, validate it, come back to it in a month, hand it to a different model or to a friend who disagrees with you, and run the devil's advocate on it again. Your model of a question gets better over years instead of resetting every time you open a chat.

The grades on inductive and abductive links are meant to be earned, not guessed: pair the map with research, go and count the cases and the counter-cases, and let the strength and confidence move. A map where research changed nothing was not looked at hard enough.

### Limits

It does not make the reasoning right: a model or a person fills in `confidence: well-supported` as fluently as they write prose, so the format forces the question and the research and the sceptic answer it. A fully graded map is persuasive, which is why the devil's advocate step exists and should be run by someone, or something, that wants the map to be wrong. And it is not for quick questions; for a one-off, a good prompt is enough.

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
- **devils-advocate** attacks an existing map as a sceptic would, asking not just "is anything missing?" but "is this collectively convincing?". Run it on its own, now and then, on any map, and especially on the ones you like.

The intended loop: build the map, research the links that are not deductive until the grades are earned, run the devil's advocate, revise, and keep the file. Each pass through that loop is a chance to notice you were wrong, which is the point.

## Language-agnostic

The protocol is JSON and JSON Schema; any language can read, write and validate it. The validators here are optional conveniences, not part of the spec.

| Validator | |
| :-- | :-- |
| [Python](validators/python/) | `python3 validators/python/reasoning_map.py my-map.json`. Standard library only |

## Examples and viewer

- **[examples/](examples/)**: `template.json`, every field once with placeholders, to copy, and one worked example: what ended the dinosaurs. It needs every part of the format, from a deduction that is still uncertain to a piece of folklore.
- **[viewer/](viewer/)**: one example renderer, a single HTML file. It is fully detached from the format: any other renderer can read the same files. To see the dinosaur example drawn:

```
git clone https://github.com/simoncelinder/reasoning-map
cd reasoning-map
python3 -m http.server
```

Then open [http://localhost:8000/viewer/](http://localhost:8000/viewer/).

## What is not here

Anyone's actual reasoning. This repo holds the format and tools for it, nothing else. Keep your own maps in your own repository. See [AGENTS.md](AGENTS.md).

## Status

Early (0.x). Fields may still change; a change that breaks existing maps will be called out.

## License

[MIT](LICENSE). Use the format, the validators, the viewer and the skills however you like.
