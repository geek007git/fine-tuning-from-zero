# Open tools and primary resources

Start with documentation and model cards. Check current versions, model licenses, access terms and hardware requirements before running a lab. These links are references, not claims that a particular setup has been benchmarked here.

| Need | Open resource | Use in the course |
| --- | --- | --- |
| Tensor training | [PyTorch](https://pytorch.org/get-started/locally/) | Install the appropriate CPU or GPU build |
| Tokenizers, models and training | [Transformers training guide](https://huggingface.co/docs/transformers/training) | Classifier lab and model loading |
| Load and manage datasets | [Datasets documentation](https://huggingface.co/docs/datasets/) | Train, validation and test splits |
| Train a small adapter | [PEFT LoRA guide](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora) | What is updated and saved |
| Quantized adapter training | [PEFT quantization guide](https://huggingface.co/docs/peft/main/en/developer_guides/quantization) | Optional QLoRA extension |
| Supervised language-model tuning | [TRL SFTTrainer guide](https://huggingface.co/docs/trl/sft_trainer) | Prompt-completion SFT lab |
| Supported dataset structures | [TRL dataset formats](https://huggingface.co/docs/trl/dataset_formats) | Format prompts and completions |
| Evaluation methods | [Evaluate documentation](https://huggingface.co/docs/evaluate/index) | Compare predictions consistently |
| Small open base for JSON lab | [Qwen2.5-0.5B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) | Confirm template, license and limitations |
| Small encoder for classification | [DistilBERT model card](https://huggingface.co/distilbert/distilbert-base-uncased) | Confirm English-only limitations |
| Dataset and model documentation | [Hugging Face model cards](https://huggingface.co/docs/hub/model-cards) and [dataset cards](https://huggingface.co/docs/hub/datasets-cards) | Document evidence and limitations |

## Research papers for the engineer pass

- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685): why a small trained matrix can adapt a frozen model.
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314): why quantization can reduce memory during adapter training.
- [Direct Preference Optimization](https://arxiv.org/abs/2305.18290): optional advanced method after supervised tuning and evaluation.

## Source selection rules

Use data you are allowed to train and redistribute; record where each record came from and any consent restrictions. Read model and dataset cards before reuse. For multilingual claims, test English, Hindi and Tamil separately with speakers who can judge correctness. Do not use a leaderboard score in place of a held-out evaluation matched to your actual task.
