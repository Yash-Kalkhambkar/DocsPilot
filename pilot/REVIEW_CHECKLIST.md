# Human Accuracy Review Checklist

Every AI-generated documentation topic must pass through this checklist before publishing.

## Purpose

AI-generated content may contain:

- **Hallucinated details:** Plausible but incorrect facts, numbers, or configurations
- **Stale context:** Information from older versions or deprecated features
- **Terminology drift:** Inconsistent use of preferred terms
- **Missing nuance:** Oversimplified explanations missing important edge cases

Human review ensures accuracy, completeness, and compliance.

## Review Process

### Step 1: Verify Against Product

**For task topics:**

- [ ] Run every step against the actual product
- [ ] Confirm each command executes without errors
- [ ] Verify expected results match actual results
- [ ] Check screenshots or outputs are current
- [ ] Test on a clean environment (not just your configured dev setup)

**For concept topics:**

- [ ] Confirm architectural descriptions match codebase
- [ ] Verify component interactions are accurate
- [ ] Check feature descriptions against product behavior
- [ ] Validate workflow stages exist and are correctly ordered

**For reference topics:**

- [ ] Extract API endpoints from OpenAPI spec or code
- [ ] Verify environment variables against `.env.example` or config files
- [ ] Check default values in configuration
- [ ] Confirm code examples compile/run

**Mark as `TODO(verify)` if:**

- Cannot verify against code (missing feature, unclear documentation)
- Requires access you don't have (production environment, external service)
- Contradictory information in code (resolve before publishing)

### Step 2: Validate Numbers and Names

- [ ] Check all numeric values (port numbers, thresholds, counts)
- [ ] Verify file paths exist in repository
- [ ] Confirm model IDs, API versions, package names
- [ ] Validate URLs are correct and accessible
- [ ] Check dates, version numbers, release names

**Common errors to catch:**

- Invented port numbers (8080 instead of 8000)
- Wrong file paths (old directory structure)
- Deprecated model IDs or API versions
- Dead links or redirected URLs

### Step 3: Check Terminology

- [ ] All terms match `style/TERMINOLOGY.md`
- [ ] Product names capitalized correctly (CreditShield, AWS Bedrock, PostgreSQL)
- [ ] Acronyms spelled out on first use
- [ ] No rejected variants (e.g., "Postgres" instead of "PostgreSQL")
- [ ] Consistent term usage throughout topic

**Use Vale to automate:**

```bash
vale docs/your-topic.md
```

Fix all terminology errors flagged by Vale.

### Step 4: Verify No Confidential Data

- [ ] No production credentials, API keys, or secrets
- [ ] No customer names, email addresses, or personal data
- [ ] No internal system URLs or IP addresses
- [ ] No proprietary algorithms or business logic
- [ ] Examples use dummy/test data only

**Safe to include:**

- Public AWS service names and regions
- Open-source library names and versions
- Public GitHub repository URLs
- Documented API endpoints
- Example data clearly marked as test/demo

**Never include:**

- Real AWS access keys or secret keys
- Production database credentials
- Customer loan applications or personal data
- Internal Slack channels or email addresses
- Unpublished features or roadmap details

### Step 5: Check Style Compliance

- [ ] Active voice, second person, present tense
- [ ] Sentences under 25 words (run Vale SentenceLength check)
- [ ] No filler words: simply, just, please note, obviously
- [ ] Headings in sentence case
- [ ] Code blocks have language specified
- [ ] One idea per sentence

**Run full Vale check:**

```bash
vale docs/your-topic.md
```

Address warnings and errors.

### Step 6: Validate Links and References

- [ ] All internal links resolve to existing files
- [ ] All anchors point to existing headings
- [ ] External links return success HTTP status
- [ ] Related topics linked appropriately
- [ ] Cross-references bidirectional where appropriate

**Run link checker:**

```bash
python scripts/check_links.py
```

### Step 7: Review for Completeness

- [ ] Topic covers stated scope (nothing important missing)
- [ ] Prerequisites clearly stated
- [ ] Expected results defined for tasks
- [ ] Troubleshooting section addresses common issues
- [ ] Next steps or related topics provided

### Step 8: Sign Off

**Reviewer information:**

- **Reviewer name:** [Your name]
- **Review date:** [YYYY-MM-DD]
- **Verification method:** [Ran against local dev / Checked against code / Verified with SME]

**Update front matter:**

```yaml
reviewed_by: "Your Name"
```

**Do NOT set `ai_assisted: false`** — keep `ai_assisted: true` to maintain transparency about content origin.

## Review Timing

**When to review:**

- Immediately after AI generation (while context is fresh)
- Before merging pull request with AI-generated content
- Before publishing to production documentation site

**How long it takes:**

- Task topic (5-10 steps): 15-30 minutes
- Concept topic: 10-20 minutes
- Reference topic: 20-40 minutes (depending on API complexity)

Log actual time spent in `pilot/log.csv`.

## Escalation

If you find errors that suggest systematic issues:

1. Document the error type in `pilot/FINDINGS.md`
2. Check if similar errors exist in other AI-generated topics
3. Update prompt template to prevent recurrence
4. Consider whether human-authored content is more appropriate

## Examples of Caught Errors

### Hallucinated Configuration

**AI-generated:**
> Set `MAX_WORKERS=4` to configure the number of worker processes.

**Reality:** `MAX_WORKERS` variable does not exist in codebase. Worker count is hardcoded or uses different variable name.

**Fix:** Remove or replace with correct configuration variable after verifying in code.

### Stale Context

**AI-generated:**
> Use `pip install mkdocs==1.4.2` to install MkDocs.

**Reality:** `requirements.txt` specifies `mkdocs==1.5.3`. AI used outdated version from training data.

**Fix:** Update version to match `requirements.txt`.

### Terminology Drift

**AI-generated:**
> The Bedrock API returns the LLM response...

**Reality:** Style guide specifies "AWS Bedrock" not "Bedrock".

**Fix:** Change to "AWS Bedrock API" throughout topic.

### Missing Edge Case

**AI-generated:**
> Run `uvicorn app.main:app --reload` to start the server.

**Reality:** Command fails if `.env` file not created first. Common error for new developers.

**Fix:** Add prerequisite step to create `.env` file from `.env.example`.

## Tools for Review

- **Vale:** Automated style and terminology checking
- **Link checker:** `scripts/check_links.py`
- **Metadata validator:** `scripts/validate_metadata.py`
- **Product environment:** Local CreditShield instance for testing
- **Code repository:** Source of truth for all product facts

## Sign-Off Statement

By signing off on this checklist, I confirm:

- I have verified all facts against the product or codebase
- I have checked all numbers, names, and configurations
- I have validated terminology against the terminology list
- I have confirmed no confidential or customer data is present
- The topic is accurate, complete, and ready for publication

**Reviewer:** _______________  
**Date:** _______________
