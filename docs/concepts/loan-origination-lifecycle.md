---
title: Loan Origination Lifecycle
topic_type: concept
audience: loan officers, credit analysts, underwriters
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: ""
---

# Loan Origination Lifecycle

CreditShield manages loan applications through a 7-stage lifecycle from initial contact to post-decision handover.

## Why a Structured Lifecycle Matters

A structured loan origination workflow provides:

- **Consistency:** Every application follows the same evaluation process
- **Accountability:** Clear ownership at each stage
- **Audit trail:** Complete history of decisions and actions
- **Compliance:** Systematic enforcement of regulatory requirements
- **Efficiency:** Automated steps reduce manual workload

## The 7 Stages

### Stage 1: Lead and Application Intake

**Owner:** Loan Officer

**What happens:**

- Borrower creates account (mobile or web)
- Basic profile information collected
- Loan type and amount requested
- Initial consent captured for data processing
- Application Reference Number (ARN) assigned

**System actions:**

- Create borrower record in database
- Generate unique ARN
- Initialize workflow state
- Send confirmation notification

**Exit criteria:** Borrower submits completed application with required profile fields.

### Stage 2: KYC and Document Collection

**Owner:** Loan Officer (may coordinate with Field Officer)

**What happens:**

- Borrower uploads identity documents (Aadhaar, PAN)
- Address proof submitted
- Income documents collected (salary slips, bank statements, ITR)
- Field Officer may conduct physical verification if required
- Documents validated for completeness and authenticity

**System actions:**

- Store document metadata (file paths, upload timestamps)
- Run document tampering detection
- Flag incomplete or suspicious documents
- Update workflow status to verification pending/completed

**Exit criteria:** All required documents uploaded and validated. KYC status marked complete.

### Stage 3: Eligibility and Rule Screening

**Owner:** System (automated) + Credit Analyst (manual review if needed)

**What happens:**

- Backend and AI agent run 50+ underwriting rules
- Income summary generated
- Fraud signals detected and flagged
- Hard rule violations cause auto-reject
- Soft rule violations trigger manual review

**System actions:**

- Execute income analysis tool
- Execute fraud analysis tool
- Execute rule violation tool
- Generate preliminary risk assessment
- Flag applications with hard-stop conditions

**Exit criteria:** Rule screening complete. Applications with hard rule violations marked for rejection. Applications with soft rule violations escalated to Credit Analyst.

### Stage 4: Credit Analysis

**Owner:** Credit Analyst

**What happens:**

- Credit Analyst reviews borrower profile
- AI agent provides explainable risk rationale
- Bureau data (if available) evaluated
- Income stability assessed
- Counterfactual improvements identified
- Analyst proposes recommendation (approve/reject/rework)

**System actions:**

- Generate 4-page appraisal report
- Retrieve relevant RBI circulars and policies via RAG
- Present AI analysis with confidence scores
- Record analyst recommendation with rationale

**Exit criteria:** Credit Analyst submits recommendation with documented rationale.

### Stage 5: Underwriting Decision

**Owner:** Underwriter (typically Branch Manager)

**What happens:**

- Underwriter reviews Credit Analyst recommendation
- Final policy and risk assessment performed
- Portfolio fit evaluated
- Decision options: sanction, conditional sanction, reject, send back for clarification
- Approval conditions specified if conditional sanction

**System actions:**

- Present complete application history and audit trail
- Display all rule violations and AI analysis
- Record final decision with conditions
- Update application status

**Exit criteria:** Underwriter issues final decision. Status updated to sanctioned, conditionally sanctioned, or rejected.

### Stage 6: Offer and Acceptance

**Owner:** Loan Officer

**What happens:**

- Approved terms and conditions published to borrower
- Borrower reviews offer details (amount, tenure, interest rate, EMI)
- Borrower selects offer and submits acceptance
- Final consent and agreement signed
- Terms locked for disbursal

**System actions:**

- Generate loan agreement document
- Send offer notification to borrower
- Capture borrower acceptance timestamp
- Update status to offer accepted

**Exit criteria:** Borrower accepts offer and signs loan agreement.

### Stage 7: Post-Decision Handover

**Owner:** System Admin + Loan Officer

**What happens:**

- Application data handed over to disbursal system (external or integrated)
- Borrower and operations teams notified of next steps
- Tracker updated with disbursal timeline
- Case closed in Loan Origination System workflow

**System actions:**

- Mark workflow as complete
- Archive application data
- Maintain read-only audit trail
- Continue tracker visibility for borrower

**Exit criteria:** Application transitioned to downstream disbursal/onboarding system.

## Stakeholder Responsibilities

### Loan Officer

- **Stage 1:** Capture application with minimum quality standards
- **Stage 2:** Ensure document completeness, coordinate with borrower for missing items
- **Stage 6:** Communicate offer terms and assist with acceptance
- **Stage 7:** Notify borrower of next steps

### Field Officer

- **Stage 2:** Conduct on-ground verification of residence, business, or employment
- **Stage 2:** Upload field observations to support underwriting

### Credit Analyst

- **Stage 3:** Manual review of soft rule violations
- **Stage 4:** Validate AI outputs, perform financial assessment, submit recommendation

### Underwriter (Branch Manager)

- **Stage 5:** Final credit decision with policy compliance confirmation

### System Admin

- **All stages:** Monitor access control, audit logs, workflow health
- **Stage 7:** Oversee handover to downstream systems

## Workflow Status Values

Applications progress through these status values:

| Status | Stage | Meaning |
|--------|-------|---------|
| `draft` | 1 | Application started but not submitted |
| `submitted` | 1 | Application submitted, awaiting KYC |
| `kyc_pending` | 2 | KYC documents required |
| `kyc_complete` | 2 | KYC validation passed |
| `screening` | 3 | Automated rule screening in progress |
| `manual_review` | 3-4 | Soft rule violations flagged for analyst review |
| `analysis` | 4 | Credit Analyst performing assessment |
| `underwriting` | 5 | Underwriter reviewing for final decision |
| `sanctioned` | 5 | Approved unconditionally |
| `conditional_sanction` | 5 | Approved with conditions |
| `rejected` | 3-5 | Application rejected (can occur at multiple stages) |
| `offer_pending` | 6 | Offer sent, awaiting borrower acceptance |
| `offer_accepted` | 6 | Borrower accepted offer |
| `closed` | 7 | Workflow complete, handed over |

## Decision Points

The lifecycle includes three major decision points:

1. **Stage 3:** Hard rule violations cause automatic rejection (no human intervention)
2. **Stage 4:** Credit Analyst recommendation determines whether application proceeds to underwriting
3. **Stage 5:** Underwriter final decision determines sanction or rejection

## Typical Timeline

| Stage | Duration (Business Days) |
|-------|--------------------------|
| 1. Application Intake | 0-1 |
| 2. KYC and Documents | 1-3 |
| 3. Eligibility Screening | 0 (automated) |
| 4. Credit Analysis | 1-2 |
| 5. Underwriting Decision | 1 |
| 6. Offer and Acceptance | 1-3 |
| 7. Post-Decision Handover | 0-1 |
| **Total** | **4-11** |

Timelines vary based on document completeness, field verification requirements, and manual review complexity.

## Workflow Controls

### Escalation Rules

- Applications stuck in any stage for more than 5 business days trigger escalation alerts
- Multiple soft rule violations escalate to senior underwriter
- Fraud signals escalate immediately regardless of stage

### Rework Loops

Underwriters can send applications back to earlier stages:

- Back to Credit Analyst for additional analysis
- Back to Loan Officer for document clarification
- Back to Field Officer for re-verification

Rework loops are logged in audit trail with reason codes.

### Parallel Processing

Stages 2 and 3 can overlap:

- Rule screening begins as soon as minimum document set available
- KYC validation can continue while preliminary screening runs

## Related Topics

- [Underwriting Rules](underwriting-rules.md) — Details on 50+ automated rules
- [Generate an Appraisal Report](../tasks/generate-an-appraisal-report.md) — How to create the 4-page report used in Stage 4
- [API Endpoints](../reference/api-endpoints.md) — API operations for each workflow stage
