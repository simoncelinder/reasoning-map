---
name: reasoning-map
description: Think through a question by building a reasoning map, a JSON file of claims broken down into a tree, with typed and graded arrows between them. Use when the user wants to analyse a problem, a decision, a debate or a "why" question rigorously, or asks for a reasoning map.
---

# Build a reasoning map

The user gives a question or problem. You think it through by building a reasoning map: a JSON file in the format at https://github.com/simoncelinder/reasoning-map/tree/main/protocol. The format is the discipline. Every arrow must say what kind of reasoning it is, and every claim that carries weight must say what would refute it. Do not summarise into the format afterwards; think in it.

**Where the file goes.** Write the map wherever the user keeps their maps, and ask if unsure. Never write a map into the reasoning-map repository itself: it holds the format only, never anyone's actual reasoning.

## 1. Frame

- Restate the question so it has an answer. "What about remote work?" is not a question; "Why did our team's output drop after going remote?" is.
- Name its type, because it decides what the tree breaks down:
  - **Why** (diagnosis): the tree breaks down possible causes.
  - **How** (solution): the tree breaks down ways to reach the goal.
  - **Whether** (evaluation): the tree breaks down what would have to be true for yes.
- If the question is ambiguous in a way that changes the tree, ask once before going further.

## 2. Issue tree: the breakdown

Break the question into an issue tree using `parent`. The tree is the breakdown, not the reasoning.

- **Mutually exclusive, collectively exhaustive (MECE) at levels 1 and 2.** No two branches cover the same ground, and together they leave nothing important out. Deeper down, aim for no big overlaps and nothing important missing; forcing strict MECE at depth produces tidy, empty trees.
- **State the cut.** Each split follows one principle, written in the parent's `text`: price × volume, internal vs external, supply vs demand, before vs after. A split you cannot name a principle for is usually not exhaustive.
- **2 to 5 branches per box. Siblings at the same level of abstraction.** "Pricing" next to "the March discount email" is a level mismatch: one belongs under the other.
- **Depth 2 or 3 for most questions.** Go deeper only where the answer actually turns.
- **The first node is the root**: the central claim of the map. Give the outcome its own node rather than pointing arrows at the root.

## 3. Turn branches into claims

An issue tree is usually written as questions. A reasoning map holds claims, because a question cannot be wrong. Turn each branch into the hypothesis you would bet on: "Is demand falling?" becomes "Demand is falling". Keep the original question in `text` if it helps.

## 4. Reasoning: the arrows

Arrows carry the reasoning and may cross branches and form loops. Real causes do not respect the tree; never bend the tree to avoid an arrow.

Every arrow gets an `inference`:

| `inference` | Use when | Must add |
| :-- | :-- | :-- |
| deductive | If the premises hold, the target holds, no exceptions | `given`: the premises, stated so they can be checked |
| inductive | Generalised from cases | the cases, in `for` / `against` on the claim |
| abductive | The best available explanation of what is observed | the rival explanations, in `note` |
| causal | A mechanism you assert without further support | honesty that it is only asserted |

Add `combines: "multiply"` when causes amplify each other rather than add (one near zero sinks the outcome). It is often the key structural claim; look for it.

## 5. Evidence and grades

- Put evidence on the claim it bears on, in `for` and `against`, one item each, with a source where there is one. A claim with only `for` evidence has not been looked at.
- Grade every arrow on two separate scales:
  - `strength` (small, medium, large): if the link is real, how much it moves its target.
  - `confidence` (established, well-supported, suggestive, contested, folklore): how sure we are it exists as stated.
- They come apart. Large and contested is the shape of a risk worth watching; say so when you see it.
- A deductive arrow's confidence is its premises' confidence, never more. Valid logic on a shaky premise is shaky.
- A definition or identity gets a confidence and no strength; the claim it supports gets a `measure` instead of a `falsifier`.
- Every claim with a `weight` gets a `falsifier`: the observation that would show it is wrong. If you cannot write one, the claim is either true by definition (give it a `measure`) or not yet a claim.
- If you have research tools, use them on the inductive and abductive links first: count the cases, find the counter-cases, and let the grade move. A research step that changes nothing was probably not looking hard enough.

## 6. Challenge it

Before presenting the map, run the `devils-advocate` skill on it if it is installed, or do its checks yourself: a sceptic reading the whole tree, looking for what is missing, double-counted or assumed. Revise, and tell the user what changed.

## 7. Output

- Write the JSON with `"profiles": ["reasoning", "grades"]`, one node or edge per line so diffs stay readable.
- Validate it if a validator is available (`python3 validators/python/reasoning_map.py MAP.json` in a clone of the reasoning-map repo) and fix the errors and warnings.
- Then a short summary in prose:
  1. The answer, in one or two sentences.
  2. **Where it rests**: the one to three non-deductive arrows the answer depends on, with their strength and confidence. This is usually where the real uncertainty is, and the part the user should check.
  3. What would change the answer: the falsifiers that matter most.

## Field reference

```json
{
 "id": "short-id", "title": "Title", "core": "The answer in one or two sentences.",
 "profiles": ["reasoning", "grades"],
 "nodes": [
  {"id": "root", "label": "Central claim", "kind": "claim"},
  {"id": "a", "label": "Branch A", "text": "Split by: ...", "kind": "group"},
  {"id": "a1", "label": "A claim that can be wrong", "parent": "a", "kind": "driver",
   "weight": "High", "for": ["..."], "against": ["..."], "falsifier": "..."},
  {"id": "out", "label": "The outcome", "kind": "outcome"}
 ],
 "edges": [
  {"from": "a1", "to": "out", "label": "short relation", "inference": "abductive",
   "strength": "large", "confidence": "suggestive", "note": "Rival explanation: ..."}
 ]
}
```

`kind` is a rendering hint: claim, group, part, driver, mechanism, condition, outcome, failure, demoted. Edge `type` is a hint too: failure, dampens, weak.
