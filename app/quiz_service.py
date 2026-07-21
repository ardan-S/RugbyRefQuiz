import random

from questions.loader import (
    get_available_laws_from_yaml,
    get_chain_bank,
    get_question_bank,
    get_topics,
    get_topic_chain_ids,
    get_topic_question_ids,
)

DIFFICULTIES = ['beginner', 'intermediate', 'advanced']
QUESTION_TYPES = ['factual', 'sanction', 'scenario', 'procedural',
                  'scenario_chain']


def get_available_laws():
    """Get list of available laws with their question counts."""
    return get_available_laws_from_yaml()


def get_available_topics():
    """Get curated practice topics keyed by slug."""
    return get_topics()


def get_question(question_id):
    """Look up a single question (with law metadata) by its ID."""
    return get_question_bank().get(question_id)


def get_questions(question_ids):
    """Look up multiple questions by ID, skipping any that no longer exist."""
    bank = get_question_bank()
    return [bank[qid] for qid in question_ids if qid in bank]


def get_quiz_item(item_id):
    """Look up a quiz item - a single question or a scenario chain - by ID."""
    return get_question_bank().get(item_id) or get_chain_bank().get(item_id)


def is_chain(item):
    """True if a quiz item is a scenario chain rather than a question."""
    return item is not None and item.get('kind') == 'chain'


def select_question_ids(selected_laws=None, topic_slugs=None,
                        difficulty=None, question_type=None,
                        difficulties=None, question_types=None):
    """
    Get IDs of all quiz items matching the given selection, in a stable order.

    Items are single questions plus scenario chains (which count as one
    question each). An item is included if it belongs to any selected law OR
    any selected topic (union). If neither laws nor topics are given, all
    items are candidates. Difficulty/type filters are then applied on top;
    the 'scenario_chain' type selects chains only, any other type excludes
    chains.

    Args:
        selected_laws: List of law numbers to include
        topic_slugs: List of curated topic slugs to include
        difficulty: Legacy single difficulty filter
        question_type: Legacy single question-type filter
        difficulties: Difficulties to include (OR within this filter)
        question_types: Question types to include (OR within this filter)

    Returns:
        List of question/chain IDs
    """
    laws = set(selected_laws or [])
    selected_difficulties = set(difficulties or [])
    selected_types = set(question_types or [])
    if difficulty:
        selected_difficulties.add(difficulty)
    if question_type:
        selected_types.add(question_type)
    topic_qids = set()
    topic_cids = set()
    for slug in topic_slugs or []:
        topic_qids.update(get_topic_question_ids(slug))
        topic_cids.update(get_topic_chain_ids(slug))

    restrict = bool(laws or topic_slugs)
    ids = []

    if not selected_types or selected_types - {'scenario_chain'}:
        for qid, q in get_question_bank().items():
            if restrict and q['law'] not in laws and qid not in topic_qids:
                continue
            if (selected_difficulties
                    and q.get('difficulty') not in selected_difficulties):
                continue
            if selected_types and q.get('type') not in selected_types:
                continue
            ids.append(qid)

    if not selected_types or 'scenario_chain' in selected_types:
        for cid, c in get_chain_bank().items():
            if (restrict and not laws.intersection(c.get('laws') or [])
                    and cid not in topic_cids):
                continue
            if (selected_difficulties
                    and c.get('difficulty') not in selected_difficulties):
                continue
            ids.append(cid)

    return ids


def check_answer(question, selected):
    """Check if the selected answer is correct (works for chain steps too)."""
    return selected in question['answers']


def shuffle_options(options):
    """Return a shuffled copy of the options list."""
    shuffled = options[:]
    random.shuffle(shuffled)
    return shuffled
