import random

from questions.loader import (
    get_available_laws_from_yaml,
    load_questions_for_laws_yaml,
    get_questions_with_metadata,
)


def get_available_laws():
    """Get list of available laws with their question counts."""
    return get_available_laws_from_yaml()


def load_questions_for_laws(selected_laws=None):
    """Load questions for specified laws. If None, load all."""
    return load_questions_for_laws_yaml(selected_laws)


def load_all_questions():
    """Flatten all question sets into a single list of questions."""
    return load_questions_for_laws_yaml(None)


def load_questions_filtered(
    selected_laws=None,
    difficulty=None,
    question_type=None,
    tags=None
):
    """
    Load questions with filtering support.

    Args:
        selected_laws: List of law numbers to include
        difficulty: Filter by difficulty ('beginner', 'intermediate', 'advanced')
        question_type: Filter by type ('factual', 'sanction', 'scenario', etc.)
        tags: Filter by tags (questions must have at least one matching tag)

    Returns:
        List of question dicts with full metadata
    """
    return get_questions_with_metadata(
        law_numbers=selected_laws,
        difficulty=difficulty,
        question_type=question_type,
        tags=tags
    )


def get_next_question_idx(asked_idxs, total):
    """Get a random unasked question index."""
    if len(asked_idxs) >= total:
        return None
    available = [i for i in range(total) if i not in asked_idxs]
    return random.choice(available)


def check_answer(question, selected):
    """Check if the selected answer is correct."""
    return selected in question.answers


def shuffle_options(options):
    """Return a shuffled copy of the options list."""
    shuffled = options[:]
    random.shuffle(shuffled)
    return shuffled
