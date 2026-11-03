---
title: API Endpoints
topic_type: reference
audience: developers
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: ""
---

# API Endpoints

Complete reference for CreditShield REST API endpoints.

## Base URL

**Local development:** `http://127.0.0.1:8000`

**Production:** Configure per deployment

## Authentication

Most endpoints require JWT authentication. Include token in `Authorization` header:

```
Authorization: Bearer <your-jwt-token>
```

Obtain token from `/api/v1/auth/login` endpoint.

## System Health

### GET /health/db

Check database connectivity.

**Authentication:** Not required

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "database": "connected"
}
```

## Authentication Endpoints

### POST /api/v1/auth/login

Generate JWT token for internal users (system admin, loan officers, analysts, underwriters).

**Authentication:** Not required

**Request body:**

```json
{
  "username": "system_admin",
  "password": "Admin@123"
}
```

**Response:** `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "user": {
    "username": "system_admin",
    "role": "system_admin"
  }
}
```

**Errors:**

- `401 Unauthorized`: Invalid username or password

## Borrower Authentication

### POST /api/v1/borrower/auth/signup

Create new borrower account.

**Authentication:** Not required

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

**Response:** `201 Created`

```json
{
  "id": 42,
  "full_name": "Mohit Tade",
  "email": "mohit@example.com",
  "mobile_number": "9876543210",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

**Errors:**

- `400 Bad Request`: Email or mobile already registered
- `422 Unprocessable Entity`: Password does not meet requirements

### POST /api/v1/borrower/auth/login

Log in as borrower.

**Authentication:** Not required

**Request body:**

```json
{
  "identifier": "mohit@example.com",
  "password": "Abcd1234!"
}
```

`identifier` can be email or mobile number.

**Response:** `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "borrower": {
    "id": 42,
    "full_name": "Mohit Tade",
    "email": "mohit@example.com"
  }
}
```

**Errors:**

- `401 Unauthorized`: Invalid identifier or password

### GET /api/v1/borrower/auth/me

Get current borrower profile.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "id": 42,
  "full_name": "Mohit Tade",
  "email": "mohit@example.com",
  "mobile_number": "9876543210",
  "is_active": true,
  "created_at": "2026-11-01T10:30:00Z"
}
```

## Borrower Journey

### GET /api/v1/borrower/kyc/status

Get KYC verification status for current borrower.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "status": "kyc_pending",
  "required_documents": [
    "aadhaar",
    "pan",
    "address_proof",
    "income_proof"
  ],
  "submitted_documents": ["aadhaar", "pan"],
  "pending_documents": ["address_proof", "income_proof"]
}
```

### POST /api/v1/borrower/kyc/complete

Mark KYC as complete (called after all documents uploaded).

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "status": "kyc_complete",
  "message": "KYC verification completed successfully"
}
```

### POST /api/v1/borrower/eligibility/check

Check loan eligibility for borrower.

**Authentication:** Required (Bearer token)

**Request body:**

```json
{
  "loan_type": "personal",
  "loan_amount": 500000,
  "tenure_months": 24
}
```

**Response:** `200 OK`

```json
{
  "eligible": true,
  "loan_type": "personal",
  "max_loan_amount": 750000,
  "min_tenure": 12,
  "max_tenure": 60,
  "estimated_interest_rate": 12.5,
  "estimated_emi": 23539
}
```

### GET /api/v1/borrower/loan-types

List available loan products.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "loan_types": [
    {
      "code": "personal",
      "name": "Personal Loan",
      "min_amount": 50000,
      "max_amount": 1000000,
      "interest_rate_range": "10.5% - 18%"
    },
    {
      "code": "education",
      "name": "Education Loan",
      "min_amount": 100000,
      "max_amount": 5000000,
      "interest_rate_range": "8.5% - 12%"
    }
  ]
}
```

### POST /api/v1/borrower/applications

Create new loan application.

**Authentication:** Required (Bearer token)

**Request body:**

```json
{
  "loan_type": "personal",
  "loan_amount": 500000,
  "tenure_months": 24,
  "purpose": "Debt consolidation"
}
```

**Response:** `201 Created`

```json
{
  "arn": "APPROVE-2026-001",
  "loan_type": "personal",
  "loan_amount": 500000,
  "status": "submitted",
  "created_at": "2026-11-03T14:30:00Z"
}
```

### GET /api/v1/borrower/applications/current

Get current active application for borrower.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "arn": "APPROVE-2026-001",
  "loan_type": "personal",
  "loan_amount": 500000,
  "status": "kyc_pending",
  "created_at": "2026-11-03T14:30:00Z",
  "updated_at": "2026-11-03T15:00:00Z"
}
```

**Response:** `404 Not Found` if no active application

### GET /api/v1/borrower/documents/required

List required documents for current application.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "required": [
    {
      "type": "bank_statement",
      "description": "Last 6 months bank statement",
      "format": "PDF or CSV"
    },
    {
      "type": "salary_slip",
      "description": "Last 3 months salary slips",
      "format": "PDF"
    }
  ]
}
```

### POST /api/v1/borrower/consent/submit

Submit borrower consent for data processing.

**Authentication:** Required (Bearer token)

**Request body:**

```json
{
  "consent_type": "data_processing",
  "agreed": true
}
```

**Response:** `200 OK`

```json
{
  "consent_id": "CONSENT-001",
  "status": "accepted",
  "timestamp": "2026-11-03T14:45:00Z"
}
```

### GET /api/v1/borrower/rbi/checkpoint

Get RBI compliance checkpoint status.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "rbi_compliant": true,
  "checks_passed": ["kyc_verified", "consent_obtained", "cooling_period_respected"],
  "checks_pending": []
}
```

### GET /api/v1/borrower/risk-score

Retrieve risk assessment score.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "risk_score": 72,
  "risk_level": "MODERATE",
  "factors": [
    {"name": "Income Stability", "score": 80},
    {"name": "Credit Behaviour", "score": 65},
    {"name": "Financial Discipline", "score": 70}
  ]
}
```

### GET /api/v1/borrower/offers

Get available loan offers for borrower.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "offers": [
    {
      "offer_id": "OFFER-001",
      "loan_amount": 500000,
      "interest_rate": 12.5,
      "tenure_months": 24,
      "emi": 23539,
      "processing_fee": 5000,
      "valid_until": "2026-11-10T23:59:59Z"
    }
  ]
}
```

### POST /api/v1/borrower/offers/{offer_id}/select

Select and accept a loan offer.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "offer_id": "OFFER-001",
  "status": "accepted",
  "next_step": "agreement_signing"
}
```

### GET /api/v1/borrower/agreement

Get loan agreement details.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "agreement_id": "AGREEMENT-001",
  "loan_amount": 500000,
  "interest_rate": 12.5,
  "tenure_months": 24,
  "terms_url": "https://example.com/agreements/AGREEMENT-001.pdf"
}
```

### GET /api/v1/borrower/dashboard

Get borrower dashboard data.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "profile_completion": 85,
  "kyc_status": "complete",
  "active_applications": 1,
  "pending_actions": ["upload_income_proof"]
}
```

### GET /api/v1/borrower/tracker

Get application status tracker.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "arn": "APPROVE-2026-001",
  "current_stage": "credit_analysis",
  "stages": [
    {"name": "Application Intake", "status": "complete", "completed_at": "2026-11-03T14:30:00Z"},
    {"name": "KYC Verification", "status": "complete", "completed_at": "2026-11-03T15:00:00Z"},
    {"name": "Credit Analysis", "status": "in_progress", "completed_at": null},
    {"name": "Underwriting", "status": "pending", "completed_at": null}
  ]
}
```

### GET /api/v1/borrower/notifications

Get borrower notifications.

**Authentication:** Required (Bearer token)

**Response:** `200 OK`

```json
{
  "notifications": [
    {
      "id": 101,
      "type": "status_update",
      "message": "Your application is under credit analysis",
      "timestamp": "2026-11-03T16:00:00Z",
      "read": false
    }
  ]
}
```

## Risk Analysis

### POST /api/v1/risk/professional-report

Generate 4-page professional appraisal report.

**Authentication:** Required (system_admin or analyst role)

**Request (multipart/form-data):**

- `loan_type` (string): Loan type code (personal, education, business, micro, bnpl)
- `loan_amount` (float): Requested amount in rupees
- `statement` (file): Bank statement (CSV or PDF)
- `rules_path` (string): Path to underwriting rules directory
- `model_path` (string): Path to ML model file
- `use_bedrock` (boolean): Enable AWS Bedrock LLM (true/false)
- `output_format` (string): Output format (text or html)

**Response:** `200 OK`

Plain text or HTML formatted 4-page appraisal report.

**Errors:**

- `400 Bad Request`: Missing required parameters or invalid file
- `500 Internal Server Error`: Report generation failed

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP status codes:**

- `400 Bad Request`: Invalid input parameters
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server-side error

## Rate Limiting

TODO(verify) — Check if rate limiting implemented.

## Pagination

TODO(verify) — Check pagination parameters for list endpoints.

## API Versioning

Current API version: `v1`

Base path: `/api/v1/`

Future versions will be released under `/api/v2/`, `/api/v3/`, etc.

## Interactive Documentation

View interactive API documentation with request/response examples:

**Local:** `http://127.0.0.1:8000/docs`

Swagger UI automatically generated from FastAPI route definitions.

## Related Topics

- [Configuration](configuration.md) — Environment variables for API configuration
- [Run CreditShield Locally](../tasks/run-creditshield-locally.md) — Start the API server
- [Loan Origination Lifecycle](../concepts/loan-origination-lifecycle.md) — Workflow stages these APIs support
