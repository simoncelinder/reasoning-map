---
name: devils-advocate
description: Attack an existing reasoning map as a sharp sceptic would, find what is missing, double-counted, assumed or over-graded, and propose concrete changes to the map. Use when the user asks to challenge, stress-test or play devil's advocate on a reasoning map, or after building one.
---

# Devil's advocate on a reasoning map

The input is a reasoning map: a JSON file in the format at https://github.com/simoncelinder/reasoning-map/tree/main/protocol. If the user gives prose instead, say that this works on a map and offer to build one first.

The test is not only "is the tree exhaustive?" but **"is it collectively convincing?"** Read the whole map as a smart sceptic who wants to say no. Where would they push, and would the map survive?

## How to attack

Read every node and edge first. Then go **where the weight sits**, not top to bottom: start with the arrows the conclusion depends on that are large in strength and not deductive, then deductive arrows on shaky premises. A finding on a minor branch is worth less than one on the load-bearing arrow.

Check, in roughly this order:

1. **Missing branches.** What would a person who disagrees put in the tree that has no place there? Name the branch and where it would go. This is the most common failure, and the one the author is least able to see.
2. **Overlaps.** Two branches that count the same thing twice, so the evidence for it is counted twice.
3. **Premises.** For each deductive arrow, attack the `given`, not the logic. Is it true here, now, at this scale? An arrow whose premise is weaker than its confidence is over-graded.
4. **Rival explanations.** For each abductive arrow, name the best alternative that explains the same observation. If the map does not mention it, the arrow is over-graded.
5. **Cases.** For each inductive arrow: how many cases, chosen how? Survivorship (only the cases that worked were looked at), a single era, or cases picked from memory all lower the grade.
6. **Direction and confounding.** Could the arrow run the other way, or could a third factor drive both ends?
7. **Add or multiply.** Causes that amplify each other drawn as if they add, or the reverse.
8. **Asymmetric scepticism.** Is the map stricter with claims it dislikes than with claims it likes? Hold every arrow to the same standard of evidence.
9. **Folklore.** A claim that sounds right, circulates widely and has no defensible source. Grade it `folklore` or remove it.
10. **Falsifiers.** A weighted claim with no falsifier, or one so vague nothing could ever trigger it. Write a sharper one.
11. **Abstraction.** Siblings at different levels of abstraction, or a branch broken down far deeper than the answer needs while another is left as one box.

## Output

A numbered list of findings, most damaging first. Each one:

- **Where**: the node id or `from->to` edge.
- **The objection**, in one or two sentences, as the sceptic would say it.
- **The change**: a concrete edit to the map. Add a branch, lower a confidence, add a rival in `note`, rewrite a `given`, add a falsifier, add evidence `against`. If the right change is "go and find out", say what to look for.

Then one line: **does the conclusion survive?** Yes, yes but less certain, or no, and why.

Apply the changes the user accepts. Record each change where a reader will see it: the reason a grade dropped goes in the arrow's `note`, new counter-evidence in `against`. Do not add fields the format does not define. If the map lives in a git repository, commit the revision separately so the critique shows up in the history.

## What this is not

Not a list of everything that could conceivably be wrong. Ten findings that each move a grade or add a branch beat thirty nitpicks. If the map is sound, say so, and say what was checked; a devil's advocate that always finds a fatal flaw is as useless as one that never does.
