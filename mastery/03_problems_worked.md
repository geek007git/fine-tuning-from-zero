# Problems lab book: debug the claim before changing the model

Read [Part 3](../en/03_problems.md) first. Every incident below follows **symptom → competing explanations → evidence → smallest safe experiment → interpretation**. A single bad metric rarely tells you what caused it.

## Problem A. Suspiciously high accuracy

**Incident:** A router scores 99% on randomly separated messages, but a new-customer pilot fails.

**Hypotheses:** repeated customer templates crossed splits; a future outcome appears in input; test examples are easier than live requests; labels disagree with the live routing rule.

**Evidence:** find repeated conversation IDs, normalize exact text, inspect near-duplicates and timestamps, compare test/live lengths and sources, and ask a domain reviewer to relabel a small sample. If several messages per customer share the same resolution, random rows are not independent examples.

**Experiment:** create a new group-aware, time-aware held-out set, freeze it and rerun the original baseline and adapted model unchanged. Do not use the old 99% as an unbiased estimate. **Teach back:** Why can checking for exact duplicate strings alone miss this leak?

## Problem B. Good overall accuracy, terrible rare-class recall

**Incident:** 950 of 1,000 tickets are billing. A model predicts billing for all tickets: its accuracy is 95%, but it identifies none of the 50 non-billing requests.

**Evidence:** confusion matrix, class counts by split, per-class recall and macro F1. Check if the minority examples are mislabeled or underrepresented by source, language or time. **Small experiment:** write a rule baseline and collect/review informative minority records; change one training factor at a time. Do not automatically oversample duplicated minority cases into both train and test. **Teach back:** Why is 95% accuracy bad here even though it looks high?

## Problem C. Training gets better while validation gets worse

**Incident:** At epoch 1, training loss is 0.50 and validation loss 0.55. At epoch 8, training loss is 0.05 and validation loss 1.20.

**Possible causes:** memorization, mislabeled validation data, mismatch between train and validation, overconfident wrong answers. Check whether validation macro F1 and errors also degrade. **Small experiment:** compare early checkpoints on validation and keep the best; inspect training duplicates and annotator disagreement; consider fewer epochs and more representative data. Resist the urge to pick a checkpoint using the final test. **Teach back:** What pattern suggests overfitting, and what other data problem could look similar?

## Problem D. All predictions become one label

**Incident:** After fine-tuning, every ticket becomes `account`.

**First inspect:** label ID order at train and inference; train class balance; incorrect target or padding labels; truncation that removes decisive text; whether the newly initialized classification head was trained; confusion matrix. Then inspect learning rate, steps and validation loss. **Small experiment:** hand-check five tokenized rows with their label IDs, then try to overfit a very small *training-only* sample as a debugging probe. A model that cannot even learn those examples may have a wiring error; succeeding on them does not prove generalization. **Teach back:** Why do you inspect label mapping before adding more epochs?

## Problem E. Text generation works but JSON fails

**Incident:** The assistant answers "This sounds like billing" but the application rejects its response.

**Decompose the failure:** Was the output parseable JSON? If yes, did it have precisely `category` and `reason` with required types? If yes, was `category` allowed? If yes, was it correct? Was `reason` supported by the ticket? Each measure answers a different question.

**Small experiment:** apply a schema-constrained prompt/validator to the base model and compare with SFT on identical prompts. Audit the rendered chat template and completion-only loss positions. Count invalid outputs as failures rather than dropping them from the denominator. **Teach back:** Give one example that passes JSON parsing and fails the schema.

## Problem F. A convincing reason is invented

**Incident:** A ticket says "I paid yesterday"; the model writes `{"category":"billing","reason":"Two charges were reversed"}`. The category is plausible but the reason contains events absent from the input.

**Evidence:** human review using a rubric: each factual claim must be supported by the ticket or an authorized external source. Track unsupported reasons as a separate error type. **Small experiment:** use a prompt that requests an exact supporting quote and add examples of non-inferential reasons. Compare both prompts or models on a fresh held-out set. A matching label does not erase a false explanation. **Teach back:** Which words in the generated reason go beyond the provided evidence?

## Problem G. GPU runs out of memory

**Incident:** Loading succeeds, but training fails on long examples.

**Check:** model size, context length, longest examples, per-device batch, precision, saved optimizer states, whether the training method updates the whole model. **Small experiment:** use a genuinely shorter representative input, then lower per-device batch and use gradient accumulation; compare a smaller model or adapter and measure memory. Do not blindly truncate the evidence-bearing part of a ticket. If considering QLoRA, verify hardware and software support first. **Teach back:** Why can QLoRA reduce stored base-weight memory while a long sequence still fails?

## Problem H. A model looks great in English, fails in Tamil

**Incident:** A model trained and tested on English is proposed for Tamil and Hindi support.

**Evidence needed:** license/coverage of the chosen model, labeled examples in each target language, code-switched cases, reviewed annotator policy, per-language metrics and actual errors. **Small experiment:** start with human-reviewed evaluation slices, then compare a multilingual base, multilingual adaptation and a suitable baseline. Translating the same small English test mechanically does not capture regional phrasing or real customer queries. **Teach back:** What would you need before saying the system supports three languages?

## Problem I. Scores differ between two runs

**Incident:** Another engineer reports a different result using "the same model."

**Check:** exact dataset snapshot and test IDs; base and tokenizer revision; adapter and prompt; random seed; package versions; device, precision, shuffling and generation settings. Hardware and numerical operations can make strict bitwise reproduction difficult. **Small experiment:** compare raw predictions on the same IDs and trace the first divergent output; record the environment. **Teach back:** Why is the model name alone insufficient to reproduce an adapter result?

## Problem J. The model passes a benchmark but fails deployment

**Incident:** Offline accuracy improves, yet live latency doubles and a new policy causes wrong replies.

**Evidence:** measure p50 and high-percentile latency on target hardware, parse failures, human escalations, policy freshness, cost per request and failure impact. Compare against predeclared acceptance limits. **Small experiment:** shadow or limited deployment with explicit rollback, subject to local policy; inspect live failures without sending private records to an unauthorized service. A higher score is one requirement among several. **Teach back:** What outcome would make you retain the baseline?

## Problem K. Test results improved after repeated prompt edits

**Incident:** A team reads the frozen test failures, adds examples to the prompt, reruns the same test ten times, and reports the best score.

**Diagnosis:** the test became a development set even if its rows never entered a gradient step. **Action:** preserve the run history, label the old test as used for selection, create a fresh untouched evaluation set and state any limits caused by small sample size. **Teach back:** How can an experimenter leak test information without touching training code?

## Problem L. Two annotators disagree

**Incident:** One calls "Cannot download my invoice" billing; another calls it technical.

**Check:** issue policy, whether the download failure concerns an interface defect or unavailable document, and whether multiple labels or a human-review queue are allowed. **Small experiment:** write a label rule with positive and counterexamples, let both label a new blind sample, record disagreements, and revise policy before retraining. **Teach back:** Why can more compute make this problem worse rather than better?

## Diagnostic order you can remember

1. **Task:** Is the answer rule clear, and was the needed information present at prediction time?
2. **Data:** Are labels, splits, duplicates, languages and rights sound?
3. **Baseline:** What errors already occur without training?
4. **Training:** Which weights changed, on what examples, with which loss?
5. **Evaluation:** Same IDs and rubric, honest denominators, relevant slices?
6. **Operations:** Can the artifact load, serve and fall back safely?

If you start by increasing epochs, you skip the first three checks that often explain the failure. Complete three incident writeups using the form: symptom, three hypotheses, evidence collected, one controlled change, observed result, remaining uncertainty. Do not invent an observed result when you have not run an experiment.
