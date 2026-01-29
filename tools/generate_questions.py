#!/usr/bin/env python3
"""
AI-assisted question generation from Laws of the Game PDF.

Usage:
    python tools/generate_questions.py --law 3 --section 3.5 --count 5

Requirements:
    - PyMuPDF (fitz) for PDF text extraction
    - anthropic SDK for Claude API access
    - ANTHROPIC_API_KEY environment variable

This script:
1. Extracts text from the specified law section of the PDF
2. Sends the text to Claude with a structured prompt
3. Outputs candidate questions in YAML format
4. Marks questions as 'contributor: ai-generated' for review
"""

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import anthropic
except ImportError:
    anthropic = None

import yaml

# Path to the Laws PDF
PDF_PATH = Path(__file__).parent.parent / "2026en-laws-of-the-game-compressed.pdf"

# Approximate page ranges for each law (0-indexed, adjust as needed)
# These are estimates - actual pages may vary by PDF version
LAW_PAGE_RANGES = {
    1: (28, 32),    # The Ground
    2: (32, 33),    # The Ball
    3: (33, 38),    # The Team
    4: (38, 40),    # Players' Clothing
    5: (40, 43),    # Time
    6: (43, 52),    # Match Officials
    7: (52, 54),    # Advantage
    8: (54, 60),    # Scoring
    9: (60, 72),    # Foul Play
    10: (72, 75),   # Offside and Onside in Open Play
    11: (75, 77),   # Knock-On or Throw Forward
    12: (77, 88),   # Touch and Lineout
    13: (88, 90),   # Mark
    14: (90, 94),   # Tackle
    15: (94, 98),   # Ruck
    16: (98, 101),  # Maul
    17: (101, 120), # Scrum
    18: (120, 124), # Penalty and Free-Kick
    19: (124, 130), # Scrum, Lineout, Restart, Free-Kick
    20: (130, 132), # Goal
    21: (132, 136), # In-Goal
    22: (136, 140), # Touch In-Goal and Beyond
}

# Law titles for reference
LAW_TITLES = {
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


def extract_text_from_pdf(pdf_path: Path, start_page: int = 0, end_page: int = None) -> str:
    """
    Extract text from a PDF file.

    Args:
        pdf_path: Path to PDF file
        start_page: First page to extract (0-indexed)
        end_page: Last page to extract (exclusive), None for all

    Returns:
        Extracted text as a string
    """
    if fitz is None:
        raise ImportError("PyMuPDF (fitz) is required. Install with: pip install PyMuPDF")

    doc = fitz.open(pdf_path)
    text_parts = []

    if end_page is None:
        end_page = len(doc)

    for page_num in range(start_page, min(end_page, len(doc))):
        page = doc[page_num]
        text_parts.append(page.get_text())

    doc.close()
    return "\n".join(text_parts)


def extract_law_section(pdf_text: str, law_number: int, section: str = None) -> str:
    """
    Extract a specific law section from the full PDF text.

    Args:
        pdf_text: Full PDF text
        law_number: Law number (1-22)
        section: Optional section reference like "3.5"

    Returns:
        Extracted section text
    """
    # Look for law headers like "LAW 3" or "Law 3"
    law_pattern = rf'LAW\s+{law_number}\b[:\s]*(.*?)(?=LAW\s+\d+\b|$)'
    match = re.search(law_pattern, pdf_text, re.IGNORECASE | re.DOTALL)

    if not match:
        # Try alternate patterns
        law_pattern = rf'Law\s+{law_number}\s*[-:]\s*(.*?)(?=Law\s+\d+|$)'
        match = re.search(law_pattern, pdf_text, re.IGNORECASE | re.DOTALL)

    if match:
        law_text = match.group(0)

        if section:
            # Try to extract specific section
            section_pattern = rf'{section}\s+(.*?)(?=\d+\.\d+|$)'
            section_match = re.search(section_pattern, law_text, re.DOTALL)
            if section_match:
                return section_match.group(0)

        return law_text[:5000]  # Limit text length

    return ""


def generate_questions_prompt(law_text: str, law_number: int, count: int = 5) -> str:
    """Generate the prompt for Claude to create questions."""
    law_title = LAW_TITLES.get(law_number, f"Law {law_number}")

    return f"""You are generating quiz questions for rugby referee training based on the Laws of the Game.

LAW {law_number}: {law_title}

LAW TEXT:
{law_text}

Generate exactly {count} quiz questions following this YAML structure. Output ONLY valid YAML with no additional text.

Requirements:
- Mix of types: factual (direct law knowledge), sanction (what penalty applies), scenario (situation-based)
- Include difficulty levels: beginner (basic facts), intermediate (application), advanced (edge cases)
- Each question should have 4 options with exactly one correct answer
- Add a brief explanation referencing the specific law text
- Add relevant tags (lowercase, hyphenated)
- Use law_reference format like "{law_number}.1" or "{law_number}.5.2"

Output format (YAML only, no markdown code blocks):
- id: L{law_number:02d}-NEW-001
  text: "Your question text here?"
  type: factual
  difficulty: intermediate
  options:
    - "Option A"
    - "Option B"
    - "Option C"
    - "Option D"
  answers:
    - "Option B"
  law_reference: "{law_number}.1"
  tags:
    - relevant-tag
  explanation: "Brief explanation referencing the law."
  contributor: ai-generated

Generate {count} questions now:"""


def call_claude_api(prompt: str) -> str:
    """
    Call Claude API to generate questions.

    Returns:
        Generated YAML text
    """
    if anthropic is None:
        raise ImportError("anthropic SDK is required. Install with: pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def parse_generated_yaml(yaml_text: str) -> list[dict]:
    """
    Parse the generated YAML text into question dicts.

    Args:
        yaml_text: YAML text from Claude

    Returns:
        List of question dictionaries
    """
    # Clean up the text - remove any markdown code block markers
    yaml_text = yaml_text.strip()
    if yaml_text.startswith("```"):
        # Remove opening ```yaml or ``` and closing ```
        yaml_text = re.sub(r'^```(?:yaml)?\s*', '', yaml_text)
        yaml_text = re.sub(r'\s*```$', '', yaml_text)

    try:
        questions = yaml.safe_load(yaml_text)
        if isinstance(questions, list):
            return questions
        return []
    except yaml.YAMLError as e:
        print(f"Warning: Could not parse YAML: {e}", file=sys.stderr)
        return []


def generate_questions(
    law_number: int,
    section: str = None,
    count: int = 5,
    output_file: str = None
) -> list[dict]:
    """
    Generate questions for a law section.

    Args:
        law_number: Law number (1-22)
        section: Optional section reference
        count: Number of questions to generate
        output_file: Optional file to write YAML output

    Returns:
        List of generated question dicts
    """
    print(f"Extracting text from PDF for Law {law_number}...")

    # Extract PDF text
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found at {PDF_PATH}")

    pdf_text = extract_text_from_pdf(PDF_PATH)
    law_text = extract_law_section(pdf_text, law_number, section)

    if not law_text:
        print(f"Warning: Could not extract text for Law {law_number}", file=sys.stderr)
        print("Using generic prompt without law text...", file=sys.stderr)
        law_text = f"[Law {law_number}: {LAW_TITLES.get(law_number, 'Unknown')}]"

    print(f"Extracted {len(law_text)} characters of law text")
    print(f"Generating {count} questions with Claude API...")

    # Generate prompt and call API
    prompt = generate_questions_prompt(law_text, law_number, count)
    response = call_claude_api(prompt)

    # Parse response
    questions = parse_generated_yaml(response)

    print(f"Generated {len(questions)} questions")

    # Output
    if output_file:
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(questions, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"Wrote questions to {output_file}")
    else:
        print("\nGenerated questions (YAML):\n")
        print(yaml.dump(questions, default_flow_style=False, allow_unicode=True, sort_keys=False))

    return questions


def main():
    parser = argparse.ArgumentParser(
        description='Generate quiz questions from Laws of the Game PDF using AI'
    )
    parser.add_argument(
        '--law', '-l',
        type=int,
        required=True,
        choices=range(1, 23),
        help='Law number (1-22)'
    )
    parser.add_argument(
        '--section', '-s',
        type=str,
        default=None,
        help='Specific section reference (e.g., "3.5")'
    )
    parser.add_argument(
        '--count', '-c',
        type=int,
        default=5,
        help='Number of questions to generate (default: 5)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output file path (default: print to stdout)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Extract text only, do not call API'
    )
    args = parser.parse_args()

    # Check dependencies
    if fitz is None:
        print("Error: PyMuPDF is required. Install with: pip install PyMuPDF", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run and anthropic is None:
        print("Error: anthropic SDK is required. Install with: pip install anthropic", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f"Extracting text for Law {args.law}...")
        if not PDF_PATH.exists():
            print(f"Error: PDF not found at {PDF_PATH}", file=sys.stderr)
            sys.exit(1)

        pdf_text = extract_text_from_pdf(PDF_PATH)
        law_text = extract_law_section(pdf_text, args.law, args.section)

        if law_text:
            print(f"\nExtracted {len(law_text)} characters:\n")
            print(law_text[:2000])
            if len(law_text) > 2000:
                print(f"\n... ({len(law_text) - 2000} more characters)")
        else:
            print("No text extracted for this law section.")
        sys.exit(0)

    try:
        generate_questions(
            law_number=args.law,
            section=args.section,
            count=args.count,
            output_file=args.output
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
