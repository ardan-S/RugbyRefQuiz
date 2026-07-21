# Question Style Guide

Standards for every question in `questions/data/`. New and edited questions
must conform. Source of truth: **World Rugby Laws of the Game 2026** (the PDF
in the repo root).

## The stem (question text)

- Self-contained: answerable without seeing the options.
- One defensibly correct answer under the current laws. If two options could
  be argued, the question is broken - fix it or cut it.
- **Scenario grammar:** teams are always **Red** and **Blue**, players named
  by shirt number ("Red 7 tackles Blue 12"). Present tense. State only the
  context that matters (score, clock, prior warnings) - no decoration.
- **Scenario and sanction questions address the reader as the referee:**
  "What do you award?", "What's your decision?". Factual and procedural
  questions stay neutral: "What is the maximum...".
- No trick questions. Difficulty comes from the law, not from wordplay.

## Options

- 4 options for most questions (3 acceptable where the decision space is
  genuinely small; more only for good reason).
- Distractors must be *plausible*: real misconceptions, adjacent sanctions,
  or near-miss values - never obvious filler.
- Sanction questions draw from the real decision space: Play on / Advantage /
  Scrum / Free-kick / Penalty / Penalty try / cards, with the offending team
  identified where it matters ("Penalty to Red").
- All options grammatically parallel and similar in length. The correct
  answer must not be systematically the longest or most detailed.
- Never "All of the above" / "None of the above".

## Answers

- `answers` lists every option that would be accepted (usually one).
- The answer must be verifiable against a specific clause of the laws.

## Law references and quotes

- `law_reference`: the clause the answer rests on, in World Rugby citation
  style within the law: `14.5`, `14.5a`, `9.7b`.
- `law_quote`: **verbatim wording** from the 2026 laws that settles the
  question. Trim with an ellipsis (...) where needed; never paraphrase inside
  the quote. Keep it to the sentence(s) that decide the answer.
- Facts that live in tables or diagrams (dimensions, goalpost specs) can't be
  quoted verbatim: use a labelled summary instead - `"Dimensions table: field
  of play length - minimum 94, maximum 100 metres."`, `"Goal posts diagram:
  5.6m apart, 3m to top edge of bar."`
- `explanation`: 1-3 sentences of practical refereeing guidance. Do not
  restate the quote - add what it means in practice ("watch for...",
  "the common error is...").

## Difficulty levels

- **beginner** - single fact any new referee must know (dimensions, player
  counts, basic definitions).
- **intermediate** - applying a law to a straightforward match situation;
  the routine matchday call.
- **advanced** - edge cases, multi-law interactions, restart subtleties,
  materiality judgments.

## Types

- **factual** - recall of law content.
- **procedural** - how a process runs (replacements, cards, restarts admin).
- **sanction** - an offence happened; what is the sanction/restart?
- **scenario** - a match situation where the *decision itself* is the test;
  must contain enough context that the decision isn't mechanical.

## Housekeeping

- IDs are stable once published; new questions continue the law's numbering.
- Tags: lowercase-hyphenated, reuse existing tags before inventing new ones.
- When the laws change season-on-season, affected questions are updated, not
  silently left stale; `metadata.source` names the edition they were checked
  against.

## Scenario chains (questions/scenarios/)

A chain is one match situation followed by 2-4 linked decisions mirroring the
real refereeing sequence (offence? -> advantage or whistle? -> sanction? ->
restart?). Schema: `questions/scenario_schema.yaml`. IDs: `CH-XXX-###`
(`CH-BRK-`, `CH-FP-`, `CH-MAUL-`, ...).

- **Setup**: 2-4 sentences. Include only context that matters to a decision -
  score, clock, a prior warning, field position. If a detail is in the setup,
  some step should turn on it.
- **Canonical path**: each step's text may carry the story forward, and must
  assume the *correct* previous call (the app shows the correct answer after
  every step, so the storyline holds even after a miss).
- **Materiality**: chains are the home of "play on - nothing material" as a
  legitimate, sometimes correct answer. At least one distractor per chain
  should be the *over-refereed* call.
- **Steps** follow question style: Red/Blue voice, addressed to "you" the
  referee, verbatim `law_quote` per step, clause-level `law_reference`,
  practical `explanation`.
- **Scoring**: a chain counts as ONE question and only scores if every step
  is correct - keep chains to decisions a competent referee should link, not
  trivia sequences.
