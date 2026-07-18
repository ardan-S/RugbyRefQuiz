import random

from questions.loader import (
    get_available_laws_from_yaml,
    get_question_bank,
)

DIFFICULTIES = ['beginner', 'intermediate', 'advanced']
QUESTION_TYPES = ['factual', 'sanction', 'scenario', 'procedural', 'hypothetical']


def get_available_laws():
    """Get list of available laws with their question counts."""
    return get_available_laws_from_yaml()


def get_question(question_id):
    """Look up a single question (with law metadata) by its ID."""
    return get_question_bank().get(question_id)


def get_questions(question_ids):
    """Look up multiple questions by ID, skipping any that no longer exist."""
    bank = get_question_bank()
    return [bank[qid] for qid in question_ids if qid in bank]


def select_question_ids(selected_laws=None, difficulty=None, question_type=None):
    """
    Get IDs of all questions matching the given filters.

    Args:
        selected_laws: List of law numbers to include (None = all)
        difficulty: Filter by difficulty ('beginner', 'intermediate', 'advanced')
        question_type: Filter by type ('factual', 'sanction', 'scenario', ...)

    Returns:
        List of question IDs
    """
    laws = set(selected_laws) if selected_laws else None
    ids = []
    for qid, q in get_question_bank().items():
        if laws is not None and q['law'] not in laws:
            continue
        if difficulty and q.get('difficulty') != difficulty:
            continue
        if question_type and q.get('type') != question_type:
            continue
        ids.append(qid)
    return ids


def check_answer(question, selected):
    """Check if the selected answer is correct."""
    return selected in question['answers']


def shuffle_options(options):
    """Return a shuffled copy of the options list."""
    shuffled = options[:]
    random.shuffle(shuffled)
    return shuffled
