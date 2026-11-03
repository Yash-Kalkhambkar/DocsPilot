"""Tests for build_release_notes.py script."""

import pytest
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from build_release_notes import (
    parse_conventional_commit,
    group_commits,
    format_release_notes,
)


def test_parse_conventional_commit_with_scope():
    """Test parsing conventional commit with scope."""
    message = "feat(api): add borrower authentication endpoints"
    result = parse_conventional_commit(message)
    
    assert result is not None
    assert result["type"] == "feat"
    assert result["scope"] == "api"
    assert result["description"] == "add borrower authentication endpoints"


def test_parse_conventional_commit_without_scope():
    """Test parsing conventional commit without scope."""
    message = "fix: resolve database connection timeout"
    result = parse_conventional_commit(message)
    
    assert result is not None
    assert result["type"] == "fix"
    assert result["scope"] == ""
    assert result["description"] == "resolve database connection timeout"


def test_parse_conventional_commit_invalid():
    """Test parsing non-conventional commit message."""
    message = "This is not a conventional commit"
    result = parse_conventional_commit(message)
    
    assert result is None


def test_group_commits():
    """Test grouping commits by type."""
    commits = [
        "feat(api): add new endpoint",
        "fix: fix bug",
        "docs: update README",
        "Non-conventional commit message",
        "feat: add feature",
    ]
    
    groups = group_commits(commits)
    
    assert len(groups["feat"]) == 2
    assert len(groups["fix"]) == 1
    assert len(groups["docs"]) == 1
    assert len(groups["other"]) == 1


def test_format_release_notes():
    """Test formatting release notes markdown."""
    groups = {
        "feat": [
            {"type": "feat", "scope": "api", "description": "add borrower auth"},
            {"type": "feat", "scope": "", "description": "add RAG support"},
        ],
        "fix": [
            {"type": "fix", "scope": "db", "description": "fix connection leak"},
        ],
        "docs": [],
        "other": [],
    }
    
    markdown = format_release_notes(groups, version="v0.1.0", date="2026-11-03")
    
    assert "# CreditShield v0.1.0" in markdown
    assert "**Release Date:** 2026-11-03" in markdown
    assert "## Features" in markdown
    assert "add borrower auth (api)" in markdown
    assert "add RAG support" in markdown
    assert "## Bug Fixes" in markdown
    assert "fix connection leak (db)" in markdown
    # No docs or other sections since empty
    assert "## Documentation" not in markdown
    assert "## Other Changes" not in markdown
