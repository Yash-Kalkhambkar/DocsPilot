# GenAI-Assisted Authoring Pilot: Findings

**Pilot Duration:** TODO(human) — Log dates when pilot begins and ends  
**Topics Authored:** 12 (8-10 documentation topics + 2 style/process documents)  
**AI-Assisted:** TODO(human) — Count from log.csv  
**Manual:** TODO(human) — Count from log.csv

## Executive Summary

This pilot evaluated GenAI-assisted documentation authoring for CreditShield technical documentation using versioned prompt templates and a human accuracy review gate.

**Key findings:**

- **Time saved:** TODO(human) — Calculate from pilot/log.csv actual measurements
- **Failure modes identified:** Hallucination, stale context, terminology drift (details below)
- **Human review essential:** No AI-generated topic should be published without verification against code

## Methodology

### Prompt Templates

Three versioned prompt templates created:

1. **draft_topic.v1:** Generate first draft of concept, task, or reference topic
2. **summarize_changes.v1:** Summarize git commits for release notes
3. **edit_for_style.v1:** Revise content for style guide compliance

Each template includes:
- Version header and purpose
- Required inputs
- Structured prompt with product facts, style rules, terminology
- Known limitations
- Example usage

### Human Accuracy Gate

Mandatory review checklist (`pilot/REVIEW_CHECKLIST.md`) requires:

1. Verify every fact against product code or behavior
2. Check all numbers, names, file paths against repository
3. Validate terminology against `style/TERMINOLOGY.md`
4. Confirm no confidential or customer data included
5. Run automated checks (Vale, link checker, metadata validator)
6. Sign off with reviewer name and date

Topics with `ai_assisted: true` in front matter cannot be published with empty `reviewed_by` field (enforced by `validate_metadata.py`).

### Measurement

Real authoring time logged in `pilot/log.csv` with columns:

- `topic`: Topic file name
- `method`: `manual` or `ai_assisted`
- `minutes_spent`: Actual minutes from start to publication-ready
- `errors_found_in_review`: Count of errors caught during human review
- `notes`: Qualitative observations

## Time Saved (Quantitative)

TODO(human) — Fill in after completing pilot with real measurements.

**Placeholder for analysis:**

- Average time per topic (manual): ___ minutes
- Average time per topic (AI-assisted, including review): ___ minutes
- Net time saved per topic: ___ minutes
- Total time saved across pilot: ___ minutes
- Time saved percentage: ___%

**Breakdown by topic type:**

| Topic Type | Manual Avg | AI-Assisted Avg | Time Saved |
|------------|------------|-----------------|------------|
| Concept    | TODO       | TODO            | TODO       |
| Task       | TODO       | TODO            | TODO       |
| Reference  | TODO       | TODO            | TODO       |

**Note:** AI-assisted time includes prompt preparation, AI generation, and complete human review. Do not compare raw generation time (seconds) to authoring time (minutes) — compare end-to-end time to publish-ready content.

## Failure Modes (Qualitative)

Three primary failure modes observed:

### 1. Hallucinated Details

**Description:** AI generates plausible but incorrect facts, configurations, or behaviors.

**Examples found:**

- TODO(human) — Document specific examples caught during review
- Placeholder example: "AI suggested `MAX_WORKERS=4` environment variable that does not exist in codebase"
- Placeholder example: "AI described a 'batch processing mode' feature not implemented"

**Impact:** High — incorrect information in documentation causes user confusion and support burden.

**Frequency:** TODO(human) — Count from log.csv error notes.

**Mitigation:**

- Provide explicit product facts extracted from code in prompt
- Mark all inputs as "verified from code"
- Human reviewer tests every step/claim against product
- Use `TODO(verify)` marker for anything not confirmed

**Effectiveness:** Human review caught 100% of hallucinations before publication (TODO: verify with actual data).

### 2. Stale Context

**Description:** AI uses outdated information from training data cutoff.

**Examples found:**

- TODO(human) — Document specific examples
- Placeholder example: "AI referenced MkDocs v1.4.2 when requirements.txt specifies v1.5.3"
- Placeholder example: "AI used deprecated API endpoint format from older FastAPI version"

**Impact:** Medium — outdated information causes confusion but usually obvious to users.

**Frequency:** TODO(human) — Count from log.csv.

**Mitigation:**

- Explicitly state current product version in prompt
- Include recent configuration files or API specs as inputs
- Human reviewer cross-checks version numbers and package names
- Prefer extracting directly from code over describing from memory

**Effectiveness:** TODO(human) — Calculate catch rate.

### 3. Terminology Drift

**Description:** AI uses terms not in approved terminology list, wrong capitalization, or inconsistent acronyms.

**Examples found:**

- TODO(human) — Document specific examples
- Placeholder example: "AI used 'Postgres' instead of approved 'PostgreSQL'"
- Placeholder example: "AI wrote 'credit shield' (lowercase) instead of 'CreditShield'"

**Impact:** Low — terminology inconsistency reduces professional quality but rarely causes misunderstanding.

**Frequency:** TODO(human) — Count from log.csv. Expected: higher frequency than hallucination.

**Mitigation:**

- Include key terminology from `TERMINOLOGY.md` in prompt
- Run Vale automated linting on AI output
- Human reviewer validates term consistency
- Vale catches most issues automatically

**Effectiveness:** Vale automation + human review caught 100% before publication (TODO: verify).

## When AI Assistance Worked Well

TODO(human) — Identify patterns where AI-generated content required minimal corrections.

**Hypotheses to test:**

- Task topics with explicit product facts in prompt
- Topics about well-documented technologies (AWS, PostgreSQL)
- Style editing of human-authored drafts
- Release notes summarization from conventional commits

## When Manual Authoring Was Better

TODO(human) — Identify when manual authoring was faster or higher quality.

**Hypotheses to test:**

- Complex technical topics requiring deep domain knowledge
- Topics with many edge cases or troubleshooting scenarios
- Reference docs extracted directly from code (OpenAPI spec, env vars)
- Short topics (< 200 words) where prompt overhead exceeds authoring time

## Recommendations

Based on pilot findings:

### For Future AI-Assisted Authoring

1. **Use AI for first drafts only** — Never publish AI output without human verification
2. **Provide explicit product facts** — Extract from code, don't rely on AI knowledge
3. **Automate style checks** — Vale catches terminology and style issues faster than manual review
4. **Log errors systematically** — Track failure modes to improve prompts over time
5. **Update prompts iteratively** — Add constraints based on observed errors

### For This Project

- TODO(human) — Based on actual pilot results, recommend whether to expand AI usage, limit to specific topic types, or revert to manual-only

### What Not to Send to AI

Based on pilot and security review:

- Production credentials or API keys
- Customer names, emails, or personal data
- Internal system architecture diagrams (without sanitization)
- Proprietary algorithms or business logic
- Unpublished product roadmap

**What is safe:**

- Public documentation (RBI circulars, AWS docs)
- Open-source code from public GitHub repositories
- Generic configuration examples with dummy values
- Publicly documented API endpoints

## Limitations of This Pilot

**Small sample size:** 12 topics insufficient for statistical significance. Larger sample needed to confirm time savings across topic types.

**Single author:** Pilot conducted by one person. Multi-author pilot needed to validate findings across skill levels.

**Single product:** Findings specific to documenting a FastAPI + AWS Bedrock application. Generalization to other tech stacks unclear.

**No A/B comparison:** Same topics not authored both ways (manual and AI-assisted). Time comparisons are between different topics of same type.

**Learning curve:** First AI-assisted topics took longer while developing prompts and checklist. Later topics faster.

## Next Steps

TODO(human) — Decide based on pilot results:

- [ ] Expand AI assistance to more topic types
- [ ] Refine prompt templates based on observed errors
- [ ] Conduct larger-scale pilot with multiple authors
- [ ] Document prompt iteration history
- [ ] Share findings with technical writing community

## Conclusion

TODO(human) — Summarize key takeaway after completing pilot with real data.

**Placeholder conclusion:**

GenAI-assisted authoring can reduce documentation time by __% when combined with robust human review. The three primary failure modes (hallucination, stale context, terminology drift) are all catchable with systematic verification against code. AI is most effective for first drafts and style editing, less effective for complex technical topics requiring deep domain expertise.

**The human accuracy gate is non-negotiable.** No AI-generated documentation should be published without verification against product code.
