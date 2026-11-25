"""Reference fine-tuning lab; requires dependencies in requirements.txt."""
import argparse
import json
from pathlib import Path

from datasets import Dataset
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          Trainer, TrainingArguments, set_seed)

from audit_and_baseline import LABELS, audit, metrics, read_rows

MODEL_ID = "distilbert/distilbert-base-uncased"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="runs/classifier")
    # With only 15 training tickets, a small learning rate and few epochs give
    # just a handful of optimizer steps and the model barely moves from chance.
    parser.add_argument("--epochs", type=float, default=15)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    rows = read_rows()
    audit(rows)
    set_seed(args.seed)
    label2id = {label: index for index, label in enumerate(LABELS)}
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_ID, num_labels=len(LABELS), label2id=label2id,
        id2label={i: label for label, i in label2id.items()})

    def build(split):
        part = [r for r in rows if r["split"] == split]
        dataset = Dataset.from_list([{"text": r["text"], "labels": label2id[r["label"]]} for r in part])
        return dataset.map(lambda batch: tokenizer(batch["text"], truncation=True, max_length=128), batched=True), part

    train, _ = build("train")
    validation, _ = build("validation")
    test, test_rows = build("test")
    settings = TrainingArguments(
        output_dir=str(output / "checkpoints"), num_train_epochs=args.epochs,
        learning_rate=args.learning_rate, per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=8, eval_strategy="epoch",
        save_strategy="epoch", save_total_limit=1, load_best_model_at_end=True,
        metric_for_best_model="eval_loss", seed=args.seed,
        report_to="none", logging_steps=5)
    trainer = Trainer(model=model, args=settings, train_dataset=train,
                      eval_dataset=validation, processing_class=tokenizer)
    trainer.train()
    trainer.save_model(str(output / "model"))
    tokenizer.save_pretrained(str(output / "model"))
    prediction = trainer.predict(test)
    guessed = prediction.predictions.argmax(axis=-1)
    evaluation_rows = [
        {"id": row["id"], "text": row["text"], "label": row["label"],
         "prediction": LABELS[int(index)]}
        for row, index in zip(test_rows, guessed)
    ]
    (output / "final_test.json").write_text(json.dumps(metrics(evaluation_rows), indent=2), encoding="utf-8")
    with (output / "test_predictions.jsonl").open("w", encoding="utf-8") as stream:
        for row in evaluation_rows:
            stream.write(json.dumps(row) + "\n")
    (output / "run_info.json").write_text(json.dumps({"base_model": MODEL_ID, "seed": args.seed,
        "epochs": args.epochs, "learning_rate": args.learning_rate, "batch_size": args.batch_size,
        "training_rows": len(train), "validation_rows": len(validation), "test_rows": len(test)}, indent=2), encoding="utf-8")
    print("Saved model and frozen-test evaluation to", output)


if __name__ == "__main__":
    main()
