# Practice workbook: 24 exercises with worked answers

**Author: Shanmugapriyan S**

Use this after each matching phase. Write your answer before opening the worked solution. A correct answer should explain *why* the choice follows from the evidence.

## Concepts: diagnose the task

**C1.** A refund policy changes every Friday. A user asks what this week's policy says. Choose prompt change, retrieval, or fine-tuning as your first step.

**C2.** A team wants all support replies to be polite and output valid JSON. They have 40 good examples. What baseline comes before training?

**C3.** A training ticket is "Card charged twice." The test ticket from the same case is "Two payments on my card." Is a random row split safe?

**C4.** Training loss improves from 0.7 to 0.2 while validation macro F1 drops from 0.74 to 0.61. What is the likely issue, and what should you examine?

**C5.** Two labels have 500 examples each; a third has 20. Why can accuracy be misleading? Name two other measurements.

**C6.** An LLM gives a fluent refund promise it cannot fulfill. Is fluency evidence of correctness? What should the evaluator check?

### Worked answers: concepts

1. **C1:** Retrieve the current authorized policy and check the answer against its date and content. Weight updates do not automatically keep pace with changing documents.
2. **C2:** Try a clear prompt, an output schema with parser and retry, and the untuned model on frozen examples. Only consider SFT after measuring remaining format or behavior failures.
3. **C3:** No. These are related examples from one case; assign the whole conversation or customer group to one split before training.
4. **C4:** Possible overfitting or a split/data mismatch. Check per-class validation errors, learning curves, mislabeled cases, and whether data duplicates crossed splits; choose settings using validation, then test once.
5. **C5:** Always predicting a majority label can score highly while failing the rare class. Report per-class recall and macro F1; include a confusion matrix.
6. **C6:** No. Check the specific promise against an authoritative source and label unsupported claims as failures, even if the wording is excellent.

## Methods: choose and explain the training plan

**M1.** You have 4 GB of GPU memory and want to tune a 7B model. What must you check before choosing QLoRA?

**M2.** Compare full encoder fine-tuning and LoRA on a decoder for three-label routing. What different capabilities are you asking each model to learn?

**M3.** For `{"prompt":"Ticket: ...", "completion":"{...}"}`, which tokens should normally contribute to completion-only loss?

**M4.** You trained a LoRA adapter. Another engineer has the adapter folder but not your model revision. Can they reproduce it reliably?

**M5.** You change the training examples and the base model together, and the score rises. Which change caused the improvement?

**M6.** You have 90 examples and wish to compare 30 hyperparameters. What happens if you choose the best on a 10-example validation set?

### Worked answers: methods

1. **M1:** Verify model/license and supported quantization on actual hardware, estimate memory for weights, activations, optimizer and context length, and try a small test run. QLoRA saves memory but does not guarantee a fit.
2. **M2:** An encoder classifier maps a ticket to one class; an SFT decoder generates a reply such as JSON. Start with the simpler classifier when labels alone solve the task.
3. **M3:** Target answer tokens, with prompt tokens masked. Inspect one encoded sample and loss labels; training on the prompt too changes the objective.
4. **M4:** Not reliably. Record base model ID/revision, tokenizer/chat template, adapter config and package versions.
5. **M5:** The experiment cannot isolate the cause. Repeat comparisons changing one factor with the same held-out data and evaluation.
6. **M6:** Selection overfits the small validation set. Reduce arbitrary trials, collect more data and reserve a separate untouched test set.

## Problems: debug failures

**P1.** All test tickets from one customer are classified correctly; those from new customers fail. What group split would you try?

**P2.** The model returns `{"category":"billing"}` when the required schema also has `reason`. Is that valid JSON? Is it a valid task output?

**P3.** A model always predicts `account`. What three checks come before turning up the learning rate?

**P4.** GPU runs out of memory on a long example. Name four possible changes and one risk from truncating.

**P5.** English test results are good. Can you say the model handles Hindi and Tamil well?

**P6.** A refreshed training run produces worse results after a new policy. What should an engineer preserve for comparison and rollback?

### Worked answers: problems

1. **P1:** Split by customer or conversation so all related messages stay together, then check domain or time shift.
2. **P2:** It is syntactically valid JSON but fails the required schema. Track parse validity and schema validity separately if your rubric needs the distinction.
3. **P3:** Inspect label mapping and train class counts, examples and preprocessing, and per-class confusion/validation predictions. Then examine optimization settings.
4. **P4:** Shorten context after checking useful fields, reduce batch size, use accumulation, choose smaller model or adapter/quantization. Truncation might remove the fact that determines the label.
5. **P5:** No. Build language-specific and code-switched test slices with reviewed labels; report their own metrics.
6. **P6:** Preserve previous model/adapter plus base revision, tokenizer, data/split IDs, run configuration, predictions, latency and policy version. Compare and retain a rollback artifact.

## Projects: judge a completed system

**J1.** On 15 fictional test items a model improves from 0.80 to 0.87 accuracy. Can you claim production improvement?

**J2.** A team tests the final model, edits the prompt in response to test errors, and retests the same 15 examples. How should it report this?

**J3.** A support model incorrectly routes emergency safety messages to ordinary support. Which metric and operating rule matter?

**J4.** An assistant outputs perfect categories but invents reasons. What separate measures belong in the report?

**J5.** An external dataset has a download button but no clear license. May you publish a fine-tuned model and redistribute the data without checking terms?

**J6.** A capstone beats a baseline but takes 20 times longer to serve. What should determine shipping?

### Worked answers: projects

1. **J1:** No. Fifteen toy examples are too small and unrepresentative; report raw counts, uncertainty, and a larger task-matched held-out evaluation.
2. **J2:** The test has become a development set. Report the edits transparently and collect a newly frozen evaluation set for an unbiased final claim.
3. **J3:** Measure recall for safety-sensitive messages on an appropriate reviewed slice and route uncertain or sensitive messages to a human; evaluate this path.
4. **J4:** Report category accuracy, JSON/schema validity, unsupported-reason rate judged against the ticket, and representative errors.
5. **J5:** No. Confirm allowed use, redistribution and privacy conditions; document provenance and restrictions first.
6. **J6:** Decide against predeclared quality, latency, cost, reliability and human-review requirements. A quality gain alone does not decide deployment.

## Mini oral exam

Explain one of your incorrect answers to someone without ML experience. If you can explain the correct decision, a counterexample and what evidence would change your mind, you have learned the idea rather than memorized its name.
