# Independent review brief for Claude

Give a reviewer (human or AI) the repository and this brief. Ask it to review as a critical curriculum designer and ML engineer. Its suggestions are welcome; each change should be checked against the learner goal and the current documentation before incorporation.

## Copy this prompt to Claude

> Review the attached course for beginners and engineers. The mandatory teaching order is Concepts, then Methods, then Problems, then Projects. English is the authoritative core; Tamil and Hindi translations come later. Use the Feynman approach: plain explanation, concrete example, failure case, teach-back. First list **specific correctness errors with file and section**, then **places a beginner would get stuck**, then **missing end-to-end skills**, then **lab code that may fail on current dependencies**. Pay special attention to train/validation/test leakage, toy-data overclaiming, chat templates and prompt-completion masking, metrics, model/adapter save and reload, licensing, and multilingual evaluation. Distinguish verified facts from suggestions. Rank fixes as critical/high/medium/low. For each fix, provide exact replacement wording or a small code patch and explain how to verify it. Do not invent scores or claim to have executed training unless you did. Conclude with a five-task improvement plan, including one worked example per phase.

## How to send the feedback back

Paste Claude's review here or save it as `CLAUDE_FEEDBACK.md` in the course folder. We can then verify each claim, update the relevant files, rerun available checks, and publish the next course version.

## Review acceptance checks

- Keeps the required four-part order and English-first structure.
- Fixes actual learner and engineering gaps with concrete examples.
- Makes no unsupported claims that the ML labs ran.
- Separates verified API issues from uncertain version-dependent behavior.
- Maintains local links and reproducible lab setup.
