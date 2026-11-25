# Part 3 — Problems: learn from the failures

**Author: Shanmugapriyan S** · [Learning guide](LEARNING_GUIDE.md) · [Slower worked cases](../mastery/03_problems_worked.md)

This section is an engineering clinic. For every case, write **symptom → likely cause → smallest diagnostic test → fix → evidence** before reading the worked answer. Avoid changing many things at once.

## Chapter 12. Leakage and misleading splits

**Case A — duplicated customers.** A support dataset has 8,000 rows, but each customer's message appears again in a follow-up, sometimes with a pasted response. A random row split reports 96% accuracy. A customer-group split reports 76%. The random test included near copies of training examples; the grouped test is a more honest measure for new customers. Fix: normalize and hash exact duplicates, inspect near duplicates, keep conversations and customers together, re-freeze splits, then retrain every compared model. Do not retain the original 96% in a headline.

**Case B — label in the input.** An input filename is `billing_0032.txt`, and the model is allowed to see it. A nearly perfect score may just mean it read the answer. Fix: remove answer-bearing metadata and inspect a sample of inputs exactly as the model sees them.

**Case C — time travel.** A model predicts an incident category using the final incident resolution, which is written after the initial report. Fix: define the prediction time, keep only features available by then, and split later incidents into test.

**Feynman check:** If a student saw the answer key before the exam, would the exam still measure learning? Explain how each case gives the model an answer key.

**Connection to Chapter 13:** Even when no answer leaks into the input, the labels themselves may be inconsistent or the examples may cover only easy requests.

## Chapter 13. Bad labels, duplicates, and coverage gaps

**Case D — conflicting labels.** “Cannot view invoice because login fails” is labeled `billing` by one person and `account` by another. The model's loss never fully resolves because both labels look valid. Fix: write a priority rule (e.g. route the immediate blocker first), relabel a sample with two annotators, report disagreement, and add an `ambiguous` review lane if the business process needs it. Do not force every hard case into a false certainty.

**Case E — only easy examples.** Training examples are short, grammatical English; real requests include typos, Tamil-English code switching, screenshots, and vague one-word messages. A high clean-test score does not cover production. Fix: define the intended population, collect licensed representative examples, evaluate slices, and state unsupported inputs. Do not invent multilingual ability from an English-only toy dataset.

**Case F — synthetic echo.** All training and test samples were generated from one template. The model may memorize that template rather than understand real requests. Fix: split by template/source and use human-authored or real consented examples for external validity. Synthetic data can teach workflow; it is not automatically ground truth.

**Feynman check:** How can 1,000 examples be less informative than 100 carefully varied examples?

**Connection to Chapter 14:** With trustworthy labels and varied data, we can examine whether the training process is actually learning the intended task.

## Chapter 14. Training curves and optimization failures

**Case G — train loss down, validation loss up.** Likely overfitting or distribution mismatch. Check class counts, duplicate groups, validation examples, and epoch-by-epoch curves. Consider more varied data, fewer epochs, smaller learning rate, or a simpler model. Final test stays untouched while you decide.

**Case H — both losses flat.** Check that labels map to correct IDs, parameters are trainable, learning rate is nonzero, target tokens are included in the loss, and the model actually sees varied examples. Deliberately overfit a *tiny training subset* as a debugging exercise; if even that fails, the training pipeline may be broken. Do not use the tiny subset as evidence of generalization.

**Case I — NaN loss.** Check for malformed numeric values, extreme learning rate, unsupported mixed precision, broken padding/masks, and hardware-specific issues. Reproduce on a small batch with conservative settings. Log the exact batch that fails without leaking private content into public logs.

**Feynman check:** Why is “the loss moved” a weaker statement than “new unseen requests improved”?

**Connection to Chapter 15:** Even correct training can fail to fit a machine or behave differently after an adapter is loaded elsewhere.

## Chapter 15. Memory, speed, and deployment surprises

**Case J — out of memory.** Measure available memory and peak usage. Shorten sequence length only if the task still fits; reduce per-device batch size, use gradient accumulation, choose a smaller model, or use LoRA/QLoRA on compatible hardware. Gradient accumulation does not erase model-weight memory. If the target answer is truncated, an apparently faster run may learn the wrong task.

**Case K — adapter loads but answers differ.** Check the exact base model revision, tokenizer, chat template, adapter config, dtype, and generation settings. Load from disk in a fresh process and compare a fixed set of prompts. A correct training script is insufficient if serving uses a different formatting path.

**Case L — latency and maintenance.** A tuned model beats a prompt baseline by a small margin but costs more to serve and fails on new policy. Compare the whole system: quality, latency, memory, labeling cost, revision frequency, and human review. The best engineering answer may still be a simpler method.

**Feynman check:** Why can a smaller trained model be a better product than a larger one even when both produce good examples?

**Connection to Chapter 16:** We have diagnosed memory and serving problems. Now we need a complete evaluation that looks beyond one attractive number.

## Chapter 16. Evaluation beyond one number

For a classifier, construct a confusion matrix with true classes as rows and predictions as columns. Calculate per-class precision and recall; inspect at least five false positives and five false negatives for each critical class when enough exist. Compare the model to the same fixed baseline on the same cases. Report confidence intervals or uncertainty where sample size is small; never treat the 15-example toy test as a population estimate.

For a generated assistant, build a rubric with separate checks: valid schema, correct category, supported explanation, refusal/uncertainty when evidence is missing, and consistency across paraphrases. A judge model can assist, but check a sample manually and document judge limitations. Include adversarial and out-of-distribution cases. Store user feedback only with suitable permission and privacy handling.

**Worked mini example:** Suppose the test set has 90 `billing`, 5 `technical`, and 5 `account`. Always predicting `billing` gives 90% accuracy, but zero recall for the other classes. A model that improves macro F1 while slightly lowering accuracy may better serve all three queues. The business might value `account` recall most; decide this before looking at the model result.

**Connection to Projects:** The next part combines the task, method, failures, evaluation, and handoff into one complete piece of work. If you cannot explain a result's mistakes, stay with the debugging worksheet below before starting a project.

## Debugging worksheet

Copy this for each failed run:

| Field | Write your finding |
| --- | --- |
| Symptom and affected examples | |
| Baseline and tuned result on the *same* split | |
| First suspected cause | |
| Smallest test that can disprove it | |
| One change made | |
| New measurement and whether it generalized | |
| Remaining uncertainty | |

## Problems to solve before looking at the answer

1. A model scores 98% on a random split but 65% on future-month tickets. Name two plausible causes and one test for each.
2. Training loss falls while `technical` recall is zero. What three things do you inspect first?
3. An SFT model returns invalid JSON on a quarter of test prompts. What baseline and checks do you compare?
4. A LoRA adapter works on the training machine but fails after deployment. Which artifacts and settings do you inspect?

**Worked answers:** (1) Related duplicate messages or drift in policy/population; group and time split, then inspect examples by month. (2) Label mapping, class counts, and confusion matrix; then training examples for that class. (3) Prompt/schema baseline, JSON parse validity, generation settings, chat template, and held-out prompts. (4) Base revision, adapter config/weights, tokenizer/chat template, dtype, and generation settings. More than one diagnosis may be valid; show evidence.

Next: [Projects](04_projects.md).
