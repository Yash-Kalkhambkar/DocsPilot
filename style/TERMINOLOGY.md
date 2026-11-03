# CreditShield Terminology

This file defines preferred terms for CreditShield documentation. Vale enforces these terms automatically.

## Format

**Preferred term** | **Rejected variants** | **Definition**

## Product and System Terms

**CreditShield** | creditshield, Credit Shield, credit-shield | Full-stack digital lending platform for loan origination and risk decision support

**loan origination** | loan processing, lending process | The complete lifecycle from loan application to approval or rejection

**Loan Origination System** | loan processing system, LOS system | Software platform managing the loan origination lifecycle (LOS is acceptable after first use)

**appraisal report** | credit memo, assessment report, evaluation report | Bank-grade 4-page professional loan assessment document generated for loan officers

**underwriting rule** | policy check, credit rule, risk rule | Configurable decision criterion applied during credit evaluation (one of 50+ rules)

**loan officer** | bank employee, loan processor, loan agent | Front-line staff member responsible for application intake and document completeness

**credit analyst** | risk analyst, credit officer, analyst | Specialist who performs financial and risk assessment and validates AI outputs

**field officer** | field agent, verification agent, field executive | Staff member who conducts on-ground verification of residence, business, or employment

**underwriter** | credit approver, sanctioning authority, decisioner | Final decision-maker with credit authority (often Branch Manager)

**branch manager** | BM, manager, branch head | Senior role holding underwriting authority for the branch

**borrower** | customer, applicant, client, user, loan applicant | Individual applying for a loan

**system admin** | administrator, admin, sysadmin | Role managing users, access control, and system configuration

## Technical Terms

**AWS Bedrock** | Bedrock, Amazon Bedrock, AWS bedrock | Amazon Web Services' managed service for foundation models

**Llama 3 70B** | Llama3, LLama, llama | Meta's large language model with 70 billion parameters used for explainable credit decisions

**PostgreSQL** | Postgres, postgres, postgresql, PostGres | Open-source relational database system

**FastAPI** | Fast API, fast-api, fastapi | Python web framework for building APIs

**RAG** | retrieval augmented generation, rag | Retrieval-Augmented Generation: AI technique combining search with text generation (define on first use)

**FAISS** | Faiss, faiss | Facebook AI Similarity Search: library for efficient vector similarity search

**embeddings** | embedding vectors, vectors, vector embeddings | Numerical representations of text used for semantic search

**vector store** | vector database, vector index, embedding store | Database system storing and retrieving embeddings

**LLM** | llm, large language model | Large Language Model: AI system trained on text (define on first use)

**ReAct** | react, React (when referring to agent pattern) | Reasoning and Acting: AI agent pattern combining reasoning with tool use

**mock mode** | test mode, stub mode, mock-mode | Development mode that simulates AWS Bedrock without requiring credentials

## Financial and Regulatory Terms

**Application Reference Number** | ARN, application ID, app ID, reference number | Unique identifier for loan applications (ARN is acceptable after first use)

**Fixed Obligations to Income Ratio** | FOIR, debt-to-income, DTI, obligation ratio | Monthly debt payments divided by monthly income (FOIR is acceptable after first use)

**Non-Performing Asset** | NPA, bad loan, defaulted loan | Loan in default or overdue beyond specified period (NPA is acceptable after first use)

**Reserve Bank of India** | RBI, Reserve bank | India's central banking institution (RBI is acceptable after first use)

**CIBIL score** | credit score, CIBIL, bureau score | Credit score provided by Credit Information Bureau (India) Limited

**Know Your Customer** | KYC, identity verification, customer verification | Identity verification process required by financial regulations (KYC is acceptable after first use)

**Equated Monthly Installment** | EMI, monthly payment, installment | Fixed monthly loan repayment amount (EMI is acceptable after first use)

**Buy Now Pay Later** | BNPL, buy-now-pay-later | Short-term consumer financing option (BNPL is acceptable after first use)

**hard rule** | hard-stop rule, fatal rule, rejection rule | Underwriting rule that causes automatic rejection when violated

**soft rule** | soft-stop rule, warning rule, review rule | Underwriting rule that triggers manual review when violated (does not auto-reject)

**RBI circular** | RBI guideline, Reserve Bank circular, regulatory circular | Official policy document issued by Reserve Bank of India

**digital lending** | online lending, e-lending, digital loans | Lending operations conducted through digital channels

**sanction** | approval, loan approval, credit approval | Official approval to disburse a loan

**disbursal** | disbursement, payout, loan payout | Transfer of approved loan amount to borrower

## Risk and Decision Terms

**risk driver** | risk factor, risk indicator, risk signal | Factor contributing to credit risk assessment

**counterfactual** | what-if scenario, alternative scenario | Suggestion showing how borrower could qualify by changing specific factors

**fraud signal** | fraud indicator, fraud flag, suspicious activity | Pattern or behavior indicating possible fraud

**document tampering** | document fraud, fake document, forged document | Unauthorized modification of financial documents

**income stability** | income consistency, income reliability | Measure of how regular and predictable income sources are

**credit behaviour** | credit behavior, repayment behavior, credit history | Past pattern of credit usage and repayment

**financial discipline** | financial behavior, spending discipline, money management | Quality of expense management and savings habits

**loan burden** | debt burden, obligation load, debt load | Total existing debt relative to income

**lifestyle risk** | discretionary spending risk, lifestyle inflation | Risk from unsustainable spending patterns

**liquidity stress** | cash flow stress, low-balance days | Periods of insufficient cash balance

**loan stacking** | multi-loan pattern, rapid loan accumulation | Taking multiple loans in short time period

## Documentation and Process Terms

**concept topic** | conceptual topic, concept doc, overview topic | Documentation page explaining "what" and "why"

**task topic** | how-to guide, procedural topic, tutorial | Documentation page with step-by-step instructions

**reference topic** | reference doc, API reference, technical reference | Documentation page with detailed technical specifications

**release notes** | change log, changelog, version notes | Document describing changes in a product version

**front matter** | metadata, YAML header, page metadata | YAML block at start of Markdown file containing topic metadata

**style guide** | writing guide, documentation standards, style manual | Document defining writing standards and conventions

**terminology list** | glossary, term list, preferred terms | List of approved terms for consistent usage

**content gap** | documentation gap, missing content, coverage gap | Topic or information missing from documentation

## API and Configuration Terms

**endpoint** | API endpoint, route, API route | URL path for accessing an API operation

**environment variable** | env var, config variable, environment setting | Configuration value set outside the application code

**JWT token** | JSON Web Token, JWT, auth token, bearer token | Authentication token in JSON Web Token format (JWT is acceptable after first use)

**request body** | request payload, POST body, JSON body | Data sent in HTTP request

**response body** | response payload, API response, JSON response | Data returned in HTTP response

**status code** | HTTP status, response code, HTTP code | Numeric code indicating HTTP request outcome

## Workflow and Lifecycle Terms

**stage** | phase, step (when referring to lifecycle) | Major division of loan origination lifecycle (7 stages total)

**workflow** | process flow, application flow, business process | Sequence of operations and decisions in loan processing

**application status** | loan status, case status, workflow status | Current state of loan application in the lifecycle

**pending review** | under review, review pending, awaiting review | Status indicating manual review required

**auto-reject** | automatic rejection, system reject, rule-based reject | Rejection triggered automatically by hard rule violation

**conditional approval** | conditional sanction, approval with conditions | Approval requiring additional conditions to be met

## Usage Notes

- Use lowercase for generic references: "review the appraisal report"
- Use proper case only when part of a title or heading: "Appraisal Report Generation"
- Spell out acronyms on first use, then use the acronym: "Reserve Bank of India (RBI)" → "RBI"
- Prefer active voice: "Configure AWS Bedrock" not "AWS Bedrock should be configured"
- Avoid possessives with product names: "CreditShield features" not "CreditShield's features"
