# Lab 6 — Three assistant paths

Run `python eval/compare_paths.py` and fill in.

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|---|---|---|---|---|
| deterministic | 7/20| 5/5| 0.0| 0.6| Cannot answer correctly outside of hardcoded rules|
| retrieval | 16/20| 4/5| 0.0| 0.1| Exact word matching fails on plurals/synonyms (e.g., "credits" vs "credit").|
| llm (provider: stub) | 16/20| 4/5| 0.1| 0.3| Inherits retrieval errors (if the wrong chunk is found, the LLM fails).|

Which path would you ship for policy questions, and why? (3 sentences)

- I would ship the **LLM** path (RAG) for **handbook** and **policy** questions. Because training policies are text-heavy and complex, an LLM can effectively summarize and rephrase the rules into a friendly, natural answer rather than just dumping a raw paragraph to the user. However, before shipping, I would prioritize fixing the retrieval word-matching failures (like case E14) to ensure the LLM always receives the correct context.