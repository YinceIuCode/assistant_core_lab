# Lab 6 — Three assistant paths

Run `python eval/compare_paths.py` and fill in.

| Path | Correct /25 | Abstain correct /10 | p50 latency | Controllability (1–5) | Main failure mode |
|---|---|---|---|---|---|
| deterministic | 11 | 9 | 0.0 | 4 | Can only answer hardcoded rules, or usually defaults to abstaining |
| retrieval | 18 | 6 | 0.0 | 3 | Unable to answer paraphrased questions and/or abstain ambiguous questions |
| llm (provider: stub) | 18 | 6 | 0.0 | 2 | (Same with retrieval path) |

### Which path would you ship for policy questions, and why? (3 sentences)
For university policy questions, we recommend shipping the retrieval-augmented LLM path with strict grounding validation and retrieval fallback. The LLM provides concise, natural synthesized answers tailored to the student's query rather than dumping raw markdown chunks. When LLM confidence drops below threshold or provider errors occur, the system safely falls back to quoting verified retrieval chunks, preventing any risk of student misguidance.
