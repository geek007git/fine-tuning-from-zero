# Instructor route: teach, adapt and grade the course

The course is a reusable teaching core for college professors, teaching assistants and workplace trainers. Keep the sequence **Concepts → Methods → Problems → Projects** even when the calendar changes. Each chapter's story, failure case and teach-back can be taught as a short demonstration, discussion and quick check.

Use the [worked lab books](../mastery/06_mastery_pathway.md) for slower instruction and the four-level mastery assessment (recall, application, diagnosis, transfer). This prevents a short introductory run from being mistaken for demonstrated mastery.

## Pick a delivery format

| Format | Classroom plan | Expected deliverable |
| --- | --- | --- |
| 1-day workshop | Four 75-minute blocks plus breaks; run only the no-dependency audit | Label policy, baseline errors, method choice, project proposal |
| 4-week course | Two 60–90 minute sessions a week; allow lab time between meetings | Guided Project 1 and a planned Project 2 |
| 12-week semester module | Two weeks Concepts, three Methods, three Problems, four Projects, including review | Reproducible capstone and short oral defense |

Training durations and downloads vary; reserve extra lab time if a GPU run is required. Assign the no-GPU path when hardware or bandwidth is limited.

## Eight-session plan for the 4-week format

| Session | Phase | In-class activity | Check before next session |
| --- | --- | --- | --- |
| 1 | Concepts | Sort scenarios into prompt, retrieval and tuning | Explain what weights change |
| 2 | Concepts | Group related ticket examples; draw train/validation/test | Spot duplicate leakage |
| 3 | Methods | Create label policy, inspect data card, run baseline audit | Explain three baseline errors |
| 4 | Methods | Compare classifier, SFT and LoRA with a small example | Choose one method with a reason |
| 5 | Problems | Diagnose bad labels and a leaky split | Write an evidence-based fix |
| 6 | Problems | Read confusion matrices; inspect JSON parse/schema failures | Report per-class recall with denominator |
| 7 | Projects | Work in teams on Project 1 or plan Project 2 | Submit data and model card drafts |
| 8 | Projects | Demonstrate results or honest no-compute protocol; peer review | Present capstone and limitations |

## Teaching a concept in the Feynman style

For **leakage**, use two nearly identical tickets from the same customer. Ask learners to assign them to a training set and an unseen exam. Have a learner explain why memorizing one answer inflates the grade. Then introduce "group split" as the precise name for keeping both together. Ask for a counterexample: unrelated customers whose messages happen to mention the same word.

## Assessment and grading

The [workbook](../en/05_workbook.md) contains answers: use it for practice, **not as an unchanged closed-book exam**. Assess a new scenario that uses the same reasoning, ask students to justify a split or failure diagnosis, and check raw predictions. The [Project 3 rubric](../en/04_projects.md) gives a 100-point capstone grading scheme. For courses without GPU access, grade data quality, protocol, baseline and error analysis, then mark model training as an optional extension; state this adjustment before students start.

**Example fresh assessment prompt:** "An organization has five documents per customer and needs to predict future categories. A team randomly divides individual documents and reports 95% accuracy. What two split changes and two error slices would you require before accepting the result?" Suggested criteria: group by customer, respect time if future deployment matters, analyze rare classes and new-customer/time slices, explain leakage and changing distributions. Accept other justified slices.

## Classroom operations

- Demonstrate the standard-library lab before any model download; let students inspect three actual mistakes.
- Assign roles in group projects: annotation policy, data audit, baseline, evaluation and reproducibility. Rotate roles for the next task.
- State which artifacts must be submitted if training cannot run; never reward invented metrics.
- Ask students to check data and model licenses and remove sensitive information before uploading to any third-party service.
- Adapt the domain example to the class (support, research abstracts, maintenance) while keeping the same split and evaluation principles.
- Translate concepts into Hindi and Tamil only after the English source is reviewed; keep code identifiers and metric definitions consistent across languages.

## Instructor handoff

Provide the [course map](../COURSE_MAP.md), [dataset card](../templates/DATASET_CARD.md), [model card](../templates/MODEL_CARD.md), [labs](../labs/README.md), and the local [course checker](../labs/check_course.py). If modifying the syllabus, save a course version and rerun the checker before distribution.
