"""Show one training example exactly as the SFT trainer sees it.

Prints every token with a marker: TRAIN if it counts in the loss, `-` if it is
masked (label -100). Use this to check the chat template, the end-of-turn token
and completion-only masking *before* spending compute on training.

    python inspect_sft_example.py            # first training example
    python inspect_sft_example.py --index 3
"""
import argparse

from train_sft_lora import build_trainer, parse_args


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--index", type=int, default=0)
    own = parser.parse_args()
    trainer = build_trainer(parse_args(["--output", "runs/inspect_tmp"]))
    tokenizer = trainer.processing_class
    batch = trainer.data_collator([trainer.train_dataset[own.index]])
    input_ids, labels = batch["input_ids"][0].tolist(), batch["labels"][0].tolist()

    print("=== Rendered text the model reads ===")
    print(tokenizer.decode(input_ids))
    print("\n=== Token by token ===")
    for token_id, label in zip(input_ids, labels):
        mark = "TRAIN" if label != -100 else "  -  "
        print(f"{mark}  {token_id:>7}  {tokenizer.decode([token_id])!r}")
    trained = sum(label != -100 for label in labels)
    print(f"\n{trained} of {len(labels)} tokens count in the loss.")
    print("Check: only the assistant's JSON and its end-of-turn token should be marked TRAIN.")


if __name__ == "__main__":
    main()
