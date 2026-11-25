# Model card and experiment report template

- Model name and version:
- Owner and review date:
- Intended use; unsupported use; user population:
- Baseline and why fine-tuning was considered:
- Base model ID, exact revision and license:
- Tokenizer/chat-template revision:
- Dataset card and split/frozen-test IDs:
- Training method (full, LoRA, QLoRA, SFT), seed, settings and package versions:
- Hardware, peak memory, training duration and inference latency:
- Metrics on validation and held-out test, with denominators:
- Per-class/per-language/per-slice results and uncertainty:
- Baseline and tuned predictions on the exact same test IDs:
- At least three representative failures or all failures if fewer:
- Safety, privacy, fairness, policy freshness and human escalation:
- How to load from a fresh process, including adapter/base pairing:
- Monitoring signals, rollback artifact and update triggers:
- Limitations, unanswered questions and decision to ship or hold:

**Rule:** Never fill a metric with a tutorial example number. If you cannot measure a field, write `not measured` and why.
