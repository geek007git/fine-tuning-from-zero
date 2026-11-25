"""Supervised LoRA fine-tuning on fictional ticket -> JSON pairs.

Uses TRL's *conversational prompt-completion* format: the prompt is a list of
chat messages and the completion is the assistant message. TRL renders both
with the model's own chat template (including the end-of-turn token), and
`completion_only_loss=True` makes only the assistant answer count in the loss.
Run `python inspect_sft_example.py` to see exactly which tokens are trained.
"""
import argparse
import json
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
from trl import SFTConfig, SFTTrainer

from audit_and_baseline import audit, read_rows

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"


def prompt_for(text):
    return ("Classify this support ticket. Return only a JSON object with keys "
            "category and reason. Allowed categories: billing, technical, account. "
            "Use the ticket's own wording as the reason; do not add facts.\nTicket: " + text)


def target_for(row):
    # Teaching simplification: the reason copies the ticket, so it is always
    # grounded. Real projects need short, human-reviewed reasons.
    return json.dumps({"category": row["label"], "reason": row["text"]})


def make_dataset(rows, split):
    """Conversational prompt-completion records for one split. Test is never used here."""
    if split == "test":
        raise ValueError("The test split is reserved for the final evaluation.")
    return Dataset.from_list([
        {"prompt": [{"role": "user", "content": prompt_for(row["text"])}],
         "completion": [{"role": "assistant", "content": target_for(row)}]}
        for row in rows if row["split"] == split
    ])


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="runs/sft_adapter")
    parser.add_argument("--epochs", type=float, default=5)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--grad-accum", type=int, default=2)
    parser.add_argument("--lora-r", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args(argv)


def build_trainer(args):
    rows = read_rows()
    audit(rows)
    set_seed(args.seed)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
    # TRL defaults to bf16, which fails on CPU-only machines. Choose precision from the hardware.
    bf16 = torch.cuda.is_available() and torch.cuda.is_bf16_supported()
    fp16 = torch.cuda.is_available() and not bf16
    config = SFTConfig(bf16=bf16, fp16=fp16,
        output_dir=str(args.output), num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size, per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum, learning_rate=args.learning_rate,
        eval_strategy="epoch", save_strategy="no", logging_steps=1, report_to="none",
        max_length=512, completion_only_loss=True, seed=args.seed)
    adapter = LoraConfig(
        r=args.lora_r, lora_alpha=2 * args.lora_r, lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Qwen2 attention names
        bias="none", task_type="CAUSAL_LM")
    return SFTTrainer(model=model, args=config,
                      train_dataset=make_dataset(rows, "train"),
                      eval_dataset=make_dataset(rows, "validation"),
                      peft_config=adapter, processing_class=tokenizer)


def main():
    args = parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    trainer = build_trainer(args)
    trainer.model.print_trainable_parameters()
    trainer.train()
    trainer.save_model(str(output))          # saves only the small LoRA adapter
    trainer.processing_class.save_pretrained(str(output))  # tokenizer + chat template
    (output / "course_run_info.json").write_text(json.dumps({
        "base_model": MODEL_ID, "seed": args.seed, "epochs": args.epochs,
        "learning_rate": args.learning_rate, "batch_size": args.batch_size,
        "grad_accum": args.grad_accum, "lora_r": args.lora_r,
        "train_split": "train", "validation_split": "validation",
        "excluded_split": "test", "log_history": trainer.state.log_history}, indent=2), encoding="utf-8")
    print("Saved LoRA adapter to", output)


if __name__ == "__main__":
    main()
