# Lab 3 — Before / after maintainability comparison

Fill in for the monolith (before) and your refactored package (after).

| Question | Before | After |
|---|---|---|
| Where would you change the credit rate? How many places? | 1 constant in code | 1 variable in `.env` |
| Can you run the tests without internet or an API key? | no | yes |
| What happens if `handbook.json` is missing? | prints and continues silently | `DataError` at startup |
| Is any secret printed or logged? | yes | no |
| How long does it take a new teammate to find the fee logic? | Long time (mixed in 160 lines of code) | Very fast (isolated in `tools.py`) |
| Number of global variables | 9 (3 mutable) | 0 |
| Number of bare `except:` blocks | 3 | 0 |
| Lines in the longest function | ~65 (`handle`) | ~15 |
| `ruff check` issues | Many issues | 0 (All checks passed!) |
| Can you swap the LLM without touching the service? | no | yes |

**Three sentences:** 
1. **What improved most:** Breaking the monolith into cohesive modules with strict dependency injection makes the codebase highly testable, secure, and deterministic.
2. **What got more complex:** The overall architecture introduced more files and advanced structural concepts (like Protocols and Pydantic models), which takes a bit more time to navigate initially.
3. **What you would still change:** I would like to replace the static CSV/JSON files with a real database integration and implement actual LLM calls for the responder logic.