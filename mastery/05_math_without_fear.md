# The small amount of math that makes fine-tuning less mysterious

This is optional on the first reading and useful before an engineer's first training run. Every numerical example is invented so that you can calculate it by hand. It does not describe measured performance of the course's models.

## 1. A prediction is a score before it is a label

Imagine a toy model assigns `billing = 2`, `technical = 1`, `account = 0`. Choosing the largest score yields billing. If we convert the scores into probabilities using softmax, we exponentiate and normalize: `e^2 ≈ 7.39`, `e^1 ≈ 2.72`, `e^0 = 1`; total ≈ 11.11. Probabilities are approximately `0.665`, `0.245`, `0.090`. They add up to 1. A real classifier's scores are not guaranteed to be calibrated probabilities of correctness, even after softmax.

**Teach back:** Why can "billing has the highest score" and "billing is surely correct" be very different statements?

## 2. Loss asks how much probability went to the right answer

Suppose billing is the correct class. With predicted probability 0.665, cross-entropy for that item is `-ln(0.665) ≈ 0.408`. If the model instead gave billing 0.1, loss would be about `2.303`. If the model confidently assigns almost zero probability to the right class, loss becomes large. Average loss across a batch combines many such penalties. It is still not a complete measure of business value, truthfulness or safety.

**Practice:** For two correct-label probabilities 0.5 and 0.25, losses are `-ln(0.5) ≈ 0.693` and `-ln(0.25) ≈ 1.386`; their average is about `1.040`. **Teach back:** What does the loss function know about an unsupported explanation? Usually nothing unless the objective and labels explicitly encode that requirement.

## 3. A gradient tells which direction to nudge

Use the tiny model `prediction = w × x` with one input `x = 3`, desired answer `y = 8`, current weight `w = 2`, and squared loss `(prediction - y)^2`. It predicts `6`, giving loss `(6 - 8)^2 = 4`. The derivative with respect to the weight is `2 × (w × x - y) × x = 2 × (-2) × 3 = -12`. With learning rate `0.1`, gradient descent changes the weight to `w_new = 2 - 0.1 × (-12) = 3.2`. The new prediction is `9.6`, with loss `(9.6 - 8)^2 = 2.56`, lower than 4 for this one example.

One bigger step could overshoot farther. A real neural model uses many parameters, minibatches, a different loss for classification or generation, and an optimizer with more machinery. The analogy shows only how an error points toward an update. **Teach back:** Why does the negative gradient cause this weight to increase?

## 4. Batch and accumulation are different levers

If a device processes 2 examples at once and waits for 4 such microbatches before updating, effective batch size is approximately `2 × 4 = 8` on one device, assuming standard accumulation. With multiple devices, multiply by the number of devices when each contributes that many examples. Some final partial batches can be smaller. Increasing accumulation can ease per-step memory pressure but changes when the optimizer updates; it is not a free speed improvement. A training epoch is one pass through the training records, not one optimizer update.

**Practice:** 24 training examples, microbatch 2, accumulation 4, one device: there are 12 microbatches and approximately 3 updates per epoch. **Teach back:** Why can "3 epochs" mean different numbers of updates for different dataset sizes?

## 5. LoRA means a constrained matrix update

A 4-by-4 matrix has 16 entries. If we express a rank-1 update as `B × A`, with `B` size 4-by-1 and `A` size 1-by-4, we train 8 entries. A rank-2 update in this toy matrix needs 4×2 + 2×4 = 16 trainable entries; the toy example no longer saves parameter count. For a much wider `d × k` matrix, LoRA needs `r(d+k)` additional entries rather than training all `dk` entries, which can be much smaller when `r` is low relative to both dimensions. Multiply the correction by the configuration's scaling factor as appropriate; the simple formula shows the structure, not every implementation detail.

For `d = k = 1000` and `r = 8`, the original matrix has `1,000,000` entries while the two adapter matrices have `8 × (1000+1000) = 16,000` trainable entries for this one matrix. This is a parameter-count comparison, **not** a complete GPU memory or accuracy prediction. **Teach back:** What remains frozen, and why is rank useful?

## 6. Bits and memory: an order-of-magnitude check

If a model has 1 billion weights stored at 16 bits each, raw weight storage alone is about 2 billion bytes (roughly 2 GB in decimal units). At 4 bits each, the ideal raw weight bits correspond to about 0.5 billion bytes. Actual training memory is larger because quantization needs metadata and computation uses activations, temporary buffers and optimizer states for trainable parameters. A memory estimate cannot be based only on raw stored weights. Precision choices may change numerical behavior and compatibility.

**Teach back:** Explain why a model whose raw quantized weights fit a device can still fail during training.

## 7. A confusion table contains more than an accuracy score

Imagine 10 tickets: 4 billing, 3 technical and 3 account. The predicted counts are:

| Actual ↓ / Predicted → | Billing | Technical | Account |
| --- | ---: | ---: | ---: |
| Billing | 3 | 1 | 0 |
| Technical | 1 | 2 | 0 |
| Account | 1 | 0 | 2 |

Rows represent actual classes; columns represent predictions, so the header arrows are only visual aids. Correct predictions are on the diagonal: `3+2+2 = 7`, so accuracy is `7/10 = 0.70`. Billing recall is `3/4 = 0.75`, while billing precision is `3/(3+1+1) = 3/5 = 0.60`. Billing F1 is `2×0.75×0.60/(0.75+0.60) ≈ 0.667`. Technical recall is `2/3 ≈ 0.667` and precision `2/3 ≈ 0.667`, so technical F1 ≈ 0.667. Account recall is `2/3 ≈ 0.667`; precision is `2/2 = 1`, so F1 ≈ 0.80. Macro F1 ≈ `(0.667+0.667+0.80)/3 ≈ 0.711`.

**Practice:** If the billing-to-technical error were fixed, calculate new accuracy and billing recall. New accuracy is `8/10 = 0.8` and billing recall is `4/4 = 1`; technical precision would change, too. **Teach back:** Why does fixing one row affect the precision of another predicted class?

## 8. Tiny test sets give jumpy percentages

With 15 held-out cases, each different correct/incorrect result changes accuracy by `1/15 ≈ 6.7 percentage points`. Going from 12 correct to 13 correct looks like 80% to about 86.7%, but it is one changed case. Keep raw predictions and denominators, study which mistake changed, and obtain a larger task-representative test set before strong claims. Reusing those 15 cases for tuning makes final evaluation less credible.

**Teach back:** Explain a one-case change without saying "the model improved by 6.7%" as though that proved a population-level effect.

## Math mastery check

Calculate by hand: one cross-entropy loss; one toy gradient update; effective batch size; parameter count for a `500 × 500` matrix with rank 5 (`5 × (500+500) = 5,000`); and one per-class recall from a confusion table. Then write the plain-English meaning of each answer. If the plain-English meaning is missing, revisit the story before memorizing the formula.
