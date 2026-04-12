# CLAUDE.md
## Project Overview

RugbyRefQuiz is a Flask web application for testing rugby refereeing knowledge against the Laws of the Game.

## Commands

**Run the application:**
```bash
python run.py
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
- `run.py` - Starts the local Flask development server
- `app/__init__.py` - Flask app factory
- `app/routes.py` - Quiz selection, question, answer, and results routes

### Question System
Questions are stored as YAML in `questions/data/` and loaded by `questions/loader.py`.

- `questions/schema.yaml` defines the structure for question files
- `tools/validate_questions.py` checks YAML files against the schema
- `app/quiz_service.py` provides the web app’s question-loading helpers

### Adding New Questions
1. Create or edit a YAML file in `questions/data/`
2. Follow the schema in `questions/schema.yaml`
3. Run `python tools/validate_questions.py`
4. Start the app with `python run.py` and test the quiz flow in the browser
