"""Compare base or adapter on the identical held-out fictional tickets."""
import argparse
import json
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from audit_and_baseline import LABELS, audit, read_rows
from train_sft_lora import MODEL_ID, prompt_for


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("base", "adapter"), required=True)
    parser.add_argument("--adapter", default="runs/sft_adapter")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = read_rows()
    audit(rows)
    # Load the tokenizer saved with the adapter so the chat template matches training.
    tokenizer = AutoTokenizer.from_pretrained(args.adapter if args.mode == "adapter" else MODEL_ID)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Half precision on GPU; full float32 on CPU, where bfloat16 can be slow or unsupported.
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, dtype="auto" if device == "cuda" else torch.float32).to(device)
    if args.mode == "adapter":
        model = PeftModel.from_pretrained(model, args.adapter)
    model.eval()
    print(f"Evaluating {args.mode} on {device}; this loads the model fresh from disk.")
    results = []
    for row in rows:
        if row["split"] != "test":
            continue
        messages = [{"role": "user", "content": prompt_for(row["text"])}]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            generated = model.generate(**inputs, max_new_tokens=100, do_sample=False,
                                       pad_token_id=tokenizer.eos_token_id)
        raw = tokenizer.decode(generated[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        try:
            parsed = json.loads(raw)
            parse_ok = True
            valid = isinstance(parsed, dict) and set(parsed) == {"category", "reason"} and isinstance(parsed["reason"], str) and isinstance(parsed["category"], str)
        except (json.JSONDecodeError, TypeError):
            parsed, parse_ok, valid = {}, False, False
        category = parsed.get("category") if valid else None
        results.append({"id": row["id"], "label": row["label"], "text": row["text"],
                        "raw": raw, "json_parse_ok": parse_ok, "schema_valid": valid,
                        "category": category,
                        "allowed_category": category in LABELS if valid else False,
                        "correct": valid and category == row["label"]})
    summary = {"mode": args.mode, "n_test": len(results),
               "json_parse_rate": sum(x["json_parse_ok"] for x in results) / len(results),
               "schema_valid_rate": sum(x["schema_valid"] for x in results) / len(results),
               "allowed_category_rate": sum(x["allowed_category"] for x in results) / len(results),
               "category_accuracy": sum(x["correct"] for x in results) / len(results),
               "unsupported_reason_rate": None,
               "note": "Human review required for unsupported reasons; toy scores are illustrative only.",
               "predictions": results}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Saved frozen test results to", output)


if __name__ == "__main__":
    main()
