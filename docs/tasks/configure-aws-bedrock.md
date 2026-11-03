---
title: Configure AWS Bedrock
topic_type: task
audience: developers
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: "Yash Kalkhambkar"
---

# Configure AWS Bedrock

Enable AWS Bedrock for production AI features including Llama 3 70B LLM and Titan Embeddings.

## Prerequisites

- AWS account with Bedrock access
- AWS CLI configured or access credentials (access key ID and secret key)
- CreditShield backend running locally (see [Run CreditShield Locally](run-creditshield-locally.md))

## Steps

### 1. Enable Bedrock model access in AWS Console

Log in to AWS Console and navigate to AWS Bedrock service.

### 2. Select the ap-south-1 region

CreditShield uses **Asia Pacific (Mumbai) ap-south-1** region by default.

Change region in top-right corner of AWS Console.

### 3. Request model access

Navigate to **Model access** in the Bedrock console left sidebar.

Click **Request model access** or **Manage model access**.

### 4. Enable Llama 3 70B Instruct

Find **Meta Llama 3 70B Instruct** in the model list.

Click **Request access** and accept terms.

Model ID: `meta.llama3-70b-instruct-v1:0`

### 5. Enable Titan Embed Text v2

Find **Amazon Titan Embed Text v2** in the model list.

Click **Request access** and accept terms.

Model ID: `amazon.titan-embed-text-v2:0`

### 6. Wait for sanction

Model access is typically granted within 5-10 minutes for standard AWS accounts.

Check status in **Model access** page. Status should change from "In progress" to "Access granted".

### 7. Obtain AWS credentials

**Option A: Use AWS CLI configuration (recommended)**

If AWS CLI is already configured:

```bash
aws configure list
```

CreditShield will use the default profile credentials automatically.

**Option B: Generate access keys**

1. Navigate to IAM in AWS Console
2. Select your user
3. Go to **Security credentials** tab
4. Click **Create access key**
5. Choose **Application running outside AWS**
6. Copy the Access Key ID and Secret Access Key

!!! danger "Never commit AWS credentials"
    Do not commit access keys to version control. Use environment variables only.

### 8. Configure environment variables

Edit `.env` file in the AI agent directory:

```bash
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
BEDROCK_MODEL_ID=meta.llama3-70b-instruct-v1:0
BEDROCK_EMBEDDING_MODEL=amazon.titan-embed-text-v2:0
MOCK_MODE=false
```

Replace `your-access-key-id` and `your-secret-access-key` with your actual credentials.

!!! note "Using IAM roles"
    If running on EC2 or ECS, attach an IAM role with Bedrock permissions instead of using access keys. Leave AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY unset.

### 9. Verify Bedrock configuration

Test the connection:

```bash
python -c "import boto3; client = boto3.client('bedrock-runtime', region_name='ap-south-1'); print('Bedrock client initialized successfully')"
```

**Expected result:** "Bedrock client initialized successfully" with no errors.

### 10. Run AI agent with real Bedrock

Start the AI agent or run tests:

```bash
cd ai_agent
python -m pytest tests/test_agent_run.py -v
```

**Expected result:** Tests execute using real AWS Bedrock instead of mock responses.

## Verify the Setup

Confirm the following:

- [ ] Llama 3 70B Instruct model access granted in ap-south-1
- [ ] Titan Embed Text v2 model access granted in ap-south-1
- [ ] AWS credentials configured (CLI or environment variables)
- [ ] `MOCK_MODE=false` set in environment
- [ ] Bedrock client initializes without errors
- [ ] AI agent tests pass with real Bedrock calls

## Configuration Options

### Change AWS Region

Edit `AWS_REGION` in `.env`:

```bash
AWS_REGION=us-east-1
```

!!! warning "Model availability varies by region"
    Not all Bedrock models are available in all regions. Confirm model availability in your target region before changing AWS_REGION.

### Use Different LLM

Edit `BEDROCK_MODEL_ID` in `.env`:

```bash
BEDROCK_MODEL_ID=anthropic.claude-v2
```

!!! note "Prompt format may differ"
    Different models require different prompt formats. CreditShield is optimized for Llama 3. Using alternative models may require code changes.

### Tune LLM Parameters

Edit these environment variables:

```bash
MAX_TOKENS=2048
TEMPERATURE=0.3
```

- `MAX_TOKENS`: Maximum tokens in LLM response (default varies by model)
- `TEMPERATURE`: Randomness (0.0 = deterministic, 1.0 = creative)

See [Configuration Reference](../reference/configuration.md) for all parameters.

## Cost Estimation

AWS Bedrock charges per token (input and output).

**Llama 3 70B Instruct pricing (as of Nov 2026):**

- Input: $0.00099 per 1000 tokens
- Output: $0.00132 per 1000 tokens

**Titan Embed Text v2 pricing:**

- $0.00002 per 1000 tokens

**Typical cost per loan application:**

- LLM tokens: ~3000 input + ~1500 output = $4.95 per 1000 applications
- Embedding tokens: ~2000 per application = $0.04 per 1000 applications
- **Total: ~$5 per 1000 applications**

Use AWS Cost Explorer to monitor actual usage.

## Troubleshooting

### Model access pending

**Cause:** Model access not yet sanctioned.

**Solution:** Wait 5-10 minutes. Refresh **Model access** page in AWS Console. Contact AWS Support if sanction delayed beyond 24 hours.

### ResourceNotFoundException

**Error message:** "Could not resolve model meta.llama3-70b-instruct-v1:0"

**Cause:** Model not available in selected region, or model ID incorrect.

**Solution:**

1. Confirm model ID matches exactly: `meta.llama3-70b-instruct-v1:0`
2. Verify region set to ap-south-1 or a region where model is available
3. Check model access status in AWS Console

### AccessDeniedException

**Error message:** "User: arn:aws:iam::123456789:user/myuser is not authorized to perform: bedrock:InvokeModel"

**Cause:** IAM permissions insufficient.

**Solution:** Attach the following policy to your IAM user or role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "*"
    }
  ]
}
```

### Credentials not found

**Error message:** "Unable to locate credentials"

**Cause:** AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY not set, and no AWS CLI profile configured.

**Solution:**

1. Configure AWS CLI: `aws configure`
2. Or set environment variables explicitly
3. Or attach IAM role if running on EC2/ECS

## Mock Mode for Development

To test without AWS credentials, enable mock mode:

```bash
MOCK_MODE=true
```

Mock mode simulates Bedrock responses for development and testing. See [Run CreditShield Locally](run-creditshield-locally.md).

## Next Steps

- Generate a [4-page appraisal report](generate-an-appraisal-report.md) using real AI
- Review [RAG Grounding](../concepts/rag-grounding.md) to understand how Bedrock is used
- Check [Configuration Reference](../reference/configuration.md) for advanced settings
