# Prompt Template: Summarize Changes for Release Notes

**Version:** v1  
**Created:** 2026-11-03  
**Purpose:** Summarize code changes or pull request for release notes

## Inputs Required

- **Commit messages:** Git log output or PR description
- **Changed files:** List of modified files with diffs (optional)
- **Target version:** Release version for these changes

## Prompt Template

```
You are a technical writer creating release notes for CreditShield v{version}.

Summarize the following changes for end users (developers, loan officers, administrators).

**Changes:**
{commit_messages_or_diff}

**Requirements:**
- Group changes by type: Features, Bug Fixes, Documentation, Breaking Changes
- Use clear, non-technical language where possible
- Focus on user impact, not implementation details
- If multiple commits relate to one feature, combine into single item
- Omit internal refactoring or test-only changes unless they affect users

**Format:**

## Features
- [User-facing description of new feature]

## Bug Fixes
- [Description of what was broken and now works]

## Documentation
- [Documentation improvements]

## Breaking Changes
- [Changes requiring user action, with migration guidance]

Generate the release notes summary now.
```

## Example Usage

### Input

```
version: 0.2.0
commit_messages:
- feat(api): add bulk document upload endpoint
- fix(auth): resolve JWT token expiration race condition
- docs: add RAG configuration guide
- refactor: extract validation logic to separate module
- test: add integration tests for borrower journey
```

### Expected Output

```
## Features
- Bulk document upload: Upload multiple borrower documents in a single API call, reducing network overhead for mobile clients

## Bug Fixes
- JWT token validation: Fixed race condition causing intermittent authentication failures near token expiration

## Documentation
- Added comprehensive RAG configuration guide with embeddings backend options and tuning parameters
```

## Known Limitations

### Over-Summarization

LLM may combine unrelated changes or omit important details.

**Mitigation:** Review output against actual commit list, expand descriptions if needed.

### Invented Impact

LLM may describe user benefits not actually realized by the change.

**Mitigation:** Verify each claim against code changes or feature behavior.

### Technical Jargon

LLM may use technical terms unfamiliar to non-developer audiences.

**Mitigation:** Review for terminology consistency, replace jargon with plain language.

## Human Accuracy Gate

Release notes must be reviewed by:

1. **Developer:** Verify technical accuracy
2. **Product owner:** Confirm user-facing impact
3. **Technical writer:** Validate language and clarity

## Version History

- **v1 (2026-11-03):** Initial version for CreditShield documentation pilot
