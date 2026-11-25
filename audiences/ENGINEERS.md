# Engineer route: make a fine-tuning decision you can defend

Use the same **Concepts → Methods → Problems → Projects** sequence, but move quickly through familiar terminology. Apply every stage to a real, bounded task with authorized data.

Use the [worked Methods](../mastery/02_methods_worked.md), [worked Problems](../mastery/03_problems_worked.md) and [worked Projects](../mastery/04_projects_worked.md) as review exercises. The [mastery pathway](../mastery/06_mastery_pathway.md) includes optional extensions after the core.

## Fast route with decision gates

| Gate | Artifact | Pass condition |
| --- | --- | --- |
| Task definition | Input/output contract, failure costs, latency and update rate | A reviewer can tell what should be escalated |
| Data readiness | [Dataset card](../templates/DATASET_CARD.md), annotation policy, privacy/access plan | Train/test group and time leakage examined; rights documented |
| Baseline | Rule or prompt, plus retrieval if facts change | Frozen test protocol and raw predictions retained |
| Adaptation | Small classifier, SFT or adapter matched to task | Method chosen for measured gap, not fashion |
| Verification | Same held-out IDs, per-slice errors, format and groundedness checks | Quality and important regressions visible with denominators |
| Delivery | [Model card](../templates/MODEL_CARD.md), load test, cost and rollback | Another engineer can reproduce and restore a known version |

Read [Methods](../en/02_methods.md) for the techniques, [Problems](../en/03_problems.md) for diagnostics, and [Project 3](../en/04_projects.md) for the capstone specification. The fictional lab is a mechanics check; replace it with a legally usable, task-matched dataset before making business claims.

## Engineering extensions beyond the toy labs

1. **Define a serving contract:** exact JSON schema or classification labels, invalid-output behavior, timeout, privacy rules and human escalation.
2. **Compare costs:** baseline versus adapted model on relevant quality, throughput, latency, memory, training effort and maintenance. Record actual hardware and environment.
3. **Test distribution shift:** new users, long/short requests, missing context, code switching, policy changes and rare or costly error types. Keep the selection set separate from the final test.
4. **Reproduce a release:** pin dataset snapshot, model and tokenizer revision, adapter revision, package versions, seed, prompts, generation settings and evaluation script. Load the saved artifact in a new process.
5. **Plan operations:** monitor schema failures, per-class drift and escalations; decide who reviews incidents, how to roll back, and when new data warrants retraining.

## Review questions before deployment

- Does a prompt, rule or retrieval solution already meet the acceptance criteria?
- What fresh labels or documents will arrive after training, and who updates them?
- Which bad predictions harm people or business processes, and what is the human fallback?
- Is there enough representative test data to support the claimed scope and languages?
- Will the license, data rights and privacy terms still be valid in the intended environment?

For English, Hindi and Tamil deployment, build reviewed test slices for each language and for code switching. Model support for those languages is a model-selection and evaluation question; translating an English score is not evidence.
