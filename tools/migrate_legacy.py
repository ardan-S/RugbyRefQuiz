#!/usr/bin/env python3
"""
Migration script to convert legacy Python question files to YAML format.

Usage:
    python tools/migrate_legacy.py [--dry-run]

This script:
1. Reads existing Python question files from questions/
2. Converts them to YAML format with inferred metadata
3. Writes YAML files to questions/data/
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

# Add parent directory to path to import question modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from questions.utils import answer_sets


# Law names for metadata
LAW_NAMES = {
    1: "The Ground",
    2: "The Ball",
    3: "The Team",
    4: "Players' Clothing",
    5: "Time",
    6: "Match Officials",
    7: "Advantage",
    8: "Scoring",
    9: "Foul Play",
    10: "Offside and Onside in Open Play",
    11: "Knock-On or Throw Forward",
    12: "Touch and Lineout",
    13: "Mark",
    14: "Tackle",
    15: "Ruck",
    16: "Maul",
    17: "Scrum",
    18: "Penalty and Free-Kick",
    19: "Scrum, Lineout, Restart, Free-Kick",
    20: "Goal",
    21: "In-Goal",
    22: "Touch In-Goal and Beyond",
}


def infer_question_type(question_text: str, set_name: str) -> str:
    """Infer question type from question text and set name."""
    text_lower = question_text.lower()
    set_lower = set_name.lower()

    if 'sanction' in set_lower:
        return 'sanction'
    if any(word in text_lower for word in ['sanction:', 'award:', 'penalty']):
        return 'sanction'
    if any(word in text_lower for word in ['scenario', 'situation', 'what happens']):
        return 'scenario'
    if any(word in text_lower for word in ['true or false', 'true/false']):
        return 'factual'
    if 'procedure' in text_lower or 'process' in text_lower:
        return 'procedural'
    return 'factual'


def infer_difficulty(question_text: str, options: list[str], set_name: str) -> str:
    """Infer difficulty from question characteristics."""
    text_lower = question_text.lower()
    set_lower = set_name.lower()

    # Sanction questions are typically intermediate or advanced
    if 'sanction' in set_lower:
        return 'intermediate'

    # True/False questions are typically beginner
    if any(word in text_lower for word in ['true or false', 'true/false']):
        return 'beginner'

    # Questions with many options or complex scenarios are advanced
    if len(options) > 5 or len(question_text) > 200:
        return 'advanced'

    # Multi-select questions (indicated by "(2 correct answers)") are harder
    if 'correct answers' in text_lower:
        return 'advanced'

    return 'intermediate'


def extract_law_reference(question_text: str, law_num: int) -> str | None:
    """Try to extract law reference from question text."""
    # Look for patterns like "Law 3.5" or "3.5" at start of comments
    patterns = [
        rf'Law\s*{law_num}\.(\d+(?:\.\d+)*)',
        rf'^{law_num}\.(\d+(?:\.\d+)*)',
    ]
    for pattern in patterns:
        match = re.search(pattern, question_text)
        if match:
            return f"{law_num}.{match.group(1)}"
    return f"{law_num}"


def generate_tags(question_text: str, set_name: str) -> list[str]:
    """Generate tags based on question content."""
    tags = []
    text_lower = question_text.lower()

    # Common rugby terms to tag
    tag_keywords = {
        'scrum': 'scrum',
        'lineout': 'lineout',
        'line-out': 'lineout',
        'ruck': 'ruck',
        'maul': 'maul',
        'tackle': 'tackle',
        'kick': 'kick',
        'penalty': 'penalty',
        'try': 'try',
        'conversion': 'conversion',
        'goal': 'goal',
        'offside': 'offside',
        'knock-on': 'knock-on',
        'knock on': 'knock-on',
        'forward pass': 'forward-pass',
        'advantage': 'advantage',
        'injury': 'injury',
        'blood': 'blood-injury',
        'replacement': 'replacement',
        'substitut': 'substitution',
        'front row': 'front-row',
        'front-row': 'front-row',
        'prop': 'front-row',
        'hooker': 'front-row',
        'referee': 'referee',
        'touch judge': 'touch-judge',
        'assistant referee': 'assistant-referee',
        'captain': 'captain',
        'clothing': 'clothing',
        'jersey': 'clothing',
        'boots': 'boots',
        'studs': 'boots',
        'time': 'time',
        'half-time': 'half-time',
        'water': 'water-break',
        'foul play': 'foul-play',
        'red card': 'red-card',
        'yellow card': 'yellow-card',
        'suspension': 'suspension',
        'sending off': 'sending-off',
        'sent off': 'sending-off',
    }

    for keyword, tag in tag_keywords.items():
        if keyword in text_lower and tag not in tags:
            tags.append(tag)

    # Add set type tag
    if 'sanction' in set_name.lower():
        if 'sanction' not in tags:
            tags.append('sanction')

    return tags[:5]  # Limit to 5 tags


def normalize_answer(answer, options: list[str]) -> str:
    """Normalize answer to ensure it matches an option exactly."""
    if isinstance(answer, str):
        return answer
    if isinstance(answer, list) and len(answer) == 1:
        return answer[0]
    return str(answer)


def convert_question_set(question_set, law_num: int) -> list[dict]:
    """Convert a QuestionSet to list of YAML-compatible question dicts."""
    questions = []
    set_name = question_set.name

    for idx, q in enumerate(question_set.questions):
        # Normalize answers to list
        answers = q.answers if isinstance(q.answers, list) else [q.answers]
        answers = [str(a) for a in answers]

        # Generate unique ID
        q_id = f"L{law_num:02d}-{idx + 1:03d}"

        question_dict = {
            'id': q_id,
            'text': q.question.strip().replace('\\', ''),
            'type': infer_question_type(q.question, set_name),
            'difficulty': infer_difficulty(q.question, q.options, set_name),
            'options': [str(o) for o in q.options],
            'answers': answers,
            'law_reference': extract_law_reference(q.question, law_num),
            'tags': generate_tags(q.question, set_name),
            'explanation': None,
            'contributor': None,
        }

        questions.append(question_dict)

    return questions


def create_yaml_file(law_num: int, questions: list[dict]) -> dict:
    """Create YAML file structure for a law."""
    return {
        'metadata': {
            'law': law_num,
            'title': LAW_NAMES.get(law_num, f'Law {law_num}'),
            'source': 'World Rugby Laws 2026',
        },
        'questions': questions,
    }


def custom_yaml_representer(dumper, data):
    """Custom YAML representer for multi-line strings."""
    if isinstance(data, str) and ('\n' in data or len(data) > 80):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(str, custom_yaml_representer)


def migrate_questions(dry_run: bool = False) -> dict[int, int]:
    """
    Migrate all legacy Python question files to YAML.

    Returns:
        Dict mapping law number to question count
    """
    questions_dir = Path(__file__).parent.parent / 'questions'
    data_dir = questions_dir / 'data'

    if not dry_run:
        data_dir.mkdir(exist_ok=True)

    # Mapping of law numbers to question sets
    law_questions: dict[int, list[dict]] = {}

    # Import and process each law file
    question_files = [
        ('Law1_TheGround', 1),
        ('Law2_TheBall', 2),
        ('Law3_Team', 3),
        ('Law4_PlayersClothing', 4),
        ('Law5_Time', 5),
        ('Law6_MatchOfficials', 6),
        ('Law7_Advantage', 7),
        ('Law8_Scoring', 8),
        ('Law14_Tackle', 14),
    ]

    for module_name, law_num in question_files:
        try:
            module = __import__(f'questions.{module_name}', fromlist=[''])

            # Find all QuestionSet objects in the module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, 'questions') and hasattr(attr, 'name'):
                    # It's a QuestionSet
                    questions = convert_question_set(attr, law_num)

                    if law_num not in law_questions:
                        law_questions[law_num] = []
                    law_questions[law_num].extend(questions)

                    print(f"  Converted {len(questions)} questions from {attr.name}")

        except ImportError as e:
            print(f"  Warning: Could not import {module_name}: {e}")
        except Exception as e:
            print(f"  Error processing {module_name}: {e}")

    # Renumber questions per law and write YAML files
    result = {}
    for law_num in sorted(law_questions.keys()):
        questions = law_questions[law_num]

        # Renumber questions sequentially
        for idx, q in enumerate(questions):
            q['id'] = f"L{law_num:02d}-{idx + 1:03d}"

        result[law_num] = len(questions)

        yaml_data = create_yaml_file(law_num, questions)
        law_title = LAW_NAMES.get(law_num, 'unknown').lower().replace(' ', '_').replace("'", '')
        filename = f"law{law_num:02d}_{law_title}.yaml"
        filepath = data_dir / filename

        if dry_run:
            print(f"  Would write {len(questions)} questions to {filename}")
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"  Wrote {len(questions)} questions to {filename}")

    return result


def main():
    parser = argparse.ArgumentParser(description='Migrate legacy Python questions to YAML')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without writing files')
    args = parser.parse_args()

    print("Migrating legacy question files to YAML format...")
    print()

    result = migrate_questions(dry_run=args.dry_run)

    print()
    print("Summary:")
    total = 0
    for law_num, count in sorted(result.items()):
        print(f"  Law {law_num}: {count} questions")
        total += count

    print()
    print(f"Total: {total} questions migrated")

    if args.dry_run:
        print()
        print("(Dry run - no files were written)")


if __name__ == '__main__':
    main()
