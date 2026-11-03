#!/usr/bin/env python3
"""
Check internal and external links in Markdown documentation.

Scans all Markdown files in docs/ directory, extracts links, verifies:
- Internal links resolve to existing files
- Internal anchors resolve to existing headings
- External links return success HTTP status

Exit code 0 on success, non-zero on failure.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse
import requests

# Timeout for external link checks
EXTERNAL_TIMEOUT = 10

# Hosts that often have issues with automated checks (allow-list)
FLAKY_HOSTS = [
    "linkedin.com",
    "facebook.com",
    "twitter.com",
]


def find_markdown_files(docs_dir: Path) -> List[Path]:
    """Find all Markdown files in docs directory."""
    return list(docs_dir.rglob("*.md"))


def extract_links(content: str) -> List[Tuple[str, int]]:
    """Extract markdown links from content.
    
    Returns list of (link_target, line_number) tuples.
    """
    links = []
    # Match [text](url) format
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    for line_num, line in enumerate(content.split('\n'), start=1):
        for match in re.finditer(pattern, line):
            link_target = match.group(2)
            links.append((link_target, line_num))
    
    return links


def is_external(link: str) -> bool:
    """Check if link is external (starts with http:// or https://)."""
    return link.startswith('http://') or link.startswith('https://')


def check_internal_link(link: str, source_file: Path, docs_dir: Path) -> Tuple[bool, str]:
    """Check if internal link resolves.
    
    Returns (success, error_message).
    """
    # Split link and anchor
    if '#' in link:
        file_part, anchor = link.split('#', 1)
    else:
        file_part, anchor = link, None
    
    # Skip empty file part (anchor-only links in same file)
    if not file_part:
        # TODO: Validate anchor exists in source_file
        return True, ""
    
    # Resolve relative path
    if file_part.startswith('/'):
        # Absolute path from docs root
        target_path = docs_dir / file_part.lstrip('/')
    else:
        # Relative path from source file
        target_path = (source_file.parent / file_part).resolve()
    
    # Check file exists
    if not target_path.exists():
        return False, f"File not found: {target_path}"
    
    # Check anchor if present
    if anchor:
        # Read target file and check for heading
        try:
            target_content = target_path.read_text(encoding='utf-8')
            # Convert anchor to heading format
            # GitHub-style anchors: lowercase, spaces to hyphens, remove special chars
            expected_heading = anchor.lower().replace('-', ' ')
            headings = extract_headings(target_content)
            heading_ids = [heading_to_id(h) for h in headings]
            
            if anchor not in heading_ids:
                return False, f"Anchor #{anchor} not found in {target_path}"
        except Exception as e:
            return False, f"Error reading {target_path}: {e}"
    
    return True, ""


def extract_headings(content: str) -> List[str]:
    """Extract markdown headings from content."""
    headings = []
    for line in content.split('\n'):
        if line.strip().startswith('#'):
            # Remove leading # symbols and strip whitespace
            heading_text = line.lstrip('#').strip()
            headings.append(heading_text)
    return headings


def heading_to_id(heading: str) -> str:
    """Convert heading text to GitHub-style anchor ID."""
    # Lowercase, replace spaces with hyphens, remove special chars
    anchor_id = heading.lower()
    anchor_id = re.sub(r'[^\w\s-]', '', anchor_id)
    anchor_id = re.sub(r'[\s]+', '-', anchor_id)
    return anchor_id


def check_external_link(link: str) -> Tuple[bool, str]:
    """Check if external link returns success status.
    
    Returns (success, error_message).
    """
    # Check if host is in flaky list
    parsed = urlparse(link)
    if any(flaky in parsed.netloc for flaky in FLAKY_HOSTS):
        return True, f"Skipped (flaky host): {parsed.netloc}"
    
    try:
        response = requests.head(link, timeout=EXTERNAL_TIMEOUT, allow_redirects=True)
        # Accept 2xx and 3xx status codes
        if response.status_code < 400:
            return True, ""
        else:
            return False, f"HTTP {response.status_code}"
    except requests.Timeout:
        return False, "Timeout"
    except requests.RequestException as e:
        return False, f"Request error: {e}"


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
    
    total_links = 0
    failed_links = 0
    errors = []
    
    for md_file in md_files:
        rel_path = md_file.relative_to(project_root)
        content = md_file.read_text(encoding='utf-8')
        links = extract_links(content)
        
        for link_target, line_num in links:
            total_links += 1
            
            if is_external(link_target):
                # Check external link
                success, error_msg = check_external_link(link_target)
                if not success:
                    failed_links += 1
                    errors.append(f"{rel_path}:{line_num} - External link failed: {link_target} ({error_msg})")
                elif error_msg:
                    # Skipped link
                    print(f"  {rel_path}:{line_num} - {error_msg}")
            else:
                # Check internal link
                success, error_msg = check_internal_link(link_target, md_file, docs_dir)
                if not success:
                    failed_links += 1
                    errors.append(f"{rel_path}:{line_num} - Internal link failed: {link_target} ({error_msg})")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Link Check Summary")
    print(f"{'='*60}")
    print(f"Total links checked: {total_links}")
    print(f"Failed links: {failed_links}")
    
    if errors:
        print(f"\n{'='*60}")
        print("Errors:")
        print(f"{'='*60}")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("\nAll links valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
