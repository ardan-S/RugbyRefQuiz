import random
from flask import Blueprint, render_template, session, redirect, url_for, request

from app.quiz_service import (
    DIFFICULTIES,
    QUESTION_TYPES,
    get_available_laws,
    get_question,
    get_questions,
    select_question_ids,
    check_answer,
    shuffle_options,
)

bp = Blueprint('main', __name__)

QUIZ_SESSION_KEYS = (
    'quiz_ids', 'position', 'score', 'wrong', 'total',
    'current_id', 'current_options', 'selected_laws', 'filters',
)


def _clear_quiz_state():
    """Remove in-progress quiz keys, leaving the last result intact."""
    for key in QUIZ_SESSION_KEYS:
        session.pop(key, None)


def _start_quiz_with_ids(question_ids):
    """Initialise quiz session state from a list of question IDs."""
    session['quiz_ids'] = question_ids
    session['position'] = 0
    session['score'] = 0
    session['wrong'] = []
    session['total'] = len(question_ids)
    session['current_id'] = None
    session['current_options'] = []
    session.pop('last_result', None)


def _render_index(**kwargs):
    return render_template(
        'index.html',
        laws=get_available_laws(),
        difficulties=DIFFICULTIES,
        question_types=QUESTION_TYPES,
        **kwargs
    )


@bp.route('/')
def index():
    return _render_index()


@bp.route('/quiz/select-count', methods=['POST'])
def select_count():
    """Process law selection and filters, then show question count selection."""
    selected_laws = request.form.getlist('laws')

    if not selected_laws:
        return _render_index(error="Please select at least one law!")

    selected_laws = [int(law) for law in selected_laws]
    difficulty = request.form.get('difficulty') or None
    question_type = request.form.get('question_type') or None

    matching_ids = select_question_ids(
        selected_laws=selected_laws,
        difficulty=difficulty,
        question_type=question_type,
    )

    if not matching_ids:
        return _render_index(
            error="No questions match those filters - try widening them.",
            selected_laws=selected_laws,
            difficulty=difficulty,
            question_type=question_type,
        )

    session['selected_laws'] = selected_laws
    session['filters'] = {
        'difficulty': difficulty,
        'question_type': question_type,
    }

    return render_template('select_count.html',
                           max_questions=len(matching_ids),
                           difficulty=difficulty,
                           question_type=question_type)


@bp.route('/quiz/start', methods=['POST'])
def start_quiz():
    """Process question count and start quiz."""
    selected_laws = session.get('selected_laws')

    if not selected_laws:
        return redirect(url_for('main.index'))

    filters = session.get('filters', {})
    question_ids = select_question_ids(
        selected_laws=selected_laws,
        difficulty=filters.get('difficulty'),
        question_type=filters.get('question_type'),
    )
    max_questions = len(question_ids)

    count_choice = request.form.get('count')
    custom_count = request.form.get('custom_count')

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

    random.shuffle(question_ids)
    _start_quiz_with_ids(question_ids[:num_questions])

    return redirect(url_for('main.quiz'))


@bp.route('/quiz/retry-missed', methods=['POST'])
def retry_missed():
    """Start a new quiz containing only the questions missed last time."""
    last_result = session.get('last_result')
    missed_ids = [w['id'] for w in last_result['wrong']] if last_result else []

    if not missed_ids:
        return redirect(url_for('main.index'))

    random.shuffle(missed_ids)
    _start_quiz_with_ids(missed_ids)

    return redirect(url_for('main.quiz'))


@bp.route('/quiz')
def quiz():
    if 'quiz_ids' not in session:
        return redirect(url_for('main.index'))
    return render_template('quiz.html',
                           score=session.get('score', 0),
                           total=session.get('total', 0),
                           answered=session.get('position', 0))


@bp.route('/quiz/question')
def get_question_route():
    if 'quiz_ids' not in session:
        return redirect(url_for('main.index'))

    quiz_ids = session['quiz_ids']
    position = session.get('position', 0)

    if position >= len(quiz_ids):
        return render_template('partials/complete.html')

    question_id = quiz_ids[position]
    question = get_question(question_id)

    if question is None:
        # Question removed from the bank since the quiz started - skip it
        session['position'] = position + 1
        session['total'] = session.get('total', len(quiz_ids)) - 1
        return get_question_route()

    session['current_id'] = question_id
    options = shuffle_options(question['options'])
    session['current_options'] = options

    return render_template('partials/question.html',
                           question=question,
                           options=options,
                           question_num=position + 1,
                           total=session.get('total', len(quiz_ids)))


@bp.route('/quiz/answer', methods=['POST'])
def submit_answer():
    if 'quiz_ids' not in session or not session.get('current_id'):
        return redirect(url_for('main.index'))

    question_id = session['current_id']
    question = get_question(question_id)
    position = session.get('position', 0)
    selected = request.form.get('answer')

    if not selected:
        return render_template('partials/question.html',
                               question=question,
                               options=session.get('current_options', []),
                               question_num=position + 1,
                               total=session.get('total', 0),
                               error="Please select an answer!")

    is_correct = check_answer(question, selected)

    if is_correct:
        session['score'] = session.get('score', 0) + 1
    else:
        wrong = session.get('wrong', [])
        wrong.append({'id': question_id, 'selected': selected})
        session['wrong'] = wrong

    session['position'] = position + 1
    session['current_id'] = None

    return render_template('partials/feedback.html',
                           is_correct=is_correct,
                           selected=selected,
                           question=question,
                           score=session.get('score', 0),
                           answered=session['position'],
                           total=session.get('total', 0))


@bp.route('/quiz/results')
def results():
    if 'quiz_ids' in session:
        # Arriving from a quiz (finished or ended early): record the result
        session['last_result'] = {
            'score': session.get('score', 0),
            'answered': session.get('position', 0),
            'planned': session.get('total', 0),
            'wrong': session.get('wrong', []),
        }
        _clear_quiz_state()

    last_result = session.get('last_result')
    if last_result is None:
        return redirect(url_for('main.index'))

    wrong_by_id = {w['id']: w['selected'] for w in last_result['wrong']}
    missed_questions = [
        {'question': q, 'selected': wrong_by_id[q['id']]}
        for q in get_questions(list(wrong_by_id))
    ]

    answered = last_result['answered']
    planned = last_result['planned']

    return render_template(
        'results.html',
        score=last_result['score'],
        total=answered,
        answered_total=answered,
        planned_total=planned,
        ended_early=0 < answered < planned,
        missed_questions=missed_questions,
    )
