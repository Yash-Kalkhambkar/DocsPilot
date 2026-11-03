---
title: RAG Grounding
topic_type: concept
audience: developers, credit analysts
product_version: 0.1.0
last_reviewed: 2026-11-03
ai_assisted: false
reviewed_by: ""
---

# RAG Grounding

CreditShield uses Retrieval-Augmented Generation (RAG) to ground AI decisions in RBI circulars, lending policies, and borrower documents.

## What RAG Does

RAG combines document retrieval with large language model (LLM) generation. Instead of relying solely on the LLM's training data, the system:

1. Searches relevant documents for the query
2. Retrieves the most relevant text chunks
3. Provides those chunks as context to the LLM
4. Instructs the LLM to answer based only on the provided context

This approach provides three benefits:

- **Accuracy:** Answers grounded in specific policy documents rather than general knowledge
- **Citations:** Every answer includes source document references
- **Control:** Responses restricted to approved policy sources, preventing hallucination

## How RAG Works in CreditShield

### Document Ingestion

Policy documents are processed during system setup:

1. **Split:** Documents divided into chunks of 300-500 tokens with small overlap
2. **Embed:** Each chunk converted to a numerical vector (embedding) representing its semantic meaning
3. **Index:** Embeddings stored in FAISS vector database for fast similarity search
4. **Metadata:** Source file, document type, and section heading tracked for each chunk

**Document sources:**

- RBI circulars (RBI Master Direction on Digital Lending 2022, KYC guidelines)
- Internal credit policies
- Lending product specifications
- Regulatory compliance documents

### Query Time Retrieval

When the AI agent needs policy information:

1. **User query or tool call:** Example: "Why was HR-01 violated?"
2. **Query embedding:** Question converted to same vector format as document chunks
3. **Similarity search:** FAISS finds top-k most semantically similar chunks (typically k=3-5)
4. **Context assembly:** Retrieved chunks combined into context for LLM
5. **Generation:** LLM generates answer restricted to retrieved context only

### Embedding Models

CreditShield supports two embedding backends:

**AWS Bedrock Titan Embed Text v2** (`amazon.titan-embed-text-v2:0`)

- Cloud-hosted model
- High quality semantic embeddings
- Requires AWS credentials
- Default for production

**Local sentence-transformers** (`all-MiniLM-L6-v2`)

- Runs locally without cloud dependency
- Faster for development
- Smaller model, slightly lower quality
- Used in mock mode

## Policy RAG

Policy RAG retrieves lending regulations and underwriting rules.

**Namespace:** `policy_global`

**When used:**

- Rule violation tool needs regulatory citation
- Credit analyst asks policy questions ("What does RBI say about FOIR limits?")
- Counterfactual tool suggests improvements ("How can borrower qualify?")

**Example query to embedding:**

"HR-01 FOIR 65 percent maximum unsecured personal loan obligations income"

**Retrieved context (example):**

> "Fixed Obligations to Income Ratio (FOIR) should not exceed 65% for unsecured personal loans as per internal credit policy aligned with RBI Master Direction on Digital Lending 2022 Section 4.3 on affordability assessment."

**Source document:** `rbi_digital_lending_2022.txt`

**LLM output with citation:**

> "HR-01 violation: FOIR 70% exceeds the maximum threshold of 65% for unsecured personal loans. Regulatory reference: RBI Master Direction — Digital Lending (2022) Section 4.3 requires affordability assessment ensuring EMI burden does not exceed borrower capacity. Source: rbi_digital_lending_2022.txt"

## Borrower Document RAG

Borrower document RAG retrieves information from uploaded loan application documents.

**Namespace:** `borrower_{ARN}` (unique per application)

**When used:**

- Income verification tool searches salary slips
- Fraud detection tool analyzes bank statements
- Credit analyst searches for specific transaction or detail

**Document types:**

- Salary slips
- Bank statements
- Income Tax Returns (ITR)
- Employment letters
- Address proofs
- Business financial statements

**Example query:**

"Salary credit from ACME Pvt Ltd in last 6 months"

**Retrieved context:**

> "Bank statement March 2026: Credit ₹75,000 from ACME PVT LTD on 2026-03-01. Bank statement April 2026: Credit ₹75,000 from ACME PVT LTD on 2026-04-01. [Similar entries for 4 more months]"

**LLM output:**

> "Borrower receives consistent monthly salary credits of ₹75,000 from ACME Pvt Ltd. Credits appear on 1st of every month for 6 consecutive months (Nov 2025 - April 2026), indicating stable salaried employment."

## Retrieval Strategies

CreditShield uses multiple retrieval strategies for robustness:

### 1. Semantic Search (Primary)

Vector similarity search using embeddings. Finds chunks with similar **meaning** to the query, even if exact words differ.

**Advantage:** Handles paraphrasing and conceptual questions.

**Example:** Query "income requirements" retrieves chunks about "minimum monthly salary", "earnings threshold", "compensation criteria".

### 2. Keyword Search (Fallback)

Text-based search for exact term matches.

**When used:** Semantic search returns no results (embedding quality issue or very specific term).

**Example:** Query "HR-01" retrieves chunks containing exact string "HR-01".

### 3. Hybrid Search

Combine semantic and keyword results, deduplicate, and rank by relevance score.

**Advantage:** Balances semantic understanding with term precision.

## RAG Configuration

Tunable parameters (environment variables):

| Variable | Default | Description |
|----------|---------|-------------|
| `RAG_TOP_K` | 3 | Number of chunks to retrieve per query |
| `RAG_CHUNK_SIZE` | 400 | Target chunk size in tokens |
| `RAG_CHUNK_OVERLAP` | 50 | Token overlap between adjacent chunks |
| `BEDROCK_EMBEDDING_MODEL` | `amazon.titan-embed-text-v2:0` | Embedding model ID |
| `VECTOR_STORE` | `in_memory` | `in_memory` or `pgvector` (pgvector not yet implemented) |

See [Configuration Reference](../reference/configuration.md) for complete list.

## Handling "I Don't Know"

When retrieved context does not contain the answer, the LLM is instructed to decline instead of guessing.

**Example:**

**Query:** "What is the maximum loan tenure for home loans?"

**Retrieved context:** [Chunks about personal loan FOIR limits, no home loan information]

**LLM output:**

> "I don't have information about home loan tenure limits in the available policy documents. The closest topic I found covers personal loan FOIR requirements. Please consult the home loan policy document or contact the credit policy team."

This prevents hallucination where the LLM invents plausible but false answers.

## RAG in the 4-Page Appraisal Report

The professional appraisal report uses RAG extensively:

- **Page 1 (Risk Drivers):** Retrieves policy citations for each identified risk
- **Page 3 (Liability Analysis):** Retrieves FOIR thresholds and debt burden policies
- **Page 4 (Recommendations):** Retrieves eligibility criteria for alternative loan products

Every risk factor and recommendation includes a source citation retrieved via RAG.

## Performance

Typical retrieval latency:

- **Semantic search:** 50-100ms for top-3 from 500 document index (in-memory FAISS)
- **Embedding generation:** 100-200ms per query (AWS Bedrock Titan)
- **Total RAG round-trip:** 150-300ms

**Optimization:**

- Pre-compute embeddings during document ingestion (one-time cost)
- Use in-memory FAISS for sub-100ms search
- Cache frequently retrieved chunks (TODO: not yet implemented)

## Document Chunking Strategy

**Why chunk:** LLMs have context window limits. Chunking allows relevant excerpts to fit in context instead of entire documents.

**Chunk size:** 300-500 tokens balances:

- **Large chunks:** More context per chunk, but fewer chunks fit in LLM window
- **Small chunks:** More chunks retrieved, but each may lack context

**Overlap:** 50-token overlap ensures sentences spanning chunk boundaries are not split.

**Splitting method:** Split by heading or paragraph boundaries, not mid-sentence.

## RAG Tools in AI Agent

The AI agent uses RAG through two tools:

### 1. Policy RAG Tool

**Tool name:** `search_policy_documents`

**Input:** Query string (e.g., "FOIR limit for unsecured loans")

**Output:** Top-k policy chunks with source citations

**Use case:** Retrieve regulatory basis for underwriting rules

### 2. Document RAG Tool

**Tool name:** `search_borrower_documents`

**Input:** Application Reference Number (ARN), query string

**Output:** Top-k chunks from borrower-uploaded documents

**Use case:** Verify income sources, analyze transaction patterns, check employment continuity

## Limitations

RAG has known limitations:

- **Query quality matters:** Vague queries retrieve irrelevant chunks. Specific queries with key terms work best.
- **Chunk boundary issues:** Answers spanning multiple chunks may be incomplete if chunks not retrieved together.
- **Semantic drift:** Embeddings may miss domain-specific jargon or rare terms. Hybrid search mitigates this.
- **No reasoning:** RAG retrieves existing text but cannot infer conclusions not stated in documents.

## Security and Privacy

- **Policy documents:** Public RBI circulars and internal policies only. No customer data.
- **Borrower documents:** Isolated per ARN. Namespace ensures one borrower cannot access another's documents.
- **Embedding privacy:** AWS Bedrock embeddings are not stored by AWS. Vectors stored locally in FAISS.

## Future Enhancements

Planned RAG improvements:

- **Pgvector backend:** Persistent vector storage in PostgreSQL for production scale
- **Multi-level indexing:** Separate indices for different document types (RBI vs internal policy)
- **Reranking:** Second-stage model reranks top-k chunks for precision
- **Semantic caching:** Cache embeddings for frequently asked questions

## Related Topics

- [Underwriting Rules](underwriting-rules.md) — How rules use RAG for regulatory citations
- [Configure AWS Bedrock](../tasks/configure-aws-bedrock.md) — Set up embeddings and LLM
- [Overview](overview.md) — How RAG fits into overall system architecture
