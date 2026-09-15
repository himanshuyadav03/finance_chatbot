# Finance AI Chatbot

An AI-powered finance chatbot that lets finance users query financial
data using natural language. The system converts questions into safe
SQL, executes them against PostgreSQL, and returns text, table, or
chart-ready responses.

It also supports metadata-based RAG, conversation memory,
fiscal-calendar-aware queries, SQL validation, and automated NL-to-SQL
evaluation.

## Features

-   Natural-language to SQL using the OpenAI API
-   Finance-aware queries for booking, invoice, collection, and
    linearity
-   4-4-5 fiscal calendar support
-   Metadata/business-rule RAG using OpenAI embeddings and FAISS
-   Session-based conversation memory for follow-up questions
-   SQL safety using SQLGlot and allowed table/column checks
-   PostgreSQL as the current development database
-   Text, table, and chart-ready API responses
-   Automated single-question and conversation evaluation

## Architecture

``` text
Finance User
     |
     v
FastAPI /ask
     |
     v
Question Validation
     |
     v
Conversation Memory
     |
     v
Metadata RAG Retrieval
     |
     v
OpenAI LLM
     |
     v
NL-to-SQL Generation
     |
     v
Capability Check
     |
     v
SQLGlot Validation
     |
     v
PostgreSQL
     |
     v
Query Result
     |
     v
Answer Generation
     |
     v
Text / Table / Chart Response
```

## Technology Stack

  Component         Technology
  ----------------- -------------------
  Language          Python
  API               FastAPI
  LLM               OpenAI API
  Database          PostgreSQL
  Database Access   SQLAlchemy
  SQL Validation    SQLGlot
  Embeddings        OpenAI Embeddings
  Vector Search     FAISS
  Validation        Pydantic
  Configuration     python-dotenv

## Supported Finance Data

### Actual Booking, Invoice and Collection

Table:

``` text
actual_booking_invoices_collection
```

Important fields include:

-   `booking_week`
-   `booking_amount`
-   `invoice_week`
-   `invoice_amount`
-   `collection_week`
-   `collection_amount`

### Booking-to-Invoice Linearity

Table:

``` text
booking_to_invoice_forecasting
```

Contains `booking_week`, `booking_amount`, and `lag_0` through `lag_10`.

The lag columns represent how bookings convert into invoices over
subsequent weeks.

### Invoice-to-Cash Linearity

Table:

``` text
invoice_to_cash_forecasting
```

Contains `invoice_week`, `invoice_amount`, and `lag_0` through `lag_10`.

The lag columns represent how invoices convert into cash collections
over subsequent weeks.

## Fiscal Calendar

The chatbot uses a 4-4-5 fiscal calendar with 52 weeks:

  Quarter   Fiscal Weeks
  --------- --------------
  Q1        Wk01-Wk13
  Q2        Wk14-Wk26
  Q3        Wk27-Wk39
  Q4        Wk40-Wk52

For example, `2025Q2` maps to `2025Wk14` through `2025Wk26`.

## RAG Workflow

RAG is used to retrieve relevant database metadata and business rules,
not financial values.

``` text
Metadata JSON
     |
     v
Document Builder
     |
     v
OpenAI Embeddings
     |
     v
FAISS Index

User Question
     |
     v
Question Embedding
     |
     v
Similarity Search
     |
     v
Top-K Metadata
     |
     v
NL-to-SQL Prompt
```

The database remains the source of truth for financial values.

## Conversation Memory

The API accepts a `session_id` and uses recent conversation history to
resolve follow-up questions.

Example:

``` text
User: What was total booking in 2025Q1?
User: What about Q2?
```

The second question is interpreted in the context of total booking for
2025Q2.

Conversation memory is currently in-memory and intended for
local/prototype use.

## SQL Safety

Generated SQL is validated before execution.

Safeguards include:

-   SELECT-only queries
-   Allowed tables
-   Allowed columns
-   Destructive operation blocking
-   SQL parsing/validation using SQLGlot
-   Read-only database access principles
-   Database statement timeout

LLM-generated SQL is never intentionally sent directly to the database
without the validation layer.

## Response Types

The system supports three response types:

### Text

For totals, percentages, and simple factual answers.

Example:

``` text
What was total booking in 2025Q1?
```

### Table

For multi-row results and breakdowns.

Example:

``` text
Show weekly booking for 2025Q1.
```

### Chart

When the user explicitly asks for a plot/chart/graph.

Example:

``` text
Plot weekly booking for 2025Q1.
```

The backend returns chart-ready data and chart configuration. Frontend
rendering is not currently implemented.

## Example Questions

``` text
What was total booking in 2025Q1?
What was total invoice in 2025Q2?
What was total collection in 2026Q3?
Show weekly booking for 2025Q1.
Plot weekly invoice for 2026Q2.
What percentage of booking is invoiced within 3 weeks?
```


## Project Structure

``` text
finance_chatbot/
├── app/
│   ├── api/
│   ├── database/
│   ├── llm/
│   ├── metadata/
│   ├── rag/
│   ├── schemas/
│   ├── security/
│   ├── services/
│   └── main.py
├── evaluation/
│   ├── test_cases.json
│   ├── conversation_test_cases.json
│   ├── run_evaluation.py
│   ├── run_conversation_evaluation.py
│   └── results/
├── metadata/
│   ├── tables.json
│   ├── columns.json
│   ├── business_rules.json
│   ├── relationships.json
│   ├── fiscal_calendar.json
│   └── sql_examples.json
├── rag_store/
├── scripts/
│   ├── load_csv_to_postgres.py
│   └── build_rag_index.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## API

### Ask a Finance Question

`POST /ask`

Example request:

``` json
{
  "question": "What was total booking in 2025Q1?",
  "session_id": "demo-session-001"
}
```

Response structure:

``` json
{
  "question": "What was total booking in 2025Q1?",
  "answer": "Total booking in 2025Q1 was ...",
  "query_type": "actual_booking",
  "response_type": "text",
  "data": [
    {
      "total_booking": 0
    }
  ],
  "chart": null
}
```

The numeric value above is illustrative. Actual values come from the
connected database.

## Local Setup

### 1. Clone the repository

``` bash
git clone <repository-url>
cd finance_chatbot
```

### 2. Create and activate a virtual environment

``` powershell
python -m venv myenv
myenv\Scripts\activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` from `.env.example` and provide the OpenAI and PostgreSQL
configuration expected by the application.

Do not commit `.env` or real credentials.

### 5. Load development data

``` powershell
$env:PYTHONPATH="."
python scripts/load_csv_to_postgres.py
```

### 6. Build the RAG index

``` powershell
$env:PYTHONPATH="."
python scripts/build_rag_index.py
```

### 7. Start the API

``` powershell
$env:PYTHONPATH="."
uvicorn app.main:app --reload
```

Use FastAPI Swagger to test `POST /ask`.

## Evaluation

The project includes an automated evaluation framework. It compares
generated-query database results with expected-query database results
rather than requiring exact SQL-string equality.

Measured areas include:

-   Query type accuracy
-   Response type accuracy
-   Database result accuracy
-   Overall accuracy
-   Follow-up/conversation behavior

Run single-question evaluation:

``` powershell
$env:PYTHONPATH="."
python evaluation/run_evaluation.py
```

Run conversation evaluation:

``` powershell
$env:PYTHONPATH="."
python evaluation/run_conversation_evaluation.py
```

Reports are saved under `evaluation/results/`.

## Current Limitations

-   PostgreSQL is currently used instead of the planned Snowflake
    integration.
-   Conversation memory is process-local/in-memory.
-   Production logging and monitoring are deferred.
-   Chart rendering requires a frontend; the API currently returns chart
    configuration/data.
-   Cloud deployment is not yet implemented.
-   The evaluation dataset should be expanded as more query patterns are
    supported.

## Future Improvements

-   Snowflake integration
-   Persistent conversation storage
-   Production logging and monitoring
-   Larger NL-to-SQL evaluation dataset
-   Improved retrieval for ambiguous follow-ups
-   Frontend chart rendering
-   Authentication and authorization
-   Containerization and cloud deployment

## Project Status

### Implemented

-   Natural-language finance queries
-   OpenAI-based NL-to-SQL
-   PostgreSQL integration
-   SQLGlot SQL validation
-   Metadata/business-rule RAG
-   FAISS vector retrieval
-   Fiscal-calendar-aware queries
-   Conversation memory
-   Text/table/chart-ready responses
-   No-data handling
-   Capability validation
-   NL-to-SQL evaluation
-   Conversation follow-up evaluation

### Deferred / Planned

-   Snowflake integration
-   Production logging and monitoring
-   Deployment

## Author

**Himanshu Yadav**

Data Scientist \| Machine Learning \| Generative AI
