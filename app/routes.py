import random
from flask import Blueprint, render_template, session, redirect, url_for, request

from app.quiz_service import (
    DIFFICULTIES,
    QUESTION_TYPES,
    get_available_laws,
    get_available_topics,
    get_questions,
    get_quiz_item,
    is_chain,
    select_question_ids,
    check_answer,
    shuffle_options,
)

bp = Blueprint('main', __name__)


def _clear_quiz_state():
    """Remove in-progress quiz keys, leaving the last result and selection."""
    for key in ('quiz_ids', 'position', 'score', 'wrong', 'total',
                'current_id', 'current_options',
                'chain_step', 'chain_ok', 'chain_steps'):
        session.pop(key, None)


def _clear_chain_state():
    """Remove the per-chain progress keys."""
    for key in ('chain_step', 'chain_ok', 'chain_steps'):
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
        topics=get_available_topics(),
        difficulties=DIFFICULTIES,
        question_types=QUESTION_TYPES,
        **kwargs
    )


def _selection_filter_values(selection, plural_key, singular_key):
    """Read a multi-value filter, including legacy single-value sessions."""
    values = selection.get(plural_key)
    if values is not None:
        return values
    value = selection.get(singular_key)
    return [value] if value else []


def _selection_question_ids(selection):
    """Get the matching question IDs for a stored selection dict."""
    difficulties = _selection_filter_values(
        selection, 'difficulties', 'difficulty'
    )
    question_types = _selection_filter_values(
        selection, 'question_types', 'question_type'
    )

    return select_question_ids(
        selected_laws=selection.get('laws'),
        topic_slugs=selection.get('topics'),
        difficulties=difficulties,
        question_types=question_types,
    )


def _share_url(selection, seed):
    """Build the absolute shareable preset URL for a selection (no count)."""
    params = {}
    difficulties = _selection_filter_values(
        selection, 'difficulties', 'difficulty'
    )
    question_types = _selection_filter_values(
        selection, 'question_types', 'question_type'
    )
    if selection.get('laws'):
        params['laws'] = ','.join(str(n) for n in selection['laws'])
    if selection.get('topics'):
        params['topics'] = ','.join(selection['topics'])
    if difficulties:
        params['difficulty'] = ','.join(difficulties)
    if question_types:
        params['type'] = ','.join(question_types)
    params['seed'] = seed
    return url_for('main.preset', _external=True, **params)


def _render_select_count(selection, seed):
    """Render the question-count page for a stored selection."""
    matching_ids = _selection_question_ids(selection)
    difficulties = _selection_filter_values(
        selection, 'difficulties', 'difficulty'
    )
    question_types = _selection_filter_values(
        selection, 'question_types', 'question_type'
    )

    laws = get_available_laws()
    topics = get_available_topics()
    selected_law_names = [
        f"Law {n}: {laws[n]['name']}" for n in selection.get('laws') or []
        if n in laws
    ]
    selected_topic_names = [
        topics[s]['name'] for s in selection.get('topics') or []
        if s in topics
    ]

    return render_template('select_count.html',
                           max_questions=len(matching_ids),
                           selected_topic_names=selected_topic_names,
                           selected_law_names=selected_law_names,
                           selected_difficulties=difficulties,
                           selected_question_types=question_types,
                           share_url_base=_share_url(selection, seed))


@bp.route('/')
def index():
    return _render_index()


@bp.route('/quiz/select-count', methods=['POST'])
def select_count():
    """Process law/topic selection and filters, then show count selection."""
    known_topics = get_available_topics()
    selected_laws = [int(law) for law in request.form.getlist('laws')]
    selected_topics = [t for t in request.form.getlist('topics')
                       if t in known_topics]

    if not selected_laws and not selected_topics:
        return _render_index(error="Please select at least one topic or law!")

    selected_difficulties = [
        value for value in DIFFICULTIES
        if value in request.form.getlist('difficulties')
    ]
    selected_question_types = [
        value for value in QUESTION_TYPES
        if value in request.form.getlist('question_types')
    ]

    selection = {
        'laws': selected_laws,
        'topics': selected_topics,
        'difficulties': selected_difficulties,
        'question_types': selected_question_types,
    }

    if not _selection_question_ids(selection):
        return _render_index(
            error="No questions match that selection - try widening it.",
            selected_laws=selected_laws,
            selected_topics=selected_topics,
            selected_difficulties=selected_difficulties,
            selected_question_types=selected_question_types,
        )

    session['selection'] = selection
    session['quiz_seed'] = random.randrange(10 ** 8)

    return _render_select_count(selection, session['quiz_seed'])


@bp.route('/quiz/preset')
def preset():
    """Start or stage a quiz from a shareable URL.

    Example: /quiz/preset?topics=breakdown&laws=9
             &difficulty=beginner,advanced&type=factual,scenario_chain
             &seed=1234&count=20
    With a seed, everyone opening the same link gets the same questions in
    the same order.
    """
    known_topics = get_available_topics()

    try:
        laws = [int(n) for n in request.args.get('laws', '').split(',') if n]
    except ValueError:
        laws = []
    laws = [n for n in laws if 1 <= n <= 21]
    topics = [t for t in request.args.get('topics', '').split(',')
              if t in known_topics]

    if not laws and not topics:
        return _render_index(
            error="That shared quiz link doesn't match any questions.")

    requested_difficulties = set(
        request.args.get('difficulty', '').split(',')
    )
    requested_question_types = set(request.args.get('type', '').split(','))
    selection = {
        'laws': laws,
        'topics': topics,
        'difficulties': [
            value for value in DIFFICULTIES
            if value in requested_difficulties
        ],
        'question_types': [
            value for value in QUESTION_TYPES
            if value in requested_question_types
        ],
    }

    matching_ids = _selection_question_ids(selection)
    if not matching_ids:
        return _render_index(
            error="That shared quiz link doesn't match any questions.")

    try:
        seed = int(request.args.get('seed', ''))
    except ValueError:
        seed = random.randrange(10 ** 8)

    session['selection'] = selection
    session['quiz_seed'] = seed

    count = request.args.get('count')
    if not count:
        return _render_select_count(selection, seed)

    if count == 'all':
        num_questions = len(matching_ids)
    else:
        try:
            num_questions = max(1, min(int(count), len(matching_ids)))
        except ValueError:
            num_questions = len(matching_ids)

    random.Random(seed).shuffle(matching_ids)
    _start_quiz_with_ids(matching_ids[:num_questions])
    return redirect(url_for('main.quiz'))


@bp.route('/quiz/start', methods=['POST'])
def start_quiz():
    """Process question count and start quiz."""
    selection = session.get('selection')

    if not selection:
        return redirect(url_for('main.index'))

    question_ids = _selection_question_ids(selection)
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

    seed = session.get('quiz_seed')
    if seed is not None:
        random.Random(seed).shuffle(question_ids)
    else:
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

    item_id = quiz_ids[position]
    item = get_quiz_item(item_id)

    if item is None:
        # Item removed from the bank since the quiz started - skip it
        session['position'] = position + 1
        session['total'] = session.get('total', len(quiz_ids)) - 1
        return get_question_route()

    total = session.get('total', len(quiz_ids))

    if is_chain(item):
        if session.get('current_id') != item_id:
            # First step of this chain: reset per-chain progress
            session['current_id'] = item_id
            session['chain_step'] = 0
            session['chain_ok'] = True
            session['chain_steps'] = []

        step_index = session.get('chain_step', 0)
        step = item['steps'][step_index]
        options = shuffle_options(step['options'])
        session['current_options'] = options

        return render_template('partials/chain_question.html',
                               chain=item,
                               step=step,
                               options=options,
                               step_num=step_index + 1,
                               step_total=len(item['steps']),
                               question_num=position + 1,
                               total=total)

    session['current_id'] = item_id
    _clear_chain_state()
    options = shuffle_options(item['options'])
    session['current_options'] = options

    return render_template('partials/question.html',
                           question=item,
                           options=options,
                           question_num=position + 1,
                           total=total)


def _submit_chain_answer(chain, position, selected):
    """Handle an answer to the current step of a scenario chain."""
    step_index = session.get('chain_step', 0)
    step = chain['steps'][step_index]
    step_total = len(chain['steps'])
    total = session.get('total', 0)

    if not selected:
        return render_template('partials/chain_question.html',
                               chain=chain,
                               step=step,
                               options=session.get('current_options', []),
                               step_num=step_index + 1,
                               step_total=step_total,
                               question_num=position + 1,
                               total=total,
                               error="Please select an answer!")

    is_correct = check_answer(step, selected)
    chain_steps = session.get('chain_steps', [])
    chain_steps.append({'selected': selected, 'correct': is_correct})
    session['chain_steps'] = chain_steps
    if not is_correct:
        session['chain_ok'] = False

    is_last = step_index + 1 >= step_total
    chain_ok = session.get('chain_ok', False)

    if is_last:
        # All-or-nothing: the chain scores one point only if every step
        # was answered correctly
        if chain_ok:
            session['score'] = session.get('score', 0) + 1
        else:
            wrong = session.get('wrong', [])
            wrong.append({'id': chain['id'], 'steps': chain_steps})
            session['wrong'] = wrong
        session['position'] = position + 1
        session['current_id'] = None
        _clear_chain_state()
    else:
        session['chain_step'] = step_index + 1

    return render_template('partials/chain_feedback.html',
                           chain=chain,
                           step=step,
                           is_correct=is_correct,
                           selected=selected,
                           step_num=step_index + 1,
                           step_total=step_total,
                           is_last=is_last,
                           chain_ok=chain_ok,
                           correct_steps=sum(
                               1 for s in chain_steps if s['correct']),
                           score=session.get('score', 0),
                           answered=session.get('position', position),
                           total=total)


@bp.route('/quiz/answer', methods=['POST'])
def submit_answer():
    if 'quiz_ids' not in session or not session.get('current_id'):
        return redirect(url_for('main.index'))

    item_id = session['current_id']
    item = get_quiz_item(item_id)
    position = session.get('position', 0)
    selected = request.form.get('answer')

    if is_chain(item):
        return _submit_chain_answer(item, position, selected)

    if not selected:
        return render_template('partials/question.html',
                               question=item,
                               options=session.get('current_options', []),
                               question_num=position + 1,
                               total=session.get('total', 0),
                               error="Please select an answer!")

    is_correct = check_answer(item, selected)

    if is_correct:
        session['score'] = session.get('score', 0) + 1
    else:
        wrong = session.get('wrong', [])
        wrong.append({'id': item_id, 'selected': selected})
        session['wrong'] = wrong

    session['position'] = position + 1
    session['current_id'] = None

    return render_template('partials/feedback.html',
                           is_correct=is_correct,
                           selected=selected,
                           question=item,
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

    wrong_by_id = {w['id']: w['selected'] for w in last_result['wrong']
                   if 'steps' not in w}
    missed_questions = [
        {'question': q, 'selected': wrong_by_id[q['id']]}
        for q in get_questions(list(wrong_by_id))
    ]

    missed_chains = []
    for w in last_result['wrong']:
        if 'steps' not in w:
            continue
        chain = get_quiz_item(w['id'])
        if not is_chain(chain):
            continue
        missed_chains.append({
            'chain': chain,
            'steps': [
                {'step': step, 'selected': result['selected'],
                 'correct': result['correct']}
                for step, result in zip(chain['steps'], w['steps'])
            ],
        })

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
        missed_chains=missed_chains,
    )
