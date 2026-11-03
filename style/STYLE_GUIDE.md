# CreditShield Documentation Style Guide

## Voice and Tone

Write in **active voice, second person, present tense**.

**Good:** "Configure AWS Bedrock by setting environment variables."  
**Avoid:** "AWS Bedrock should be configured by setting environment variables."

Keep sentences **under 25 words**. Break long explanations into multiple sentences.

Be direct and factual. Avoid filler words like "simply", "just", "easily", "please note".

## Sentence and Paragraph Structure

- One idea per sentence
- One topic per paragraph
- Start with the most important information
- Use transitions sparingly

## Headings

- Use sentence case for all headings: "Configure AWS Bedrock" not "Configure AWS BEDROCK"
- H1 (`#`) for page title only (one per page)
- H2 (`##`) for major sections
- H3 (`###`) for subsections
- H4 (`####`) sparingly, for deep nesting only
- Keep headings specific: "Run CreditShield locally" not "Running the System"

## Task Topics (How-To Guides)

Use **numbered steps** for procedures:

```markdown
## Run CreditShield locally

1. Clone the repository:
   ```bash
   git clone https://github.com/Yash-Kalkhambkar/Credshield.git
   ```

2. Install dependencies:
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env` (see [Configuration](../reference/configuration.md)).

4. Start the API server:
   ```bash
   uvicorn app.main:app --reload
   ```

**Expected result:** The API server runs at `http://127.0.0.1:8000`. Visit `/docs` to view the OpenAPI documentation.
```

### Task Topic Rules

- One action per step
- Start each step with a verb: "Configure", "Run", "Install", "Create"
- Include code blocks where appropriate
- State the **expected result** after the final step
- Verify every step against the actual product before publishing
- Link to reference topics instead of repeating configuration details

## Concept Topics

Explain the "what" and "why" only. Link to matching task and reference topics instead of repeating procedural details.

Structure:
1. One-sentence summary at the top
2. Context and purpose
3. How it works (high-level)
4. When to use it
5. Links to related tasks and reference

**Avoid:**
- Step-by-step instructions (those belong in task topics)
- Code examples (those belong in reference topics)
- Exact configuration values (those belong in reference topics)

## Reference Topics

- Extract from code, not memory
- Mark unverified items as `TODO(verify)`
- Use tables for structured data (endpoints, parameters, environment variables)
- Include code examples with syntax highlighting
- Keep examples minimal and focused

### API Endpoint Format

```markdown
### POST /api/v1/borrower/auth/signup

Create a new borrower account.

**Request body:**

```json
{
  "full_name": "Mohit Tade",
  "email": "mohit@example.com",
  "mobile_number": "9876543210",
  "password": "Abcd1234!"
}
```

**Password requirements:**
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 number
- At least 1 symbol

**Response:** `201 Created` with JWT token and borrower details.
```

## Warnings and Notes

Use **admonitions** (MkDocs Material theme):

```markdown
!!! warning "Database not initialized"
    CreditShield does not create database tables at startup. Run migrations manually or use the `/health/db` endpoint to verify connectivity.

!!! note
    Mock mode allows testing without AWS credentials. Set `MOCK_MODE=true` in your environment.

!!! danger "Production credentials"
    Never commit AWS credentials or JWT secrets to version control. Use environment variables only.
```

Types: `note`, `warning`, `danger`, `tip`, `info`

## Code Blocks

Always specify the language for syntax highlighting:

````markdown
```python
from ai_agent.pipeline.agent_orchestrator import AgentOrchestrator
orchestrator = AgentOrchestrator()
```

```bash
uvicorn app.main:app --reload
```

```json
{"status": "success"}
```
````

## Capitalization and Terminology

- Product names: **CreditShield** (not creditshield or Credit Shield)
- Proper nouns: **AWS Bedrock**, **PostgreSQL**, **FastAPI**, **React**, **Flutter**
- Acronyms: spell out on first use, then use acronym
  - "Reserve Bank of India (RBI)" → "RBI" thereafter
  - "Loan Origination System (LOS)" → "LOS" thereafter
- Technical terms: use lowercase unless proper noun
  - "appraisal report" not "Appraisal Report"
  - "underwriting rule" not "Underwriting Rule"
- UI elements: bold when referencing specific labels
  - Click **Submit** to save your changes

## File Paths and Commands

- Use inline code formatting: `app/main.py`, `.env.example`, `uvicorn`
- Use forward slashes for paths even on Windows (Git Bash convention)
- Show full relative paths from repository root: `Backend/app/main.py`

## Links

- Use descriptive link text: "See [Configuration](../reference/configuration.md)" not "See [here](../reference/configuration.md)"
- Use relative paths for internal links
- Verify external links are HTTPS and stable

## Numbers and Units

- Use numerals for numbers: "3 steps", "50+ rules", "7-stage lifecycle"
- Currency: include symbol and no space: "₹75,000" not "Rs 75000"
- Percentages: use symbol with no space: "65%" not "65 percent"
- Ranges: use en dash with no spaces: "8–10 topics"

## Lists

**Unordered lists** for items without sequence:

```markdown
- Income Stability
- Credit Behaviour
- Financial Discipline
```

**Ordered lists** for sequential steps or ranked items:

```markdown
1. Lead and Application Intake
2. KYC and Document Collection
3. Eligibility and Rule Screening
```

## Punctuation

- Use periods at the end of complete sentences in lists
- No punctuation for list items that are not complete sentences (like the bullet list above)
- Use colons to introduce code blocks, examples, or sub-lists
- Oxford comma: "income, expenses, and savings"

## Grammar and Usage

- Contractions: avoid in formal documentation ("do not" not "don't")
- Abbreviations: define on first use
- Pronouns: use "you" for the reader, avoid "we" or "one"
- Verb tense: present tense for current state, past tense only for historical notes

## Front Matter Requirements

Every topic must begin with YAML front matter:

```yaml
---
title: Configure AWS Bedrock
topic_type: task
audience: developers
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: ""
---
```

**Required fields:**
- `title`: page title
- `topic_type`: one of `concept`, `task`, `reference`, `release_notes`
- `audience`: target reader (e.g., "developers", "loan officers", "administrators")
- `product_version`: documented version
- `last_reviewed`: ISO date (YYYY-MM-DD)
- `ai_assisted`: `true` or `false`
- `reviewed_by`: reviewer name (required if `ai_assisted: true`)

## Version and Date Format

- Semantic versioning: `v0.1.0` (lowercase v, three segments)
- Dates: ISO 8601 format `YYYY-MM-DD`: "2026-11-03"
- Times: 24-hour format with timezone: "14:30 UTC"

## Writing Checklist

Before publishing any topic:

- [ ] Front matter complete and valid
- [ ] Sentences under 25 words
- [ ] Active voice, second person, present tense
- [ ] Code blocks have language specified
- [ ] All steps verified against product
- [ ] Links tested (internal and external)
- [ ] Terminology matches `TERMINOLOGY.md`
- [ ] No filler words ("simply", "just", "please note")
- [ ] No confidential data or production credentials
- [ ] Headings in sentence case
- [ ] Numbers and units formatted correctly
