# Contributing

Original course author: **Shanmugapriyan S**. Please keep the author attribution when adapting the teaching material and credit specific contributors for their changes.

Thank you for helping make this course clearer and more correct. Corrections from beginners ("I got stuck here") are as valuable as corrections from experts.

## Ground rules

1. **Keep the teaching order:** Concepts → Methods → Problems → Projects. New material goes into the phase where a learner first needs it.
2. **Follow the lesson pattern:** plain explanation → concrete example → failure case → teach-back question.
3. **Never invent numbers.** Any metric, runtime or memory figure must come from a run you actually did. State the hardware, package versions and date next to it. Illustrative numbers must be labelled as illustrative.
4. **English is the reference version.** Tamil and Hindi translations follow the reviewed English text. Keep code identifiers, label names and metric definitions identical across languages.
5. **Cite primary sources** (official documentation, papers, model cards) for API or method claims.
6. **Keep the learning route clear:** introduce a plain explanation and a useful example before unfamiliar terminology, link the chapter to the next idea, and choose a direct technical explanation whenever an analogy would mislead.

## Before opening a pull request

```bash
cd labs
python make_toy_data.py      # must not change data/toy_tickets.jsonl
python check_course.py       # local Markdown links + data audit
python -m py_compile *.py    # syntax check of every lab script
```

These checks also run automatically on GitHub (see `.github/workflows/checks.yml`). They do **not** run model training; if you change `train_*.py` or `evaluate_sft.py`, run the script yourself and paste the key output and your `pip freeze` versions into the pull request.

## Reviewing the course

[docs/REVIEW_BRIEF.md](docs/REVIEW_BRIEF.md) contains a structured review prompt (correctness → beginner sticking points → missing skills → dependency risks) that works for human or AI reviewers. Keep reviewer suggestions separate from verified fixes until each one is checked.

## Reporting problems

Use the issue templates: **Content error** for wrong or confusing text, **Lab failure** for scripts that error. Include the exact command and your package versions.
