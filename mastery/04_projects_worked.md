# Projects lab book: build, measure, explain and hand over

**Author: Shanmugapriyan S**

Read [Part 4](../en/04_projects.md) first. These projects use the same workflow but increase independence. You can complete the first stage without a GPU. Do not claim a training result you did not observe. Fill the [dataset card](../templates/DATASET_CARD.md) and [model card](../templates/MODEL_CARD.md) alongside your work rather than after you forget what changed.

## Project 0. Paper-and-Python diagnostic (no model download)

**Goal:** Show that you understand the entire evaluation loop before paying for training.

**Task:** Run `python make_toy_data.py` then `python audit_and_baseline.py` from [labs](../labs/README.md). The dataset has 45 fictional tickets with 15 each in train, validation and test. The baseline reads the test set once and lists its mistakes. The toy tickets and dictionary were developed together, so the resulting metric is a teaching demonstration and not independent evidence about production performance.

**Walkthrough of a failure:** `bil-11` is about the renewal amount, but also includes "account." The keyword rule chooses `account`; the intended primary category is `billing`. Identify the word that misled the rule, the correct task definition, and one different billing request that does not reuse the same phrasing. For `tec-12`, the rule sees no technical keyword and falls back to `billing`; what information would a language model need to understand "filter never applies"? For `acc-11`, how might the label policy distinguish a wrong profile from a billing-detail change?

**Submission:** a screenshot or plain-text run log, three errors with diagnosis, an improved baseline **proposed using validation only**, and a note explaining why you cannot claim that proposal improves the final test until a new test set is available if you already inspected these cases. Instructors may instead provide a hidden group-separated class test for fair comparison.

**Mastery check:** Explain the difference between fixing a keyword and changing the evaluation after looking at the final test. This project is complete even if you never run PyTorch.

## Project 1. Support-ticket classifier (guided)

**Goal:** Compare a simple routing rule to a trained encoder without confusing a toy demonstration for a trustworthy benchmark.

**Stage 1: Contract.** Define the three labels, input length, tie-handling and human-review rule. Write three positive examples per label and three mixed requests. The supplied toy data lacks a human-review class, so document how the production workflow would handle ambiguity.

**Stage 2: Data.** Use the [audit script](../labs/audit_and_baseline.py) to inspect duplicates, split/group overlap and per-class counts. If collecting real data, record provenance, rights, consent, annotation policy, grouping and time. Freeze a genuinely new held-out evaluation set before tuning it. Save its IDs separately.

**Stage 3: Baselines.** Measure a rule and, if available, a pretrained classifier without task training. Keep raw outputs and configurations. Decide in advance whether macro F1, account recall or another measure drives acceptance. If certain cases are harmful, define their escalation rather than optimizing a single score.

**Stage 4: Training.** The [reference script](../labs/train_classifier.py) trains a pretrained English encoder on the tiny example dataset. Inspect the label map and data preprocessing, try a small training-only overfit probe for debugging if needed, and log validation loss. A real English-only encoder is not the right basis for untested claims about Hindi or Tamil.

**Stage 5: Evaluation.** Predict on the frozen test once after choosing settings. Present a table with `n`, accuracy, macro F1 and per-class recall for both baseline and trained model. Put three raw paired predictions below the table. If the adapted model loses, explain the observed failures and why you would retain the baseline. Do not hide runs.

**Stage 6: Handoff.** Save model, tokenizer and exact base revision; load them in a separate process; fill model card; state input restrictions, confidence/human-review rule and monitoring plan. A teammate should be able to reproduce *the procedure*, even if hardware prevents bitwise-identical weights.

**Pass criterion:** Honest evidence, a correct split rule, paired predictions and a defensible keep-or-revert decision. On the 45-item toy set, accuracy is too uncertain to support a business claim.

## Project 2. Grounded structured assistant (intermediate)

**Goal:** Turn a request into a JSON object with category and a reason supported by the request.

**Stage 1: Contract.** Required keys are `category` and `reason`; category is one of three labels; reason must not introduce a new fact. Decide whether extra keys are rejected. Define an escalation path for requests mixing issues.

**Stage 2: Fair baseline.** Prompt the base model with the same instruction used after SFT. Use deterministic generation and identical test IDs. Parse with a JSON parser, check exact schema, check allowed category, check category truth and separately review grounding. A response can pass one test and fail another.

**Stage 3: Training.** Run the [LoRA SFT lab](../labs/train_sft_lora.py) on suitable hardware. Its teaching target copies the original ticket into `reason`; this demonstrates grounding but is a poor production explanation. For a real project, write reviewed short reasons and test them independently. Inspect the rendered chat prompt and loss masking; confirm base model, adapter config, tokenizer and max token length.

**Stage 4: Comparison.** Use [evaluate_sft.py](../labs/evaluate_sft.py) for base and adapter modes. The script reports JSON parse rate, exact schema rate, allowed-category rate and category accuracy on identical frozen tickets. Inspect all raw outputs; human-review unsupported reasons with an explicit rule. Report counts (`12/15`) as well as rates (`80%`), and avoid using a 15-item toy change as proof of improvement.

**Stage 5: Service proof.** Reload base plus adapter in a fresh process. Test malformed input, an empty ticket, a request mentioning two issues, a long ticket and a request in an untested language. Decide whether to reject, escalate or process each. Do not silently turn an unsupported output into a plausible-looking answer.

**Pass criterion:** Reproducible generation settings, valid comparison, grounding review and honest limitation statement. Training alone does not satisfy the project.

## Project 3. New domain, your own approved data (capstone)

**Goal:** Transfer the full protocol to a question you actually care about. Examples include maintenance fault triage or classifying research abstracts you have permission to use. Choose one well-scoped label or output contract.

**Week 1: Problem and data.** Interview a domain reviewer. Write the task contract, harm of each error, label rules with ambiguous examples, provenance/rights and privacy policy. Identify dependencies between examples, group and time fields, and an evaluation set that represents intended use. Have a reviewer audit at least 20 examples across classes; if the dataset is too small, report that limitation and narrow your claim.

**Week 2: Baseline and decision.** Run a rule or prompt baseline and, when the task asks for changing facts, include a retrieval baseline. Set a primary metric and minimum acceptable performance for costly cases before tuning. Record error categories and whether better data or rules might solve them.

**Week 3: Controlled adaptation.** Choose a small encoder for a label task or SFT adapter for generative behavior. Record exact versions, compute, seeds and all settings. Use validation for decisions and document each failed attempt. Consider larger or quantized alternatives only when measured needs justify them.

**Week 4: Review and delivery.** Freeze the winner, evaluate once on the independent final test, report slices and denominators, review unsupported statements or harmful errors, compare cost/latency to baseline, test fresh-process load, and propose monitored rollout/rollback. Have another person read the cards and reproduce the evaluation.

**Pass criterion:** [The 100-point rubric in Part 4](../en/04_projects.md) with complete evidence. There is no required score improvement: choosing the simpler baseline can earn full marks if the evidence supports it.

## Optional extension: multilingual teaching and deployment

**Goal:** Extend the capstone to English, Tamil and Hindi without transferring English-only scores to those languages.

Write the English label policy first. Work with competent speakers to produce independently reviewed examples in Tamil and Hindi and realistic mixed-language requests. Preserve semantic label definitions while allowing language-specific phrasing. Split by customer and time before translating near-duplicates; keep translations of one source case in the same split. Report counts, performance, mistakes and confidence separately for each language and mixed-language slice. Document who reviewed translations and how disagreements were resolved. Update model choice if an English-only encoder is unsuitable. This is a **separate evaluated extension**, not an automatic benefit of translating the course text.

## The handover demonstration

At the end of any project, ask a new person to:

1. State the problem in one sentence and say what happens when the model is uncertain.
2. Read the dataset card and name one risk of leakage.
3. Run or inspect the baseline and the same frozen evaluation IDs.
4. Load the saved model or adapter with the correct base and tokenizer, if trained.
5. Explain one correct answer and one failure using raw input and output.
6. Say whether the model should ship, be revised or remain a demonstration.

If the new person cannot do these steps, the project is not finished, even when a training command completed.
