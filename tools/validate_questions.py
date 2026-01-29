#!/usr/bin/env python3
"""
Validation script for YAML question files.

Usage:
    python tools/validate_questions.py [path]

If no path is provided, validates all files in questions/data/.

Exit codes:
    0: All files valid
    1: Validation errors found
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from questions.loader import load_yaml_file, validate_question_file


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

    return validate_question_file(data)


def validate_directory(dirpath: Path) -> dict[str, list[str]]:
    """
    Validate all YAML files in a directory.

    Returns:
        Dict mapping filename to list of errors
    """
    results = {}

    for yaml_file in sorted(dirpath.glob("*.yaml")):
        if yaml_file.name == "schema.yaml":
            continue

        errors = validate_file(yaml_file)
        if errors:
            results[yaml_file.name] = errors

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Validate YAML question files against schema'
    )
    parser.add_argument(
        'path',
        nargs='?',
        help='Path to validate (file or directory). Defaults to questions/data/'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show details for valid files too'
    )
    args = parser.parse_args()

    # Determine path to validate
    if args.path:
        target = Path(args.path)
    else:
        target = Path(__file__).parent.parent / 'questions' / 'data'

    if not target.exists():
        print(f"Error: Path does not exist: {target}")
        sys.exit(1)

    # Validate
    if target.is_file():
        errors = validate_file(target)
        if errors:
            print(f"INVALID: {target.name}")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print(f"VALID: {target.name}")
            sys.exit(0)

    elif target.is_dir():
        yaml_files = list(target.glob("*.yaml"))
        yaml_files = [f for f in yaml_files if f.name != "schema.yaml"]

        if not yaml_files:
            print(f"No YAML files found in {target}")
            sys.exit(0)

        results = validate_directory(target)
        valid_count = len(yaml_files) - len(results)
        invalid_count = len(results)

        # Print results
        print(f"Validated {len(yaml_files)} files in {target}")
        print()

        if args.verbose:
            for yaml_file in yaml_files:
                if yaml_file.name not in results:
                    print(f"  VALID: {yaml_file.name}")

        if results:
            print()
            for filename, errors in results.items():
                print(f"  INVALID: {filename}")
                for error in errors:
                    print(f"    - {error}")

        print()
        print(f"Summary: {valid_count} valid, {invalid_count} invalid")

        sys.exit(1 if invalid_count > 0 else 0)

    else:
        print(f"Error: Path is not a file or directory: {target}")
        sys.exit(1)


if __name__ == '__main__':
    main()
