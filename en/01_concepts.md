# Part 1 — Concepts: explain it so a beginner understands

**Author: Shanmugapriyan S** · [Learning guide](LEARNING_GUIDE.md) · [Slower worked examples](../mastery/01_concepts_worked.md)

Read in order. Each chapter has a small story, a precise explanation, a failure case, and a teach-back check. Keep a notebook with your own explanation before reading the answer key at the end.

## Chapter 1. What is a model, and what is fine-tuning?

**Simple story.** Imagine a student who has read many books. The student can write and classify sentences in general, but has never seen your support team's three routing labels. You give the student examples of requests paired with the correct label. The student changes their internal habits, then tries to label a new request. That is the intuition behind fine-tuning.

**Precisely:** a pretrained model has numerical parameters (weights) learned from earlier training. At inference, it produces predictions without changing those parameters. Fine-tuning starts from pretrained weights and updates all or some of them using task data and a loss function. For a classifier, an example might be `"My card was charged twice" → billing`. For a chat model, it might be a prompt and a desired reply. An optimizer adjusts trainable parameters to reduce error on training examples. Whether the behavior improves on *new* examples is a separate question answered by evaluation.

Pretraining from scratch starts with untrained parameters and usually needs much more data and compute. Prompting changes what we send at inference; it does not itself update weights. Retrieval supplies relevant documents at inference; it does not itself update weights. Fine-tuning changes parameters. These techniques can be combined.

**Our ticket, three ways:** A keyword rule sees "charged" and chooses billing. A general model given the instruction "Pick billing, technical, or account" may also choose billing, without changing any weights. During fine-tuning we show a pretrained model many *labeled* tickets so some trainable weights change. All three may produce the same correct label for this one easy ticket; the useful question is which approach works reliably on varied, unseen tickets at an acceptable cost.

**Failure case:** “Our policy changes every week, so we'll fine-tune once and the model will know the latest policy.” A fixed model does not magically acquire future policy updates. Supply current documents at inference and check answers against them.

**Teach back:** In two sentences, distinguish a prompt edit from fine-tuning. Then name the thing that changes during fine-tuning.

**Connection to Chapter 2:** A model can learn to route messages only after the message is converted into the pieces it reads. We will follow "My card was charged twice" through that first step.

## Chapter 2. Tokens and the path from text to a prediction

**Simple story.** A model does not read a sentence as a human does. A tokenizer turns text into IDs for pieces of text. The model processes those IDs and produces scores or probabilities. A decoder turns generated IDs back into text.

For `"Reset my password"`, a tokenizer might produce several pieces; exact pieces depend on the tokenizer. The number of words is **not** the number of tokens. The context window limits how many tokens the model can process at once. If a training example is truncated, the answer might be cut off, making the example misleading. If the tokenizer lacks a padding token for batched training, the training code must set or handle one deliberately. For chat models, a **chat template** formats roles, separators, and end markers. Do not invent separators when the chosen model provides its own template.

In classification, a model maps the representation of an input to scores for labels such as `billing`, `technical`, and `account`. In text generation, it predicts the next token repeatedly. A generated answer can sound fluent and still be wrong.

**Watch the route:** The message "My card was charged twice" becomes token IDs. The classifier processes those IDs and assigns a score to each team; the highest score becomes its chosen team. The token IDs and scores are numerical, even though you see words at the beginning and `billing` at the end. We are not claiming any particular token split for that sentence; [the worked token lesson](../mastery/01_concepts_worked.md#lesson-c-tokenization-is-a-data-contract) explains how to inspect the actual tokenizer.

**Failure case:** A learner passes the literal string `Assistant:` into every training item while the model's chat template already inserts an assistant role. The model sees inconsistent formatting and learns artifacts rather than the intended response format.

**Teach back:** Why can a 100-word prompt use more than 100 tokens? Why does cutting off the target answer damage training?

**Connection to Chapter 3:** Once we know what enters the model, we need to decide what the correct answer is and which messages belong in practice or the final test.

## Chapter 3. Examples, labels, and splits

**Simple story.** Practice questions teach; an unseen exam measures what was learned. If the exam repeats the practice questions, the grade is misleading.

A dataset is a set of examples with fields and documented meanings. A classifier record can contain `id`, `text`, `label`, `group`, and `split`. An instruction-tuning record can contain `prompt` and `completion`, or structured messages. Decide the output rule before labeling. For “I cannot open my invoice because the app crashes,” is the primary category `technical` or `billing`? Write that rule, ask two humans to label a sample, and resolve disagreements. Otherwise the model is penalized for following one reasonable interpretation.

Use three roles for data: **training** changes weights; **validation** helps choose settings or checkpoints; **test** is held aside for the final report. The exact percentages depend on dataset size and task. Preserve class coverage in each split. Keep near-duplicate tickets, multiple turns of one conversation, or multiple reports from one customer together so the model cannot memorize a paraphrase from training and “solve” it in test. For time-sensitive tasks, split by time so earlier examples predict later ones. Freeze the test before tuning and record the split seed or grouping rule.

**Place real-looking messages:** Customer A says "Charged twice" and later "I still see two payments". Keep both messages in training *or* both in test, because one can reveal the other. Customer B asks about a frozen upload; that is a different case. Training is where a model practices, validation is where you decide whether a change helped, and test is the final check after you have chosen the solution. The test is not a place to keep fixing a rule until the score looks good.

**Failure case:** The same ticket appears in training as “charged twice” and in test as “my payment was charged twice.” A high score can reflect memorization. Detect duplicate and near-duplicate groups before splitting.

**Teach back:** Explain why a random row split can fail when several rows come from the same customer. What is the difference between validation and test?

**Connection to Chapter 4:** A clean practice set can now guide learning. The next chapter explains what a training step changes, without requiring calculus.

## Chapter 4. Learning, loss, gradients, and overfitting

**Simple story.** A learner tries an answer, sees how wrong it was, and adjusts. Repeat many times. A training loop does a numerical version of this.

One training step: (1) tokenize a batch, (2) compute predictions, (3) compare predictions with targets using a **loss**, (4) compute gradients showing how parameters affect that loss, (5) let an optimizer update trainable parameters. An **epoch** is one pass over the training set. A **batch** is a group of examples in one step. **Learning rate** controls update size. Too large can destabilize training; too small can make learning slow. The **effective batch size** can increase through gradient accumulation when memory is limited.

For classification, cross-entropy heavily penalizes assigning very low probability to the correct label. For generation, next-token loss compares the desired token with the model's predicted distribution at positions included in the loss. In a prompt–completion task, we may want loss on the answer only, depending on the trainer and format. The loss is a useful training signal, **not** a complete measure of helpfulness or factuality.

Overfitting occurs when training performance improves while performance on new examples stagnates or gets worse. Watch validation metrics, preserve a final test, inspect errors, and use a small number of purposeful runs. More epochs are not automatically better.

**Think in two steps:** Suppose the intended label for "My card was charged twice" is billing. If the model initially gives billing a low score, its loss is higher than if it gives billing a high score. The training step changes allowed weights to reduce this kind of practice error. Now try "My bank took the payment twice" in validation: if the model learned only the exact word "charged," it may still fail. This difference between practice and new wording is why validation matters. [Math without fear](../mastery/05_math_without_fear.md) shows one tiny numerical update when you are ready.

**Failure case:** Training loss falls beautifully, but the model routes every test request to `billing`. Class imbalance or overfitting may be hiding behind the loss number. Check a confusion matrix and per-class recall.

**Teach back:** Why is lower training loss insufficient to claim a better model? What does learning rate change?

**Connection to Chapter 5:** A falling practice error tells us the model adapted to practice tickets. We still need to compare it with a simple method on new tickets.

## Chapter 5. Baselines and evidence of improvement

**Simple story.** If you want to know whether a new bicycle is faster, ride both on the same route with comparable conditions. A model comparison also needs the same exam.

Before training, establish a simple baseline: a keyword rule, a clear prompt, or an existing pretrained model, depending on the task. Freeze a held-out set and choose metrics tied to the cost of errors. **Accuracy** counts all correct classifications. **Precision** for a class asks how often a predicted class is correct. **Recall** asks how many real examples of a class we found. **Macro F1** gives each class equal weight, useful when some classes are rare. A confusion matrix shows which categories get mixed up. For generated answers, use a task rubric, exact-format checks where relevant, factual checks, and human review of sampled failures; one automatic metric rarely tells the whole story.

Example: 90% of requests are `billing`. A model predicting `billing` every time has 90% accuracy but 0% recall for `technical` and `account`. This is why one headline score is dangerous.

**Compare the same tickets:** Imagine a simple rule sends 12 of 15 unseen tickets to the correct team and a tuned model sends 13 of 15 correctly. That is one more correct ticket on a very small invented set, not proof the model works better for all customers. List which tickets each system fixed or broke, especially for a team that handles critical access issues. Then ask whether the gain justifies the extra training and maintenance. The [worked Projects guide](../mastery/04_projects_worked.md) turns this into a complete comparison.

Record training data version, model revision, seed, settings, compute, baseline result, tuned result, and representative failures. Repeat on an appropriate independent test when results matter. A two-point gain on 15 toy examples is not persuasive evidence.

**Failure case:** You tweak the learning rate after looking at the test errors twenty times, then report the best test score as unbiased. The test set has become part of development. Use validation for tuning and evaluate once on a fresh test.

**Teach back:** What is the baseline? Why might macro F1 reveal a problem hidden by accuracy? What would you need to claim a real improvement?

**Connection to Methods:** We can now say what counts as a fair improvement. The next part chooses a method for the problem and prepares data for it.

## Concept check — answers in your own words first

1. A company wants a chatbot to cite today's policy. What should be tried first, and why?
2. A support classifier improves on training from 70% to 99%, but test remains 70%. What happened?
3. A dataset contains five near-identical messages from each customer. How should it be split?
4. Does adding a LoRA adapter mean the entire original model was updated?

**Reasoning:** (1) Supply current, trusted policy context or retrieval and evaluate citations; weight updates alone do not maintain changing facts. (2) Likely overfitting or a mismatch; inspect test and validation slices. (3) Group by customer or conversation, or split chronologically if predicting future messages. (4) Usually no: LoRA trains small added matrices while the base weights are frozen; check the actual trainable parameter report.

Next: [Methods](02_methods.md).
