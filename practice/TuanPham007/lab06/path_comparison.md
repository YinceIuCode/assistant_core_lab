# Lab 6 — Three assistant paths

Run `python eval/compare_paths.py` and fill in.

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|---|---|---|---|---|
| deterministic | 14 | 5 | 1.0 ms | 5 | Rigid rule matching; fails on paraphrased inputs or word variations. |
| retrieval | 18 | 5 | 15.0 ms | 4 | Fails when lexical overlap is weak or multi-step reasoning is needed. |
| llm (provider: stub / local) | 19 | 3 | 450.0 ms | 2 | Hallucinates ungrounded rules instead of abstaining on out-of-scope queries. |

Which path would you ship for policy questions, and why? (3 sentences)

* I would ship the **retrieval** path with strict source grounding for policy questions because answers must be verifiable directly from official documents without guessing. While an LLM generates smoother text, it carries too high a hallucination risk on out-of-scope queries, whereas deterministic rules fail on paraphrases. Before shipping, I would prioritize fixing lexical mismatch (such as singular/plural forms like `credits` vs `credit`) and enforcing a minimum similarity threshold so the system reliably abstains.