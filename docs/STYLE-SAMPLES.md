# STYLE-SAMPLES — The Book's Voice Reference

Purpose: cross-session consistency (design doc §8.3). Chapters 9 and 10 were
approved by the editor as the voice standard ("very high-yield and insightful —
keep this tone"). This file holds verbatim excerpts with annotations naming the
*moves* they make. When drafting, imitate the moves, not the sentences.

## The register, distilled

- **Scene before concept.** The reader feels the itch in a concrete scenario
  before hearing any name for it. Definitions come second and in plain words.
- **Earned aphorisms.** Sections close on one compressed, quotable sentence that
  the preceding paragraphs paid for — never an unearned slogan, never a summary
  list in place of a landing.
- **The deflation move.** Classical form first (it's what agents produce), then
  the Pythonic collapse, then the rule for choosing. Respect the ceremony before
  removing it.
- **Anti-dogmatic symmetry.** Every strength is shown with its failure mode —
  including the failure modes of the book's own advice.
- **Warm, dry, unsentimental.** Humor is rare, deadpan, and structural ("a module
  wearing a costume"). No hype, no exclamation marks, no "simply"/"just"
  condescension, no breathless transitions.
- **Second person, two actors.** "You" is the reader and has the judgment; "your
  agent" is the capable, eager partner whose output needs sizing. The agent is
  never mocked and never trusted blindly.
- **Code commentary points, never paraphrases.** After a listing, name the one
  load-bearing detail ("the arrow worth staring at is the diamond"), don't
  re-narrate the code.

## Excerpt 1 · The Itch register

> Marketing is happy with checkout-lite, which is the problem. Last quarter they
> asked for a percentage discount. Then a fixed coupon. Then a member rate. Each
> request was "just one more case", and now the pricing function looks like this:
>
> […]
>
> The algorithm isn't the problem. The problem is that *several* algorithms are
> trapped in one body.

— Chapter 10, *The Itch*

**Moves:** opens mid-story with a small reversal (happy customer = problem);
change requests arrive as narrative beats, not requirements lists; closes on the
diagnosis compressed into one image ("trapped in one body") that the rest of the
chapter can reuse as shorthand.

## Excerpt 2 · The deflation reveal

> You have been using this pattern for years: `sorted(names, key=str.lower)` is
> the Strategy pattern — an algorithm passed in as a value. The stdlib's whole
> `key=` convention is strategies all the way down.

— Chapter 10, *Pythonic Notes*

**Moves:** dignifies the reader's existing experience instead of teaching down to
it; the pattern is revealed as something already known, which makes the vocabulary
feel like naming, not learning; ends on a dry allusion, unexplained.

## Excerpt 3 · The counterweight register

> There is no principle whose maximum is its optimum. Good design is not applying
> principles hard; it is balancing forces for *this* codebase, at *this* point in
> its life.

> The agent isn't wrong about *how*. It's wrong about *how much*.

— Chapter 9, *The Concept* and *The Itch*

**Moves:** the book's philosophical spine stated as parallel constructions short
enough to quote at an agent; criticism of the agent is precise and fair — its
competence is conceded in the same breath as its miscalibration.

## Excerpt 4 · Speculation vs. evidence

> "We might need another storage backend someday" is speculation; delete the
> interface. "Marketing has requested four discount rules in two quarters" is
> evidence; build the seam. YAGNI forbids the first and *demands* the second.

> Duplication is a debt you can see and repay any time. The wrong abstraction is a
> debt that compounds while telling you it's an asset.

— Chapter 9, *YAGNI: the case against speculation*

**Moves:** a fuzzy judgment call is converted into a sharp test with paired
examples the reader can pattern-match against; the financial metaphor is extended
one honest step, then dropped before it becomes a gimmick.

## What this voice does not do

- No section that is only bullets — bullets serve prose, not the reverse.
- No unexplained jargon before its chapter; forward references are pointers
  ("Chapter 17 shows how"), not dependencies.
- No hedging filler ("it could be argued", "in some cases") — judgments are made,
  with their limits stated plainly.
- No marketing register: nothing is "powerful", "elegant", or "game-changing".
- No moralizing at the reader; the failure modes belong to all of us, agent and
  human alike.
