# RugbyRefQuiz Roadmap

## Current State
- 579 questions across 21 laws — fully audited against the World Rugby Laws 2026
  (every question carries a verbatim law_quote, clause-level law_reference, and
  practical explanations; style per questions/STYLE_GUIDE.md)
- 15 pilot scenario chains (questions/scenarios/) — multi-step decision
  sequences with materiality calls, mixed into quizzes as single all-or-nothing
  questions; canonical-path continuation after a wrong step
- YAML-based question storage with schema validation
- Flask web app with HTMX + Tailwind/daisyUI
- Curated practice topics (questions/topics.yaml) and shareable seeded quiz links
- AI question generation tool (prototype)

---

## Top Recommendations for Rugby Referee Training

### 1. Show Explanations After Each Question (High Impact, Quick Win)
The YAML schema has an `explanation` field but it's never shown. For referee training, understanding *why* an answer is correct is more valuable than just knowing the answer. Display the law reference and explanation in the feedback screen.

### 2. Add Difficulty-Based Practice Modes
- **Beginner Mode**: Basic factual questions (what are the dimensions, how many players)
- **Match-Day Mode**: Intermediate sanctions and procedures
- **Advanced/Exam Mode**: Edge cases, multi-part scenarios

This maps to how referees actually progress: society courses → match experience → assessments.

### 3. Scenario/Video-Style Questions
Currently only 5 of 231 questions are "scenario" type. Real refereeing is about applying laws in dynamic situations. Add more questions like:
> "Blue 7 tackles White 12. Both go to ground. Blue 7 releases but stays lying across White 12. White 9 arrives and picks up the ball. What's your call?"

### 4. Wrong Answer Review / Weak Area Tracking
After a quiz, show which questions were missed and allow users to:
- Review just the ones they got wrong
- See which law areas they struggle with
- Focus future quizzes on weak areas

### 5. Complete Law Coverage
Finish the remaining law coverage and continue deepening the existing question bank, especially in higher-complexity areas.

### 6. Sanction Decision Trees
Many referee decisions follow: *"What happened?"* → *"What's the sanction?"* → *"Where's the restart?"*

### 7. Non-law section
- domestic law variations
- RFU processes (eg head contact, foul play)



Consider multi-part question sequences that mirror actual decision-making.

---

## Implementation Priority

### Quick Wins
- ~~Display question explanations in feedback~~ (done: feedback shows law reference + explanation)
- ~~Add difficulty filter to UI~~ (done)
- ~~Expose question type filtering~~ (done)
- ~~Review missed questions / retry the ones you got wrong~~ (done)
- ~~Server-side sessions~~ (done: quiz state no longer limited by the 4KB cookie)
- ~~Topic-driven practice~~ (done: curated topics in questions/topics.yaml)
- ~~Shareable quiz links~~ (done: seeded preset URLs give everyone identical quizzes)
- Implement quiz history/score tracking across sessions

### Medium-term
- Complete all 22 laws' questions
- Add user accounts with persistent storage
- Create performance dashboard showing weak areas
- Implement spaced repetition algorithm

### Advanced
- Add adaptive difficulty (adjust questions based on performance)
- Create mobile app native version
- Add peer/coach review of answers
- Integrate with official World Rugby resources
- Add match situation simulators

---

## Technical Gaps to Address
- No persistent user accounts or history
- No database (everything in YAML/sessions)
- No API for external tools
