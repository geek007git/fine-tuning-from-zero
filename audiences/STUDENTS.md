# Student route: learn without assuming a GPU

Follow the shared order: **Concepts → Methods → Problems → Projects**. This route is for first-time learners, including students who only know a little Python.

For a short introduction, read the core chapters and workbook. For mastery, follow each phase with its [worked lab book and checkpoint](../mastery/06_mastery_pathway.md) before proceeding. Use [math without fear](../mastery/05_math_without_fear.md) whenever an equation gets in the way of the idea.

## Before the course: a 30-minute Python bridge

You should be able to run `python script.py`, read a JSON object, understand a list and a loop, and change a file path. If you cannot yet do those, open [make_toy_data.py](../labs/make_toy_data.py) and find where `label`, `split`, and `text` are assigned. Run it; then open [toy_tickets.jsonl](../labs/data/toy_tickets.jsonl) and explain one line. You do not need to understand the training libraries yet.

## Four passes

| Pass | What to read and do | Evidence of understanding |
| --- | --- | --- |
| 1. Concepts | [Chapters 1–5](../en/01_concepts.md), then C1–C6 in the [workbook](../en/05_workbook.md) | Explain training, validation, test and baseline using a ticket |
| 2. Methods | [Chapters 6–11](../en/02_methods.md); run the [data audit](../labs/README.md); answer M1–M6 | Show the three baseline mistakes and choose a next experiment |
| 3. Problems | [Chapters 12–16](../en/03_problems.md); answer P1–P6 | Describe why a duplicate or wrong label breaks an evaluation |
| 4. Projects | Complete [Project 1](../en/04_projects.md) and J1–J6; try Project 2 when hardware allows | Submit data card, baseline, error log, model card and honest conclusion |

## If you have no GPU

Run the generator, audit and link checker in [labs](../labs/README.md). Trace three records by hand through the label rule, baseline prediction and confusion matrix. Write a project proposal and error analysis. A training experiment may be run on a school lab machine or suitable remote compute later; **do not invent training results**. If the course is graded without compute, the instructor can assess the protocol, baseline and diagnosis separately from the optional model run.

## Common learner questions

- **Do I need calculus?** No for the conceptual route. For advanced study, gradients explain how weights change; the first lab uses no gradient calculations.
- **Which script do I run first?** `python make_toy_data.py`, then `python audit_and_baseline.py`, from the labs directory.
- **What if my fine-tuned model loses?** Explain the result and submit it. A good experiment can show that the baseline is already sufficient.
- **When should I read the answers?** After writing your own explanation. The workbook is for practice, not a secure exam.

## Student submission checklist

Attach your own explanation, data and model cards, baseline predictions, training log **if actually run**, held-out predictions and failures, exact code/settings, and a short note about what you would change next. Quote raw denominators alongside percentages on tiny test sets.
