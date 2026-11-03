---
title: CreditShield Documentation
topic_type: reference
audience: all
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: ""
---

# CreditShield Documentation

CreditShield is a full-stack digital lending platform that automates the 7-stage loan origination lifecycle with AI-powered risk assessment.

## What CreditShield Does

CreditShield manages loan applications from initial borrower contact through final underwriting decision. The platform combines rule-based policy enforcement with explainable AI analysis to help lenders make faster, more consistent credit decisions while maintaining regulatory compliance.

**Key capabilities:**

- **7-stage workflow:** Structured loan origination from application intake to post-decision handover
- **50+ underwriting rules:** Automated hard and soft rule evaluation across 5 risk categories
- **AI-powered analysis:** AWS Bedrock with Llama 3 70B generates explainable credit decisions
- **4-page appraisal reports:** Bank-grade professional reports for loan officers
- **RAG document retrieval:** Grounds decisions in RBI circulars and lending policies
- **Multi-role access:** Distinct workflows for loan officers, credit analysts, field officers, underwriters, and administrators

## Getting Started

### For Developers

1. [Run CreditShield locally](tasks/run-creditshield-locally.md) to set up your development environment
2. [Configure AWS Bedrock](tasks/configure-aws-bedrock.md) for AI-powered risk analysis
3. Review [API Endpoints](reference/api-endpoints.md) and [Configuration](reference/configuration.md) reference

### For Loan Officers and Analysts

1. Read [Loan Origination Lifecycle](concepts/loan-origination-lifecycle.md) to understand the 7 stages
2. Learn about [Underwriting Rules](concepts/underwriting-rules.md) enforced automatically
3. Follow [Generate an Appraisal Report](tasks/generate-an-appraisal-report.md) to create loan assessments

## Documentation Structure

### Concepts

High-level explanations of how CreditShield works:

- [Overview](concepts/overview.md) — System architecture and components
- [Loan Origination Lifecycle](concepts/loan-origination-lifecycle.md) — 7 stages from application to decision
- [Underwriting Rules](concepts/underwriting-rules.md) — 50+ automated policy checks
- [RAG Grounding](concepts/rag-grounding.md) — How AI retrieves and uses policy documents

### Tasks

Step-by-step guides for common operations:

- [Run CreditShield Locally](tasks/run-creditshield-locally.md)
- [Configure AWS Bedrock](tasks/configure-aws-bedrock.md)
- [Add an Underwriting Rule](tasks/add-an-underwriting-rule.md)
- [Generate an Appraisal Report](tasks/generate-an-appraisal-report.md)

### Reference

Technical specifications and API documentation:

- [API Endpoints](reference/api-endpoints.md) — Complete endpoint list with request/response formats
- [Configuration](reference/configuration.md) — Environment variables and settings
- [Glossary](reference/glossary.md) — Terms and acronyms

### Release Notes

- [v0.1.0](release-notes/v0.1.0.md) — Initial release

## Technology Stack

- **Backend:** FastAPI + PostgreSQL
- **AI Layer:** AWS Bedrock (Llama 3 70B, Titan Embeddings), FAISS vector store
- **Frontend:** React + Vite web dashboard, Flutter mobile app
- **Deployment:** Docker + Kubernetes

## Product Version

This documentation covers **CreditShield v0.1.0**.

## Support

For issues and questions:

- **Code:** [GitHub Repository](https://github.com/Yash-Kalkhambkar/Credshield)
- **API Documentation:** View interactive OpenAPI docs at `/docs` when running locally

## Quick Links

- [Glossary](reference/glossary.md) — Definitions of terms and acronyms
- [Configuration Reference](reference/configuration.md) — All environment variables
- [API Reference](reference/api-endpoints.md) — Complete API documentation
