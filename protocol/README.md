# The protocol

A reasoning map is one JSON file. These three JSON Schema files and the rules below are the whole spec. Nothing here depends on a programming language, a renderer or a tool.

| Profile | Schema | Adds | Use it when |
| :-- | :-- | :-- | :-- |
| core | [core.schema.json](core.schema.json) | boxes (`id`, `label`, `parent`, `sub`, `text`, `kind`, `ref`) and arrows (`from`, `to`, `label`, `type`). Only `id` and `label`, `from` and `to` are required | Always. A map with only these fields is complete |
| reasoning | [reasoning.schema.json](reasoning.schema.json) | on a box: evidence `for` / `against`, `falsifier`, `measure`, `weight`. On an arrow: `inference` (deductive, inductive, abductive, causal), `given`, `combines` (add or multiply), `note` | The map makes claims worth testing |
| grades | [grades.schema.json](grades.schema.json) | on an arrow: `strength` (small, medium, large) and `confidence` (established, well-supported, suggestive, contested, folklore) | You want to show where the weight sits |

A map lists the profiles it uses in `profiles`; `core` is implied. **Profiles only add fields, never require new ones on core**, so a reader that knows only core still opens a fully graded map and ignores what it does not know.

## Shape

```json
{
 "id": "example",
 "title": "Example",
 "profiles": ["reasoning", "grades"],
 "nodes": [
  {"id": "root", "label": "The central claim"},
  {"id": "a", "label": "Driver A", "falsifier": "What would show A does not matter."},
  {"id": "b", "label": "Driver B"},
  {"id": "a1", "label": "A part of A", "parent": "a",
   "for": ["Evidence for."], "against": ["Evidence against."]}
 ],
 "edges": [
  {"from": "a", "to": "root", "inference": "inductive", "strength": "large", "confidence": "suggestive"},
  {"from": "b", "to": "root", "inference": "deductive", "given": "The premises.", "confidence": "well-supported"}
 ]
}
```

- **The first node is the root.** A node without `parent` sits under it.
- **`parent` is the breakdown, edges are the reasoning.** The breakdown is a tree, so it can be checked for gaps and overlaps. The reasoning is a graph, because real causes have feedback and the same variable in two places.
- **Edges can be written at any level.** A renderer that hides a node draws its edges from the nearest visible box that contains it.
- **Evidence sits on the claim it bears on**, never floating.

## Inference types

| `inference` | Means | Needs |
| :-- | :-- | :-- |
| deductive | If the premises hold, the target holds. No exceptions | `given`: the premises |
| inductive | Generalised from cases. Stronger with more cases, never certain | cases in `for` / `against` |
| abductive | The best available explanation of what is observed | the rival explanations, ideally in `note` |
| causal | An asserted mechanism with no further support given | honesty that it is only asserted |

## Strength is not confidence

- **`strength`**: if the link is real, how much it moves its target. The size of the coefficient.
- **`confidence`**: how sure we are the link exists as stated. The p-value side.

They come apart where it matters most: *large if true, but unproven* is the shape of a tail risk.

Two grading rules:

1. **A deductive arrow's confidence is its premises' confidence, never more.** Valid logic on a shaky premise is still shaky. This keeps "deductive" from reading as "certain".
2. **A definition or identity gets a confidence and no strength.** It moves nothing on its own. The box it points to gets a `measure` instead of a `falsifier`, since it cannot be wrong, only big or small.

| `confidence` | Means |
| :-- | :-- |
| established | Replicated, survives controls, robust across specifications |
| well-supported | Good identification, but a limited era or sample |
| suggestive | Directionally indicated, effect size unstable |
| contested | Serious people disagree; name both sides |
| folklore | Circulates widely, no defensible source |

## Rules JSON Schema cannot express

A validator in any language implements these on top of the schemas. Errors make a map invalid. Warnings flag a map that is valid but weaker than it looks.

**Errors**

1. Node ids are unique.
2. The first node is the root and has no `parent`.
3. Every `parent` names an existing node.
4. Parents do not form a cycle.
5. Every edge's `from` and `to` name existing nodes.

**Warnings**

6. Every field belongs to some profile. An unknown field is usually a typo.
7. A field from a profile is used, but that profile is not listed in `profiles`.
8. A `deductive` edge has no `given`.
9. The map lists `grades`, but an edge has no `confidence`.
10. An edge has a `strength` but no `confidence`; it would read as certain.
11. Once any node has a `falsifier`, every node with a `weight` needs a `falsifier` or a `measure`.
12. A `kind` that is not one of the listed rendering hints.

## Changing the protocol

Change the schemas and this file first, then every validator. A change that makes an existing valid map invalid is a breaking change and needs a strong reason. Adding an optional field, or a new profile, is not.
