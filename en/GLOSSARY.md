# Plain-English glossary

Use a term only when you can also explain what changes in the support-ticket example.

| Term | Simple meaning | Ticket example |
| --- | --- | --- |
| Pretrained model | Model that learned general patterns before your task | An encoder already knows many English words |
| Fine-tuning | Updating learned weights using examples of your task | Learn to label support tickets |
| Weights | Numbers the model changes while learning | Internal numbers change after training |
| Inference | Using the model to predict, without training | Predict `billing` for a new ticket |
| Token | Small piece of text the model reads | A word or word fragment in the ticket |
| Tokenizer | Rules turning text into token IDs | Turns a sentence into model inputs |
| Context window | Maximum tokens a model can read in one request | Long email may need trimming |
| Label | Correct answer assigned to an example | `technical` |
| Training set | Examples used to change weights | Historical tickets used in fitting |
| Validation set | Examples used to choose settings | Try two learning rates here |
| Test set | Frozen examples for final assessment | Report result once after choices |
| Group split | Keep related examples on the same side of a split | Same customer's paraphrases stay together |
| Leakage | Information from the answer or test set sneaks into training | Duplicate ticket appears in test |
| Baseline | Simple reference solution | Keyword router or prompted base model |
| Loss | Number describing how wrong the prediction was during training | High for a wrong confident label |
| Gradient | Direction suggesting how to change weights to reduce loss | A small adjustment after a batch |
| Learning rate | Size of a weight update | Too large can make training unstable |
| Epoch | One pass over the training examples | Two passes through all training tickets |
| Batch | Examples processed together for one update | Eight tickets in a step |
| Overfitting | Learning quirks of training data rather than the task | Memorizes specific account names |
| Accuracy | Fraction of predictions correct | 8 of 10 labels correct |
| Recall | Fraction of actual examples of a class found | Finds 7 of 10 actual billing tickets |
| Precision | Fraction of predictions of a class that are correct | 7 of 8 predicted billing are billing |
| Macro F1 | Average of per-class F1 scores, giving each class equal weight | Rare class counts as much as common one |
| Confusion matrix | Table of real labels versus predicted labels | Shows billing sent to account |
| Slice | A meaningful subset evaluated separately | Tamil or very long tickets |
| Encoder | Model representation useful for understanding/classification | DistilBERT ticket classifier |
| Decoder / causal LM | Model predicting the next token, useful for generation | Writes a JSON answer |
| SFT | Supervised fine-tuning on desired responses | Ticket prompt paired with JSON response |
| Instruction tuning | SFT on instructions and example answers | Follow an instruction to produce category |
| LoRA | Train small low-rank matrices while freezing base weights | Save a small adapter for the assistant |
| Adapter | Saved extra trainable weights used alongside a base model | LoRA weights loaded with original model |
| Rank | Size of LoRA's small update representation | `r=8` starts with eight update directions |
| Quantization | Store or compute weights with fewer bits | Reduce base-model memory use |
| QLoRA | Train a LoRA adapter with a quantized frozen base | Adapter training on constrained GPU |
| Full tuning | Train most or all base-model weights | Update the whole classifier backbone |
| PEFT | Family of methods that train relatively few parameters | LoRA is one PEFT method |
| Chat template | Model-specific way of formatting roles and turns | Formats system/user/assistant text |
| Prompt completion | Input text paired with desired output text | Ticket prompt paired with JSON |
| Target masking | Decide which tokens contribute to training loss | Train on answer tokens rather than copied prompt |
| Preference tuning | Learn from comparisons between responses | Prefer supported reason over invented reason |
| DPO | Preference optimization using chosen/rejected examples | Favor one safer JSON reason |
| Hallucination | Plausible statement without evidence | Invents a refund that did not happen |
| Schema validity | Output follows a required structure | Valid JSON with two required keys |
| Model card | Brief report of intended use, data, tests and limitations | Why routing model should not handle emergencies |
| Reproducibility | Another person can follow steps and understand the same setup | Record seed, versions, split, base revision |

## Teach-back

Explain to a classmate why a low training loss does not prove that a model routes new tickets well. Then explain why a frozen test set answers a different question from the validation set.
