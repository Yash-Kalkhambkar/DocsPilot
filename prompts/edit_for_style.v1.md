# Prompt Template: Edit for Style Guide Compliance

**Version:** v1  
**Created:** 2026-11-03  
**Purpose:** Revise existing documentation to match style guide

## Inputs Required

- **Original content:** Documentation text to revise
- **Style guide:** Key rules from `style/STYLE_GUIDE.md`
- **Terminology list:** Terms from `style/TERMINOLOGY.md`

## Prompt Template

```
You are a technical editor reviewing CreditShield documentation for style guide compliance.

Revise the following content to match the CreditShield style guide.

**Original content:**
{original_content}

**Style guide rules:**
- Active voice, second person, present tense
- Sentences under 25 words
- No filler words: simply, just, easily, please note, obviously, clearly
- No contractions: use "do not" not "don't"
- Headings in sentence case: "Configure AWS Bedrock" not "Configure AWS BEDROCK"
- Spell out acronyms on first use: "Reserve Bank of India (RBI)" then "RBI"
- One idea per sentence, one topic per paragraph

**Terminology (use these terms exactly):**
{key_terminology_from_list}

**What to preserve:**
- Technical accuracy: do not change facts, numbers, or code
- Meaning: preserve the author's intent
- Code blocks: do not modify code syntax
- Links: keep all links intact

**What to change:**
- Passive voice → active voice
- Long sentences → shorter sentences
- Filler words → removed
- Wrong terminology → correct terminology
- Wrong capitalization → correct capitalization

Provide the revised content now. If no changes needed, return the original.
```

## Example Usage

### Input

```
original_content:
"The CreditShield system can be easily configured by the developer. Simply set the DATABASE_URL environment variable and the system will automatically connect to Postgres. Please note that the connection string should be kept secret."

key_terminology:
- Use "PostgreSQL" not "Postgres"
- No filler words
```

### Expected Output

```
Configure CreditShield by setting the DATABASE_URL environment variable. The system connects to PostgreSQL automatically. Keep the connection string secret.
```

## Known Limitations

### Meaning Drift

Overly aggressive editing may change technical meaning.

**Example:**
- Original: "The system validates credentials before issuing tokens"
- Wrong edit: "The system checks credentials and issues tokens" (implies different order)
- Correct edit: "The system validates credentials, then issues tokens"

**Mitigation:** Human reviewer validates technical accuracy after style edits.

### Term Substitution Errors

LLM may substitute terms in contexts where original term was correct.

**Example:**
- Original: "The borrower fills the application form" (correct)
- Wrong edit: "The loan officer fills the application form" (wrong actor)

**Mitigation:** Review terminology changes in context, ensure substitution makes sense.

### Code Block Editing

LLM may attempt to "fix" working code to match style preferences.

**Mitigation:** Explicitly exclude code blocks from editing, or review all code changes.

## When to Use This Template

Use for:
- Draft content from junior writers
- Imported content from external sources
- Legacy documentation needing style refresh

Do NOT use for:
- Content with technical errors (fix errors first)
- Content missing required information (add information first)
- Generated code (code has different style rules)

## Human Accuracy Gate

After style editing:

1. **Compare before/after:** Verify meaning unchanged
2. **Check technical terms:** Ensure substitutions correct
3. **Run Vale:** Catch remaining style issues
4. **Read aloud:** Confirm natural flow

## Version History

- **v1 (2026-11-03):** Initial version for CreditShield documentation pilot
