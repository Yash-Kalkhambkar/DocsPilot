# DocsPilot — AI-Assisted Docs-as-Code Pipeline

![CI Status](https://github.com/Yash-Kalkhambkar/DocsPilot/workflows/Documentation%20Pipeline/badge.svg)

A production-grade documentation pipeline demonstrating technical writing excellence, automation, and responsible GenAI integration for the **CreditShield AI Loan Origination System**.

This project showcases five core capabilities: topic-based documentation with enforced style and terminology, Python automation for documentation quality gates, GenAI-assisted authoring with human accuracy review, RAG-powered docs chatbot, and quantified content gap analysis.

## What This Project Demonstrates

This portfolio piece demonstrates three professional documentation engineering competencies:

1. **Topic-based documentation:** A complete docs set (concepts, tasks, reference, release notes) in Markdown, published through MkDocs with Material theme to GitHub Pages via a Git-based CI/CD pipeline.

2. **Automated quality gates:** Python scripts enforce metadata standards, verify link integrity, and assemble release notes from Git history. Vale enforces style guide and terminology with custom rules. All checks run in CI.

3. **GenAI-assisted authoring pilot:** Versioned prompt templates for drafting, summarizing, and editing documentation. Framework for human accuracy review with checklist and findings documentation.

## Quick Start

### Prerequisites

- Python 3.11+
- Vale CLI (for style linting)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Yash-Kalkhambkar/DocsPilot.git
cd DocsPilot

# Install Python dependencies
pip install -r requirements.txt

# Install Vale (example for Linux/macOS via Homebrew)
brew install vale
```

### Run the Documentation Site Locally

```bash
mkdocs serve
```

Visit http://127.0.0.1:8000 to browse the documentation.

### Run Quality Checks

```bash
# Validate metadata in all topics
python scripts/validate_metadata.py

# Check all links (internal and external)
python scripts/check_links.py

# Run Vale style and terminology linting
vale docs/

# Run all tests
pytest tests/ -v
```



## Repository Structure

```
DocsPilot/
├── README.md                     # This file
├── mkdocs.yml                    # MkDocs configuration
├── docs/                         # Documentation source
│   ├── concepts/                 # Concept topics (what and why)
│   ├── tasks/                    # Task topics (how-to guides)
│   ├── reference/                # Reference topics (API, config, glossary)
│   └── release-notes/            # Version release notes
├── style/
│   ├── STYLE_GUIDE.md            # Voice, tone, formatting standards
│   └── TERMINOLOGY.md            # Preferred terms and definitions
├── .vale.ini                     # Vale linting configuration
├── styles/DocsPilot/             # Custom Vale rules
├── scripts/
│   ├── check_links.py            # Link integrity validation
│   ├── validate_metadata.py     # Front matter validation
│   └── build_release_notes.py   # Generate release notes from Git log
├── prompts/                      # GenAI prompt templates
├── pilot/
│   ├── REVIEW_CHECKLIST.md       # Human accuracy gate
│   ├── log.csv                   # Authoring time measurements
│   └── FINDINGS.md               # GenAI pilot results

├── tests/                        # Pytest test suite
└── .github/workflows/docs.yml    # CI/CD pipeline
```

## How I Use AI in This Workflow

### GenAI-Assisted Authoring

I use large language models to **draft** documentation topics, but never publish without human review. My workflow:

1. **Prompt templates** in `prompts/` provide structured inputs (product facts, topic type, target audience) to the LLM
2. **Human accuracy gate** (`pilot/REVIEW_CHECKLIST.md`) requires verification of every step against the product code, every number and name against source files, and every term against the terminology list
3. **Metadata tracking** marks AI-assisted topics with `ai_assisted: true` and requires a `reviewed_by` signature
4. **Failure mode documentation** in `pilot/FINDINGS.md` records hallucinations, stale context, and terminology drift found during review

### What I Do Not Send to AI Tools

- Customer data or confidential information
- Production credentials or secrets
- Private codebases without authorization
- Unverified facts that might be amplified into documentation



## Live Documentation

**Published site:** https://yash-kalkhambkar.github.io/DocsPilot/

## Limitations

This is a portfolio demonstration with known constraints:

- **Small documentation set:** 11 topics cover core CreditShield features only. A production docs site would require 50-100 topics.
- **No usage analytics:** A production site would track page views, search queries, and user feedback to guide content priorities.
- **GenAI pilot framework only:** Prompt templates and review checklist created, but pilot measurements not yet conducted.

## Technology Stack

- **Documentation:** Markdown, MkDocs, Material theme, GitHub Pages
- **Language:** Python 3.11+
- **Quality gates:** Vale (style/terminology), pytest
- **CI/CD:** GitHub Actions
- **RAG:** FAISS, sentence-transformers (all-MiniLM-L6-v2), AWS Bedrock
- **Embeddings:** Local (sentence-transformers) or cloud (AWS Bedrock)

## License

MIT License - see LICENSE file for details.

## Contact

**Yash Kalkhambkar**  
Portfolio project for Content Engineer Intern application  
GitHub: [@Yash-Kalkhambkar](https://github.com/Yash-Kalkhambkar)
