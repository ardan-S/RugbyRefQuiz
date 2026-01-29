# CLAUDE.md
## Project Overview

RugbyRefQuiz is a PyQt5 desktop application for testing rugby refereeing knowledge based on the Laws of the Game.

## Commands

**Run the application:**
```bash
conda activate RefQuiz
python quiz.py
```

**Lint:**
```bash
flake8
```

**Environment setup:**
```bash
conda env create -f environment.yml
conda activate RefQuiz
```

### Entry Point
- `quiz.py` - Contains `QuizApp` class (PyQt5 QWidget) that runs the quiz

### Question System
Questions are in `questions/` directory, organized by Law number:
- Each law file (e.g., `Law1_TheGround.py`) exports `QuestionSet` objects named `standard_questions_LX` and optionally `sanction_questions_LX`
- `questions/utils.py` defines:
  - `Question(question, options, answers)` - Single question with text, list of options, and list of correct answers
  - `QuestionSet(name, questions)` - Named collection of Question objects
  - `answer_sets` - Reusable answer option lists for common question types

### Adding New Questions
1. Create or edit a law file in `questions/`
2. Import `Question`, `QuestionSet`, and optionally `answer_sets` from `questions.utils`
3. Create a `QuestionSet` with your questions
4. Import and add the `QuestionSet` to `all_questions` list in `quiz.py`
