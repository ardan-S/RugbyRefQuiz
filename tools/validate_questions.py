#!/usr/bin/env python3
"""
Validation script for YAML question and scenario chain files.

Usage:
    python tools/validate_questions.py [path]

If no path is provided, validates all files in questions/data/ and
questions/scenarios/. Files containing a top-level `chains` key are
validated against the scenario schema; everything else against the
question schema.

Exit codes:
    0: All files valid
    1: Validation errors found
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from questions.loader import (  # noqa: E402
    load_yaml_file,
    validate_question_file,
    validate_scenario_file,
)

SKIP_NAMES = {"schema.yaml", "scenario_schema.yaml", "topics.yaml"}


def validate_file(filepath: Path) -> list[str]:
    """
    Validate a single YAML file.

    Returns:
        List of error messages (empty if valid)
    """
    try:
        data = load_yaml_file(filepath)
    except Exception as e:
        return [f"Failed to parse YAML: {e}"]

    if not data:
        return ["File is empty or invalid"]

    if 'chains' in data:
        return validate_scenario_file(data)
    return validate_question_file(data)


def validate_directory(dirpath: Path) -> dict[str, list[str]]:
    """
    Validate all YAML files in a directory.

    Returns:
        Dict mapping filename to list of errors
    """
    results = {}

    for yaml_file in sorted(dirpath.glob("*.yaml")):
        if yaml_file.name in SKIP_NAMES:
            continue

        errors = validate_file(yaml_file)
        if errors:
            results[yaml_file.name] = errors

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Validate YAML question/scenario files against schema'
    )
    parser.add_argument(
        'path',
        nargs='?',
        help='Path to validate (file or directory). Defaults to '
             'questions/data/ and questions/scenarios/'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show details for valid files too'
    )
    args = parser.parse_args()

    # Determine paths to validate
    if args.path:
        targets = [Path(args.path)]
    else:
        base = Path(__file__).parent.parent / 'questions'
        targets = [base / 'data']
        if (base / 'scenarios').exists():
            targets.append(base / 'scenarios')

    for target in targets:
        if not target.exists():
            print(f"Error: Path does not exist: {target}")
            sys.exit(1)

    if len(targets) == 1 and targets[0].is_file():
        target = targets[0]
        errors = validate_file(target)
        if errors:
            print(f"INVALID: {target.name}")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print(f"VALID: {target.name}")
            sys.exit(0)

    total_files = 0
    total_invalid = 0

    for target in targets:
        if not target.is_dir():
            print(f"Error: Path is not a file or directory: {target}")
            sys.exit(1)

        yaml_files = [f for f in target.glob("*.yaml")
                      if f.name not in SKIP_NAMES]

        if not yaml_files:
            print(f"No YAML files found in {target}")
            continue

        results = validate_directory(target)
        total_files += len(yaml_files)
        total_invalid += len(results)

        print(f"Validated {len(yaml_files)} files in {target}")

        if args.verbose:
            for yaml_file in yaml_files:
                if yaml_file.name not in results:
                    print(f"  VALID: {yaml_file.name}")

        for filename, errors in results.items():
            print(f"  INVALID: {filename}")
            for error in errors:
                print(f"    - {error}")

        print()

    print(f"Summary: {total_files - total_invalid} valid, "
          f"{total_invalid} invalid")

    sys.exit(1 if total_invalid > 0 else 0)


if __name__ == '__main__':
    main()
