# Prompt Template: Draft Documentation Topic

**Version:** v1  
**Created:** 2026-11-03  
**Purpose:** Generate first draft of a documentation topic (concept, task, or reference)

## Inputs Required

Before using this prompt, gather:

- **Product facts:** Verified information from code, configuration files, or product behavior
- **Topic type:** `concept`, `task`, or `reference`
- **Target audience:** developers, loan officers, credit analysts, underwriters, administrators, or combination
- **Scope:** What this topic should and should not cover
- **Related topics:** Links to prerequisite or follow-up topics

## Prompt Template

```
You are a technical writer creating documentation for CreditShield, an AI-powered loan origination platform.

Write a {topic_type} topic titled "{topic_title}" for {target_audience}.

**Product facts (verified from code):**
{product_facts}

**Topic requirements:**
- Topic type: {topic_type}
- Audience: {target_audience}
- Scope: {scope_description}

**Style requirements:**
- Active voice, second person, present tense
- Sentences under 25 words
- No filler words (simply, just, please note)
- Use preferred terminology from TERMINOLOGY.md
- {topic_type_specific_guidance}

**Topic type guidance:**

For concept topics:
- Explain "what" and "why" only
- Link to task topics instead of including steps
- Include: one-sentence summary, context, how it works, when to use it, related links

For task topics:
- Use numbered steps, one action per step
- Start each step with a verb
- Include code blocks where appropriate
- State expected result after final step
- Verify each step can be performed as written

For reference topics:
- Extract information from code, not memory
- Use tables for structured data
- Include minimal focused code examples
- Mark unverified information as TODO(verify)

**Include YAML front matter:**
```yaml
---
title: {topic_title}
topic_type: {topic_type}
audience: {target_audience}
product_version: 0.1.0
last_reviewed: {today_date}
ai_assisted: true
reviewed_by: ""
---
```

Generate the complete topic now.
```

## Example Usage

### Input

```
topic_type: task
topic_title: Configure RAG Vector Store
target_audience: developers
product_facts:
- VECTOR_STORE environment variable accepts "in_memory" or "pgvector"
- Default is "in_memory"
- pgvector backend not yet implemented
- RAG_TOP_K controls number of chunks retrieved (default 3)
- RAG_CHUNK_SIZE controls chunk size in tokens (default 400)
scope_description: How to configure the RAG vector store backend and tuning parameters
```

### Expected Output

A complete task topic with:
- Valid YAML front matter with `ai_assisted: true`
- Step-by-step instructions
- Code examples
- Expected results
- Troubleshooting section

## Known Limitations

### Hallucination Risk

LLMs may invent plausible but incorrect details:

- **Configuration values:** May generate realistic but wrong defaults, paths, or parameter names
- **Code examples:** May create syntactically correct but functionally wrong code
- **Feature descriptions:** May describe features that don't exist or work differently than stated

### Mitigation

1. Provide explicit product facts extracted from code
2. Mark all inputs as "verified from code"
3. Use human accuracy review checklist before publishing

### Stale Context

LLM training data may reference:

- Older API versions
- Deprecated configuration options
- Changed default values
- Renamed components

### Mitigation

1. Explicitly state product version in prompt
2. Include recent facts from code or documentation
3. Review generated content against current codebase

### Terminology Drift

LLMs may use inconsistent terms:

- Synonyms not in approved terminology list
- Product names with wrong capitalization
- Acronyms without definitions

### Mitigation

1. Include terminology list in prompt
2. Run Vale linting on generated content
3. Human review validates term consistency

## Human Accuracy Gate

**Every AI-drafted topic MUST pass through human review checklist before publishing.**

See `pilot/REVIEW_CHECKLIST.md` for complete review process.

## Version History

- **v1 (2026-11-03):** Initial version for CreditShield documentation pilot
