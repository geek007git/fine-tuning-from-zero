"""Compare two prediction files on the *same* frozen test IDs, case by case.

Example:
    python compare_predictions.py runs/baseline/test_predictions.jsonl runs/classifier/test_predictions.jsonl

Each file is JSON Lines with at least `id`, `label` and `prediction`.
Standard library only.
"""
import argparse
import json
from pathlib import Path


def load(path):
    with Path(path).open(encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream if line.strip()]
    return {row["id"]: row for row in rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("before", help="predictions of the reference system, e.g. the baseline")
    parser.add_argument("after", help="predictions of the new system, e.g. the fine-tuned model")
    args = parser.parse_args()
    before, after = load(args.before), load(args.after)
    if set(before) != set(after):
        raise SystemExit("The two files cover different test IDs; the comparison would not be fair.\n"
                         f"Only in before: {sorted(set(before) - set(after))}\n"
                         f"Only in after: {sorted(set(after) - set(before))}")
    for key in before:
        if before[key]["label"] != after[key]["label"]:
            raise SystemExit(f"Gold label differs for {key}; the files use different data versions.")

    both_right = both_wrong = fixed = broken = 0
    print(f"{'id':<8} {'label':<10} {'before':<10} {'after':<10} change")
    for key in sorted(before):
        label = before[key]["label"]
        old, new = before[key]["prediction"], after[key]["prediction"]
        old_ok, new_ok = old == label, new == label
        if old_ok and new_ok:
            both_right += 1
            continue
        if not old_ok and not new_ok:
            both_wrong += 1
            change = "still wrong"
        elif new_ok:
            fixed += 1
            change = "FIXED"
        else:
            broken += 1
            change = "BROKEN"
        print(f"{key:<8} {label:<10} {old:<10} {new:<10} {change}")

    n = len(before)
    print(f"\nn = {n}: before {both_right + broken}/{n} correct, after {both_right + fixed}/{n} correct")
    print(f"both right {both_right}, both wrong {both_wrong}, fixed {fixed}, broken {broken}")
    print("Only the fixed and broken cases differ between the systems. With so few of them, "
          "the difference may be noise; collect a larger frozen test before claiming improvement.")


if __name__ == "__main__":
    main()
