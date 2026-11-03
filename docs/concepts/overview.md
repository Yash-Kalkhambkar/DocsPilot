---
title: CreditShield Overview
topic_type: concept
audience: developers, loan officers
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: "Yash Kalkhambkar"
---

# CreditShield Overview

CreditShield is an end-to-end digital lending platform for loan origination and risk decision support.

## What CreditShield Is

CreditShield manages the complete journey from loan application submission to final underwriting decision. The platform combines automated rule enforcement, AI-powered risk analysis, and human oversight to help lenders process applications faster while maintaining credit quality and regulatory compliance.

The system serves two primary audiences:

- **Borrowers** interact through mobile and web interfaces to submit applications, upload documents, and track progress
- **Lending staff** (loan officers, credit analysts, field officers, underwriters, administrators) use the web dashboard to review applications, validate information, and make credit decisions

## System Architecture

CreditShield consists of four main components:

### Backend API

Technology: FastAPI + PostgreSQL

The backend manages:

- User authentication (JWT tokens)
- Borrower authentication and profiles
- Application workflow state
- Document storage metadata
- API layer for all system operations

See [API Endpoints](../reference/api-endpoints.md) for the complete endpoint list.

### AI Agent Layer

Technology: Python ReAct agent + AWS Bedrock (Llama 3 70B) + FAISS

The AI agent provides:

- Explainable credit risk analysis
- Retrieval-Augmented Generation (RAG) over RBI circulars and lending policies
- Fraud detection and income verification
- Rule violation reporting with regulatory citations
- Counterfactual recommendations (what borrowers can change to qualify)
- 4-page professional appraisal reports

The agent architecture uses tool calling to perform specific analysis tasks. See [RAG Grounding](rag-grounding.md) for details on how the agent retrieves policy documents.

### Web Dashboard

Technology: React + Vite

Internal operations interface for lending staff. Provides role-specific views and workflows for:

- Loan officers: application intake, document review, borrower communication
- Credit analysts: financial assessment, AI output validation, recommendation submission
- Field officers: verification task assignment, on-ground observation upload
- Underwriters: final decision-making with policy compliance checks
- System admins: user management, access control, audit logs

### Mobile Application

Technology: Flutter

Borrower-facing interface for:

- Account creation and login
- KYC document upload
- Loan application submission
- Offer selection
- Application status tracking
- Notifications

## How the Components Work Together

1. Borrower submits application through mobile app
2. Backend API stores application and triggers workflow
3. AI agent runs automated rule checks and generates risk analysis
4. Lending staff review application and AI outputs through web dashboard
5. Field officer (if needed) completes physical verification
6. Credit analyst validates analysis and submits recommendation
7. Underwriter makes final decision
8. Backend updates application status and notifies borrower

## Key Features

### Automated Rule Enforcement

50+ configurable underwriting rules organized across 5 risk categories automatically evaluate every application. Hard rules cause auto-reject. Soft rules trigger manual review. See [Underwriting Rules](underwriting-rules.md).

### Explainable AI Decisions

Every AI-generated recommendation includes:

- Clear rationale with specific data points
- Regulatory citations from RBI circulars and lending policies
- Confidence level for the recommendation
- Counterfactual suggestions for improvement

### Dual Validation

AI outputs undergo validation and auto-correction across retry rounds before presentation to human reviewers.

### Audit Trail

Complete workflow history retained for every application:

- Who performed each action
- When the action occurred
- What decision was made
- Why the decision was made (captured rationale)

### Mock Mode

Developers can run the full system without AWS credentials. Mock mode simulates all AWS Bedrock interactions for testing and development. See [Configure AWS Bedrock](../tasks/configure-aws-bedrock.md).

## Supported Loan Types

CreditShield handles multiple loan products with product-specific rules:

- Personal loans
- Education loans
- Business loans
- Micro loans
- Buy Now Pay Later (BNPL)

## Regulatory Compliance

The platform grounds decisions in:

- RBI Master Direction on Digital Lending (2022)
- Internal credit policies
- Lender-specific underwriting guidelines

RAG retrieval ensures every rule violation cites the relevant regulatory source. See [RAG Grounding](rag-grounding.md).

## Deployment Options

CreditShield supports:

- Local development (see [Run CreditShield Locally](../tasks/run-creditshield-locally.md))
- Docker containers (docker-compose provided)
- Kubernetes orchestration (manifests available in repository)

## What CreditShield Does Not Do

- **Post-disbursal loan servicing:** Repayment tracking and collections are handled by downstream systems
- **Credit bureau integration:** CIBIL scores and bureau data must be obtained through external integrations
- **Payment gateway integration:** Disbursal and repayment processing require separate payment system integration
- **Automatic model retraining:** ML models are trained offline and deployed manually

## Next Steps

- Learn the [Loan Origination Lifecycle](loan-origination-lifecycle.md)
- Understand [Underwriting Rules](underwriting-rules.md)
- [Run CreditShield locally](../tasks/run-creditshield-locally.md) to explore the system
