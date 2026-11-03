---
title: Generate an Appraisal Report
topic_type: task
audience: developers, credit analysts
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: "Yash Kalkhambkar"
---

# Generate an Appraisal Report

Generate a 4-page professional loan appraisal report for loan officers and underwriters.

## Prerequisites

- CreditShield backend running (see [Run CreditShield Locally](run-creditshield-locally.md))
- AWS Bedrock configured (see [Configure AWS Bedrock](configure-aws-bedrock.md)) or mock mode enabled
- Borrower application with uploaded bank statement

## What the Appraisal Report Contains

The 4-page report includes:

**Page 1:** Executive summary, applicant profile, loan request overview, key financial snapshot, risk drivers, final credit decision

**Page 2:** Income and cashflow analysis, liquidity analysis, financial discipline assessment

**Page 3:** Expense behavior, liability analysis, loan affordability assessment

**Page 4:** Behavioral risk signals, credit bureau insights (if available), recommendations

See the [Underwriting Rules](../concepts/underwriting-rules.md) concept for how rules influence the report.

## Steps

### 1. Prepare test data

Ensure you have:

- Application Reference Number (ARN) for a submitted loan application
- Bank statement CSV or PDF uploaded for the borrower
- Loan type and amount specified

### 2. Call the API endpoint

**Endpoint:** `POST /api/v1/risk/professional-report`

**Request (multipart/form-data):**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/risk/professional-report \
  -F "loan_type=personal" \
  -F "loan_amount=500000" \
  -F "statement=@bank_statement.csv" \
  -F "rules_path=ai_agent/rules" \
  -F "model_path=loan_appraisal_model/model.pkl" \
  -F "use_bedrock=true" \
  -F "output_format=text"
```

**Parameters:**

- `loan_type`: personal, education, business, micro, bnpl
- `loan_amount`: Requested loan amount in rupees
- `statement`: Bank statement file (CSV or PDF)
- `rules_path`: Path to underwriting rules directory (TODO: verify location)
- `model_path`: Path to ML model file (TODO: verify location)
- `use_bedrock`: `true` to use AWS Bedrock LLM, `false` for mock
- `output_format`: `text` or `html`

### 3. Wait for generation

Report generation takes 10-30 seconds depending on:

- Bank statement size (number of transactions)
- Bedrock LLM response time
- Number of RAG retrievals

**Expected response:** Plain text or HTML formatted 4-page report.

### 4. Review the report

The report output begins with:

```text
================================================================================
                   PROFESSIONAL LOAN APPRAISAL REPORT
================================================================================

================================================================================
                           PAGE 1: EXECUTIVE SUMMARY
================================================================================

APPLICANT PROFILE & FINANCIAL HEALTH
────────────────────────────────────────────────────────────────────────────────

Classification: Salaried
Financial Health: Moderate
...
```

### 5. Save the report

Save to file:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/risk/professional-report \
  -F "loan_type=personal" \
  -F "loan_amount=500000" \
  -F "statement=@bank_statement.csv" \
  -F "use_bedrock=true" \
  -F "output_format=text" \
  > appraisal_report.txt
```

Or with HTML format:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/risk/professional-report \
  -F "loan_type=personal" \
  -F "loan_amount=500000" \
  -F "statement=@bank_statement.csv" \
  -F "use_bedrock=true" \
  -F "output_format=html" \
  > appraisal_report.html
```

## Use from Python Service Layer

Call programmatically from backend code:

```python
from app.services.loan_appraisal_service import LoanAppraisalService

service = LoanAppraisalService()

# Analyze the loan application
analysis_result = service.analyze_loan(
    loan_type="personal",
    loan_amount=500000,
    statement_path="bank_statement.csv",
    rules_path="ai_agent/rules",
    model_path="loan_appraisal_model/model.pkl",
    use_bedrock=True
)

# Generate professional report
report = service.generate_professional_report(
    analysis_result=analysis_result,
    output_format='text'
)

print(report)
```

## Report Sections Explained

### Executive Summary (Page 1)

**Applicant Profile:** Classifies borrower as Student, Salaried, Self-employed, or Unemployed based on income patterns.

**Financial Health:** Rates overall health as Strong, Moderate, or Weak.

**Loan Request Overview:** Loan type, amount, assumed tenure (24 months), estimated EMI.

**Key Financial Snapshot:** Income, expenses, savings ratio, inflow vs outflow, liquidity stress.

**Top Risk Drivers:** 4-6 major risks with explanations.

**Final Credit Decision:**
- Risk Level: LOW / MODERATE / HIGH
- Recommendation: APPROVE / APPROVE_WITH_CAUTION / REJECT
- Confidence Level: HIGH / MEDIUM / LOW
- Final Score: X/100

**Decision Justification:** Why the recommendation was made.

### Income & Cashflow (Page 2)

**Income Analysis:** Source identification, stability, monthly estimate, trend, risks.

**Cashflow Analysis:** 12-month inflow/outflow, net savings, savings ratio interpretation.

**Liquidity Analysis:** Min/max/average balance, low-balance days, stress days, month-end stress.

**Financial Discipline:** Spending vs earning behavior, consistency, volatility.

### Expense & Liability (Page 3)

**Expense Behavior:** Essential spending breakdown (rent, food, travel, bills), discretionary spending, lifestyle insight.

**Liability Analysis:** Existing EMIs, BNPL/credit usage, hidden liabilities, debt-to-income ratio, annual debt payment.

**Loan Affordability:**
- Expected monthly EMI
- EMI-to-income ratio
- Current surplus
- Expected surplus after new EMI
- Classification: AFFORDABLE / RISKY / NOT_AFFORDABLE
- Detailed rationale

### Behavioral Risk & Recommendations (Page 4)

**Behavioral Risk Signals:** TODO(verify) — Pattern-based risk indicators.

**Credit Bureau Insights:** CIBIL score, bureau data analysis (if available).

**Recommendations:** Actions for approval, caution items for conditional approval, or reasons for rejection.

## Customizing the Report

### Change Loan Tenure Assumption

Default: 24 months

To modify: TODO(verify) — Check `professional_report_formatter.py` for tenure configuration.

### Adjust Risk Thresholds

FOIR limits, savings ratio thresholds, and other risk parameters configured in:

- TODO(verify) Underwriting rules files
- TODO(verify) ML model parameters
- TODO(verify) Service layer configuration

### Add Custom Sections

TODO(verify) — Modify `Backend/app/services/professional_report_formatter.py` to add sections.

## Troubleshooting

### Missing data in report

**Cause:** Bank statement does not contain expected transaction patterns.

**Solution:**

1. Ensure bank statement covers at least 3 months of transactions
2. Check CSV format matches expected schema (date, description, credit, debit, balance columns)
3. Review transaction categorization logic

### Bedrock timeout

**Cause:** LLM taking too long to respond.

**Solution:**

1. Reduce `MAX_TOKENS` in environment variables
2. Use mock mode for testing: `use_bedrock=false`
3. Check AWS Bedrock service status

### "TODO(verify)" in report output

**Cause:** Data not available from bank statement or bureau.

**Solution:** Placeholder text used when data cannot be extracted. Review source data quality.

## Report Quality

The report quality depends on:

- **Bank statement completeness:** More transactions = better income/expense analysis
- **Transaction categorization accuracy:** ML model trained on labeled transaction data
- **Bureau data availability:** Credit score and history improve risk assessment
- **RAG policy retrieval:** Accurate regulatory citations require well-indexed policy documents

## Using Mock Mode

To generate reports without AWS Bedrock:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/risk/professional-report \
  -F "loan_type=personal" \
  -F "loan_amount=500000" \
  -F "statement=@bank_statement.csv" \
  -F "use_bedrock=false" \
  -F "output_format=text"
```

Mock mode returns canned text for AI-generated sections. Numerical analysis (income, expenses, FOIR) still computed from real data.

## Next Steps

- Review [Underwriting Rules](../concepts/underwriting-rules.md) that influence the report
- Learn about [RAG Grounding](../concepts/rag-grounding.md) for regulatory citations in the report
- Understand the [Loan Origination Lifecycle](../concepts/loan-origination-lifecycle.md) to see when reports are generated
