---
title: Glossary
topic_type: reference
audience: all
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: "Yash Kalkhambkar"
---

# Glossary

Definitions of terms and acronyms used in CreditShield documentation.

## A

**Appraisal report**  
Bank-grade 4-page professional loan assessment document generated for loan officers.

**Application Reference Number (ARN)**  
Unique identifier assigned to each loan application.

**AWS Bedrock**  
Amazon Web Services' managed service for foundation models including LLMs and embeddings.

## B

**BNPL (Buy Now Pay Later)**  
Short-term consumer financing option allowing delayed payment.

**Borrower**  
Individual applying for a loan through CreditShield.

**Branch manager**  
Senior role holding final underwriting authority for the branch.

## C

**CIBIL score**  
Credit score provided by Credit Information Bureau (India) Limited, ranging 300-900.

**Counterfactual**  
Suggestion showing how a borrower could qualify by changing specific factors.

**Credit analyst**  
Specialist who performs financial and risk assessment and validates AI outputs.

**Credit behaviour**  
Past pattern of credit usage and repayment.

**CreditShield**  
Full-stack digital lending platform for loan origination and risk decision support.

## D

**Digital lending**  
Lending operations conducted through digital channels rather than physical branches.

**Disbursal**  
Transfer of approved loan amount to borrower's account.

**Document tampering**  
Unauthorized modification of financial documents such as salary slips or bank statements.

## E

**Embeddings**  
Numerical vector representations of text used for semantic search in RAG systems.

**EMI (Equated Monthly Installment)**  
Fixed monthly loan repayment amount including principal and interest.

## F

**FAISS**  
Facebook AI Similarity Search: library for efficient vector similarity search, used for RAG indexing.

**FastAPI**  
Python web framework used for CreditShield backend API.

**Field officer**  
Staff member who conducts on-ground verification of residence, business, or employment.

**Financial discipline**  
Quality of expense management and savings habits.

**Fixed Obligations to Income Ratio (FOIR)**  
Monthly debt payments divided by monthly income, expressed as percentage. Key metric for loan affordability.

**Fraud signal**  
Pattern or behavior indicating possible fraudulent activity.

## H

**Hard rule**  
Underwriting rule that causes automatic rejection when violated, with no manual override.

## I

**Income stability**  
Measure of how regular and predictable income sources are over time.

## J

**JWT (JSON Web Token)**  
Authentication token format used for API access control.

## K

**Know Your Customer (KYC)**  
Identity verification process required by financial regulations.

## L

**Lifestyle risk**  
Risk from unsustainable spending patterns or discretionary expenses.

**Liquidity stress**  
Periods of insufficient cash balance in borrower's bank account.

**Llama 3 70B**  
Meta's large language model with 70 billion parameters used for explainable credit decisions.

**LLM (Large Language Model)**  
AI system trained on large text corpora to generate human-like text.

**Loan burden**  
Total existing debt obligations relative to income.

**Loan officer**  
Front-line staff responsible for application intake and document completeness.

**Loan origination**  
Complete lifecycle from loan application to approval or rejection.

**Loan Origination System (LOS)**  
Software platform managing the loan origination lifecycle.

**Loan stacking**  
Taking multiple loans in a short time period, typically indicating financial distress.

## M

**Mock mode**  
Development mode that simulates AWS Bedrock without requiring credentials.

## N

**Non-Performing Asset (NPA)**  
Loan in default or overdue beyond the specified period.

## P

**PostgreSQL**  
Open-source relational database system used for CreditShield backend.

## R

**RAG (Retrieval-Augmented Generation)**  
AI technique combining document search with text generation to ground answers in specific sources.

**RBI (Reserve Bank of India)**  
India's central banking institution and financial regulator.

**RBI circular**  
Official policy document issued by Reserve Bank of India.

**ReAct**  
Reasoning and Acting: AI agent pattern combining reasoning with tool use.

**Risk driver**  
Factor contributing to overall credit risk assessment.

## S

**Sanction**  
Official approval to disburse a loan.

**Soft rule**  
Underwriting rule that triggers manual review when violated, allowing potential override with documented rationale.

**System admin**  
Role managing users, access control, and system configuration.

## U

**Underwriter**  
Final decision-maker with credit authority, typically a branch manager.

**Underwriting rule**  
Configurable decision criterion applied during credit evaluation.

## V

**Vector store**  
Database system storing and retrieving embeddings for semantic search.

## Acronyms Reference

| Acronym | Full Term | Definition |
|---------|-----------|------------|
| ARN | Application Reference Number | Unique loan application identifier |
| AWS | Amazon Web Services | Cloud computing platform |
| BNPL | Buy Now Pay Later | Short-term financing option |
| CIBIL | Credit Information Bureau (India) Limited | Credit bureau providing credit scores |
| EMI | Equated Monthly Installment | Fixed monthly loan payment |
| FAISS | Facebook AI Similarity Search | Vector similarity search library |
| FOIR | Fixed Obligations to Income Ratio | Debt-to-income metric |
| JWT | JSON Web Token | Authentication token format |
| KYC | Know Your Customer | Identity verification process |
| LLM | Large Language Model | AI text generation system |
| LOS | Loan Origination System | Loan workflow management platform |
| NPA | Non-Performing Asset | Defaulted loan |
| RAG | Retrieval-Augmented Generation | AI technique combining search and generation |
| RBI | Reserve Bank of India | Central bank and regulator |

## Rule IDs Reference

### Hard Rules

| Rule ID | Name | Description |
|---------|------|-------------|
| HR-01 | FOIR Maximum | Fixed Obligations to Income Ratio must not exceed 65% |
| HR-02 | Document Tampering | No document alteration detected |
| HR-03 | NPA/Write-off History | No NPA or write-off in last 36 months |
| HR-04 | Income Variance | Verified income within 50% of declared income |
| HR-05 | Loan Stacking | Maximum 3 new unsecured loans in 90 days |
| HR-06 | Minimum CIBIL Score | Minimum score 550 for unsecured personal loans |
| HR-07 | Minimum Income | Income meets product-specific threshold |

### Soft Rules

| Rule ID | Name | Description |
|---------|------|-------------|
| SR-01 | Income Variability | Income coefficient of variation triggers review |

## Workflow Status Values

| Status | Stage | Meaning |
|--------|-------|---------|
| `draft` | 1 | Application started but not submitted |
| `submitted` | 1 | Application submitted, awaiting KYC |
| `kyc_pending` | 2 | KYC documents required |
| `kyc_complete` | 2 | KYC validation passed |
| `screening` | 3 | Automated rule screening in progress |
| `manual_review` | 3-4 | Soft rule violations flagged |
| `analysis` | 4 | Credit Analyst performing assessment |
| `underwriting` | 5 | Underwriter reviewing for final decision |
| `sanctioned` | 5 | Approved unconditionally |
| `conditional_sanction` | 5 | Approved with conditions |
| `rejected` | 3-5 | Application rejected |
| `offer_pending` | 6 | Offer sent, awaiting acceptance |
| `offer_accepted` | 6 | Borrower accepted offer |
| `closed` | 7 | Workflow complete, handed over |

## Related Topics

- [Underwriting Rules](../concepts/underwriting-rules.md) — Detailed rule explanations
- [Loan Origination Lifecycle](../concepts/loan-origination-lifecycle.md) — Workflow stages
- [Configuration](configuration.md) — Environment variables and settings
