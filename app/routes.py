import random
from flask import Blueprint, render_template, session, redirect, url_for, request

from app.quiz_service import (
    load_questions_for_laws,
    get_available_laws,
    get_next_question_idx,
    check_answer,
    shuffle_options
)

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    laws = get_available_laws()
    return render_template('index.html', laws=laws)


@bp.route('/quiz/select-count', methods=['POST'])
def select_count():
    """Process law selection and show question count selection."""
    selected_laws = request.form.getlist('laws')

    if not selected_laws:
        laws = get_available_laws()
        return render_template('index.html', laws=laws,
                               error="Please select at least one law!")

    # Convert to integers
    selected_laws = [int(law) for law in selected_laws]

    # Store in session
    session['selected_laws'] = selected_laws

    # Get question count for selected laws
    questions = load_questions_for_laws(selected_laws)
    max_questions = len(questions)

    return render_template('select_count.html',
                           max_questions=max_questions,
                           selected_laws=selected_laws)


@bp.route('/quiz/start', methods=['POST'])
def start_quiz():
    """Process question count and start quiz."""
    selected_laws = session.get('selected_laws')

    if not selected_laws:
        return redirect(url_for('main.index'))

    # Get question count choice
    count_choice = request.form.get('count')
    custom_count = request.form.get('custom_count')

    questions = load_questions_for_laws(selected_laws)
    max_questions = len(questions)

    # Determine number of questions
    if count_choice == 'custom' and custom_count:
        try:
            num_questions = int(custom_count)
            num_questions = max(1, min(num_questions, max_questions))
        except ValueError:
            num_questions = max_questions
    elif count_choice == 'all':
        num_questions = max_questions
    else:
        try:
            num_questions = int(count_choice)
            num_questions = min(num_questions, max_questions)
        except (ValueError, TypeError):
            num_questions = max_questions

    # Shuffle and select questions
    random.shuffle(questions)
    selected_questions = questions[:num_questions]

    # Store questions in session (serialize to dicts)
    session['questions'] = [
        {'question': q.question, 'options': q.options, 'answers': q.answers}
        for q in selected_questions
    ]
    session['asked_idxs'] = []
    session['current_idx'] = None
    session['score'] = 0
    session['total'] = num_questions
    session['current_options'] = []

    return redirect(url_for('main.quiz'))


@bp.route('/quiz')
def quiz():
    if 'questions' not in session:
        return redirect(url_for('main.index'))
    return render_template('quiz.html',
                           score=session.get('score', 0),
                           total=session.get('total', 0),
                           answered=len(session.get('asked_idxs', [])))


@bp.route('/quiz/question')
def get_question():
    if 'questions' not in session:
        return redirect(url_for('main.index'))

    questions = session['questions']
    asked_idxs = session.get('asked_idxs', [])

    # Check if we've answered all questions
    if len(asked_idxs) >= session.get('total', len(questions)):
        return render_template('partials/complete.html')

    # Get next question index
    next_idx = get_next_question_idx(asked_idxs, len(questions))

    if next_idx is None:
        return render_template('partials/complete.html')

    session['current_idx'] = next_idx
    question = questions[next_idx]
    options = shuffle_options(question['options'])
    session['current_options'] = options

    return render_template('partials/question.html',
                           question=question['question'],
                           options=options,
                           question_num=len(asked_idxs) + 1,
                           total=session.get('total', len(questions)))


@bp.route('/quiz/answer', methods=['POST'])
def submit_answer():
    if 'questions' not in session or session.get('current_idx') is None:
        return redirect(url_for('main.index'))

    questions = session['questions']
    current_idx = session['current_idx']
    question = questions[current_idx]

    selected = request.form.get('answer')

    if not selected:
        # No answer selected
        options = session.get('current_options', [])
        return render_template('partials/question.html',
                               question=question['question'],
                               options=options,
                               question_num=len(session['asked_idxs']) + 1,
                               total=session.get('total', len(questions)),
                               error="Please select an answer!")

    is_correct = selected in question['answers']

    if is_correct:
        session['score'] = session.get('score', 0) + 1

    # Mark question as asked
    asked_idxs = session.get('asked_idxs', [])
    asked_idxs.append(current_idx)
    session['asked_idxs'] = asked_idxs

    return render_template('partials/feedback.html',
                           is_correct=is_correct,
                           selected=selected,
                           correct_answers=question['answers'],
                           score=session.get('score', 0),
                           answered=len(asked_idxs),
                           total=session.get('total', len(questions)))


@bp.route('/quiz/results')
def results():
    score = session.get('score', 0)
    planned_total = session.get('total', 0)
    answered_total = len(session.get('asked_idxs', []))
    total = answered_total
    ended_early = 0 < answered_total < planned_total
    # Clear session
    session.clear()
    return render_template(
        'results.html',
        score=score,
        total=total,
        answered_total=answered_total,
        planned_total=planned_total,
        ended_early=ended_early
    )
