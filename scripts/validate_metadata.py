#!/usr/bin/env python3
"""
Validate YAML front matter in documentation topics.

Checks that every Markdown file in docs/ has:
- Valid YAML front matter
- Required keys: title, topic_type, audience, product_version, last_reviewed, ai_assisted, reviewed_by
- Valid topic_type values: concept, task, reference, release_notes
- ISO date format for last_reviewed
- If ai_assisted is true, reviewed_by must be non-empty

Exit code 0 on success, non-zero on failure.
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import yaml


REQUIRED_KEYS = [
    "title",
    "topic_type",
    "audience",
    "product_version",
    "last_reviewed",
    "ai_assisted",
    "reviewed_by",
]

VALID_TOPIC_TYPES = ["concept", "task", "reference", "release_notes"]


def find_markdown_files(docs_dir: Path) -> List[Path]:
    """Find all Markdown files in docs directory."""
    return list(docs_dir.rglob("*.md"))


def extract_front_matter(content: str) -> Tuple[bool, Dict, str]:
    """Extract YAML front matter from markdown content.
    
    Returns (has_front_matter, front_matter_dict, error_message).
    """
    # Check if file starts with ---
    if not content.startswith('---'):
        return False, {}, "No front matter found (must start with ---)"
    
    # Find closing ---
    lines = content.split('\n')
    closing_index = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            closing_index = i
            break
    
    if closing_index == -1:
        return False, {}, "Front matter not properly closed (missing closing ---)"
    
    # Extract YAML content
    yaml_content = '\n'.join(lines[1:closing_index])
    
    # Parse YAML
    try:
        front_matter = yaml.safe_load(yaml_content)
        if not isinstance(front_matter, dict):
            return False, {}, "Front matter is not a valid YAML dictionary"
        return True, front_matter, ""
    except yaml.YAMLError as e:
        return False, {}, f"YAML parsing error: {e}"


def validate_front_matter(front_matter: Dict) -> List[str]:
    """Validate front matter contains required keys and valid values.
    
    Returns list of error messages (empty if valid).
    """
    errors = []
    
    # Check required keys
    for key in REQUIRED_KEYS:
        if key not in front_matter:
            errors.append(f"Missing required key: {key}")
    
    # If required keys missing, return early
    if errors:
        return errors
    
    # Validate topic_type
    topic_type = front_matter.get("topic_type", "")
    if topic_type not in VALID_TOPIC_TYPES:
        errors.append(f"Invalid topic_type: '{topic_type}'. Must be one of: {', '.join(VALID_TOPIC_TYPES)}")
    
    # Validate last_reviewed is ISO date (YYYY-MM-DD)
    last_reviewed = front_matter.get("last_reviewed", "")
    if not validate_iso_date(last_reviewed):
        errors.append(f"Invalid last_reviewed date: '{last_reviewed}'. Must be ISO format (YYYY-MM-DD)")
    
    # Validate ai_assisted is boolean
    ai_assisted = front_matter.get("ai_assisted")
    if not isinstance(ai_assisted, bool):
        errors.append(f"Invalid ai_assisted value: '{ai_assisted}'. Must be true or false")
    
    # If ai_assisted is true, reviewed_by must be non-empty
    if ai_assisted is True:
        reviewed_by = front_matter.get("reviewed_by", "")
        if not reviewed_by or reviewed_by.strip() == "":
            errors.append("ai_assisted is true but reviewed_by is empty. AI-assisted topics must be reviewed.")
    
    return errors


def validate_iso_date(date_str: str) -> bool:
    """Validate string is ISO date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(str(date_str), "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


def main():
    """Main entry point."""
    # Find docs directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / "docs"
    
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        sys.exit(1)
    
    # Find all markdown files
    md_files = find_markdown_files(docs_dir)
    print(f"Found {len(md_files)} Markdown files")
    
    total_files = len(md_files)
    failed_files = 0
    all_errors = []
    
    for md_file in md_files:
        rel_path = md_file.relative_to(project_root)
        content = md_file.read_text(encoding='utf-8')
        
        # Extract front matter
        has_fm, front_matter, error_msg = extract_front_matter(content)
        
        if not has_fm:
            failed_files += 1
            all_errors.append(f"{rel_path}: {error_msg}")
            continue
        
        # Validate front matter
        errors = validate_front_matter(front_matter)
        if errors:
            failed_files += 1
            for error in errors:
                all_errors.append(f"{rel_path}: {error}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Metadata Validation Summary")
    print(f"{'='*60}")
    print(f"Total files checked: {total_files}")
    print(f"Failed files: {failed_files}")
    
    if all_errors:
        print(f"\n{'='*60}")
        print("Errors:")
        print(f"{'='*60}")
        for error in all_errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("\nAll metadata valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
