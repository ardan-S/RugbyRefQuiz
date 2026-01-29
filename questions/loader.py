"""
YAML Question Loader for RugbyRefQuiz

Loads and validates question files from the questions/data/ directory.
Returns Question objects compatible with the existing quiz system.
"""

import os
from pathlib import Path
from typing import Optional

import yaml
import jsonschema

from questions.utils import Question, QuestionSet


# Directory containing YAML question files
DATA_DIR = Path(__file__).parent / "data"
SCHEMA_PATH = Path(__file__).parent / "schema.yaml"


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


def _yaml_question_to_question(q: dict) -> Question:
    """Convert a YAML question dict to a Question object."""
    return Question(
        question=q['text'],
        options=q['options'],
        answers=q['answers']
    )


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
    questions = []
    law_metadata = {}
    validation_errors = []

    if not DATA_DIR.exists():
        return questions, law_metadata

    for yaml_file in sorted(DATA_DIR.glob("*.yaml")):
        data = load_yaml_file(yaml_file)

        if not data:
            continue

        law_num = data.get('metadata', {}).get('law')

        # Skip if filtering by law number and this isn't in the list
        if law_numbers is not None and law_num not in law_numbers:
            continue

        # Validate if requested
        if validate:
            errors = validate_question_file(data)
            if errors:
                validation_errors.extend([f"{yaml_file.name}: {e}" for e in errors])

        # Store metadata
        if law_num:
            law_metadata[law_num] = {
                'number': law_num,
                'name': data['metadata'].get('title', f'Law {law_num}'),
                'source': data['metadata'].get('source'),
            }

        # Convert questions
        for q in data.get('questions', []):
            questions.append(_yaml_question_to_question(q))

    if validation_errors:
        raise ValueError(
            "Question file validation errors:\n" + "\n".join(validation_errors)
        )

    return questions, law_metadata


def get_available_laws_from_yaml() -> dict[int, dict]:
    """
    Get list of available laws with their question counts from YAML files.

    Returns:
        Dict mapping law number to law info with question_count
    """
    laws = {}

    if not DATA_DIR.exists():
        return laws

    for yaml_file in sorted(DATA_DIR.glob("*.yaml")):
        data = load_yaml_file(yaml_file)

        if not data or 'metadata' not in data:
            continue

        law_num = data['metadata'].get('law')
        if law_num is None:
            continue

        question_count = len(data.get('questions', []))

        if law_num not in laws:
            laws[law_num] = {
                'number': law_num,
                'name': data['metadata'].get('title', f'Law {law_num}'),
                'question_count': question_count
            }
        else:
            laws[law_num]['question_count'] += question_count

    return dict(sorted(laws.items()))


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

    if not DATA_DIR.exists():
        return results

    for yaml_file in sorted(DATA_DIR.glob("*.yaml")):
        data = load_yaml_file(yaml_file)

        if not data:
            continue

        law_num = data.get('metadata', {}).get('law')

        if law_numbers is not None and law_num not in law_numbers:
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
