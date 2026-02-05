# RugbyRefQuiz Roadmap

## Current State (January 2026)
- 231 questions across 8 laws (of 22)
- YAML-based question storage with schema validation
- Flask web app with HTMX
- PyQt5 desktop app
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
Missing 14 laws including critical ones:
- **Law 9 (Foul Play)** - Most complex and important for referees
- **Law 15-17 (Ruck, Maul, Scrum)** - Core breakdown/set piece laws
- **Law 10 (Offside)** - Common mistakes for new referees

### 6. Sanction Decision Trees
Many referee decisions follow: *"What happened?"* → *"What's the sanction?"* → *"Where's the restart?"*

### 7. Non-law section
- domestic law variations
- RFU processes (eg head contact, foul play)



Consider multi-part question sequences that mirror actual decision-making.

---

## Implementation Priority

### Quick Wins
- Display question explanations in feedback
- Add difficulty filter to UI
- Expose question type filtering
- Implement quiz history/score tracking

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
- Desktop app has session/state limitations
