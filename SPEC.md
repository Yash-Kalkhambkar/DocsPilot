# DocsPilot Specification

## Overview

DocsPilot is an AI-assisted docs-as-code pipeline demonstrating professional technical writing, automation, GenAI integration, and RAG chatbot capabilities for a Content Engineer Intern portfolio submission.

**Product being documented:** CreditShield — AI Loan Origination System

**Priority tiers:**
- **P0 (must ship, ~4h):** Docs set, style guide, terminology, MkDocs site, CI publish, Python automation with tests, Vale linting
- **P1 (~1.5h):** GenAI authoring pilot with prompt templates, review checklist, pilot log, findings
- **P2 (~2.5h):** RAG docs chatbot with evaluation set, scoring, content-gap report
- **Always (~0.5h):** Professional README as writing sample

## Requirements

### R1. Topic-based documentation set (P0)

**R1.1** The docs SHALL contain 8 to 10 topics, each typed as `concept`, `task`, or `reference`, in the folders shown in the build spec.

**R1.2** Every topic SHALL begin with YAML front matter containing: `title`, `topic_type`, `audience`, `product_version`, `last_reviewed`, `ai_assisted` (true/false), and `reviewed_by`.

**R1.3** Task topics SHALL use numbered steps, one action per step, and state the expected result after the steps. Every step SHALL be verified against the actual product or code.

**R1.4** Concept topics SHALL explain the "what" and "why" only, and link to the matching task and reference topics instead of repeating them.

**R1.5** Reference topics SHALL be generated from or checked against the real code (API endpoints, environment variables, config keys). Unknown items SHALL be marked `TODO(verify)`.

**R1.6** The docs SHALL include one release-notes page for `v0.1.0`.

**R1.7** The glossary SHALL define every term listed in `style/TERMINOLOGY.md`.

### R2. Style guide and terminology (P0)

**R2.1** `style/STYLE_GUIDE.md` SHALL define: voice (active, second person, present tense), sentence length limit, heading rules, step formatting, how to write warnings and notes, and capitalisation rules. Keep it to about two pages.

**R2.2** `style/TERMINOLOGY.md` SHALL list preferred terms, rejected variants, and a one-line definition for each.

**R2.3** The style guide and terminology list SHALL be the single source for the Vale ruleset (R4).

### R3. Python automation (P0)

Each script SHALL be runnable from the command line, print a clear summary, and exit non-zero on failure so CI can fail the build.

**R3.1** `check_links.py` SHALL scan all Markdown files and verify internal links and anchors resolve, and external links return a success status (with a timeout and a small allow-list for flaky hosts).

**R3.2** `validate_metadata.py` SHALL verify every topic has the required front matter keys (R1.2), valid `topic_type` values, and an ISO date for `last_reviewed`.

**R3.3** `build_release_notes.py` SHALL read `git log` between two tags (or since a given commit), group conventional-commit messages (`feat`, `fix`, `docs`) into sections, and write a Markdown release-notes page.

**R3.4** Each script SHALL have `pytest` tests in `tests/` using small fixture files (including at least one broken-link case and one missing-metadata case).

### R4. Style and terminology linting (P0)

**R4.1** Vale SHALL be configured through `.vale.ini` with a custom style in `styles/DocsPilot/` containing at least: a terminology substitution rule built from R2.2, a sentence-length warning, a passive-voice warning, and a rule that flags filler words ("simply", "just", "please note").

**R4.2** Terminology violations SHALL be errors. Style suggestions SHALL be warnings.

### R5. CI/CD pipeline (P0)

**R5.1** On every pull request, `.github/workflows/docs.yml` SHALL run: metadata validation, link check, Vale, `pytest`, and `mkdocs build --strict`. Any failure SHALL fail the check.

**R5.2** On push to `main`, the workflow SHALL also deploy the built site to GitHub Pages.

**R5.3** The README SHALL show a status badge for this workflow and link to the live site.

### R6. GenAI-assisted authoring pilot (P1)

**R6.1** `prompts/` SHALL contain at least three prompt templates (`draft_topic`, `summarize_changes`, `edit_for_style`). Each file SHALL have a version header, purpose, inputs, the prompt text, and known limitations.

**R6.2** `pilot/REVIEW_CHECKLIST.md` SHALL define the human accuracy gate: verify each step against the product, check every number and name against the code, check terminology against `TERMINOLOGY.md`, confirm no confidential or customer data was sent to the model, and sign off with name and date.

**R6.3** Topics drafted with AI help SHALL set `ai_assisted: true` and `reviewed_by` in their front matter. `validate_metadata.py` SHALL fail if `ai_assisted: true` and `reviewed_by` is empty.

**R6.4** `pilot/log.csv` SHALL have the columns `topic, method (manual|ai_assisted), minutes_spent, errors_found_in_review, notes`. Leave the rows as `TODO(human)`.

**R6.5** `pilot/FINDINGS.md` SHALL summarise: time saved (from the real log), and a section on failure modes (hallucinated details, stale context, terminology drift) with concrete examples found during review. Use placeholders for anything not yet measured.

### R7. RAG docs chatbot (P2)

**R7.1** `rag/ingest.py` SHALL split docs by heading into chunks of roughly 300 to 500 tokens with a small overlap, keep metadata (`source_file`, `heading`, `topic_type`), embed them, and save a FAISS index plus a metadata file.

**R7.2** `rag/ask.py` SHALL take a question, retrieve the top-k chunks, call the LLM with a prompt that restricts answers to the retrieved context, and print the answer with citations to source files.

**R7.3** If the retrieved context does not contain the answer, the bot SHALL say it does not know and name the closest topic, instead of guessing.

**R7.4** The embedding backend and the LLM client SHALL sit behind small interfaces so tests run offline with stubs.

### R8. Evaluation and content-gap report (P2)

**R8.1** `eval/questions.yaml` SHALL contain 15 to 20 questions. Each has `question`, `expected_topic` (file), and `answerable` (true/false). At least 4 questions SHALL be unanswerable from the docs.

**R8.2** `eval/run_eval.py` SHALL compute: retrieval hit rate at k (did the expected topic appear in the top-k), citation correctness (does the answer cite the expected topic), and unanswerable-question handling rate (did the bot correctly decline).

**R8.3** The script SHALL write `eval/gaps_report.md` listing questions where retrieval failed or the bot declined an answerable question, with a suggested topic to add or improve.

**R8.4** Report only what the script actually measures. Never hard-code results.

### R9. README as a writing sample (always)

The README SHALL be written to professional documentation standards: a one-paragraph summary, a "What this project demonstrates" section mapped to the five goals, a quickstart (clone, install, run docs locally, run lint, run tests, build the index, ask a question), the repo map, a "How I use AI in this workflow" section (including the human accuracy gate and what I do not send to AI tools), and honest limitations.

## Design

### Architecture

```
DocsPilot/
├── README.md                     # writing sample + project overview
├── mkdocs.yml                    # MkDocs configuration with Material theme
├── docs/                         # documentation source
│   ├── index.md
│   ├── concepts/                 # concept topics
│   ├── tasks/                    # task topics
│   ├── reference/                # reference topics
│   └── release-notes/            # release notes
├── style/                        # style guide and terminology
│   ├── STYLE_GUIDE.md
│   └── TERMINOLOGY.md
├── .vale.ini                     # Vale configuration
├── styles/DocsPilot/             # custom Vale rules
├── scripts/                      # Python automation
│   ├── check_links.py
│   ├── validate_metadata.py
│   └── build_release_notes.py
├── prompts/                      # GenAI prompt templates
├── pilot/                        # GenAI pilot artifacts
├── rag/                          # RAG chatbot
│   ├── ingest.py
│   ├── ask.py
│   └── embeddings.py
├── eval/                         # RAG evaluation
│   ├── questions.yaml
│   ├── run_eval.py
│   └── gaps_report.md
├── tests/                        # pytest tests
├── .github/workflows/docs.yml    # CI/CD pipeline
├── requirements.txt
└── product-source/               # git-ignored CreditShield copy
```

### Technology Stack

- **Docs:** Markdown, MkDocs with Material theme, GitHub Pages
- **Language:** Python 3.11+, pytest
- **Lint:** Vale (style and terminology), markdownlint optional
- **CI/CD:** GitHub Actions
- **RAG:** faiss-cpu, sentence-transformers (all-MiniLM-L6-v2), AWS Bedrock
- **Chatbot UI:** CLI first (ask.py), optional Streamlit

### Data Flow

1. **Documentation authoring:** Write Markdown → validate metadata → check links → lint with Vale
2. **GenAI pilot:** Use prompt templates → draft content → human review checklist → measure & log
3. **RAG chatbot:** Ingest docs → chunk & embed → FAISS index → retrieve → LLM answer with citations
4. **Evaluation:** Run eval questions → score retrieval & citations → generate gap report

### Guardrails

1. No invented numbers, timings, accuracy scores, or user counts
2. No confidential or customer data in prompts, logs, or docs
3. Do not document features not found in code - use `TODO(verify)`
4. Keep AI-drafted text marked in front matter and reviewed
5. All secrets from environment variables only
6. Plain, concise, fact-based English - short sentences, active voice

## Tasks

### P0: Core Documentation Pipeline (Must Ship)

#### Task 1: Repository Scaffolding
- Create `.gitignore` (include `product-source/`, `.env`, `__pycache__/`, etc.)
- Create `requirements.txt` with dependencies
- Create `mkdocs.yml` with Material theme configuration
- Create directory structure for docs, style, scripts, tests
- Initialize basic README structure

#### Task 2: Clone and Analyze CreditShield
- Clone CreditShield repo into `product-source/`
- Extract facts into `product-source/FACTS.md` (endpoints, env vars, run steps)
- Verify against actual code - no guessing

#### Task 3: Style Guide and Terminology
- Write `style/STYLE_GUIDE.md` (voice, sentence length, headings, steps, warnings, caps)
- Write `style/TERMINOLOGY.md` (preferred terms, rejected variants, definitions)
- Keep concise and practical

#### Task 4: Documentation Topics
- Write 4 concept topics (overview, lifecycle, rules, RAG)
- Write 4 task topics (run locally, configure AWS, add rule, generate report)
- Write 3 reference topics (API endpoints, configuration, glossary)
- Write release notes for v0.1.0
- All topics include proper YAML front matter (R1.2)
- Task topics verified against code
- Glossary matches terminology list

#### Task 5: Python Automation Scripts
- Write `scripts/check_links.py` (internal links, anchors, external URLs)
- Write `scripts/validate_metadata.py` (front matter validation)
- Write `scripts/build_release_notes.py` (parse git log, group commits)
- Each script: CLI runnable, clear output, non-zero exit on failure

#### Task 6: Pytest Test Suite
- Write tests for `check_links.py` (broken links, valid links)
- Write tests for `validate_metadata.py` (missing fields, invalid values)
- Write tests for `build_release_notes.py` (commit parsing)
- Create fixture files in `tests/fixtures/`

#### Task 7: Vale Linting Configuration
- Create `.vale.ini` configuration
- Create `styles/DocsPilot/` custom rules
  - Terminology.yml (from TERMINOLOGY.md, errors)
  - SentenceLength.yml (warnings)
  - PassiveVoice.yml (warnings)
  - FillerWords.yml (warnings for "simply", "just", "please note")

#### Task 8: CI/CD Pipeline
- Create `.github/workflows/docs.yml`
- On PR: run metadata validation, link check, Vale, pytest, mkdocs build --strict
- On push to main: also deploy to GitHub Pages
- Configure GitHub Pages in repo settings

#### Task 9: Verify P0 Complete
- Run all checks locally
- Verify MkDocs site builds
- Commit and push
- Verify CI passes
- Verify site deploys to GitHub Pages

### P1: GenAI Authoring Pilot

#### Task 10: Prompt Templates
- Create `prompts/draft_topic.v1.md` (version, purpose, inputs, prompt, limitations)
- Create `prompts/summarize_changes.v1.md`
- Create `prompts/edit_for_style.v1.md`

#### Task 11: Human Review Process
- Create `pilot/REVIEW_CHECKLIST.md` (accuracy gate steps)
- Create `pilot/log.csv` with columns, TODO(human) rows
- Update `validate_metadata.py` to enforce ai_assisted + reviewed_by rule

#### Task 12: Findings Document
- Create `pilot/FINDINGS.md` skeleton
- Sections: time saved (placeholder), failure modes (placeholders)
- Mark measurement sections as TODO(human)

### P2: RAG Docs Chatbot

#### Task 13: Embeddings Interface
- Create `rag/embeddings.py` with abstract interface
- Implement local sentence-transformers backend
- Implement AWS Bedrock embeddings backend
- Support offline stub for testing

#### Task 14: Document Ingestion
- Create `rag/ingest.py`
- Split docs by heading into 300-500 token chunks with overlap
- Keep metadata (source_file, heading, topic_type)
- Embed chunks and save FAISS index + metadata JSON

#### Task 15: Question Answering CLI
- Create `rag/ask.py`
- Retrieve top-k chunks for question
- Call LLM with context-restricted prompt
- Print answer with source citations
- Handle "don't know" cases with closest topic

#### Task 16: LLM Interface
- Create abstraction for LLM calls in `rag/`
- AWS Bedrock implementation
- Stub implementation for tests
- Environment variable configuration

#### Task 17: Evaluation Set
- Create `eval/questions.yaml`
- 15-20 questions with question, expected_topic, answerable
- At least 4 unanswerable questions

#### Task 18: Evaluation Runner
- Create `eval/run_eval.py`
- Compute retrieval hit rate at k
- Compute citation correctness
- Compute unanswerable handling rate
- Generate `eval/gaps_report.md`
- Report only actual measurements

### Always: Professional README

#### Task 19: Polish README
- One-paragraph summary
- "What this project demonstrates" (map to 5 goals)
- Quickstart (clone, install, run docs, lint, tests, build index, ask question)
- Repository map
- "How I use AI in this workflow" section
- Human accuracy gate explanation
- Honest limitations
- CI badge and live site link

## Definition of Done

- [ ] Topic-based docs exist in Markdown/MkDocs with style guide and terminology
- [ ] Published through GitHub Actions pipeline to GitHub Pages
- [ ] Python automation for link checks, metadata validation, release notes
- [ ] Vale style/terminology linting runs in CI as quality gate
- [ ] GenAI pilot with prompt templates, review checklist, FINDINGS.md
- [ ] RAG chatbot with evaluation set, scoring, gap report
- [ ] CI green on main
- [ ] Live docs site loads
- [ ] README renders well on GitHub
- [ ] Repository is public and named "DocsPilot"
