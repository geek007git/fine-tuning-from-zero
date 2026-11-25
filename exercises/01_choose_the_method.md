# Exercise 01 — Choose a sensible first method

**Author: Shanmugapriyan S**

For each case, choose **prompt or rules**, **retrieval/current context**, or **fine-tuning candidate**. Write one sentence explaining how you would evaluate the choice.

1. A chatbot must quote today's refund policy from a company document that changes weekly.
2. A team has 2,000 labeled support messages and wants consistent routing to three categories. A keyword rule scores 72% on a held-out test set.
3. A model occasionally writes answers in a long format; a short, explicit output template has not been tried.
4. A model must learn a stable shorthand used in thousands of labeled machine maintenance reports.

## Suggested reasoning

1. Retrieval/current context first. Check whether answers match the current document, with citations to the relevant passage.
2. Fine-tuning is a candidate **after** testing a stronger prompt or pretrained classifier baseline. Compare all methods on the same held-out examples and inspect errors per class.
3. Try a clearer prompt/template first. Compare compliance on a fixed set of requests.
4. Fine-tuning may help if a simpler glossary/context baseline is insufficient. Hold out reports by machine or time so near-duplicate reports do not leak into evaluation.

There is no universal method based on the story alone. The measured baseline and the cost of wrong answers decide.

Next: [Part 1 — Concepts](../en/01_concepts.md).
