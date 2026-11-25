# Changelog

## v1.0.0: first GitHub release (2026-11-26)

### Labs: verified end to end
- All three labs were **run end to end on CPU** using current libraries (transformers 5.24, TRL 1.19, PEFT 0.22, torch 2.15). Measured results are in [labs/README.md](labs/README.md#verified-reference-run).
- **Fixed: the classifier lab learned nothing.** Three epochs at a learning rate of 2e-5 with batch size 8 gave only 6 optimizer steps on 15 tickets. Validation loss stayed at ln 3 ≈ 1.10 (chance) and test accuracy was 4/15. New defaults (15 epochs, 5e-5, batch size 4) reach 13/15. The old setting is kept as a teaching experiment.
- **Fixed: the SFT lab crashed on CPU-only machines.** TRL 1.x defaults to bf16. Precision is now chosen from the hardware.
- SFT data now uses TRL's conversational prompt–completion format, so TRL applies the model's own chat template and end-of-turn token instead of using pre-rendered strings.
- LoRA now targets all attention projections (`q/k/v/o_proj`), and training hyperparameters are command-line flags.
- `evaluate_sft.py` now uses the GPU when one is available and loads the tokenizer saved with the adapter.
- New: `inspect_sft_example.py` prints which tokens count in the loss.
- New: `compare_predictions.py` gives a paired comparison of two systems on the same test IDs (fixed / broken / still wrong).
- `audit_and_baseline.py` saves baseline predictions for that comparison.
- New: `colab_labs.ipynb` runs all labs on a free GPU.
- New: `requirements-lock.txt` pins the exact verified versions. `requirements.txt` now has compatible ranges (old minimums such as `trl>=0.12` allowed versions the scripts do not support).
- `check_course.py` now skips virtualenvs and run folders.

### Course text
- Lesson 0 (`en/00_start_here.md`, formerly `lesson_01/`) and Exercise 01 are now linked into the learning path.
- Chapter 16: the toy test has 15 examples, not 12.

### Repository
- New README with learning path, quick start and real example output.
- Licenses: CC BY 4.0 for content, MIT for code.
- Contributing guide, issue and PR templates, and a GitHub Actions workflow (link check, data audit, baseline, syntax check).
- Review brief moved to `docs/REVIEW_BRIEF.md`.
