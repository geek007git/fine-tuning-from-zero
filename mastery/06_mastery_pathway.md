# Mastery pathway: practice until you can explain and transfer

**Author: Shanmugapriyan S**

This pathway complements the four core parts. **Mastery is demonstrated through a new problem**, not the number of pages read or a model that happened to train. Work through each stage in order. Use a different small example for each teach-back, then return to the course's support-ticket example to verify you can transfer the idea.

## Repeat this simple teaching loop for every lesson

1. **Say it plainly:** one sentence with no technical vocabulary.
2. **Show one real input and output:** identify which data is visible at prediction time.
3. **Name the precise term:** define it without losing the plain meaning.
4. **Break it:** construct a case where the idea is misused or fails.
5. **Teach it back:** explain the example and failure to another person.
6. **Change domains:** repeat with a different task such as abstract classification or maintenance triage.

If step 4 or 6 fails, reread the worked example and try again. Do not advance just because you recognize the term.

## Stage 1: Concepts mastery

**Read:** [Core Concepts](../en/01_concepts.md), [worked Concepts](01_concepts_worked.md), and [math without fear](05_math_without_fear.md) as needed.

**Do:** Draw an end-to-end pipeline from source records to a held-out claim. Define one stable label task and one question that depends on changing documents. For each choose a baseline and explain why. Compute precision and recall for one class from an invented 3-by-3 confusion table.

**Pass when:** You can explain what changes in fine-tuning, why a prompt or retrieval is different, and why test leakage invalidates a result. If you cannot give a concrete leakage example, repeat the group-split exercise.

## Stage 2: Methods mastery

**Read:** [Core Methods](../en/02_methods.md), [worked Methods](02_methods_worked.md), and the [lab guide](../labs/README.md).

**Do:** Produce a three-row method decision table (classification, grounded changing facts, formatted output). For a prompt-completion record, mark answer tokens included in loss. Draw `W + BA` with shapes. Run the standard-library audit and record all baseline errors.

**Pass when:** You can justify a method based on a measured failure and explain exactly what the training script saves. Name at least two reasons a quantized adapter run might still run out of memory.

## Stage 3: Problems mastery

**Read:** [Core Problems](../en/03_problems.md) and [worked Problems](03_problems_worked.md).

**Do:** Diagnose three incidents using competing hypotheses, evidence, a controlled change and uncertainty. One must be a leakage or selection-bias incident; one must be a data/label incident; one must involve model output or deployment.

**Pass when:** Your explanation distinguishes the observation from its possible causes, and your proposed experiment could disprove your favored explanation. "Train more" without a data or evaluation check is not an acceptable diagnosis.

## Stage 4: Projects mastery

**Read:** [Core Projects](../en/04_projects.md), [worked Projects](04_projects_worked.md), and [workbook](../en/05_workbook.md).

**Do:** Complete Project 0, then Project 1 or 2 if compute is available, then propose a new-domain capstone. Produce a dataset card, baseline prediction table, frozen evaluation protocol, error analysis and model card. When training is possible, add saved artifact and fresh-process reload evidence.

**Pass when:** Another person can reproduce your evaluation and explain why you would keep or reject the adapted model. An honest decision to keep a simpler baseline can pass.

## Four levels of assessment

| Level | Evidence | Example question |
| --- | --- | --- |
| Recall | Define accurately | What is a validation set? |
| Application | Work a new example | Split messages from the same customer safely |
| Diagnosis | Find a cause and test it | Why does accuracy rise while rare-class recall falls? |
| Transfer | Build and defend a new task | Evaluate multilingual maintenance triage with an escalation path |

Aim to reach **Transfer** for each phase. Professors can use the table to design new assessments instead of reusing the worked answers as exam questions.

## Optional engineer extensions after the core

- **Preference methods:** compare chosen and rejected responses only after strong supervised data and evaluation. Ask what human preference means for your domain.
- **Quantized adapter training:** verify hardware support, target modules, peak memory, load/reload compatibility and measured quality. The course's supplied LoRA lab is not itself a QLoRA run.
- **Retrieval with tuning:** separate mistakes caused by missing current evidence from mistakes caused by failing to follow output instructions.
- **Serving at scale:** study batching, high-percentile latency, monitoring, drift, rollback and versioned prompts; measure on the target infrastructure.
- **Specialized tasks:** code, vision and speech need task-appropriate models, datasets and evaluators; do not infer support from this text-only ticket example.
- **Research quality:** multiple seeds where practical, uncertainty/denominators, independent test sets, explicit baselines and a record of every attempted condition.

These extensions are avenues for deeper study, not claims that a text-only beginner course fully teaches every model family. Use the [primary documentation and papers](../RESOURCES.md) before building each extension.

## Professor's oral defense prompt

Hand a learner a new example: "A maintenance team stores four notes for each machine. A model sees a note in training and a similar note from the same machine in test. The organization wants predictions for entirely new machines in a new month." Ask the learner to propose a split, a baseline, one metric, one costly failure, one training method and one reason to abstain. A strong answer connects each choice to the new-machine deployment and identifies both machine-group and time leakage. Follow up by asking how the answer changes if the task is to quote today's maintenance policy.
