# Study Assistant (CSC10014) — assistant_core_lab

Backend service for the CSC10014 Smart Virtual Assistant, combining core business logic, a RESTful FastAPI web service, and persistent SQLite storage with SQLModel.

---

## 📁 Project Structure

- `src/assistant_core/` — Core service logic (Lab 3): message routing, knowledge base (offices & rules), and responders.
- `src/assistant_api/` — Web API service (Lab 4 & 5) built with FastAPI and SQLite persistence (`db.py`).
- `practice/` — Individual student practice workspaces (`practice/<github-username>/lab04/` and `lab05/`).
- `scripts/` — Database migrations runner (`migrate.py`), synthetic seed data generator (`seed.py`), and issue automation (`create_issues.py`).
- `sql/` — DDL migrations (`001_init.sql`, `002_add_faq.sql`), schema critique (`bad_schema.sql`), and analytical queries (`my_queries.sql`).
- `docs/` — Architecture documentation, design worksheets (`docs/lab5/data_model.md`), and verification screenshots.
- `tests/` — Automated test suites using `pytest` (core, API, and database repository tests).
- `api-tests/` — Manual verification scripts (`curl_tests.sh`) and Postman collection.

---

## 🚀 Setup & Installation

### 1. Create and activate virtual environment

- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (Git Bash) / macOS / Linux:**
  ```bash
  python -m venv .venv
  source .venv/Scripts/activate      # On Linux/macOS: source .venv/bin/activate
  ```

### 2. Install dependencies & link local package

```bash
pip install -r requirements.txt
pip install -e .
```

### 3. Environment configuration

Copy the sample environment file:
- **Windows:**
  ```cmd
  copy .env.example .env
  ```
- **Linux / macOS / Git Bash:**
  ```bash
  cp .env.example .env
  ```

Ensure `.env` contains:
```env
DATABASE_URL=sqlite:///assistant.db
SESSION_SALT=dev-salt
API_ADMIN_KEY=change-me
RATE_LIMIT_PER_MIN=30
```

---

## 🗄️ Database Management (Lab 5)

### Apply Schema Migrations
Apply versioned migrations sequentially (`001_init.sql`, `002_add_faq.sql`):
```bash
python scripts/migrate.py assistant.db
```

### Seed Synthetic Data
Generate 300 realistic interactions and feedback entries for local testing and analytics:
```bash
python scripts/seed.py assistant.db 300
```

---

## 🏃 Running the Application

### Start the FastAPI Server

```bash
uvicorn assistant_api.main:create_app --factory --reload
```

Once running, access the interactive API docs:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### CLI Mode (Lab 3)

The standalone command-line interface remains operational:
```bash
python -m assistant_core "where is the library"
```

---

## 📡 API Contract (v1)

| Method | Path | Headers / Parameters | Success Response | Error Responses |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/health` | _None_ | `200 OK`<br>`{"status":"ok", "version":"1.0.0"}` | — |
| **POST** | `/v1/chat` | `{"message": str, "session_id"?: str}` | `200 OK`<br>`{"answer": str, "intent": str, "sources": [], "degraded": bool, "request_id": str}` | `422` (Invalid request)<br>`429` (Rate limit exceeded) |
| **POST** | `/v1/feedback` | `{"request_id": str, "rating": int (-1/0/1), "comment"?: str}` | `201 Created`<br>Feedback object with `id` and `created_at` | `404` (Unknown request id)<br>`422` (Invalid rating or body) |
| **GET** | `/v1/feedback` | Query: `limit=100`<br>Header: `X-API-Key: <API_ADMIN_KEY>` | `200 OK`<br>List of persisted feedback records (newest first) | `401` (Missing or invalid API key) |
| **GET** | `/v1/stats/intents` | Header: `X-API-Key: <API_ADMIN_KEY>` | `200 OK`<br>`[{"intent": str, "requests": int, "avg_latency_ms": float, "unresolved": int}, ...]` | `401` (Missing or invalid API key) |
| **GET** | `/v1/weather` | _None_ | `200 OK`<br>`{"temperature_c": float, "wind_kmh": float, "description": str, "observed_at": str, "stale": bool}` | `503` (Weather service unavailable) |
| **GET** | `/v1/offices` | _None_ | `200 OK`<br>`[{"name": str, "room": str, "hours": str}, ...]` _(Sorted alphabetically by name)_ | — |

> **Unified Error Format:**  
> ```json
> {
>   "error": {
>     "code": "<error_code>",
>     "message": "<descriptive_error_message>"
>   }
> }
> ```

---

## 🔒 Privacy by Design

- **No Raw User Prompts:** Chat message content and answers are never stored in the database.
- **Salted Session Hashing:** Session IDs are anonymized using SHA-256 combined with a secret `SESSION_SALT` from `.env`.
- **Minimal Metadata:** Only non-identifiable operational metadata (`intent`, `topic`, `latency_ms`, `resolved`, `degraded`) is persisted to optimize assistant accuracy while safeguarding student privacy.

---

## 🧪 Testing

### 1. Automated Test Suite (Pytest)

Run all unit tests across core, API, and database modules:
```bash
pytest -q
```

Or run targeted modules:
```bash
pytest -q tests/test_db.py     # Database repository tests
pytest -q tests/test_api.py    # REST API endpoint tests
```

### 2. Manual Verification Scripts

- **Using curl (Git Bash / Linux):**
  ```bash
  bash api-tests/curl_tests.sh
  ```
- **Using Postman / Bruno:**
  Import `api-tests/study-assistant.postman_collection.json` into Postman to inspect endpoints interactively.

### 3. Individual Practice Verification
- **SQL Practice (Q1–Q15):**
  ```bash
  python practice/<github-username>/lab05/check.py
  ```
- **Python Repository Practice (D1–D3):**
  ```bash
  pytest -q practice/<github-username>/lab05/test_school_repo.py
  ```
