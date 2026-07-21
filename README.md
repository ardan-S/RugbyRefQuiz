# RugbyRefQuiz

Web-based quiz app for practising rugby refereeing knowledge against the Laws of the Game.

Live site: https://rugbyrefquiz.onrender.com

## What It Does

The app lets you:

- practise by curated topic (the breakdown, scrum, foul play, ...) or by law
- filter by difficulty and question type
- choose how many questions to answer
- work through a multiple-choice quiz in the browser
- get immediate feedback with the law reference and an explanation
- review the questions you missed and retry just those
- share a quiz link that gives everyone the same questions in the same order

Topics are defined in `questions/topics.yaml` - each topic maps to whole laws
plus cross-law tags, so "The Breakdown" pulls in tackle/ruck questions wherever
they live.

Question content is stored in YAML under `questions/data/` and validated against `questions/schema.yaml`.

## Stack

- Flask (with Flask-Session for server-side quiz state)
- HTMX
- Pico CSS
- YAML question bank with JSON Schema validation

## Run Locally

### Using `venv`

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Then open `http://127.0.0.1:5000`.

### Using Conda

```bash
conda env create -f environment.yml
conda activate RefQuiz
python run.py
```

## Deploy On Render

This repo includes a `render.yaml` blueprint for a single Python web service.

### What Render Will Use

- build command: `pip install -r requirements.txt`
- start command: `gunicorn --bind 0.0.0.0:$PORT run:app`
- health check: `/`
- generated secret: `SECRET_KEY`
- instance type: `free` by default in `render.yaml`

### Deploy Steps

1. Push this repo to GitHub.
2. In Render, create a new Blueprint or Web Service from the repository.
3. If Render detects `render.yaml`, accept the proposed service config.
4. Wait for the first deploy to finish.
5. Open the generated `onrender.com` URL.

### Notes

- The free plan is fine for testing and light personal use, but Render may spin the service down after inactivity.
- If you want faster wake-ups and a more reliable public-facing deployment, switch the service plan from `free` to `starter` in Render.
- If you already created a Render service manually, make sure its start command matches `gunicorn --bind 0.0.0.0:$PORT run:app`.

## Project Structure

```text
app/
  __init__.py            Flask app factory
  routes.py              Web routes and quiz session flow
  quiz_service.py        Question-loading and quiz helpers
  templates/             Jinja templates and HTMX partials
questions/
  data/                  YAML question files
  schema.yaml            Validation schema
  loader.py              YAML loading and filtering
tools/
  validate_questions.py  Validate question files
  generate_questions.py  Optional AI-assisted question generation
run.py                   Local development entry point
```

## Working With Questions

Validate all question files:

```bash
python tools/validate_questions.py
```

Validate one file:

```bash
python tools/validate_questions.py questions/data/law14_tackle.yaml
```

## Optional AI-Assisted Question Generation

`tools/generate_questions.py` can generate draft YAML questions from the bundled Laws PDF.

Extra requirements:

- `anthropic`
- `ANTHROPIC_API_KEY`

Example:

```bash
python tools/generate_questions.py --law 3 --section 3.5 --count 5
```

Generated questions should be reviewed and validated before being added to the quiz.
