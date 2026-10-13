---
name: compare-maps
description: Compare two reasoning maps of the same question, built by two people, and find where their disagreement actually lies: the crux, and the observation that would settle it. Use when two people have each mapped a question and want to know where they really differ, or when a debate keeps going round in circles.
---

# Find the crux between two maps

Input: two reasoning maps of the same question, in the format at https://github.com/simoncelinder/reasoning-map/tree/main/protocol, each built by a different person. Output: where they actually disagree, in one line, and what would settle it.

The deliverable is not a list of differences. It is the sentence "your real disagreement is X", backed by the diff. Two people who argue about a conclusion are usually arguing about something upstream that neither has said out loud; the job is to find it.

## 1. Align the maps

The two maps use different ids, labels and breakdowns. Match claims by meaning, not by text. For each claim in map A, find the claim in map B that says the same thing, or note that there is none. Be strict: "crime is rising" and "violent crime is rising" are different claims. When unsure, list the pair as "possibly the same" and ask.

## 2. Diff, in this order

The order matters: the earlier kinds of difference explain the later ones.

1. **Framing.** Compare the `parent` trees. How did each person cut the problem? Two people who break the same question into different branches are not disagreeing about facts yet; they are looking at different objects. Name the two framings in one line each.
2. **Missing branches.** Claims one map has and the other does not. These are "you have not considered this", not "you are wrong".
3. **Same link, different grade.** The format says which kind of disagreement it is:
   - different `strength`, same `confidence`: they agree it is real and disagree how much it matters;
   - different `confidence`, same `strength`: they disagree whether it is real at all;
   - both: say so.
   These need different conversations. Never report "they disagree on this link" without saying which.
4. **Same link, different inference type.** One calls it deductive, the other inductive or abductive. This is a disagreement about what kind of argument it is, usually the deepest one, and almost never named in conversation.
5. **Different premises.** Same deductive link, different `given`. Often the whole disagreement is here: same logic, different starting assumptions, and the assumptions are values rather than facts. Say when a premise is a value, because no evidence will move it.
6. **Different falsifiers.** For the same claim, what would change each person's mind. Where the falsifiers differ, they are holding the claim to different standards.

## 3. Find the crux

From the diff, pick the smallest set of differences that, if resolved, would bring the two conclusions together. Usually one or two links. Test it: if A adopted B's grade on just this link, would A's conclusion move? If not, it is not the crux, keep looking.

Then name the observation that would settle it: a `falsifier` in one map that the other person would also accept, or if neither map has one, write it. That is the experiment, the data, the case study, the thing to go and look at. If the crux is a value premise, say that too: no observation settles it, and the two should stop arguing about evidence.

## 4. Output

Short. In this order:

1. **One line:** "Your real disagreement is ..." Name the link or premise, and which kind of disagreement it is (how much, whether, what kind of argument, or a value).
2. **What would settle it:** the observation, in one or two sentences. Or "nothing; this is a value difference".
3. **What you agree on** that you might not have known you agreed on. People overestimate how far apart they are; the list of shared links is often the most useful part for the relationship.
4. **The rest of the diff**, briefly, grouped by the six kinds above, for the record.

Do not soften the crux into a list of "areas to explore". If the maps support a one-line answer, give it. If they do not, say what is missing from the maps that would let you.

## What this is not

Not a judge. It does not say who is right; it says where to look. Two maps built in bad faith diff into two sets of motivated grades, and this skill cannot tell. Run `devils-advocate` on each map first if there is any doubt.
