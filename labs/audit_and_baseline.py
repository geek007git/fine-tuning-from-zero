"""Standard-library dataset audit, keyword baseline, and frozen test metrics."""
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

LABELS = ("billing", "technical", "account")
SPLITS = ("train", "validation", "test")
DATA = Path(__file__).parent / "data" / "toy_tickets.jsonl"
WORDS = {
    "billing": {"invoice", "charge", "charged", "payment", "refund", "receipt", "bill", "fee", "tax", "bank", "discount", "price", "card", "paid", "checkout"},
    "technical": {"app", "crashes", "freeze", "frozen", "screen", "video", "export", "browser", "error", "loading", "download", "microphone", "page", "sync", "search", "chart", "desktop", "program"},
    "account": {"login", "profile", "password", "sign", "verification", "authentication", "account", "locked", "device", "security", "username", "access", "invitation", "email"},
}


def read_rows(path=DATA):
    with Path(path).open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def audit(rows):
    ids = set()
    text_split = {}
    group_split = {}
    counts = Counter()
    for row in rows:
        if not all(k in row for k in ("id", "group", "split", "text", "label")):
            raise ValueError("Record missing a required field")
        key = str(row["id"])
        if key in ids:
            raise ValueError(f"Duplicate id: {key}")
        ids.add(key)
        if row["label"] not in LABELS or row["split"] not in SPLITS:
            raise ValueError(f"Unknown label/split on {key}")
        if not isinstance(row["text"], str) or not row["text"].strip():
            raise ValueError(f"Empty text on {key}")
        normalized = " ".join(row["text"].casefold().split())
        if normalized in text_split:
            raise ValueError(f"Duplicate text: {key} and {text_split[normalized]}")
        text_split[normalized] = key
        if row["group"] in group_split and group_split[row["group"]] != row["split"]:
            raise ValueError(f"Group crosses splits: {row['group']}")
        group_split[row["group"]] = row["split"]
        counts[(row["split"], row["label"])] += 1
    for split in SPLITS:
        for label in LABELS:
            if counts[(split, label)] == 0:
                raise ValueError(f"Missing {label} in {split}")
    return counts


def predict(text):
    tokens = set(re.findall(r"[a-z]+", text.casefold()))
    scores = {label: len(tokens & words) for label, words in WORDS.items()}
    return max(LABELS, key=lambda label: scores[label])  # fixed tie-break


def metrics(rows):
    if not rows:
        raise ValueError("No rows to evaluate")
    matrix = {label: Counter() for label in LABELS}
    mistakes = []
    for row in rows:
        actual, predicted = row["label"], row["prediction"]
        if actual not in LABELS or predicted not in LABELS:
            raise ValueError("Invalid actual or predicted label")
        matrix[actual][predicted] += 1
        if actual != predicted:
            mistakes.append({"id": row["id"], "actual": actual, "prediction": predicted})
    per_class = {}
    for label in LABELS:
        tp = matrix[label][label]
        actual_count = sum(matrix[label].values())
        predicted_count = sum(matrix[actual][label] for actual in LABELS)
        recall = tp / actual_count if actual_count else 0.0
        precision = tp / predicted_count if predicted_count else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_class[label] = {"recall": recall, "precision": precision, "f1": f1, "support": actual_count}
    return {"accuracy": sum(matrix[x][x] for x in LABELS) / len(rows),
            "macro_f1": sum(per_class[x]["f1"] for x in LABELS) / len(LABELS),
            "per_class": per_class, "confusion": {x: dict(matrix[x]) for x in LABELS},
            "mistakes": mistakes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="runs/baseline",
                        help="folder for baseline predictions and metrics")
    args = parser.parse_args()
    rows = read_rows()
    counts = audit(rows)
    print("Counts:", json.dumps({split: {label: counts[(split, label)] for label in LABELS} for split in SPLITS}))
    test = [{"id": row["id"], "text": row["text"], "label": row["label"],
             "prediction": predict(row["text"])} for row in rows if row["split"] == "test"]
    result = metrics(test)
    print("Frozen test keyword baseline:")
    print(json.dumps(result, indent=2))
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "final_test.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    with (output / "test_predictions.jsonl").open("w", encoding="utf-8") as stream:
        for row in test:
            stream.write(json.dumps(row) + "\n")
    print("Saved baseline predictions to", output / "test_predictions.jsonl")


if __name__ == "__main__":
    main()
