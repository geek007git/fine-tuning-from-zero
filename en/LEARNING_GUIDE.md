# How to study Fine-Tuning from Zero

**Author: Shanmugapriyan S**

Welcome. This is a learning module, so reading a definition and moving on is not the goal. You should be able to explain an idea to another beginner, use it on a new example, and notice when it fails. This guide connects the lessons so you never have to guess why a topic comes next.

## One familiar story for the whole course

A small company receives messages such as:

> "My card was charged twice."

Three teams help customers: `billing` handles payments, `technical` handles a broken app, and `account` handles login and profiles. Your job is to send each message to the right team. We call this **routing**. You can do it with a simple rule, a prompted model, or a trained classifier. Later you will also ask a model to produce a JSON response with the chosen team and a reason.

We use this same situation throughout the course so that only **one new idea changes at a time**. When you see another domain, such as research abstracts or machine faults, ask: "What is the message? What is the correct answer? How will I know whether the system worked?"

Some comparisons are useful and others hide the real mechanism. "Practice questions and an exam" helps explain why test examples must stay unseen. But no everyday analogy fully explains how gradients or LoRA matrices work. Where an analogy stops helping, the lesson switches to a small technical example and works through it slowly.

## Your route through the four parts

| Part | The question it answers | What you will do before moving on |
| --- | --- | --- |
| [Concepts](01_concepts.md) | What actually changes when we fine-tune, and how do we tell whether it learned? | Describe one ticket, its label, the split, a baseline and a mistake |
| [Methods](02_methods.md) | Which way should we solve or train for this task? | Choose a method and explain why a simpler method may work |
| [Problems](03_problems.md) | What can make a good-looking result misleading or a model fail? | Diagnose one failure from evidence, without guessing |
| [Projects](04_projects.md) | Can we build, test and hand over something another person can judge? | Deliver a baseline, evidence, failure analysis and a reproducible result |

Start with [Lesson 0](00_start_here.md). You can read the core sections without any model downloads. If a chapter feels too fast, follow its link to the matching [worked Concepts](../mastery/01_concepts_worked.md), [worked Methods](../mastery/02_methods_worked.md), [worked Problems](../mastery/03_problems_worked.md), or [worked Projects](../mastery/04_projects_worked.md) guide. The [glossary](GLOSSARY.md) explains terms in ordinary language. The [math guide](../mastery/05_math_without_fear.md) provides small calculations only when they help.

## What a single study session looks like

1. **Read one chapter.** After each paragraph, say what happened to the support ticket in your own words.
2. **Work its example.** Write the input, the expected answer and what the model or rule did. If there is a number, write what that number measures.
3. **Notice the failure.** A lesson is not learned until you can name a case where it could go wrong.
4. **Answer the teach-back question without looking.** Imagine explaining it to a classmate who has not studied machine learning.
5. **Check the worked guide or workbook.** Correct your explanation and try a *different* ticket. Familiar wording is not the same as understanding.
6. **Write one sentence that leads to the next lesson.** Example: "Now that I know what a label is, I must decide which examples can be used for practice and which must be saved for evaluation."

If you have only a little Python, use the [student route](../audiences/STUDENTS.md) and the no-download audit first. If you have a working ML task, use the [engineer route](../audiences/ENGINEERS.md). Professors can use the [instructor route](../audiences/INSTRUCTORS.md) with class activities and assessment criteria. All routes follow the same concept-to-project order.

## A slow, worked walk through the whole course

**First, understand the request.** The text "My card was charged twice" is an *input*. `billing` is a *label*: the answer someone has agreed is right. If one reviewer calls a message billing and another calls it account, write a rule for which team should receive it before training. Otherwise the model receives contradictory practice questions.

**Next, try a simple baseline.** A rule that looks for "charged" might send this request to billing. It may fail on "The amount taken from my bank is wrong" if the rule lacks those words. Save its answers and errors. You cannot say a complicated model helped unless you compare it with something concrete.

**Then, separate practice from evaluation.** Training examples let the model change; validation examples help you choose settings; final test examples ask how the chosen solution behaves on unseen requests. If two messages from one customer describe the same issue, keep them on one side of the split. If you read test mistakes and adjust your rule, the test has become practice, too.

**After that, choose a method.** For a stable three-team routing job, you may train a small classifier. If you need to quote a payment policy that changes every week, supplying the current policy may be more useful than teaching old wording to the model. If you need a JSON answer with a supported reason, try a strong prompt and output validation before training an assistant.

**Finally, examine failures.** Suppose a model is right on 12 of 15 tickets and another on 13 of 15. That is one more correct ticket in a tiny toy set. Look at *which* messages changed, whether any important class became worse, whether the JSON is valid, and whether its explanation says something the customer never said. Decide whether the more complicated approach really helps.

The next parts give names and technical detail to these steps. Keep returning to the one ticket when a term seems abstract.

## A map from one lesson to the next

| Chapter | What you learn with the support ticket | Why the next chapter follows |
| --- | --- | --- |
| 1. Fine-tuning | A model may learn to choose `billing` | It must first receive text in a form it can process |
| 2. Tokens | A tokenizer turns the request into IDs | We need examples with agreed answers |
| 3. Data and splits | Related tickets stay together | Now we can describe how practice changes the model |
| 4. Learning | Loss and updates respond to examples | We need a fair way to decide whether they helped |
| 5. Baselines | Compare on the same unseen requests | We can choose which approach to try |
| 6. Method choice | Rule, prompt, retrieval or training | Chosen training needs trustworthy data |
| 7. Data preparation | Fix labels and freeze the split | The first training method is a classifier |
| 8. Full tuning | Train a small model to choose a team | Larger models motivate training fewer weights |
| 9. LoRA | Train a small adapter alongside a base | We can use an assistant to generate structured answers |
| 10. SFT | Learn from prompt-and-answer examples | Runs and deployment need further decisions |
| 11. Delivery | Save, compare and reload correctly | We now test where the pipeline can fail |
| 12. Leakage | Detect seen answers disguised as new tickets | Honest splits still need good labels |
| 13. Data quality | Fix inconsistent and narrow examples | Then diagnose how the training itself behaves |
| 14. Training failures | Examine curves and broken settings | A correct run must also fit available resources |
| 15. Resource failures | Handle memory, latency and load errors | One metric still cannot judge the whole system |
| 16. Evaluation | Check classes, explanations and limits | You are ready to build a whole project |

## If you get stuck

- **A term is confusing:** read its [glossary entry](GLOSSARY.md), say it without the technical term, then return to the ticket.
- **A number is confusing:** use [math without fear](../mastery/05_math_without_fear.md). Ask what the numerator and denominator count.
- **A training script is confusing:** begin with the standard-library [lab guide](../labs/README.md), which needs no GPU. Trace one record through the output.
- **The project feels too large:** complete [Project 0](../mastery/04_projects_worked.md) first. It demonstrates the reasoning without model training.
- **The model loses to the baseline:** report that honestly. Knowing when a simpler system is enough is part of the skill.

**Continue:** [Lesson 0: a first explanation of fine-tuning](00_start_here.md).
