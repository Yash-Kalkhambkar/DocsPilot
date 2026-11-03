# DocsPilot Deployment Guide

## What's Been Built

**DocsPilot** is a complete AI-assisted docs-as-code pipeline for CreditShield, demonstrating:

1. ✅ **Topic-based documentation** (11 topics: concepts, tasks, reference, release notes)
2. ✅ **Automated quality gates** (Python scripts for validation, link checking, release notes)
3. ✅ **GenAI-assisted authoring pilot** (prompt templates, human review checklist, findings framework)
4. ✅ **Style enforcement** (Vale with custom rules for terminology, sentence length, passive voice, filler words)
5. ⏸️ **RAG documentation chatbot** (not yet implemented - P2 work remaining)

## Current Status

- **P0 (Must Ship): 100% Complete** ✅
- **P1 (GenAI Pilot): 100% Complete** ✅
- **P2 (RAG Chatbot): 0% Complete** ⏸️

**Files Created:** 40 files (39 initial + STATUS.md)  
**Time Spent:** ~5.5 hours of ~8 hour target

## Quick Start (No Installation Required)

You can view and edit all files immediately. To deploy:

### Option 1: Deploy Now (Skip Testing)

If you want to deploy immediately without running local tests:

```bash
# Push to GitHub
git push origin main

# Then enable GitHub Pages:
# 1. Go to repository Settings → Pages
# 2. Source: Deploy from a branch
# 3. Branch: gh-pages / root
# 4. Save

# CI will run automatically and deploy docs
```

The GitHub Actions workflow will:
- Validate metadata
- Check links
- Run Vale linting
- Run pytest tests
- Build MkDocs site
- Deploy to GitHub Pages

If CI fails, you'll see errors in the Actions tab.

### Option 2: Test Locally First

To test before pushing, install Python and dependencies:

**1. Install Python 3.11+**

Download from: https://www.python.org/downloads/

Or use winget (if not already running):
```powershell
winget install Python.Python.3.11
```

**2. Refresh terminal and verify:**
```bash
python --version
pip --version
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run validation scripts:**
```bash
# Validate metadata
python scripts/validate_metadata.py

# Check links
python scripts/check_links.py

# Run tests
pytest tests/ -v
```

**5. Build and preview docs:**
```bash
mkdocs serve
```

Visit: http://127.0.0.1:8000

**6. Install Vale for linting (optional):**

Download from: https://github.com/errata-ai/vale/releases

Run:
```bash
vale docs/
```

## Repository Setup

### Make Repository Public

1. Go to repository Settings → General
2. Scroll to "Danger Zone"
3. Click "Change repository visibility"
4. Select "Public"
5. Type repository name to confirm

### Enable GitHub Pages

1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` / `root`
4. Save

GitHub Actions will deploy on every push to `main`.

### Update README Badge

After first CI run, the badge will activate:

```markdown
![CI Status](https://github.com/Yash-Kalkhambkar/DocsPilot/workflows/Documentation%20Pipeline/badge.svg)
```

## What Each Component Does

### Documentation (`docs/`)

- **index.md**: Landing page with overview and quick links
- **concepts/**: Explain what and why (overview, lifecycle, rules, RAG)
- **tasks/**: Step-by-step how-to guides (run locally, configure AWS, add rule, generate report)
- **reference/**: Technical specs (API endpoints, configuration, glossary)
- **release-notes/**: Version history (v0.1.0)

### Style & Quality (`style/`, `.vale.ini`, `styles/`)

- **STYLE_GUIDE.md**: Voice, tone, sentence structure rules
- **TERMINOLOGY.md**: Preferred terms (80+ entries)
- **Vale rules**: Automated enforcement (errors for terminology, warnings for style)

### Automation (`scripts/`)

- **validate_metadata.py**: Check YAML front matter in all topics
- **check_links.py**: Verify internal and external links
- **build_release_notes.py**: Generate release notes from git conventional commits

### Tests (`tests/`)

- **test_validate_metadata.py**: 9 test cases for metadata validation
- **test_check_links.py**: 4 test cases for link checking
- **test_build_release_notes.py**: 4 test cases for release notes generation
- **fixtures/**: Test data

### GenAI Pilot (`prompts/`, `pilot/`)

- **Prompt templates**: Draft topics, summarize changes, edit for style
- **REVIEW_CHECKLIST.md**: 8-step human accuracy gate
- **log.csv**: Authoring time measurements (marked TODO for you to fill)
- **FINDINGS.md**: Pilot results framework (time saved, failure modes)

### CI/CD (`.github/workflows/`)

- **docs.yml**: Automated pipeline
  - On PR: validate, lint, test, build
  - On push to main: deploy to GitHub Pages

## Resume Claims You Can Make

After pushing to GitHub and enabling Pages:

✅ "Built a topic-based documentation site with MkDocs, governed by a written style guide and terminology list, published through a Git-based GitHub Actions pipeline"

✅ "Implemented Python automation for link validation, metadata validation, and release-note assembly from Git history, with Vale style linting running in CI as a quality gate"

✅ "Piloted GenAI-assisted authoring with versioned prompt templates and a human accuracy-review checklist, documenting failure modes and mitigation strategies"

⏸️ "Built a RAG docs chatbot with embeddings, FAISS, and LLM, evaluated with a test set that scores answer quality and reports content gaps" — **Only claim if you complete P2**

## To Complete P2 (RAG Chatbot) - ~2.5 hours

If you have time, implement:

1. **`rag/embeddings.py`**: Abstract interface with sentence-transformers and AWS Bedrock backends
2. **`rag/ingest.py`**: Chunk docs (300-500 tokens), embed, save FAISS index
3. **`rag/ask.py`**: CLI that retrieves chunks and asks LLM with citations
4. **`eval/questions.yaml`**: 15-20 test questions (4+ unanswerable)
5. **`eval/run_eval.py`**: Score retrieval hit rate, citation correctness, "don't know" handling
6. **`eval/gaps_report.md`**: Generated report from eval results

Use the CreditShield `ai_agent/rag/` code as reference (it's in `product-source/`).

## Files You May Want to Customize

Before deploying, consider updating:

1. **README.md**: Add your name, customize the intro
2. **mkdocs.yml**: Update `site_url` to your actual GitHub Pages URL
3. **docs/index.md**: Personalize the welcome message
4. **pilot/log.csv**: Fill in TODO(human) rows with real authoring times
5. **pilot/FINDINGS.md**: Complete TODO(human) sections with actual measurements

## Troubleshooting

### "Python not found"
- Install Python 3.11+ from python.org
- Restart terminal after installation
- Add Python to PATH during installation

### "vale: command not found"
- Download Vale from GitHub releases
- Extract and add to PATH
- Or skip Vale and rely on CI

### Links fail in CI but work locally
- Check that all internal links use relative paths
- Ensure external links are HTTPS (not HTTP)
- Some sites block CI bots (already allow-listed in script)

### MkDocs build fails
- Check for broken internal links
- Validate YAML in mkdocs.yml
- Ensure all nav entries point to existing files

### GitHub Pages not deploying
- Check that gh-pages branch exists after first CI run
- Verify Pages source is set to `gh-pages` branch
- Wait 2-3 minutes after push for deployment

## Next Actions

1. **Review the documentation** - Read through topics, check for accuracy
2. **Customize as needed** - Add your voice to README and docs
3. **Push to GitHub** - `git push origin main`
4. **Enable Pages** - Repository Settings → Pages
5. **Verify deployment** - Check CI status, visit live site
6. **(Optional) Complete P2** - Implement RAG chatbot
7. **Update resume** - Add verified claims from STATUS.md
8. **Practice explanation** - Be ready to discuss methodology and findings

## What Makes This Portfolio Stand Out

1. **Honest implementation**: TODO(human) markers show you don't fake data
2. **Professional structure**: Real docs-as-code workflow, not a demo
3. **Systematic approach**: Style guide → Vale rules → CI enforcement
4. **AI transparency**: Clear about what AI did, what humans verify
5. **Documented trade-offs**: Known limitations stated upfront

## Time to Deploy: ~5 minutes

Just push and enable Pages. CI handles the rest.

Good luck with your Content Engineer Intern application! 🚀
