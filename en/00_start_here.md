# Lesson 0 — Start here: what is fine-tuning?

**Goal:** Understand what changes in a model and when training is a useful choice. Time: about 20–30 minutes. No installation required.

## Start with a problem

A support team receives: “I can sign in, but my invoice shows the wrong amount.” The desired routing label is `billing`.

An existing pretrained model can read general text. Fine-tuning continues its training on examples of the **specific behavior** we want: here, pairing support requests with routing labels. During training, an optimizer changes some model parameters so the model's output better matches the provided examples. At inference time, the model uses those learned parameters to predict a label for a new request.

Think of the dataset as practice questions with answers. The model parameters are the part that learns. The validation and test examples are questions we keep aside to see whether it learned a useful pattern rather than memorizing the practice sheet.

| Term | Simple meaning | This lesson's example |
| --- | --- | --- |
| Pretrained model | A model already trained on broad data | A general text model |
| Input | What the model sees | “My invoice is wrong” |
| Target/label | What we want it to output | `billing` |
| Training | Updating parameters using examples | Practice on labeled requests |
| Inference | Using a model without updating it | Route a new request |
| Baseline | Existing method to beat | A keyword rule or untuned model |
| Held-out test | Examples withheld from training and tuning | New requests seen only in final evaluation |

## A tiny example

| Request | Correct label |
| --- | --- |
| “My card was charged twice.” | `billing` |
| “The app crashes when I upload a photo.” | `technical` |
| “I forgot my password.” | `account` |

If a new request says “I cannot access my invoice because the app crashes,” the label is ambiguous. Before training, define whether the team prioritizes the crash (`technical`) or invoice (`billing`). More data cannot repair inconsistent labeling rules on its own.

## Do we need fine-tuning?

Try the simplest measurable solution first. A clear prompt, a keyword rule, or supplying up-to-date reference information may solve the task. Fine-tuning is a candidate when repeated examples demonstrate a stable desired behavior that simpler baselines cannot reach. Training does not automatically give the model current facts or access to a private database.

## Your check

1. In “I forgot my password” → `account`, name the input and target.
2. Why should we test on requests the model did not train on?
3. If the support policy changes daily, would examples alone keep answers current?

**Answers:** (1) The request is the input and `account` is the target. (2) To measure generalization rather than memorization. (3) No; provide current policy information at inference time and evaluate that setup.

Next: try [Exercise 01 — choose a sensible first method](../exercises/01_choose_the_method.md), then start [Part 1 — Concepts](01_concepts.md).
