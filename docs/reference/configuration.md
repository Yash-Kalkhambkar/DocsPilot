---
title: Configuration
topic_type: reference
audience: developers
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: ""
---

# Configuration

Environment variables and configuration options for CreditShield.

## Configuration Files

- **Backend:** `.env` in `Backend/` directory
- **AI Agent:** Environment variables in shell or `.env` in AI agent directory

Create configuration files from examples:

```bash
cp Backend/.env.example Backend/.env
```

## Backend Configuration

### Database

**DATABASE_URL**

PostgreSQL connection string.

**Format:** `postgresql://username:password@host:port/database`

**Example:** `postgresql://postgres:secret@localhost:5432/creditshield`

**Required:** Yes

### Authentication

**JWT_SECRET_KEY**

Secret key for signing JWT tokens.

**Format:** Random string (at least 32 characters)

**Generate:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Required:** Yes

!!! danger "Keep secret"
    Never commit JWT_SECRET_KEY to version control. Use different keys per environment.

**JWT_ALGORITHM**

Algorithm for JWT token generation.

**Default:** `HS256`

**Options:** `HS256`, `HS384`, `HS512`, `RS256`

**Required:** No

### System Admin Credentials

**SYSTEM_ADMIN_USERNAME**

Username for system administrator account.

**Default:** `system_admin`

**Required:** No (uses default if not set)

**SYSTEM_ADMIN_PASSWORD**

Password for system administrator account.

**Default:** `Admin@123`

**Required:** No (uses default if not set)

!!! warning "Change default password"
    Change the default system admin password before deploying to production.

### Server Configuration

**HOST**

API server host address.

**Default:** `0.0.0.0`

**PORT**

API server port.

**Default:** `8000`

**RELOAD**

Enable auto-reload on code changes (development only).

**Default:** `true` (development), `false` (production)

## AI Agent Configuration

### AWS Credentials

**AWS_REGION**

AWS region for Bedrock service.

**Default:** `ap-south-1`

**Options:** Any AWS region with Bedrock availability

**Required:** Yes (unless mock mode)

**AWS_ACCESS_KEY_ID**

AWS access key ID.

**Format:** 20-character alphanumeric string

**Required:** Yes (unless using IAM role or mock mode)

!!! danger "Never commit AWS credentials"
    Do not commit AWS credentials to version control. Use environment variables or IAM roles.

**AWS_SECRET_ACCESS_KEY**

AWS secret access key.

**Format:** 40-character alphanumeric string

**Required:** Yes (unless using IAM role or mock mode)

### Mock Mode

**MOCK_MODE**

Enable mock mode to simulate AWS Bedrock without credentials.

**Options:** `true`, `false`

**Default:** `true` if AWS credentials not found, otherwise `false`

**Use case:** Development and testing without AWS account

### Bedrock Models

**BEDROCK_MODEL_ID**

LLM model identifier for text generation.

**Default:** `meta.llama3-70b-instruct-v1:0`

**Options:**
- `meta.llama3-70b-instruct-v1:0` (recommended)
- `anthropic.claude-v2`
- `anthropic.claude-3-sonnet-20240229-v1:0`

**Required:** No (uses default)

**BEDROCK_EMBEDDING_MODEL**

Embedding model for RAG.

**Default:** `amazon.titan-embed-text-v2:0`

**Options:**
- `amazon.titan-embed-text-v2:0` (recommended)
- `amazon.titan-embed-text-v1`

**Required:** No (uses default)

### LLM Parameters

**MAX_TOKENS**

Maximum tokens in LLM response.

**Default:** Model-specific (typically 2048)

**Range:** 100-4096

**Higher values:** Allow longer responses but increase cost and latency

**TEMPERATURE**

LLM sampling temperature.

**Default:** `0.3`

**Range:** 0.0-1.0

- `0.0`: Deterministic, always selects highest probability token
- `0.3`: Slight randomness (recommended for factual tasks)
- `1.0`: Maximum creativity

### RAG Configuration

**VECTOR_STORE**

Vector database backend for RAG.

**Options:** `in_memory`, `pgvector`

**Default:** `in_memory`

**Notes:**
- `in_memory`: FAISS index in process memory (fast, not persistent)
- `pgvector`: PostgreSQL extension (TODO: not yet implemented)

**RAG_TOP_K**

Number of document chunks to retrieve per query.

**Default:** `3`

**Range:** 1-10

**Higher values:** More context but slower and may include irrelevant chunks

**RAG_CHUNK_SIZE**

Target chunk size in tokens for document splitting.

**Default:** `400`

**Range:** 100-1000

**Optimal range:** 300-500 tokens per chunk

**RAG_CHUNK_OVERLAP**

Token overlap between adjacent chunks.

**Default:** `50`

**Range:** 0-200

**Purpose:** Prevent sentences from being split across chunk boundaries

## ML Model Configuration

**MODEL_PATH**

Path to trained ML model file for loan appraisal.

**Example:** `loan_appraisal_model/model.pkl`

**Required:** Yes (for appraisal report generation)

**RULES_PATH**

Path to underwriting rules directory.

**Example:** `ai_agent/rules`

**Required:** Yes (for rule evaluation)

## Logging Configuration

**LOG_LEVEL**

Logging verbosity.

**Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

**Default:** `INFO`

**FASTMCP_LOG_LEVEL**

Logging level for FastMCP library (if used).

**Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`

**Default:** `ERROR`

## Docker Configuration

When running in Docker, set environment variables in `docker-compose.yml`:

```yaml
environment:
  - DATABASE_URL=postgresql://postgres:password@db:5432/creditshield
  - JWT_SECRET_KEY=${JWT_SECRET_KEY}
  - AWS_REGION=ap-south-1
  - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
  - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
  - MOCK_MODE=false
```

Use `.env` file for sensitive values and reference with `${VARIABLE}` syntax.

## Kubernetes Configuration

Store secrets in Kubernetes secrets:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: creditshield-secrets
type: Opaque
stringData:
  database-url: postgresql://postgres:password@db:5432/creditshield
  jwt-secret-key: your-generated-secret
  aws-access-key-id: your-aws-key
  aws-secret-access-key: your-aws-secret
```

Reference in deployment:

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: creditshield-secrets
        key: database-url
```

## Configuration Validation

Validate configuration on startup:

```python
from app.core.config import settings

print(f"Database: {settings.DATABASE_URL}")
print(f"JWT Algorithm: {settings.JWT_ALGORITHM}")
print(f"AWS Region: {settings.AWS_REGION}")
print(f"Mock Mode: {settings.MOCK_MODE}")
```

Missing required variables will raise configuration errors.

## Environment-Specific Configuration

### Development

```bash
DATABASE_URL=postgresql://postgres:dev@localhost:5432/creditshield_dev
JWT_SECRET_KEY=dev-secret-not-for-production
MOCK_MODE=true
LOG_LEVEL=DEBUG
```

### Staging

```bash
DATABASE_URL=postgresql://postgres:staging@db-staging:5432/creditshield_staging
JWT_SECRET_KEY=<generated-secret>
AWS_REGION=ap-south-1
MOCK_MODE=false
LOG_LEVEL=INFO
```

### Production

```bash
DATABASE_URL=postgresql://postgres:<secret>@db-prod:5432/creditshield_prod
JWT_SECRET_KEY=<generated-secret>
AWS_REGION=ap-south-1
MOCK_MODE=false
LOG_LEVEL=WARNING
RELOAD=false
```

## Security Best Practices

1. **Never commit secrets** to version control
2. **Use different secrets per environment** (dev, staging, production)
3. **Rotate JWT secrets periodically** (invalidates existing tokens)
4. **Use IAM roles instead of access keys** when running on AWS (EC2, ECS, Lambda)
5. **Restrict database user permissions** (no need for superuser access)
6. **Use HTTPS in production** (not HTTP)

## Configuration Troubleshooting

### "DATABASE_URL not set" error

**Solution:** Create `.env` file in Backend/ directory with DATABASE_URL variable.

### JWT tokens not validating

**Cause:** JWT_SECRET_KEY mismatch or not loaded.

**Solution:** Restart API server after changing `.env`. Confirm `.env` file in correct directory.

### "Unable to locate credentials" (AWS)

**Cause:** AWS credentials not set and not using mock mode.

**Solution:** Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, or set MOCK_MODE=true.

### Mock mode not activating

**Cause:** AWS credentials present and MOCK_MODE not explicitly set to true.

**Solution:** Set `MOCK_MODE=true` explicitly to override credential detection.

## Related Topics

- [Run CreditShield Locally](../tasks/run-creditshield-locally.md) — Set up development environment
- [Configure AWS Bedrock](../tasks/configure-aws-bedrock.md) — AWS-specific configuration
- [API Endpoints](api-endpoints.md) — Endpoints requiring authentication
