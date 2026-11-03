---
title: Run CreditShield Locally
topic_type: task
audience: developers
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: "Yash Kalkhambkar"
---

# Run CreditShield Locally

Set up CreditShield development environment and run the backend API locally.

## Prerequisites

- Python 3.11 or later
- PostgreSQL 14 or later
- Git
- pip (Python package manager)

## Steps

### 1. Clone the repository

```bash
git clone https://github.com/Yash-Kalkhambkar/Credshield.git
cd Credshield
```

### 2. Set up the backend

Navigate to the Backend directory:

```bash
cd Backend
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**On Linux/macOS:**

```bash
source venv/bin/activate
```

**On Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**

```cmd
venv\Scripts\activate.bat
```

### 5. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure the following required variables:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/creditshield
JWT_SECRET_KEY=your-secret-key-here
SYSTEM_ADMIN_USERNAME=system_admin
SYSTEM_ADMIN_PASSWORD=Admin@123
```

Replace `user`, `password`, and database name with your PostgreSQL credentials.

!!! warning "Generate a secure JWT secret"
    Generate a random secret key for JWT_SECRET_KEY. Do not use the example value in production.

    ```bash
    python -c "import secrets; print(secrets.token_urlsafe(32))"
    ```

See [Configuration Reference](../reference/configuration.md) for all available environment variables.

### 7. Verify database connectivity

Start the API server in development mode:

```bash
uvicorn app.main:app --reload
```

!!! note "Database tables not auto-created"
    CreditShield does not create database tables at startup. The above command starts the API but the database remains empty until migrations are run or tables are created manually.

### 8. Test the health endpoint

Open a browser or use `curl`:

```bash
curl http://127.0.0.1:8000/health/db
```

**Expected response:** JSON indicating database connection status.

### 9. View API documentation

Navigate to `http://127.0.0.1:8000/docs` in your browser.

**Expected result:** Interactive OpenAPI (Swagger) documentation displaying all available endpoints.

### 10. Test authentication

Use the system admin credentials to obtain a JWT token:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"system_admin","password":"Admin@123"}'
```

**Expected response:** JSON with `access_token` field.

## Optional: Set Up AI Agent in Mock Mode

To test AI features without AWS credentials:

### 1. Navigate to the AI agent directory

```bash
cd ../ai_agent
```

(Or from repository root: `cd "Design Loan Origination Dashboard/ai_agent"` — path differs based on directory structure)

### 2. Install AI agent dependencies

```bash
pip install -r requirements-agent.txt
```

### 3. Enable mock mode

**On Linux/macOS:**

```bash
export MOCK_MODE=true
```

**On Windows (PowerShell):**

```powershell
$env:MOCK_MODE="true"
```

### 4. Run AI agent tests

```bash
python -m pytest tests -v
```

**Expected result:** All tests pass. AI agent uses mock LLM and embeddings instead of AWS Bedrock.

## Verify the Setup

Confirm the following:

- [ ] Backend API running at `http://127.0.0.1:8000`
- [ ] OpenAPI docs accessible at `/docs`
- [ ] Database health check returns success
- [ ] JWT token generated successfully with system admin credentials
- [ ] AI agent tests pass in mock mode (if set up)

## Troubleshooting

### Connection refused when accessing API

**Cause:** API server not running or using wrong port.

**Solution:** Confirm `uvicorn` command completed without errors. Check that port 8000 is not in use by another application.

### Database connection error

**Cause:** PostgreSQL not running or credentials incorrect.

**Solution:**

1. Verify PostgreSQL service is running:
   ```bash
   pg_isready
   ```

2. Confirm credentials in `.env` match your PostgreSQL setup.

3. Ensure database exists. Create if needed:
   ```sql
   CREATE DATABASE creditshield;
   ```

### Import errors when running tests

**Cause:** PYTHONPATH not set for AI agent tests.

**Solution:** Set PYTHONPATH before running pytest:

**On Linux/macOS:**

```bash
export PYTHONPATH=.
```

**On Windows (PowerShell):**

```powershell
$env:PYTHONPATH="."
```

Then re-run: `python -m pytest ai_agent/tests -v`

### JWT token invalid or expired

**Cause:** JWT_SECRET_KEY mismatch between token generation and validation.

**Solution:** Ensure `.env` file loaded correctly. Restart API server after changing `.env`.

## Next Steps

- [Configure AWS Bedrock](configure-aws-bedrock.md) to enable production AI features
- Review [API Endpoints](../reference/api-endpoints.md) for available operations
- Read [Loan Origination Lifecycle](../concepts/loan-origination-lifecycle.md) to understand the workflow

## Security Notes

- Never commit `.env` file to version control
- Use strong passwords for system admin account in production
- Generate unique JWT_SECRET_KEY per environment
- Use HTTPS in production, not HTTP
