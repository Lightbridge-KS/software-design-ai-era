# The Two-Prompt Experiment — Methodology

The outcomes printed in Chapter 1 are real, not authored. This file records how
they were produced, so the experiment is reproducible (and re-runnable as agents
evolve).

## Setup

- **Starter:** `starter/discounts.py` — checkout-lite's discount `if/elif` chain
  (the same code Chapter 10 treats in full).
- **Isolation:** two fresh temporary directories *outside* the book's repository,
  each containing only the identical starter file. No conventions file, no other
  context. The agent's only inputs were the file and one prompt.
- **Agent:** Claude Code 2.1.175, non-interactive (`claude -p`), default model
  (Claude Fable 5), file edits auto-accepted. One run per prompt; outputs taken
  as they came (no cherry-picking among retries).
- **Honest caveat:** the runs used a real developer machine, including that
  developer's global preferences file — which is the realistic condition: this is
  what an ordinary, reasonably configured agent does.

## The two prompts

**Prompt A (vague):**

> Clean up discounts.py and make it more maintainable. Edit the file in place.

**Prompt B (design vocabulary):**

> Refactor apply_discount in discounts.py to the Strategy pattern using functions
> as strategies and a registry dict. Keep the public function signature
> unchanged. Do not introduce new classes or dependencies. Edit the file in
> place.

## Results

- `outcome-a/discounts.py` — the file after Prompt A, verbatim
- `outcome-a/response.md` — the agent's reply, verbatim
- `outcome-b/discounts.py` — the file after Prompt B, verbatim
- `outcome-b/response.md` — the agent's reply, verbatim

The chapter may trim listings for length; trims are marked with `[…]`. Nothing
else is edited.
