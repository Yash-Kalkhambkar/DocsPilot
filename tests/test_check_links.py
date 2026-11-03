"""Tests for check_links.py script."""

import pytest
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_links import (
    extract_links,
    is_external,
    heading_to_id,
    extract_headings,
)


def test_extract_links():
    """Test link extraction from markdown."""
    content = """
    Some text with a [link](../concepts/overview.md) and another [external link](https://example.com).
    Also an [anchor link](#heading-one).
    """
    links = extract_links(content)
    
    assert len(links) == 3
    assert ("../concepts/overview.md", 2) in links
    assert ("https://example.com", 2) in links
    assert ("#heading-one", 3) in links


def test_is_external():
    """Test external link detection."""
    assert is_external("https://example.com") is True
    assert is_external("http://example.com") is True
    assert is_external("../concepts/overview.md") is False
    assert is_external("/reference/api.md") is False
    assert is_external("#anchor") is False


def test_heading_to_id():
    """Test heading to anchor ID conversion."""
    assert heading_to_id("Configure AWS Bedrock") == "configure-aws-bedrock"
    assert heading_to_id("API Endpoints") == "api-endpoints"
    assert heading_to_id("What's New?") == "whats-new"
    assert heading_to_id("Step 1: Install") == "step-1-install"


def test_extract_headings():
    """Test heading extraction from markdown."""
    content = """
# Main Heading

Some text.

## Subheading One

More text.

### Subheading Two

Even more text.
    """
    headings = extract_headings(content)
    
    assert len(headings) == 3
    assert "Main Heading" in headings
    assert "Subheading One" in headings
    assert "Subheading Two" in headings
