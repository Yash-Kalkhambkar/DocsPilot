#!/usr/bin/env python3
"""
Build release notes from git commit history.

Reads git log between two tags (or since a commit), groups conventional commit
messages (feat, fix, docs) into sections, and writes a Markdown release notes page.

Usage:
    python build_release_notes.py --from-tag v0.0.1 --to-tag v0.1.0 --output docs/release-notes/v0.1.0.md
    python build_release_notes.py --since-commit abc123 --output docs/release-notes/next.md

Exit code 0 on success, non-zero on failure.
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def run_git_command(args: List[str]) -> str:
    """Run git command and return output."""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)


def get_commits(from_ref: str = None, to_ref: str = "HEAD") -> List[str]:
    """Get commit messages between two refs.
    
    If from_ref is None, gets all commits up to to_ref.
    """
    if from_ref:
        # Get commits between from_ref and to_ref
        range_spec = f"{from_ref}..{to_ref}"
    else:
        # Get all commits up to to_ref
        range_spec = to_ref
    
    log_output = run_git_command(['log', range_spec, '--pretty=format:%s'])
    
    if not log_output:
        return []
    
    return log_output.split('\n')


def parse_conventional_commit(message: str) -> Dict[str, str]:
    """Parse conventional commit message.
    
    Format: type(scope): description
    
    Returns dict with 'type', 'scope', 'description', or None if not conventional format.
    """
    # Match type(scope): description or type: description
    pattern = r'^(\w+)(?:\(([^)]+)\))?: (.+)$'
    match = re.match(pattern, message.strip())
    
    if match:
        return {
            'type': match.group(1).lower(),
            'scope': match.group(2) if match.group(2) else '',
            'description': match.group(3),
        }
    
    return None


def group_commits(commits: List[str]) -> Dict[str, List[Dict]]:
    """Group commits by type (feat, fix, docs, etc.)."""
    groups = {
        'feat': [],
        'fix': [],
        'docs': [],
        'other': [],
    }
    
    for commit in commits:
        parsed = parse_conventional_commit(commit)
        
        if parsed:
            commit_type = parsed['type']
            if commit_type in groups:
                groups[commit_type].append(parsed)
            else:
                # Non-standard type, add to other
                groups['other'].append({
                    'type': commit_type,
                    'scope': parsed['scope'],
                    'description': parsed['description'],
                })
        else:
            # Not conventional format, add to other
            groups['other'].append({
                'type': 'other',
                'scope': '',
                'description': commit,
            })
    
    return groups


def format_release_notes(groups: Dict[str, List[Dict]], version: str = None, date: str = None) -> str:
    """Format grouped commits as Markdown release notes."""
    lines = []
    
    # Header
    if version:
        lines.append(f"# CreditShield {version}")
    else:
        lines.append("# CreditShield Release Notes")
    
    lines.append("")
    
    if date:
        lines.append(f"**Release Date:** {date}")
    else:
        lines.append(f"**Release Date:** {datetime.now().strftime('%Y-%m-%d')}")
    
    lines.append("")
    
    # Features
    if groups['feat']:
        lines.append("## Features")
        lines.append("")
        for commit in groups['feat']:
            scope_str = f" ({commit['scope']})" if commit['scope'] else ""
            lines.append(f"- {commit['description']}{scope_str}")
        lines.append("")
    
    # Fixes
    if groups['fix']:
        lines.append("## Bug Fixes")
        lines.append("")
        for commit in groups['fix']:
            scope_str = f" ({commit['scope']})" if commit['scope'] else ""
            lines.append(f"- {commit['description']}{scope_str}")
        lines.append("")
    
    # Documentation
    if groups['docs']:
        lines.append("## Documentation")
        lines.append("")
        for commit in groups['docs']:
            scope_str = f" ({commit['scope']})" if commit['scope'] else ""
            lines.append(f"- {commit['description']}{scope_str}")
        lines.append("")
    
    # Other
    if groups['other']:
        lines.append("## Other Changes")
        lines.append("")
        for commit in groups['other']:
            if commit['type'] != 'other':
                type_str = f"**{commit['type']}**: "
            else:
                type_str = ""
            scope_str = f" ({commit['scope']})" if commit['scope'] else ""
            lines.append(f"- {type_str}{commit['description']}{scope_str}")
        lines.append("")
    
    return '\n'.join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build release notes from git history")
    parser.add_argument('--from-tag', help='Start tag/commit (exclusive)')
    parser.add_argument('--to-tag', default='HEAD', help='End tag/commit (inclusive, default: HEAD)')
    parser.add_argument('--since-commit', help='Get commits since this commit (alias for --from-tag)')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--version', help='Version string for header (e.g., v0.1.0)')
    parser.add_argument('--date', help='Release date (default: today)')
    
    args = parser.parse_args()
    
    # Determine from reference
    from_ref = args.from_tag or args.since_commit
    
    # Get commits
    print(f"Fetching commits from {from_ref or 'beginning'} to {args.to_tag}...")
    commits = get_commits(from_ref, args.to_tag)
    
    if not commits:
        print("No commits found in range")
        sys.exit(1)
    
    print(f"Found {len(commits)} commits")
    
    # Group commits
    groups = group_commits(commits)
    
    # Format release notes
    release_notes = format_release_notes(groups, args.version, args.date)
    
    # Write to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(release_notes, encoding='utf-8')
    
    print(f"\nRelease notes written to: {output_path}")
    print(f"\n{'='*60}")
    print("Summary:")
    print(f"{'='*60}")
    print(f"Features: {len(groups['feat'])}")
    print(f"Bug Fixes: {len(groups['fix'])}")
    print(f"Documentation: {len(groups['docs'])}")
    print(f"Other: {len(groups['other'])}")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
