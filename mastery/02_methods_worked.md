# Methods lab book: every training choice has a reason

Read [Part 2](../en/02_methods.md) after the [concepts lab book](01_concepts_worked.md). Here we turn vocabulary into a repeatable experiment. Always ask: **What gap did we measure? What method addresses it? What other explanation could produce the apparent gain?**

## Lesson A. Choose a method from the failure, not the model's size

**Story:** If a door does not open because you have the wrong key, buying a larger hammer is a poor plan.

| Observed problem | First intervention to test | Evidence that it helped |
| --- | --- | --- |
| Wrong current policy | Retrieve dated, authorized policy | Supported answers on unseen current-policy questions |
| Wrong output format | Prompt with schema, validation and retry | Valid schema rate and task correctness |
| Stable wrong labels after a rule baseline | Trained classifier | Per-class metrics on the same frozen test |
| Repeated response style or task demonstrations | SFT, perhaps LoRA | Groundedness, schema and task rubric |
| Model or task too large for memory | Smaller model, shorter inputs, LoRA or QLoRA | Measured memory and quality on target hardware |

The table is a decision aid, not a law. A task may need both retrieval and tuned output behavior. If a prompt and validator already meet requirements, training is optional. **Try it:** A team wants every answer to include the latest warranty period. Write one baseline experiment, one metric and one reason not to start with weight updates. **Teach back:** Describe the exact failure a chosen method is supposed to fix.

## Lesson B. Design one training record completely

**Story:** A teacher must know what question was asked and what answer counts as correct. Randomly collected sentences are not yet a dataset.

**Worked record:**

```json
{"id":"case-017","group":"conversation-017","split":"train","text":"I cannot sign in after resetting my password","label":"account"}
```

The ID identifies the row; group keeps dependent rows together; split determines when it may be viewed; text is what will exist at prediction time; label follows the written policy. Never leave a future-resolution note inside `text` if it would not be available when a real request arrives. For ambiguous requests, write a priority rule or escalate instead of forcing a confident but arbitrary label.

**SFT transformation:** One prompt asks for JSON, and one completion gives the desired object. If the required explanation is grounded, a reliable annotation must include the explanation criterion, not merely a label. In the toy lab the `reason` copies input wording so it is supported; real projects should create concise human-reviewed reasons. **Mistake to catch:** Training on synthetic outputs and evaluating against the same generator without independent human labels. **Teach back:** Which field would cause future-information leakage if filled from a completed support outcome?

## Lesson C. Freeze the experiment before trying methods

**Worked sequence:**

1. Define success and cost of errors. For instance, account recovery recall matters especially when users are locked out.
2. Write label policy and data card; audit duplicates and dependent groups.
3. Assign groups to train, validation and test. Keep test IDs in a recorded file; inspect enough to verify labeling but do not optimize on test mistakes.
4. Establish a baseline with configuration and raw predictions. If it fails, categorize the failures before choosing a model.
5. Choose a small set of predeclared runs; compare on validation. Record every change and its effect.
6. Freeze the selected method, run the final test, and report all required metrics and failures.

**Why:** Repeatedly modifying a model after looking at test failures teaches the experimenter the test answers. This is leakage through the research process even if no test row enters the training script. **Teach back:** What should you do after discovering a test error that inspires a new feature?

## Lesson D. Walk through classifier training

**Story:** A pre-trained reader recognizes words and context; a new label head learns the course's three categories.

The [classifier script](../labs/train_classifier.py) performs these actions: load a model and its tokenizer; map labels to IDs; tokenize each split; initialize a classification head; update parameters on training records; use validation loss for choosing a checkpoint; save the model and tokenizer; then predict the frozen test. The classification head's random initialization is normal. Keep an eye on training and validation losses, per-class errors, input truncation and a base model that does not support the input language.

**Hyperparameter map:**

| Setting | What it changes | Too-small or too-large symptom |
| --- | --- | --- |
| Learning rate | Size of update | Too small: little learning; too large: unstable |
| Epochs | Passes over training data | Too few: underfit; too many: memorization |
| Per-device batch | Examples in one device step | Too large: memory failure; too small: noisy steps |
| Gradient accumulation | Number of steps combined before update | Changes effective batch and update frequency |
| Max tokens | Visible input length | Too short: decisive evidence disappears; too long: memory/latency cost |
| Seed | Initialization and shuffle choices | Different runs may vary; seed alone is not a guarantee of identical hardware results |

**Try it:** Open the script and identify where `train`, `validation`, and `test` appear. Say exactly when test predictions are created. **Mistake to catch:** Trying ten methods on the toy test set and presenting only the best one as a final score. **Teach back:** What part of a new classification model starts from task-specific random weights?

## Lesson E. LoRA with small matrices you can draw

**Story:** Keep a large dictionary printed as it is; attach a thin transparent page of corrections. The result of reading both together changes even though the printed pages remain intact.

Suppose a 4-by-4 weight matrix `W` has 16 entries. A rank-1 update can be written `B × A` with `B` shaped 4-by-1 and `A` shaped 1-by-4, totaling 8 trained entries. Real Transformer matrices are much larger, may need higher ranks, and contain many modules; this tiny example only illustrates the idea. With rank 2, the extra matrices here contain 16 entries, showing that savings depend on matrix dimensions and rank. LoRA learns the new matrices while typically freezing `W`. The adapter stores those updates, not the entire base model.

In practice specify target modules for the chosen model architecture. `r` sets rank, `lora_alpha` affects scaling, and dropout applies regularization. Record trainable parameter count and compare measured quality, memory and latency. **Mistake to catch:** Assuming the same `target_modules` names work for every architecture. **Teach back:** Draw `W + BA`; tell a peer which part is frozen, which is learned, and what is needed to load the adapter.

## Lesson F. QLoRA is a memory strategy with limits

**Story:** Store the printed dictionary in a more compact representation while still writing the thin correction page at useful training precision.

Quantizing the frozen base weights can reduce memory; LoRA adapter training adds trainable parameters. Other memory consumers remain: activations, optimizer states for trainable weights, temporary computations and long sequences. Hardware, software support and performance vary; a particular model fitting is a measurement, not a promise. A QLoRA run is not simply adding `quantization=True` to any existing script. Inspect supported loading options and dependencies on the current hardware, then compare against an appropriate smaller-model baseline. Consult the [PEFT quantization guide](https://huggingface.co/docs/peft/main/en/developer_guides/quantization) when setting up a real run.

**Mistake to catch:** Reporting "4-bit training" as though every numerical operation and every trained value uses four bits. **Teach back:** Name at least three things besides stored base weights that use memory.

## Lesson G. SFT: which tokens are actually graded?

**Story:** A teacher gives a question and grades the answer. If the teacher grades the student for copying the question, training aims at the wrong task.

Toy prompt: `Ticket: Card charged twice. Return category JSON.` Desired completion: `{"category":"billing"}`. With completion-only loss, positions corresponding to the prompt are ignored in the training objective; positions in the desired completion contribute. In many training implementations ignored positions are marked `-100` in label tensors. This number is a convention in the loss interface, **not** a class or token to generate. A chat template adds role markers and end markers; inspecting the full rendered training sample and a few masked label positions is essential. Training and inference must use a compatible format. Official [TRL SFT documentation](https://huggingface.co/docs/trl/sft_trainer) describes prompt-completion format and masking.

**Worked check:** If your rendered input is `[user role][question][assistant role][answer][end]`, place a mark under only the answer-related positions that should affect the selected objective. Now imagine max length truncates `[answer]`; the model sees almost no meaningful target. **Mistake to catch:** Assuming a config flag proves masking is correct without inspecting a tokenized example. **Teach back:** Why can a model have low next-token loss yet still produce invalid JSON?

## Lesson H. From saved file to actual service

**Story:** Baking one good cake in your kitchen is not proof your bakery can produce safe cakes all week.

After training, load the model or adapter in a fresh process; verify that the tokenizer, base model revision and chat template match training. On identical requests, record raw outputs, parse/schema errors, category mistakes, unsupported reasons, latency and resource use. A deployed model needs a versioned artifact, monitoring, rollback and a defined human-review path. For changing facts, connect authorized current data rather than assuming weight updates maintain freshness.

**Try it:** Write a release note with one sentence each for intended users, unsupported use, evaluation evidence, rollback version and who handles escalations. **Mistake to catch:** Publishing only the adapter weights and losing the base revision and prompt. **Teach back:** What is the difference between a good checkpoint and a reliable service?

## Methods mastery checkpoint

Make a one-page decision table for three tasks: stable ticket classification; changing warranty answers; strict JSON extraction. For each name a baseline, a possible adaptation, a primary metric, an expensive failure and the artifact you would save. Draw one LoRA matrix example and mark the SFT loss positions. If those two explanations are unclear, repeat Lessons E and G before debugging a training run.
