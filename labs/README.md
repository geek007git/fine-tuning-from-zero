# Hands-on labs: from dataset to evaluated model

Work here after reading [Concepts](../en/01_concepts.md), [Methods](../en/02_methods.md) and [Problems](../en/03_problems.md). All tickets are invented. They demonstrate mechanics; scores on 15 toy test tickets do not predict real-world performance.

| Lab | Script(s) | Needs | Time on a laptop CPU |
| --- | --- | --- | --- |
| 1. Audit + keyword baseline | `audit_and_baseline.py` | Python only | seconds |
| 2. Fine-tune a classifier | `train_classifier.py`, `compare_predictions.py` | ML packages | ~3 min + one-time 270 MB download |
| 3. LoRA SFT of a chat model | `inspect_sft_example.py`, `train_sft_lora.py`, `evaluate_sft.py` | ML packages | see [verified run](#verified-reference-run) + one-time 1 GB download |

No local setup? Use the [Colab notebook](colab_labs.ipynb), which runs all three labs on a free GPU.

## 0. Create an isolated environment

Lab 1 needs only Python 3.10+. For Labs 2–3, use Python 3.10–3.12. From this `labs/` folder:

```powershell
# Windows (PowerShell)
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

```bash
# Linux / macOS
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` gives compatible version ranges. [`requirements-lock.txt`](requirements-lock.txt) pins the exact versions used for the verified run below. For an NVIDIA GPU, install PyTorch first using the [official selector](https://pytorch.org/get-started/locally/), then check it with `python -c "import torch; print(torch.cuda.is_available())"`. Record your own environment with `python -m pip freeze > run-requirements.txt` next to your results.

## 1. Inspect data and establish a baseline

```bash
python make_toy_data.py          # (re)creates data/toy_tickets.jsonl
python audit_and_baseline.py     # audit + keyword baseline on the frozen test
```

Each record has `id`, `group`, `split`, `text`, `label`. The audit **fails loudly** on duplicate IDs, duplicate normalized text, a group crossing splits, unknown labels, or a class missing from a split. It then scores a keyword classifier on the 15 test tickets and saves `runs/baseline/test_predictions.jsonl`.

Expected result: **12/15 correct**, with mistakes on `bil-11`, `tec-12` and `acc-11`. [Projects worked](../mastery/04_projects_worked.md#project-0-paper-and-python-diagnostic-no-model-download) walks through why each one fails.

The toy data and the keyword list were written together, so this number is a worked example, **not an unbiased estimate**. For a real benchmark, fix the baseline and protocol before looking at test labels.

## 2. Fine-tune a ticket classifier

```bash
python train_classifier.py --output runs/classifier
python compare_predictions.py runs/baseline/test_predictions.jsonl runs/classifier/test_predictions.jsonl
```

The script fully fine-tunes [DistilBERT](https://huggingface.co/distilbert/distilbert-base-uncased) (an English encoder) with a new 3-class head. It uses validation loss to choose the best epoch and predicts the test set **once** at the end. Look at `runs/classifier/final_test.json`, `test_predictions.jsonl` and `run_info.json`.

Flags: `--epochs` (default 15), `--learning-rate` (5e-5), `--batch-size` (4), `--seed` (42).

> **Try this. It is the most useful experiment in the lab.** Run with `--epochs 3 --learning-rate 2e-5 --batch-size 8`. With only 15 training tickets, that gives just 6 optimizer steps. Validation loss stays at about 1.10 ≈ ln 3, which is exactly random guessing among 3 classes, and test accuracy collapses. The training "finished", but nothing was learned. Explain why using [effective batch size and steps](../mastery/05_math_without_fear.md#4-batch-and-accumulation-are-different-levers).

`compare_predictions.py` shows which tickets each system got right on the **same IDs**. Read the FIXED and BROKEN rows, not only the totals.

## 3. Structured JSON assistant with LoRA

```bash
python inspect_sft_example.py                       # 1. see which tokens are trained
python evaluate_sft.py --mode base --output runs/base_eval.json          # 2. baseline
python train_sft_lora.py --output runs/sft_adapter                       # 3. train adapter
python evaluate_sft.py --mode adapter --adapter runs/sft_adapter --output runs/adapter_eval.json  # 4. fresh reload + eval
```

1. **Inspect first.** `inspect_sft_example.py` prints one training example token by token and marks the ones that count in the loss. Only the assistant's JSON and its end-of-turn token should be marked `TRAIN`. If the prompt is marked too, the masking is wrong.
2. **Baseline.** The untouched [Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) gets the identical prompt.
3. **Train.** The data uses TRL's *conversational prompt–completion* format, so TRL applies the model's own chat template. LoRA (`r=8`) is attached to the attention projections, and only about 0.2% of parameters train. Flags: `--epochs`, `--learning-rate`, `--batch-size`, `--grad-accum`, `--lora-r`, `--seed`.
4. **Evaluate.** The base model and the adapter are loaded fresh from disk. Both runs use the same 15 test tickets, the same greedy decoding and the same parser. The script reports `json_parse_rate`, `schema_valid_rate` (exactly the keys `category` and `reason`), `allowed_category_rate` and `category_accuracy`. Invalid output counts as a failure; it is never dropped from the denominator.

Whether each `reason` is supported by the ticket needs **human review**. The script leaves `unsupported_reason_rate` as `null` on purpose.

In this toy lab the training `reason` copies the ticket text, so it is always grounded but is a poor explanation. In a real project, write short human-reviewed reasons.

## 4. Make the experiment defensible

Record: dataset source and license, split rule and seed, baseline predictions, model ID **and revision**, training configuration, package versions, test IDs, mistakes, runtime and hardware. Then fill in the [model card](../templates/MODEL_CARD.md). Before deploying anything, collect a realistic, legally usable dataset and adapt the label rules.

## Verified reference run

These are measured outputs from one run on **CPU only** (Windows 11, Python 3.11, no GPU), using the exact versions in [`requirements-lock.txt`](requirements-lock.txt), with default flags and seed 42. They show what you should roughly expect. They are **not** benchmarks: on 15 test tickets, a single ticket moves accuracy by 6.7 points. GPU runs and other library versions can produce different numbers.

**Lab 1: keyword baseline (test, n = 15)**

| | accuracy | macro F1 | mistakes |
| --- | --- | --- | --- |
| Keyword rule | 12/15 (0.80) | 0.805 | bil-11, tec-12, acc-11 |

**Lab 2: DistilBERT classifier (test, n = 15)** — validation loss 1.093 → 0.248 over 15 epochs, about 3 minutes on CPU

| | accuracy | macro F1 | vs. baseline on same IDs |
| --- | --- | --- | --- |
| Fine-tuned DistilBERT | 13/15 (0.87) | 0.866 | 3 fixed, 2 broken |
| Same script, `--epochs 3 --learning-rate 2e-5 --batch-size 8` | 4/15 (0.27) | 0.199 | validation loss stuck at about 1.10 |

**Lab 3: Qwen2.5-0.5B-Instruct + LoRA (test, n = 15)**

SFT_RESULTS_PLACEHOLDER

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError: torch` | Virtual environment not active | Activate `.venv`, then reinstall the requirements |
| `TypeError: ... unexpected keyword argument` in `SFTConfig` or `TrainingArguments` | Library version outside the tested range | `pip install -r requirements-lock.txt` |
| Validation loss stays at about 1.10 (classifier) | Too few optimizer steps | More epochs or a higher learning rate; see the experiment above |
| `CUDA out of memory` | Batch or sequence too large | `--batch-size 1 --grad-accum 4`; see [Chapter 15](../en/03_problems.md#chapter-15-memory-speed-and-deployment-surprises) |
| Base and adapter give the same outputs | Adapter path wrong, or the adapter was not trained | Check that `runs/sft_adapter/adapter_config.json` exists; pass `--adapter` |
| Downloads fail or are slow | Network or Hugging Face Hub access | Retry; set `HF_HOME` to a disk with space |

If an upstream API changes, check the [official documentation](../RESOURCES.md), pin a working version and [open an issue](https://github.com/YOUR-USERNAME/fine-tuning-from-zero/issues/new/choose).
