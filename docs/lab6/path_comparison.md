# Lab 6 — Three assistant paths

Run `python eval/compare_paths.py` and fill in.

| Path | Correct /25 | Abstain correct /10 | p50 latency | Controllability (1–5) | Main failure mode |
|---|---|---|---|---|---|
| deterministic | 11 | 9 | 0.0 | 4 | Can only answer hardcoded rules, or usually defaults to abstaining |
| retrieval | 18 | 6 | 0.0 | 3 | Unable to answer paraphrased questions and/or abstain ambiguous questions |
| llm (provider: stub) | 18 | 6 | 0.0 | 2 | (Same with retrieval path) |
