# Part 4 — Projects: build something another person can judge

Every project uses the same sequence: **problem → dataset → split → baseline → adaptation → held-out evaluation → error analysis → reproducible delivery**. Put all metric values from an actual run in your report. Do not copy example numbers from the lessons.

## Project 1. Support-ticket router (guided, beginner)

**User story:** A support team needs to route a short request to `billing`, `technical`, or `account`. A human remains responsible for ambiguous or high-impact cases.

**Input/output:** plain text request → one of three labels. Start with fictional examples in [toy_tickets.jsonl](../labs/data/toy_tickets.jsonl). They are deliberately small and easy, suitable only for a pipeline demonstration. For a serious project, collect a larger licensed dataset with varied language and label rules.

**Build plan:**

1. Write label policy: `billing` for charges/invoices, `technical` for app/device failure, `account` for login/profile/access. Define how to handle mixed requests; create a human-review category if needed.
2. Inspect counts, duplicates, group overlap, and example lengths with [audit_and_baseline.py](../labs/audit_and_baseline.py). Freeze test groups.
3. Run keyword baseline and record accuracy, per-class recall, macro F1, and mistakes.
4. Run [train_classifier.py](../labs/train_classifier.py) with a small pretrained encoder. Save model and tokenizer to a local output directory. Use validation for choices and test once at the end.
5. Compare on identical test IDs. Manually inspect at least one false positive and one false negative per class if available; do not invent missing failures.
6. Write a one-page model card: data rights, split rule, known limitations, device/versions, model revision, results, and escalation path.

**Acceptance:** A teammate can reproduce the baseline, load your saved model, evaluate the same test IDs, and explain any claim of improvement. If the tuned model does not beat the baseline, explain why and keep the simpler solution.

**Stretch:** Replace toy data with consented multilingual support requests. Establish separate English, Hindi, Tamil, and code-switched test slices. Do not claim cross-language accuracy without those measured slices.

## Project 2. Structured-response assistant (guided, intermediate)

**User story:** Given a support ticket, produce compact JSON with `category` and `reason`. The output must be valid JSON, use an allowed category, and give a reason supported by the ticket.

**Input/output example:** input `"My card was charged twice"`; expected shape `{"category":"billing","reason":"Duplicate charge"}`. The exact wording of the reason need not match if the rubric judges it supported.

**Build plan:**

1. Make an untrained prompt/template baseline with the same held-out prompts and deterministic generation settings. Parse every response as JSON; count schema validity and category correctness separately.
2. Build a prompt–completion training set. Ensure no response appears as a test paraphrase. Inspect the rendered chat template and target-token masking on a few records.
3. Run [train_sft_lora.py](../labs/train_sft_lora.py) on compatible hardware using a small open model and PEFT adapter. Record base model revision and adapter config. Use the script as a reference implementation; install and test dependencies first.
4. Load the saved adapter in a fresh process and generate on the frozen test prompts. Measure schema validity, allowed-label rate, category accuracy, and unsupported reason rate using human review.
5. Try a stronger prompt/schema baseline before crediting the fine-tune. Compare latency, memory, and maintenance effort as well as output quality.

**Acceptance:** The dataset format, base model, adapter, evaluation script, raw predictions, and failure log are available. A successful training run alone does not complete this project.

**Stretch:** Try a new, disjoint set of paraphrases from humans. Compare LoRA against a model trained with full updates only if hardware and model size permit a fair comparison. QLoRA is an optional memory experiment, not an automatic accuracy upgrade.

## Project 3. Domain adaptation capstone (open-ended, engineer)

Choose one lawful, bounded domain. Examples: maintenance fault triage, public research abstract classification, or a knowledge-base assistant for documents you can legally use. Do not start with confidential production data. State what the system must do and what it must refuse or escalate.

### Proposal template

- **Audience and decision:** Who uses the output? What happens if it is wrong?
- **Inputs/outputs:** Three examples and three difficult counterexamples.
- **Data:** Provenance, license, consent, period, languages, label guide, and exclusions.
- **Prediction time:** Which fields are truly available then?
- **Split:** Group and time rules, frozen test IDs, and duplicate handling.
- **Baselines:** At least a simple rule/prompt and an untuned pretrained model when appropriate.
- **Metric:** Main metric, per-slice metrics, human rubric, failure thresholds, latency/cost target.
- **Method:** Why full tuning, LoRA/QLoRA, retrieval, or no training is appropriate.
- **Compute:** Device, memory, duration, package and model revisions.
- **Delivery:** Saved artifact, inference demo, model card, rollback and update plan.

### Milestones

**M1 — Dataset card and frozen test:** show schema and 20 audited examples across classes; document ambiguous cases. **M2 — Baseline:** show metric and raw predictions on test. **M3 — Training:** run at least one controlled adaptation with saved config and logs. **M4 — Evaluation:** compare baseline and trained outputs on the same frozen set; review failures and uncertainty. **M5 — Delivery:** fresh-process load, model card, intended/unsupported uses, and next improvement.

### Final report outline

1. Problem and why the chosen method fits.
2. Data provenance, rights, labeling, and leakage safeguards.
3. Experimental setup and reproducibility (hardware, seed, versions, revisions).
4. Baseline versus trained result table, including per-class or per-slice detail.
5. Representative failures and what they imply.
6. Serving costs, operational checks, privacy handling, and next steps.

### Rubric (100 points)

| Criterion | Points | What earns full credit |
| --- | ---: | --- |
| Task and metric definition | 10 | Measurable, tied to user error cost |
| Data provenance and label quality | 20 | Rights, privacy, ambiguity, distribution documented |
| Split and leakage control | 15 | Frozen, group/time appropriate, duplicates audited |
| Baselines and experiment | 15 | Fair comparison; configs and run records saved |
| Evaluation and error analysis | 20 | Same test, per-slice detail, honest uncertainty |
| Reproducibility and delivery | 15 | Fresh load, script, model card, limitations |
| Explanation | 5 | Learner can explain tradeoffs in plain language |

## Oral teach-back exam

Explain your project to a beginner in three minutes without saying “epoch,” “LoRA,” or “gradient” in the first minute. Then explain those three terms accurately using your own project. Finally, answer: **What result would make you decide not to deploy the fine-tuned model?**

## Course completion standard

Finishing the labs is not enough. Submit the report and demonstrate that someone else can reproduce the evaluation. If the best result is a prompt or retrieval baseline, that is a valid engineering conclusion.
