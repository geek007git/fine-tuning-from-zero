# Course map: Concepts → Methods → Problems → Projects

## Learner profile and outcomes

Prerequisites for the full lab route: basic Python, reading CSV/JSON, and familiarity with using an AI model. The [student Python bridge](audiences/STUDENTS.md) helps beginners start. No calculus or GPU is required for the reading, exercises and standard-library audit. Model labs require a compatible Python environment, model downloads, and suitable CPU/GPU resources.

Audience routes: [students](audiences/STUDENTS.md) use a paced no-GPU option; [engineers](audiences/ENGINEERS.md) use production decision gates; [professors and instructors](audiences/INSTRUCTORS.md) have workshop, four-week and semester plans with assessment guidance. All routes preserve the same four-phase order.

After the course, a learner can (a) decide whether fine-tuning is appropriate, (b) build and audit a dataset, (c) run a baseline, (d) train and evaluate an adapted model, (e) diagnose common failures, and (f) document deployment risks and reproducibility.

| Phase | Chapters | Output | Suggested study time |
| --- | --- | --- | --- |
| **1. Concepts** | 1–5: model, tokens, data, training, evaluation | Explain the entire pipeline without jargon | 5–7 hours |
| **2. Methods** | 6–11: decision tree, full tuning, PEFT, SFT, preferences, run management | Baseline + two training methods | 8–12 hours plus compute |
| **3. Problems** | 12–16: leakage, data quality, overfitting, resource limits, behavior failures | Error log with fixes | 5–7 hours |
| **4. Projects** | Guided classifier, structured assistant, domain capstone | Reproducible portfolio project | 10-20 hours plus compute |

These are planning estimates. Actual training time depends on model, dataset, hardware, and batch settings.

The first-pass core is compact; deeper [worked Concepts](mastery/01_concepts_worked.md), [worked Methods](mastery/02_methods_worked.md), [worked Problems](mastery/03_problems_worked.md) and [worked Projects](mastery/04_projects_worked.md) teach calculations, decisions and failure diagnosis more slowly. Use [math without fear](mastery/05_math_without_fear.md) and the [mastery pathway](mastery/06_mastery_pathway.md) for advanced checkpoints and cross-domain transfer. The four phases remain in the required order.

## Learning checks

Use the [24-question practice workbook](en/05_workbook.md) after each phase. Answers are included for self-study; read them after writing your own response.

- **After Concepts:** explain “what is updated” and “what is held out” with the support-ticket example.
- **After Methods:** show baseline and tuned predictions on the same test items; name all training knobs and saved artifacts.
- **After Problems:** find and fix a deliberately leaky or mislabeled data example.
- **After Projects:** another learner can run the instructions and understand the result, including failures.

## Three depth levels

1. **First pass:** read the simple explanation, work the paper exercises, run the no-dependency audit.
2. **Builder pass:** run the classifier lab and the LoRA SFT lab on appropriate hardware; save predictions and metrics.
3. **Engineer pass:** add a real licensed dataset, group-aware split, per-slice analysis, cost record, model card, and deployment checks.

## One example that grows through the course

We use fictional support tickets labeled `billing`, `technical`, and `account`. In Concepts, you identify input and target. In Methods, you compare a keyword baseline and a pretrained classifier. In Problems, you discover ambiguous tickets and duplicate-leakage traps. In Projects, you ship a tested routing model and a structured-response assistant. The course never substitutes toy scores for real evidence of production quality.

## Order of work in every project

Define task and success metric → inspect data rights and examples → freeze split → measure baseline → train → evaluate on the same held-out split → analyze failures → document → decide whether to deploy. A new model is optional when a simpler baseline already meets the requirements.

Fill the [dataset card](templates/DATASET_CARD.md) before training and the [model card](templates/MODEL_CARD.md) when reporting outcomes. If an independent reviewer checks the course, use the [review brief](docs/REVIEW_BRIEF.md) and keep its findings separate from measured results.
