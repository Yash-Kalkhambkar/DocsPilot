---
title: Add an Underwriting Rule
topic_type: task
audience: developers
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: "Yash Kalkhambkar"
---

# Add an Underwriting Rule

Add a custom underwriting rule to CreditShield's automated policy enforcement.

## Prerequisites

- CreditShield repository cloned locally
- Understanding of [Underwriting Rules](../concepts/underwriting-rules.md)
- Python development environment set up

## Rule Design Checklist

Before implementing, define:

- [ ] Rule ID (format: `HR-##` for hard rules, `SR-##` for soft rules)
- [ ] Rule name (human-readable description)
- [ ] Threshold value and unit
- [ ] Calculation method (formula or data source)
- [ ] Hard vs soft classification (auto-reject or manual review)
- [ ] Applicable loan products (all products, or specific types)
- [ ] Regulatory basis (RBI circular, internal policy)

## Steps

### 1. Define the rule specification

Create a rule specification document:

```yaml
rule_id: HR-08
rule_name: Maximum Open Credit Cards
description: Borrower must not have more than 5 active credit cards
threshold: 5
calculation: Count of active credit cards from bureau report
severity: hard
applicable_products:
  - personal_loan
  - education_loan
regulatory_basis: Internal credit policy Section 2.4 on credit exposure limits
```

### 2. Add rule logic to data adapter

**File:** TODO(verify) `ai_agent/data_adapter.py` or backend service layer

Add rule evaluation method:

```python
def check_max_credit_cards(self, arn: str) -> dict:
    """Check if borrower exceeds maximum credit card limit."""
    borrower_data = self.get_borrower_profile(arn)
    bureau_data = self.get_bureau_report(arn)
    
    active_cards = bureau_data.get("active_credit_cards", 0)
    threshold = 5
    
    violation = active_cards > threshold
    
    return {
        "rule_id": "HR-08",
        "name": "Maximum Open Credit Cards",
        "triggered_value": active_cards,
        "threshold": threshold,
        "violated": violation,
        "detail": f"Borrower has {active_cards} active credit cards, exceeds maximum of {threshold}",
    }
```

### 3. Register rule in violation tool

**File:** `ai_agent/tools/rule_violation_tool.py`

Add RAG query hint for regulatory citation:

```python
_RULE_ID_RAG_QUERY: dict[str, str] = {
    # ... existing rules ...
    "HR-08": "HR-08 maximum open credit cards limit credit exposure policy",
}
```

### 4. Add rule to policy evaluation workflow

**File:** TODO(verify) Backend service or AI agent orchestrator

Register rule in evaluation list:

```python
UNDERWRITING_RULES = [
    # ... existing rules ...
    "HR-08",  # Maximum Open Credit Cards
]
```

### 5. Create regulatory policy document

Add policy text to `document/` directory:

**File:** `document/internal_credit_policy.txt`

```text
Section 2.4: Credit Exposure Limits

Borrowers applying for unsecured personal or education loans must not maintain more than 5 active credit cards. Excessive credit card holdings indicate potential over-leveraging and credit dependency. This limit aligns with conservative credit risk management practices.

Rule ID: HR-08
Threshold: 5 active credit cards
Action: Automatic rejection if exceeded
```

### 6. Ingest policy document into RAG

Run RAG ingestion to index the new policy:

```bash
cd ai_agent/rag
python ingest.py --source ../../document/internal_credit_policy.txt
```

**Expected result:** Policy document chunked, embedded, and added to FAISS index.

### 7. Write unit tests

**File:** `ai_agent/tests/test_rules.py`

```python
def test_hr08_max_credit_cards_pass():
    """Test HR-08 passes when credit cards below threshold."""
    adapter = MockDataAdapter()
    adapter.set_bureau_data("TEST-001", {"active_credit_cards": 3})
    
    result = adapter.check_max_credit_cards("TEST-001")
    
    assert result["violated"] is False
    assert result["triggered_value"] == 3

def test_hr08_max_credit_cards_fail():
    """Test HR-08 fails when credit cards exceed threshold."""
    adapter = MockDataAdapter()
    adapter.set_bureau_data("TEST-002", {"active_credit_cards": 7})
    
    result = adapter.check_max_credit_cards("TEST-002")
    
    assert result["violated"] is True
    assert result["triggered_value"] == 7
    assert result["rule_id"] == "HR-08"
```

### 8. Run tests

```bash
python -m pytest ai_agent/tests/test_rules.py::test_hr08_max_credit_cards_pass -v
python -m pytest ai_agent/tests/test_rules.py::test_hr08_max_credit_cards_fail -v
```

**Expected result:** Both tests pass.

### 9. Test end-to-end with sample application

Create test application:

```python
from ai_agent.pipeline.agent_orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()
result = orchestrator.analyse_application(
    arn="TEST-003",
    query="Check rule violations"
)

print(result)
```

**Expected result:** HR-08 violation appears in rule violation list if test borrower has >5 credit cards.

### 10. Document the rule

Add entry to [Underwriting Rules](../concepts/underwriting-rules.md) documentation:

```markdown
### HR-08: Maximum Open Credit Cards

**Rule:** Borrower must not have more than 5 active credit cards.

**Data source:** Credit bureau report.

**Example violation:** Borrower has 7 active credit cards. Violates HR-08.

**Why it matters:** Excessive credit cards indicate over-leveraging and credit dependency.
```

## Verify the Rule

Confirm the following:

- [ ] Rule logic implemented in data adapter
- [ ] Rule registered in violation tool
- [ ] RAG query hint added for citation retrieval
- [ ] Policy document created and ingested
- [ ] Unit tests written and passing
- [ ] End-to-end test shows rule in violation list
- [ ] Documentation updated

## Soft Rule vs Hard Rule

To make the rule soft (manual review) instead of hard (auto-reject):

1. Change rule ID to `SR-##` format
2. Modify violation handler to escalate instead of reject
3. Update documentation to indicate manual review trigger

## Rule Configuration

To make threshold configurable:

Add environment variable:

```bash
RULE_HR08_THRESHOLD=5
```

Update rule logic to read from config:

```python
threshold = int(os.getenv("RULE_HR08_THRESHOLD", "5"))
```

## Troubleshooting

### Rule not triggering

**Cause:** Rule not registered in evaluation workflow.

**Solution:** Confirm rule ID added to `UNDERWRITING_RULES` list in orchestrator.

### RAG citation not found

**Cause:** Policy document not ingested or query hint poor quality.

**Solution:**

1. Re-run RAG ingestion: `python ingest.py`
2. Improve query hint in `_RULE_ID_RAG_QUERY` with more specific terms
3. Verify policy document contains rule ID text

### Bureau data not available

**Cause:** Data adapter does not provide required field.

**Solution:** Add field to mock data adapter or backend API response:

```python
def get_bureau_report(self, arn: str) -> dict:
    return {
        "active_credit_cards": 3,  # Add this field
        # ... other bureau fields
    }
```

## Next Steps

- Review all [Underwriting Rules](../concepts/underwriting-rules.md)
- Understand [RAG Grounding](../concepts/rag-grounding.md) for citation retrieval
- Learn about [Loan Origination Lifecycle](../concepts/loan-origination-lifecycle.md) to see when rules are evaluated
