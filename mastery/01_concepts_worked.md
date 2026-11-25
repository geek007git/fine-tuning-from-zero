# Concepts lab book: make the invisible parts visible

**Author: Shanmugapriyan S**

Read [Part 1](../en/01_concepts.md) first. This book slows down the most confusing ideas. For each lesson, follow **story → worked example → common mistake → explain it yourself**. Draw a diagram on paper whenever you cannot explain what goes into the model and what comes out.

## Lesson A. Define the job before the model

**Story:** A mechanic cannot choose a tool until you say whether the car needs a tire repaired or an engine diagnosed. In the same way, "make an AI better" is not a training task.

**Worked example:** A support team receives: "The app crashed before I could see my invoice." Possible jobs differ:

| Job | Input | Required output | What counts as success |
| --- | --- | --- | --- |
| Routing | Ticket text | One of `billing`, `technical`, `account` | Correct primary queue |
| Extraction | Ticket text | JSON with issue and product | Fields supported by text |
| Answering | Ticket plus current policy | Helpful response with cited current policy | No invented policy or promise |
| Summarization | Conversation | Short summary for an agent | Important facts preserved |

The same sentence may deserve different models and datasets for each job. In routing, agree on a rule: perhaps "if the app failed, route technical, even when a document is mentioned." Without this rule, two annotators may assign different labels and both believe they are right.

**Mistake to catch:** Training on ambiguous targets and calling disagreement a model problem. First repair the task definition. **Teach back:** Describe one ticket that a human would disagree about; write a rule that resolves it and one reason it might still need review.

## Lesson B. A model is a function with adjustable numbers

**Story:** Think of a sound mixer with many dials. The input music does not alter the dials by itself. Training changes selected dials; inference uses the dials as they are.

**Worked example:** A toy classifier receives two features: whether the ticket mentions a charge and whether it mentions a login. Imagine scores `billing = 2 × charge`, `account = 3 × login`. For "I cannot log in", the second score wins. This is a tiny analogy, **not** how the provided Transformer internally works. A pretrained model has far more adjustable numbers and complex interactions. Full fine-tuning changes many of them; LoRA trains small added matrices and usually leaves the base numbers frozen. A prompt changes the input; retrieval adds outside text; neither inherently changes the weights.

**Mistake to catch:** "We gave the model a document once, so it permanently learned it." A document in a prompt is input for that request unless a separate training process updates weights. **Teach back:** Use the mixer analogy to explain the difference between changing dials and changing the music being played.

## Lesson C. Tokenization is a data contract

**Story:** A model receives numbered pieces of text, like tiles with IDs; it does not literally see letters the way you do.

**Worked example:** Consider "charged twice!" One tokenizer might produce pieces resembling `charged`, ` twice`, `!`; another might split `charg` and `ed`. These are **illustrations**: the actual pieces depend on the selected tokenizer. A token limit of 128 concerns those pieces plus any special/chat-template tokens, not 128 words. A long ticket might have the decisive clause at the end: "Ignore the invoice; the real problem is I cannot sign in." If truncation drops that clause, even a perfect human annotator would appear inconsistent with the visible input.

**Check by hand:** Pick three long records and mark the clause that determines the answer. Inspect whether it survives the model's tokenizer and maximum length before training. **Mistake to catch:** Writing a completion after the maximum length so the trainer has little or no answer left to learn. **Teach back:** Explain why token limits and label quality interact.

## Lesson D. Training loss is a practice signal, not a grade

**Story:** A student does well on practiced flashcards but fails new exam questions. The flashcard score reflects practice; the exam reflects generalization.

**Worked example:** Suppose a classifier gives the correct label probability 0.8. Its one-item cross-entropy loss is `-ln(0.8) ≈ 0.223`. If it assigns 0.1 to the correct label, loss is `-ln(0.1) ≈ 2.303`. The greater penalty tells an optimizer that a confident wrong answer needs attention. A step roughly means: predict → compute loss → calculate how trainable weights influence loss → adjust weights. The exact update depends on optimizer and schedule. A model can reduce training loss by remembering phrases in those same tickets, while doing worse on unseen customers.

**Mini calculation:** If correct-label probabilities for two examples are 0.8 and 0.1, average loss is `(0.223 + 2.303)/2 ≈ 1.263`. Do not mistake this two-example number for a real model result. **Mistake to catch:** "Loss went down, so we can deploy." Ask for held-out evidence and failures. **Teach back:** What does loss reward, and which important qualities such as groundedness does it fail to measure directly?

## Lesson E. Why three splits exist

**Story:** Practice set, practice exam and final exam serve different purposes. Looking at the final exam while changing your answers turns it into another practice exam.

**Worked example:** Four customer conversations each contain three messages. If you randomly split the twelve messages, the same customer's repeated question may appear in both training and test. Instead, keep all three messages for each conversation in one split. With only four customers, a reliable estimate is still impossible; grouping fixes one leak but cannot create enough evidence. For a changing service, you may train on earlier weeks and test later weeks, also grouping related conversations. Record the exact rule before seeing test labels.

**Concrete audit:** In the toy dataset, `group` denotes an independent fictional case. The audit rejects a group in multiple splits. In real data, `group` should represent the true source of dependence: customer, patient, case, document family or experiment. **Mistake to catch:** Using a convenient arbitrary group ID that does not reflect real duplication. **Teach back:** Why does a group split improve honesty without guaranteeing a representative test set?

## Lesson F. Work out precision, recall and macro F1

**Story:** A security guard who stops everyone catches all threats but is not good at deciding who poses one. We therefore examine different kinds of mistakes.

**Worked example:** Imagine 10 actual billing tickets. A router labels 8 billing; 2 go to other queues. It labels 12 tickets billing overall, including 4 that were not billing. Billing recall is `8 / 10 = 0.80`; precision is `8 / 12 ≈ 0.67`; F1 is `2 × 0.80 × 0.67 / (0.80 + 0.67) ≈ 0.73`. Repeat for technical and account, then average their F1 values for macro F1. Macro F1 gives each class an equal vote, unlike overall accuracy when classes are imbalanced. Denominators matter: 80% recall on 5 examples means one error, and one more mistake would make it 60%.

**Try it:** If account has 5 actual items and 4 found, recall is 0.8. If 5 items were predicted account and 4 were correct, precision is also 0.8; F1 is 0.8. **Mistake to catch:** Reporting "90% good" without counts or class-specific failures. **Teach back:** Explain recall as a question a nontechnical support manager could ask.

## Lesson G. Good scores can still hide a bad system

**Story:** An average temperature of 24°C does not tell you whether some rooms are freezing. A single evaluation number hides who and what fails.

**Worked example:** A router gets 98% overall accuracy across 1,000 English tickets. It could still route all 10 urgent access-recovery requests to the wrong team. A report should include per-class recall, rare classes, long requests, source and language slices, and human escalation outcomes. If the team intends to serve Tamil and Hindi, evaluate real reviewed Tamil, Hindi and mixed-language requests independently. English accuracy does not imply those abilities.

**Mistake to catch:** Measuring the easiest majority examples and assuming the same quality on new users. **Teach back:** Name two populations or circumstances that the course's 45 fictional examples do not represent.

## Lesson H. The decision to abstain

**Story:** An honest student says "I do not know" rather than confidently guessing a high-stakes answer. A useful routing system can likewise send uncertain tickets to a human.

**Worked example:** A model outputs scores for billing, technical and account. A team may set a confidence threshold after studying validation errors and costs: below the threshold, ask a person. A score is not automatically a trustworthy probability; check calibration on representative validation data. Evaluate how many tickets are escalated **and** how often the remaining automated tickets are wrong. If the threshold is chosen using test cases, collect a new untouched evaluation set.

**Mistake to catch:** Treating confidence as proof of correctness. **Teach back:** Explain how a human-review rule might improve safety while increasing workload.

## Concept mastery checkpoint

Without rereading, draw the flow `source → labeling → split → baseline → training → validation → frozen test → failure review`. For each transition write one failure and its detection method. Then explain Lessons D, E and F in three minutes to a classmate. If you cannot compute one example of recall, revisit Lesson F before moving to Methods.
