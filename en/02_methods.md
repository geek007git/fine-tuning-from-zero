# Part 2 — Methods: choose and run the right adaptation

You know the words now. Here we turn them into decisions. Each method is a tool with a cost, failure mode, and test. Use the same held-out examples across methods.

## Chapter 6. Decide what to try before training

**Simple story:** If a car has an empty fuel tank, changing its engine is the wrong repair. If a model lacks current facts, adding those facts at inference is usually the first experiment. If it misunderstands a stable response pattern despite good examples, adaptation may help.

Use this order:

1. Define the input, desired output, users, error cost, and measurable success criterion.
2. Try an explicit prompt, output schema, and a few representative examples. Save their results.
3. If the task needs changing facts, retrieve current authorized source material and require evidence in the answer.
4. If a repeated, stable behavior remains weak, compare a trained model with the baseline.
5. Estimate labeling effort, training/inference cost, latency, maintenance, and rights before committing.

**Example:** For classifying 2,000 historic support tickets into three stable categories, a small classifier is plausible. For quoting a refund policy that changes weekly, retrieval is the natural first method. For extracting exactly three fields from messages, first try a constrained schema and validation.

**Teach back:** Which problem does retrieval solve better than a one-time fine-tune? What measured evidence would justify training?

## Chapter 7. Prepare the data, then freeze the experiment

Write a data card: source, license, collection period, intended use, known gaps, label instructions, annotator agreement, and private-data handling. Remove or replace secrets and personal identifiers before making examples available to a third-party service. Deduplicate and inspect a random sample per class. Keep a record of exclusions. Do not let generated labels or synthetic examples silently become “ground truth.”

For classification, use `text` and `label` plus a stable `group` field. For SFT, choose a supported `prompt`/`completion` or conversational format; test the chosen model's chat template on one example. Split before repeated training experiments. In an example with 100 customer conversations, split by conversation rather than by message. In a forecasting-like task, use past-to-future order. Test labels must not be derivable from a feature that would not exist at inference.

**A data-quality checklist:** expected classes; class counts; empty/short/long examples; duplicate or near-duplicate groups; contradictory labels; Unicode and language variety; train/validation/test overlap; leakage from filenames, timestamps, or copied answer text; license and privacy. A dataset with 60 clean examples is valuable for learning the pipeline but not proof of production readiness.

**Teach back:** Why do we inspect examples before training? What can an impressive test score hide if we split related messages across sets?

## Chapter 8. Full fine-tuning of a small classifier

**Simple story:** You adjust many of the student's habits to fit the new job. Full fine-tuning updates a large share of the model's parameters. A sequence classifier adds or initializes a task-specific classification head on top of a pretrained language encoder. The head starts untrained; that is expected.

The standard sequence is: load a licensed pretrained checkpoint and tokenizer; create label IDs; tokenize with a suitable maximum length; load training and validation data; set seed, batch size, learning rate, and evaluation strategy; train; save checkpoint; run the final test separately; compare with the baseline and inspect errors. The [classifier lab](../labs/README.md) shows a concrete script.

CPU training can be practical for a small demonstration but may be slow; a GPU helps. Model choice, input length, and batch size affect memory. A too-small toy dataset can yield noisy results; the lab is for learning, not expected accuracy. For class imbalance, report per-class metrics and consider collecting more examples before changing loss weights.

**Failure case:** Changing the training dataset and the model at the same time makes it hard to know what helped. Log one change at a time on a fixed split.

**Teach back:** What is pretrained here? What starts untrained? What does the final test measure?

## Chapter 9. PEFT, LoRA, and QLoRA

**Simple story:** Instead of rewriting a large textbook, you attach a small set of notes that change how you use it. LoRA adds trainable low-rank matrices to selected linear transformations while the base model is usually frozen. A simplified update is `W' = W + BA`: the original matrix `W` stays, while the smaller `B` and `A` learn a task-specific change. `rank r` controls the inner size of that update; `alpha` scales it; dropout can regularize it. The exact target modules depend on model architecture.

**QLoRA** keeps the base model quantized (commonly 4-bit) while training LoRA adapters, reducing base-weight memory. It does not mean every operation is 4-bit, and it is not guaranteed to fit on any GPU. Quantization can alter numerical behavior. Full tuning, LoRA, and QLoRA are **parameter/memory methods**, not different task definitions. The generated assistant may still need supervised training examples.

Compare trainable parameter counts, peak memory, wall time, validation quality, and final held-out quality. Save adapter configuration and base-model revision together; an adapter alone depends on a compatible base. Merging an adapter into a model is a separate deployment choice and should be checked against outputs before and after.

**Failure case:** You train a LoRA adapter and publish only its directory without documenting the base model. Another engineer cannot reproduce predictions. Record both, including revisions and tokenizer/chat template.

**Teach back:** What does `W + BA` mean? Why can QLoRA use less memory than full tuning? What file must travel with an adapter's documentation?

## Chapter 10. Supervised fine-tuning of a chat model

**Simple story:** A language model learns from demonstrations of how an assistant should answer. In supervised fine-tuning (SFT), we provide prompts and desired completions or conversations. The trainer computes a loss on target tokens selected by the data format and masking configuration. The model does not “understand” a policy merely because we put it in a few responses; evaluate compliance on unseen requests.

Example record: prompt `"Route this ticket. Return JSON with category and reason: My card was charged twice."`; completion `{"category":"billing","reason":"Duplicate charge"}`. For a real model, use its tokenizer and chat template. Decide whether the loss includes the whole conversation or only assistant completion; verify the trainer's behavior with a tiny batch. Limit `max_length` to fit resources without truncating important answers. A structured-output test should parse JSON, validate allowed labels, and compare the category to a reference label.

The open-source [TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer) supports prompt–completion and conversational data; [dataset formats](https://huggingface.co/docs/trl/dataset_formats) explain the shapes. PEFT can train a LoRA adapter on a causal language model. Our [SFT lab](../labs/README.md) uses a small instruct model as a teaching example; its training run requires appropriate hardware and is not a measured benchmark in this repo.

**Failure case:** Mixing differently formatted prompts between training and inference can erase the benefit of tuning. Test the exact inference prompt format that users will see.

**Teach back:** Why do we need a chat template? Why is lower token loss not the same as correct JSON or factual answers?

## Chapter 11. Preference methods, run management, and deployment

SFT teaches from target responses. Preference methods such as DPO use comparisons between preferred and less-preferred answers; reinforcement learning methods add further training machinery. They are **later-stage options**, not a prerequisite for a beginner's first fine-tune. If the reference answers themselves are inconsistent, preference training does not remove the underlying data problem. We cover the concept and decision boundary here rather than pretending a toy preference run proves improved helpfulness.

For every run, record: task definition; source and license; train/validation/test IDs; model and tokenizer revision; framework versions; seed; hyperparameters; device and precision; training logs; before/after predictions; metrics; failure examples; and estimated compute. Save the model or adapter, config, tokenizer if needed, and a model card. Test loading from disk in a fresh process. Measure serving latency, memory, unsafe or unsupported inputs, and behavior after a policy change.

**What to report:** “On 300 held-out tickets, macro F1 improved from X to Y, with recall for account tickets changing from A to B; results are limited to English and this support domain.” Do not replace `X/Y/A/B` with numbers you have not measured.

**Teach back:** When would you postpone preference optimization? Which artifacts are needed for another engineer to reproduce a LoRA result?

## Method selection practice

| Scenario | First defensible method | Evidence to collect |
| --- | --- | --- |
| Weekly policy updates | Retrieval/current context | Correct citations and freshness |
| Stable 3-class ticket routing | Baseline, then small classifier | Macro F1, per-class recall, confusion matrix |
| Consistent output tone and JSON form | Prompt/schema, then SFT candidate | Parse validity and task rubric on new prompts |
| Large model exceeds GPU memory | Smaller model or LoRA/QLoRA | Measured memory, speed, quality |

Next: [Problems](03_problems.md).
