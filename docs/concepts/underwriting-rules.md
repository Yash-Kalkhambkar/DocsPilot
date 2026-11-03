---
title: Underwriting Rules
topic_type: concept
audience: credit analysts, underwriters, developers
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: "Yash Kalkhambkar"
---

# Underwriting Rules

CreditShield enforces 50+ configurable underwriting rules across 5 risk categories to automate policy compliance and risk assessment.

## What Underwriting Rules Do

Underwriting rules systematically evaluate loan applications against lender policy and regulatory requirements. Each rule tests a specific condition (income threshold, debt ratio, CIBIL score) and returns a pass or fail result.

Rules provide three benefits:

1. **Consistency:** Every application evaluated against identical criteria
2. **Speed:** Automated rule execution completes in seconds
3. **Auditability:** Rule violations documented with regulatory citations

## Hard Rules vs Soft Rules

### Hard Rules

Hard rules cause **automatic rejection** when violated. No manual override allowed.

**Use case:** Violations indicate unacceptable risk or regulatory non-compliance.

**Example:** A borrower with CIBIL score 480 violates HR-06 (minimum 550 for unsecured personal loans). The application auto-rejects without reaching credit analyst review.

### Soft Rules

Soft rules trigger **manual review** when violated. Credit Analyst or Underwriter can approve with documented rationale.

**Use case:** Violations indicate elevated risk but may be acceptable with compensating factors.

**Example:** A borrower with income variability 35% violates SR-01 (threshold 30%). Credit Analyst reviews income sources and may approve if variability is seasonal and predictable.

## The 5 Risk Categories

### 1. Income Stability

Evaluates income source reliability and consistency.

**Example rules:**
- Minimum income threshold per loan product
- Income variability coefficient limit
- Income verification vs declared variance
- Continuous employment duration requirement

**Why it matters:** Stable income indicates ability to service debt over loan tenure.

### 2. Credit Behaviour

Assesses past credit usage and repayment patterns.

**Example rules:**
- Minimum CIBIL score threshold
- No NPA (Non-Performing Asset) or write-off in last 36 months
- Maximum enquiries in last 90 days
- No active disputes with lenders

**Why it matters:** Past credit behaviour predicts future repayment likelihood.

### 3. Financial Discipline

Measures expense management and savings habits.

**Example rules:**
- Minimum savings ratio (monthly income minus expenses)
- Maximum overdraft frequency
- Minimum average bank balance
- Liquidity stress threshold

**Why it matters:** Financial discipline indicates borrower ability to absorb income shocks.

### 4. Loan Burden

Calculates total debt relative to income.

**Example rules:**
- FOIR (Fixed Obligations to Income Ratio) maximum 65% for unsecured personal loans
- Maximum number of active loans
- Loan stacking detection (3+ new loans in 90 days)
- Total EMI to income ratio

**Why it matters:** Excessive loan burden reduces repayment capacity and increases default risk.

### 5. Lifestyle Risk

Identifies spending patterns indicating unsustainable lifestyle.

**Example rules:**
- Discretionary spending as percentage of income
- Luxury goods transaction frequency
- High-value cash withdrawal patterns
- Gambling or speculative activity detection

**Why it matters:** Lifestyle risk can consume income needed for EMI payments.

## Key Hard Rules

The following hard rules are confirmed in the codebase:

### HR-01: FOIR Maximum

**Rule:** Fixed Obligations to Income Ratio must not exceed 65% for unsecured personal loans.

**Calculation:** `(Total Monthly EMI Obligations / Monthly Income) × 100`

**Example violation:** Borrower earns ₹50,000/month with existing EMIs totaling ₹35,000/month. FOIR = 70%. Violates HR-01.

**Regulatory basis:** RBI Master Direction on Digital Lending, internal credit policy.

### HR-02: Document Tampering

**Rule:** No document tampering detected in salary slips, bank statements, or ITR.

**Detection method:** AI fraud analysis tool checks for altered amounts, modified dates, inconsistent fonts, digital manipulation artifacts.

**Example violation:** Bank statement shows signs of PDF editing. Transaction amounts modified. Violates HR-02.

### HR-03: NPA/Write-off History

**Rule:** No NPA or write-off in last 36 months as borrower or guarantor.

**Data source:** Credit bureau reports, internal lender history.

**Example violation:** Borrower defaulted on personal loan 24 months ago. Loan written off by previous lender. Violates HR-03.

### HR-04: Income Variance

**Rule:** Verified income must not vary by more than 50% from declared income.

**Verification sources:** Bank statement credit analysis, salary slip verification, ITR cross-check.

**Example violation:** Borrower declared monthly income ₹60,000. Bank statement shows average monthly credits ₹35,000. Variance = 42%. Violates HR-04 if threshold is 40%.

### HR-05: Loan Stacking

**Rule:** Maximum 3 new unsecured loans in 90-day period.

**Detection method:** Credit bureau enquiry count, internal application database.

**Example violation:** Borrower applied for 4 personal loans across 3 lenders in last 75 days. Violates HR-05.

**Why it matters:** Loan stacking indicates financial distress or fraud.

### HR-06: Minimum CIBIL Score

**Rule:** Minimum CIBIL score 550 for unsecured personal loans.

**Data source:** Credit bureau report.

**Example violation:** Borrower CIBIL score 520. Violates HR-06.

**Note:** Threshold varies by loan product. Education loans may accept lower scores.

### HR-07: Minimum Income

**Rule:** Verified monthly income must meet or exceed product-specific minimum.

**Thresholds (example):**
- Personal loan: ₹25,000/month
- Home loan: ₹40,000/month
- Business loan: ₹50,000/month

**Example violation:** Borrower applies for personal loan with verified income ₹20,000/month. Violates HR-07.

## Key Soft Rules

### SR-01: Income Variability

**Rule:** Income coefficient of variation (CV) triggers manual review if above threshold.

**Calculation:** `(Standard Deviation of Monthly Income / Mean Monthly Income) × 100`

**Typical threshold:** 30%

**Example:** Freelancer with monthly income ranging ₹30,000–₹90,000. CV = 35%. Triggers SR-01 for manual review.

**Credit Analyst action:** Assess if variability is seasonal, project-based, or indicates income instability.

## How Rules Are Evaluated

1. **Trigger point:** Stage 3 (Eligibility and Rule Screening) in the loan origination lifecycle
2. **Execution:** AI agent `rule_violation_tool` runs all applicable rules
3. **Data sources:** Borrower profile, uploaded documents, credit bureau, bank statement analysis
4. **Output:** List of violated rules with triggered values, thresholds, regulatory citations
5. **Action:** Hard rules cause auto-reject. Soft rules escalate to Credit Analyst.

## Rule Configuration

Rules are **configurable per loan product and lender policy**. Parameters that can be adjusted:

- Threshold values (FOIR limit, minimum income, CIBIL score)
- Hard vs soft classification (whether violation auto-rejects)
- Loan product applicability (rules apply to personal loans only, or all products)
- Regional variations (different thresholds for metro vs non-metro borrowers)

**Configuration location:** TODO(verify) — Check ai_agent or Backend service layer for rule definition files.

## Rule Violation Reports

When a rule is violated, CreditShield generates a report containing:

- **Rule ID:** Unique identifier (e.g., HR-01, SR-01)
- **Rule name:** Human-readable description
- **Triggered value:** Actual value calculated for this borrower
- **Threshold:** Policy threshold that was exceeded
- **Detail:** Explanation of why violation occurred
- **Regulation reference:** Citation from RBI circular or lending policy (retrieved via RAG)
- **Source document:** Policy file containing the rule definition
- **Severity:** Hard (fatal) or soft (warning)

See [RAG Grounding](rag-grounding.md) for details on how regulatory citations are retrieved.

## Counterfactual Analysis

When a rule is violated, the AI agent can generate **counterfactual recommendations** showing what the borrower could change to pass the rule.

**Example counterfactual for HR-01 (FOIR) violation:**

> "Current FOIR is 70% (₹35,000 EMI / ₹50,000 income). To meet the 65% threshold, either:
> - Increase verified income to ₹53,850/month, or
> - Reduce existing EMI obligations by ₹2,500/month (close one existing loan), or
> - Request lower loan amount reducing new EMI by ₹2,500/month"

See [Generate an Appraisal Report](../tasks/generate-an-appraisal-report.md) for examples.

## Adding Custom Rules

Lenders can add custom rules specific to their portfolio risk appetite. See [Add an Underwriting Rule](../tasks/add-an-underwriting-rule.md).

## Regulatory Grounding

Every rule violation cites the relevant regulation or policy:

- **RBI Master Direction:** Digital Lending (2022)
- **RBI Guidelines:** Credit Bureau reporting, KYC norms
- **Internal Policy:** Lender-specific credit policies

Citations are retrieved automatically via RAG from policy documents stored in the `document/` directory.

## Performance

Rule evaluation completes in under 3 seconds for a typical application with:

- 50+ rules executed
- 3 months of bank statement data
- 10+ documents analyzed
- RAG retrieval for 5-10 policy citations

## Audit and Compliance

Rule violations are logged for every application:

- Which rules were evaluated
- Which rules were violated
- Threshold values at time of evaluation
- Whether violation caused rejection or manual review
- Who overrode soft rule violations (if applicable) with rationale

Audit logs support compliance reporting and model governance.

## Related Topics

- [Loan Origination Lifecycle](loan-origination-lifecycle.md) — When rules are evaluated in the workflow
- [RAG Grounding](rag-grounding.md) — How regulatory citations are retrieved
- [Add an Underwriting Rule](../tasks/add-an-underwriting-rule.md) — Step-by-step guide for developers
