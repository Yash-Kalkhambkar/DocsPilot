"""Tests for validate_metadata.py script."""

import pytest
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_metadata import (
    extract_front_matter,
    validate_front_matter,
    validate_iso_date,
)


def test_extract_front_matter_valid():
    """Test extracting valid YAML front matter."""
    content = """---
title: Test Topic
topic_type: concept
---

# Test Topic

Content here.
"""
    has_fm, front_matter, error = extract_front_matter(content)
    
    assert has_fm is True
    assert front_matter["title"] == "Test Topic"
    assert front_matter["topic_type"] == "concept"
    assert error == ""


def test_extract_front_matter_missing():
    """Test handling missing front matter."""
    content = """# Test Topic

No front matter here.
"""
    has_fm, front_matter, error = extract_front_matter(content)
    
    assert has_fm is False
    assert "No front matter found" in error


def test_extract_front_matter_invalid_yaml():
    """Test handling invalid YAML."""
    content = """---
title: Test
invalid yaml here: [unclosed bracket
---

Content.
"""
    has_fm, front_matter, error = extract_front_matter(content)
    
    assert has_fm is False
    assert "YAML parsing error" in error


def test_validate_front_matter_missing_required():
    """Test validation catches missing required keys."""
    front_matter = {
        "title": "Test",
        # Missing other required keys
    }
    
    errors = validate_front_matter(front_matter)
    
    assert len(errors) > 0
    assert any("Missing required key" in error for error in errors)


def test_validate_front_matter_invalid_topic_type():
    """Test validation catches invalid topic_type."""
    front_matter = {
        "title": "Test",
        "topic_type": "invalid_type",
        "audience": "developers",
        "product_version": "0.1.0",
        "last_reviewed": "2026-11-03",
        "ai_assisted": False,
        "reviewed_by": "",
    }
    
    errors = validate_front_matter(front_matter)
    
    assert len(errors) > 0
    assert any("Invalid topic_type" in error for error in errors)


def test_validate_front_matter_invalid_date():
    """Test validation catches invalid date format."""
    front_matter = {
        "title": "Test",
        "topic_type": "concept",
        "audience": "developers",
        "product_version": "0.1.0",
        "last_reviewed": "Nov 3, 2026",  # Not ISO format
        "ai_assisted": False,
        "reviewed_by": "",
    }
    
    errors = validate_front_matter(front_matter)
    
    assert len(errors) > 0
    assert any("Invalid last_reviewed date" in error for error in errors)


def test_validate_front_matter_ai_assisted_without_reviewer():
    """Test validation catches ai_assisted=true with empty reviewed_by."""
    front_matter = {
        "title": "Test",
        "topic_type": "concept",
        "audience": "developers",
        "product_version": "0.1.0",
        "last_reviewed": "2026-11-03",
        "ai_assisted": True,
        "reviewed_by": "",  # Empty reviewer
    }
    
    errors = validate_front_matter(front_matter)
    
    assert len(errors) > 0
    assert any("reviewed_by is empty" in error for error in errors)


def test_validate_front_matter_valid():
    """Test validation passes for valid front matter."""
    front_matter = {
        "title": "Test Topic",
        "topic_type": "concept",
        "audience": "developers",
        "product_version": "0.1.0",
        "last_reviewed": "2026-11-03",
        "ai_assisted": False,
        "reviewed_by": "",
    }
    
    errors = validate_front_matter(front_matter)
    
    assert len(errors) == 0


def test_validate_iso_date():
    """Test ISO date validation."""
    assert validate_iso_date("2026-11-03") is True
    assert validate_iso_date("2026-01-01") is True
    assert validate_iso_date("Nov 3, 2026") is False
    assert validate_iso_date("2026/11/03") is False
    assert validate_iso_date("invalid") is False
