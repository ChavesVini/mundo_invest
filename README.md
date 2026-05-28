# Mundo Invest - Pipefy Integration & Client Backend

This project features a high-performance API developed with **FastAPI** designed to manage client requests and provide seamless integration with the Pipefy platform using **GraphQL**. The architecture enforces strict data contract validation via Pydantic, relational persistence using SQLAlchemy, and an explicit idempotency lock mechanism to guarantee secure Webhook processing.

---

## Tech Stack

* **Python 3.12**
* **FastAPI** (High-performance asynchronous web framework)
* **Pydantic V2** (Data validation and settings management via schemas)
* **SQLAlchemy** (Object-Relational Mapping / ORM)
* **SQLite** (Local relational database)
* **Pytest** (Automated testing framework)

---

## Local Setup & Execution

### 1. Clone the Repository and Install Dependencies
Ensure you have Python 3.12+ installed on your machine. In your terminal, run:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows PowerShell):
.\venv\Scripts\Activate.ps1

# On Linux/Mac: 
source venv/bin/activate

# Install project requirements
pip install -r requirements.txt
```

### 2. Start the API Server
The main.py script acts as the application bootstrap, automatically orchestrating table creation within the local SQLite database (mundo_invest.db) upon startup.

```bash
uvicorn mundo_invest.main:app --reload
```

The API will be up and running at: http://localhost:8000

Interactive API documentation (Swagger UI) will be accessible at: http://localhost:8000/docs

## Running Automated Tests
The test suite thoroughly validates the three core workflows of the application in isolation: client creation, webhook priority evaluation, and the idempotency layer.

To trigger the tests, run the following command from the project root:

```bash
pytest tests/
```

## API Endpoints & Request Examples

### 1. Create New Client (POST /mundo_invest/clients)
Persists client records into the local database and triggers a simulated GraphQL CreateNewCard mutation to Pipefy.

Request Body Example (JSON):

```JSON
{
  "name": "Claudio Rico",
  "email": "claudio.rico@example.com",
  "request_type": "Abertura de Conta",
  "asset_value": 250000.0
}
```

### 2. Process Pipefy Webhook (POST /mundo_invest/webhooks/pipefy/card-updated)
Handles card updates sent by external automated actions, cross-checks the unique event_id to block duplicate inputs, and updates fields in Pipefy using a single GraphQL request optimized with Aliases.

Request Body Example (JSON):

```JSON
{
  "event_id": "evt_teste_readme_123",
  "card_id": "card_gerado_999",
  "email": "claudio.rico@example.com",
  "timestamp": "2026-05-27T23:00:00Z"
}
```

## Production Vision (Scalable AWS Cloud Architecture)
To migrate this architecture into an enterprise production environment capable of scaling to millions of transactions while mitigating system degradation, the infrastructure can be mapped directly to AWS managed services:

### Entry Point (AWS API Gateway): 
Acts as the highly available front door replacing the local Uvicorn instance. It handles secure routing for client inputs and ingestion for incoming Pipefy Webhooks, supplying native throttling mechanisms to protect downstream components from payload spikes.

### Serverless Compute Layer (AWS Lambda): 
The core business workflows managed by our application Services are deployed into AWS Lambda functions. This fully serverless compute stack automatically scales horizontally per request, offering zero idle-state costs and ensuring seamless concurrency control.

### Asynchronous Messaging & Resilience (Amazon SQS):
Webhook volume spikes from external workflow engines can trigger database bottlenecks. By decoupling the API Gateway ingestion point from the computation layer using Amazon SQS queues, payloads are safely buffered and consumed asynchronously by worker Lambda functions without dropping data.

### Persistence & Idempotency Locking (Amazon RDS / DynamoDB):
Client Ledger (Relational Domain): Handled by an Amazon RDS (PostgreSQL) multi-AZ configuration to enforce relational integrity constraints, advanced index processing, and highly available transactional storage.

### Idempotency Register (Key-Value Engine): 
The WebhookEvent checking layer maps perfectly to Amazon DynamoDB. Its single-digit millisecond NoSQL lookup speeds let the application assess whether an event_id has been processed instantly. Furthermore, enabling DynamoDB’s TTL (Time to Live) feature ensures automatic cleanup of historical event keys after a specific window, maintaining a lean, cost-efficient storage foot-print.