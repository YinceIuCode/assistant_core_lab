# Architecture Note for assistant_core

## 1. Module Responsibilities
| Module | Responsibility |
|---|---|
| `config.py` | Read settings from the environment; validate. |
| `errors.py` | Named exceptions. |
| `models.py` | Public contract: `Message`, `Response`, `Intent`, `Source`. |
| `router.py` | Choose an `Intent` with simple rules. |
| `knowledge.py` | Office directory (CSV) and handbook (JSON) with search. |
| `tools.py` | Deterministic tuition calculation. |
| `responder.py` | Response generation behind one interface (stub LLM, template). |
| `service.py` | `AssistantService.handle(Message) -> Response` (the only entry point). |
| `logging_setup.py`| Structured JSON logs. |
| `__main__.py` | Command-line interface. |

## 2. The Service Interface
The service is the only module the CLI (and later the API and UI) talks to.

```python
AssistantService.handle(msg: Message) -> Response
```
* **Message**: `text` (1-2000 chars), `session_id`
* **Response**: `answer`, `intent`, `sources[]`, `degraded` (True if a fallback was used)
* **Errors**:
  * invalid input -> `ValidationError` (handled by Pydantic)
  * startup -> `ConfigError` / `DataError`
  * provider failures never reach the caller (service uses a fallback instead)

## 3. Key Design Decisions
1. **Fees are computed in `tools.py`, never by an LLM:** This ensures exact, testable, and deterministic output.
2. **The LLM sits behind the `Responder` interface:** The stub requires no API key, meaning tests and CI can run completely offline without cost or latency.
3. **Configuration comes from the environment:** Settings are strictly loaded via `.env` (documented in `.env.example`), eliminating hard-coded secrets from the codebase.