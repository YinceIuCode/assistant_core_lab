# Module Responsibilities

| Module | Responsibility |
|---|---|
| `config.py` | Read settings from the environment; validate. |
| `errors.py` | Named exceptions. |
| `models.py` | Public contract: `Message`, `Response`, `Intent`, `Source`. |
| **`router.py`** | **Choose an `Intent` with simple rules.** |
| `knowledge.py` | Office directory (CSV) and handbook (JSON) with search. |
| `tools.py` | Deterministic tuition calculation. |
| **`responder.py`** | **Response generation behind one interface (stub LLM, template).** |
| `service.py` | `AssistantService.handle(Message) -> Response` (the only entry point). |
