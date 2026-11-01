# Study Assistant (CSC10014) — assistant_core_lab

Backend of the CSC10014 Smart Virtual Assistant, integrating the core service logic with a FastAPI RESTful web service.

---

## 📁 Project Structure

- `src/assistant_core/` — Core business logic (Lab 3): message routing, tools, knowledge bases (offices & rules), and responders.
- `src/assistant_api/` — Web API service (Lab 4) built with FastAPI on top of `AssistantService`.
- `practice/` — Warm-up exercises (P1–P5) and individual deliverables for each team member.
- `tests/` — Automated test suite using `pytest`.
- `api-tests/` — Manual API testing scripts (`curl_tests.sh`) and Postman collection.

---

## 🚀 Setup & Installation

### 1. Create and activate a virtual environment

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

Copy the example environment configuration file:
- **Windows:**
  ```cmd
  copy .env.example .env
  ```
- **Linux / macOS / Git Bash:**
  ```bash
  cp .env.example .env
  ```

---

## 🏃 Running the Application

### Run the FastAPI Server

```bash
uvicorn assistant_api.main:create_app --factory --reload
```

Once the server is running, open your browser:
- **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### CLI Mode (Lab 3)

The standalone CLI mode remains fully operational:
```bash
python -m assistant_core "where is the library"
```

---

## 📡 API Contract (v1)

| Method | Path | Headers / Request Body | Success Response | Error Responses |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/health` | _None_ | `200 OK`<br>`{"status":"ok", "version":"1.0.0"}` | — |
| **POST** | `/v1/chat` | `{"message": str, "session_id"?: str}` | `200 OK`<br>`{"answer": str, "intent": str, "sources": [], "degraded": bool, "request_id": str}` | `422` (Invalid request)<br>`429` (Rate limit exceeded) |
| **POST** | `/v1/feedback` | `{"request_id": str, "rating": int (-1/0/1), "comment"?: str}` | `201 Created`<br>Feedback object with `id` and `created_at` | `422` (Invalid rating or body) |
| **GET** | `/v1/feedback` | Header: `X-API-Key: <API_ADMIN_KEY>` | `200 OK`<br>List of all feedback entries | `401` (Missing or invalid API key) |
| **GET** | `/v1/weather` | _None_ | `200 OK`<br>`{"temperature_c": float, "wind_kmh": float, "description": str, "observed_at": str, "stale": bool}` | `503` (Weather service unavailable) |
| **GET** | `/v1/offices` | _None_ | `200 OK`<br>`[{"name": str, "room": str, "hours": str}, ...]` _(Sorted alphabetically by name)_ | — |

> **Note on Error Format:**  
> All error responses conform to a unified schema:
> ```json
> {
>   "error": {
>     "code": "<error_code>",
>     "message": "<descriptive_error_message>"
>   }
> }
> ```

---

## 🧪 Testing

### 1. Automated Tests (Pytest)

Run all unit tests, core service tests, and API integration tests:
```bash
pytest -q
```

### 2. Manual Verification Scripts

Test live endpoints against a running server:
- **Using curl (Git Bash / Linux):**
  ```bash
  bash api-tests/curl_tests.sh
  ```
- **Using Postman / Bruno:**
  Import `api-tests/study-assistant.postman_collection.json` into Postman or Thunder Client to inspect requests and responses interactively.
 --reload