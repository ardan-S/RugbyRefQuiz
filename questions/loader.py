"""
YAML question loader for RugbyRefQuiz.

Loads and validates question files from the questions/data/ directory.
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml
import jsonschema

from questions.utils import Question


# Directory containing YAML question files
DATA_DIR = Path(__file__).parent / "data"
SCHEMA_PATH = Path(__file__).parent / "schema.yaml"
TOPICS_PATH = Path(__file__).parent / "topics.yaml"
SCENARIOS_DIR = Path(__file__).parent / "scenarios"
SCENARIO_SCHEMA_PATH = Path(__file__).parent / "scenario_schema.yaml"


def _normalize_law_numbers(
    law_numbers: Optional[list[int]] = None
) -> Optional[tuple[int, ...]]:
    """Normalize a law-number filter into a cacheable tuple."""
    if law_numbers is None:
        return None
    return tuple(sorted(set(law_numbers)))


@lru_cache(maxsize=1)
def _load_schema() -> dict:
    """Load the JSON schema for question validation."""
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def validate_question_file(data: dict) -> list[str]:
    """
    Validate a question file against the schema.

    Args:
        data: Parsed YAML data from a question file

    Returns:
        List of validation error messages (empty if valid)
    """
    schema = _load_schema()
    errors = []

    validator = jsonschema.Draft202012Validator(schema)
    for error in validator.iter_errors(data):
        path = " -> ".join(str(p) for p in error.absolute_path) or "root"
        errors.append(f"{path}: {error.message}")

    # Additional validation: answers must be subset of options
    if 'questions' in data:
        for i, q in enumerate(data['questions']):
            if 'options' in q and 'answers' in q:
                invalid_answers = set(q['answers']) - set(q['options'])
                if invalid_answers:
                    errors.append(
                        f"questions[{i}].answers: {invalid_answers} not in options"
                    )

    return errors


def load_yaml_file(filepath: Path) -> dict:
    """Load and parse a single YAML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def _load_all_question_data() -> tuple[tuple[str, dict], ...]:
    """Read all question YAML files once per process."""
    if not DATA_DIR.exists():
        return ()

    all_data = []
    for yaml_file in sorted(DATA_DIR.glob("*.yaml")):
        data = load_yaml_file(yaml_file)
        if data:
            all_data.append((yaml_file.name, data))

    return tuple(all_data)


def _yaml_question_to_question(q: dict) -> Question:
    """Convert a YAML question dict to a Question object."""
    return Question(
        question=q['text'],
        options=q['options'],
        answers=q['answers']
    )


@lru_cache(maxsize=None)
def _load_questions_from_yaml_cached(
    law_numbers: Optional[tuple[int, ...]],
    validate: bool
) -> tuple[tuple[Question, ...], tuple[tuple[int, str, Optional[str]], ...]]:
    """Cached question and metadata loader backed by in-memory YAML data."""
    questions = []
    law_metadata = {}
    validation_errors = []

    for filename, data in _load_all_question_data():
        law_num = data.get('metadata', {}).get('law')

        if law_numbers is not None and law_num not in law_numbers:
            continue

        if validate:
            errors = validate_question_file(data)
            if errors:
                validation_errors.extend([f"{filename}: {e}" for e in errors])

        if law_num:
            law_metadata[law_num] = (
                law_num,
                data['metadata'].get('title', f'Law {law_num}'),
                data['metadata'].get('source'),
            )

        for q in data.get('questions', []):
            questions.append(_yaml_question_to_question(q))

    if validation_errors:
        raise ValueError(
            "Question file validation errors:\n" + "\n".join(validation_errors)
        )

    return tuple(questions), tuple(sorted(law_metadata.values()))


def load_questions_from_yaml(
    law_numbers: Optional[list[int]] = None,
    validate: bool = True
) -> tuple[list[Question], dict[int, dict]]:
    """
    Load questions from YAML files.

    Args:
        law_numbers: Optional list of law numbers to load. If None, loads all.
        validate: Whether to validate files against schema (default True)

    Returns:
        Tuple of (list of Question objects, dict of law metadata)

    Raises:
        ValueError: If validation is enabled and files contain errors
    """
    question_items, law_metadata_items = _load_questions_from_yaml_cached(
        _normalize_law_numbers(law_numbers),
        validate
    )

    law_metadata = {
        number: {'number': number, 'name': name, 'source': source}
        for number, name, source in law_metadata_items
    }
    return list(question_items), law_metadata


@lru_cache(maxsize=1)
def _get_available_laws_cached() -> tuple[tuple[int, str, int], ...]:
    """Cached list of laws with question counts."""
    laws = {}

    for _, data in _load_all_question_data():
        if 'metadata' not in data:
            continue

        law_num = data['metadata'].get('law')
        if law_num is None:
            continue

        question_count = len(data.get('questions', []))

        if law_num not in laws:
            laws[law_num] = (
                law_num,
                data['metadata'].get('title', f'Law {law_num}'),
                question_count,
            )
        else:
            _, title, existing_count = laws[law_num]
            laws[law_num] = (law_num, title, existing_count + question_count)

    return tuple(sorted(laws.values()))


def get_available_laws_from_yaml() -> dict[int, dict]:
    """
    Get list of available laws with their question counts from YAML files.

    Returns:
        Dict mapping law number to law info with question_count
    """
    return {
        number: {
            'number': number,
            'name': name,
            'question_count': question_count,
        }
        for number, name, question_count in _get_available_laws_cached()
    }


def load_questions_for_laws_yaml(selected_laws: Optional[list[int]] = None) -> list[Question]:
    """
    Load questions for specified laws from YAML files.

    Args:
        selected_laws: List of law numbers to load, or None for all

    Returns:
        List of Question objects
    """
    questions, _ = load_questions_from_yaml(law_numbers=selected_laws, validate=False)
    return questions


@lru_cache(maxsize=1)
def get_question_bank() -> dict[str, dict]:
    """
    Get all questions keyed by their unique ID, with law metadata merged in.

    Each value is the full question dict from YAML plus:
        law: law number
        law_title: human-readable law title

    Returns:
        Dict mapping question ID to question dict
    """
    bank = {}

    for _, data in _load_all_question_data():
        metadata = data.get('metadata', {})
        law_num = metadata.get('law')
        law_title = metadata.get('title', f'Law {law_num}')

        for q in data.get('questions', []):
            bank[q['id']] = {**q, 'law': law_num, 'law_title': law_title}

    return bank


@lru_cache(maxsize=1)
def _load_scenario_schema() -> dict:
    """Load the JSON schema for scenario chain validation."""
    with open(SCENARIO_SCHEMA_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def validate_scenario_file(data: dict) -> list[str]:
    """
    Validate a scenario chain file against the scenario schema.

    Returns:
        List of validation error messages (empty if valid)
    """
    schema = _load_scenario_schema()
    errors = []

    validator = jsonschema.Draft202012Validator(schema)
    for error in validator.iter_errors(data):
        path = " -> ".join(str(p) for p in error.absolute_path) or "root"
        errors.append(f"{path}: {error.message}")

    # Additional validation: each step's answers must be a subset of options
    for i, chain in enumerate(data.get('chains', [])):
        for j, step in enumerate(chain.get('steps', [])):
            if 'options' in step and 'answers' in step:
                invalid = set(step['answers']) - set(step['options'])
                if invalid:
                    errors.append(
                        f"chains[{i}].steps[{j}].answers: {invalid} not in options"
                    )

    return errors


@lru_cache(maxsize=1)
def _load_all_scenario_data() -> tuple[tuple[str, dict], ...]:
    """Read all scenario chain YAML files once per process."""
    if not SCENARIOS_DIR.exists():
        return ()

    all_data = []
    for yaml_file in sorted(SCENARIOS_DIR.glob("*.yaml")):
        data = load_yaml_file(yaml_file)
        if data:
            all_data.append((yaml_file.name, data))

    return tuple(all_data)


@lru_cache(maxsize=1)
def get_chain_bank() -> dict[str, dict]:
    """
    Get all scenario chains keyed by their unique ID.

    Each value is the full chain dict from YAML plus:
        kind: 'chain' (distinguishes chains from single questions)
        law_details: law numbers paired with their human-readable names

    Returns:
        Dict mapping chain ID to chain dict
    """
    bank = {}
    law_titles = {
        number: name
        for number, name, _ in _get_available_laws_cached()
    }

    for _, data in _load_all_scenario_data():
        for chain in data.get('chains', []):
            law_details = [
                {
                    'number': law_number,
                    'name': law_titles.get(law_number, f'Law {law_number}'),
                }
                for law_number in chain.get('laws', [])
            ]
            bank[chain['id']] = {
                **chain,
                'kind': 'chain',
                'law_details': law_details,
            }

    return bank


@lru_cache(maxsize=1)
def _load_topics() -> tuple[dict, ...]:
    """
    Load curated topics from topics.yaml and resolve their question IDs.

    A question belongs to a topic if its law is in the topic's `laws` list
    or any of its tags appear in the topic's `tags` list.
    """
    if not TOPICS_PATH.exists():
        return ()

    data = load_yaml_file(TOPICS_PATH) or {}
    bank = get_question_bank()
    chain_bank = get_chain_bank()

    topics = []
    for topic in data.get('topics', []):
        slug = topic.get('slug')
        if not slug:
            continue

        laws = set(topic.get('laws') or [])
        tags = set(topic.get('tags') or [])

        question_ids = tuple(
            qid for qid, q in bank.items()
            if q['law'] in laws or tags.intersection(q.get('tags') or [])
        )
        chain_ids = tuple(
            cid for cid, c in chain_bank.items()
            if laws.intersection(c.get('laws') or [])
            or tags.intersection(c.get('tags') or [])
        )

        topics.append({
            'slug': slug,
            'name': topic.get('name', slug),
            'description': topic.get('description', ''),
            'question_ids': question_ids,
            'chain_ids': chain_ids,
            'question_count': len(question_ids) + len(chain_ids),
        })

    return tuple(topics)


def get_topics() -> dict[str, dict]:
    """Get curated topics keyed by slug (without their question ID lists)."""
    return {
        t['slug']: {k: t[k] for k in ('slug', 'name', 'description', 'question_count')}
        for t in _load_topics()
    }


def get_topic_question_ids(slug: str) -> tuple[str, ...]:
    """Get the question IDs belonging to a topic (empty if unknown slug)."""
    for t in _load_topics():
        if t['slug'] == slug:
            return t['question_ids']
    return ()


def get_topic_chain_ids(slug: str) -> tuple[str, ...]:
    """Get the scenario chain IDs belonging to a topic (empty if unknown)."""
    for t in _load_topics():
        if t['slug'] == slug:
            return t['chain_ids']
    return ()


def get_questions_with_metadata(
    law_numbers: Optional[list[int]] = None,
    difficulty: Optional[str] = None,
    question_type: Optional[str] = None,
    tags: Optional[list[str]] = None
) -> list[dict]:
    """
    Load questions with full metadata, supporting filtering.

    Args:
        law_numbers: Filter by law numbers
        difficulty: Filter by difficulty level
        question_type: Filter by question type
        tags: Filter by tags (questions must have at least one matching tag)

    Returns:
        List of question dicts with all metadata
    """
    results = []

    normalized_laws = _normalize_law_numbers(law_numbers)

    for _, data in _load_all_question_data():
        law_num = data.get('metadata', {}).get('law')

        if normalized_laws is not None and law_num not in normalized_laws:
            continue

        for q in data.get('questions', []):
            # Apply filters
            if difficulty and q.get('difficulty') != difficulty:
                continue
            if question_type and q.get('type') != question_type:
                continue
            if tags:
                q_tags = set(q.get('tags', []))
                if not q_tags.intersection(set(tags)):
                    continue

            # Add law info to question
            q_with_law = {**q, 'law': law_num}
            results.append(q_with_law)

    return results
