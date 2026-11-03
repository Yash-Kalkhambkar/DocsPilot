# DocsPilot — AI-Assisted Docs-as-Code Pipeline

![CI Status](https://github.com/Yash-Kalkhambkar/DocsPilot/workflows/Documentation%20Pipeline/badge.svg)

A production-grade documentation pipeline demonstrating technical writing excellence, automation, and responsible GenAI integration for the **CreditShield AI Loan Origination System**.

This project showcases five core capabilities: topic-based documentation with enforced style and terminology, Python automation for documentation quality gates, GenAI-assisted authoring with human accuracy review, RAG-powered docs chatbot, and quantified content gap analysis.

## What This Project Demonstrates

This portfolio piece maps to five professional documentation engineering competencies:

1. **Topic-based documentation:** A complete docs set (concepts, tasks, reference, release notes) in Markdown, published through MkDocs with Material theme to GitHub Pages via a Git-based CI/CD pipeline.

2. **Automated quality gates:** Python scripts enforce metadata standards, verify link integrity, and assemble release notes from Git history. Vale enforces style guide and terminology with custom rules. All checks run in CI.

3. **GenAI-assisted authoring pilot:** Versioned prompt templates for drafting, summarizing, and editing documentation. Every AI-generated topic passes through a human accuracy review checklist. Real time savings and failure modes documented in `pilot/FINDINGS.md`.

4. **RAG documentation chatbot:** Embeddings (sentence-transformers/AWS Bedrock), FAISS vector search, and LLM-based question answering with source citations. Handles "I don't know" cases correctly.

5. **Evaluation and gap analysis:** A 15-20 question evaluation set scores retrieval accuracy, citation correctness, and unanswerable-question handling. Automatically generates a content gap report identifying missing or weak topics.

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

### Build and Query the RAG Chatbot

```bash
# Ingest documentation and build the index
python rag/ingest.py

# Ask a question
python rag/ask.py "How do I configure AWS Bedrock?"

# Run the evaluation suite
python eval/run_eval.py
```

The evaluation generates `eval/gaps_report.md` with content improvement recommendations.

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
├── rag/
│   ├── embeddings.py             # Embedding interface
│   ├── ingest.py                 # Document chunking and indexing
│   └── ask.py                    # Question answering CLI
├── eval/
│   ├── questions.yaml            # Evaluation question set
│   ├── run_eval.py               # RAG evaluation runner
│   └── gaps_report.md            # Generated content gap analysis
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

### RAG Chatbot Architecture

The docs chatbot uses retrieval-augmented generation with a strict constraint: **only answer from the retrieved documentation context**. If the context doesn't contain the answer, the bot says "I don't know" and names the closest available topic.

LLM and embedding interfaces are abstracted so tests run offline with stubs, and production can switch between local models (sentence-transformers) and cloud services (AWS Bedrock).

## Live Documentation

**Published site:** https://yash-kalkhambkar.github.io/DocsPilot/

## Limitations and Future Work

This is a portfolio demonstration with known constraints:

- **Small documentation set:** 8-10 topics cover core CreditShield features only. A production docs site would require 50-100 topics.
- **Evaluation set size:** 15-20 questions demonstrate the evaluation approach but are not statistically significant.
- **RAG chunking strategy:** Current implementation splits by heading with fixed token limits. Advanced approaches (semantic chunking, multi-level indexing) would improve retrieval.
- **No usage analytics:** A production site would track page views, search queries, and user feedback to guide content priorities.
- **Limited GenAI pilot data:** Timing measurements are based on authoring 8-10 topics. Statistically significant conclusions require larger samples.

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
