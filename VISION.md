# Vision — *Software Design for Programmers & AI Coding Agents*

> This is the north-star document. It states what the book is, who it's for, and the
> one structural commitment that shapes everything: **the book is multi-language.**
> Implementation details (template, refactor plan) follow from this; they live
> elsewhere and may change. The vision should not.

## Mission

Teach software developers, in the AI-coding era, the fundamentals of **codebase-level
software design** — so they can recognize the patterns an AI agent generates, and
brainstorm, judge, and *direct* that agent using the correct, time-tested vocabulary
of design principles and patterns.

The human's job has shifted from typing code to **judging and guiding** it. This book
supplies the shared language that makes that guidance precise.

## Audience

Intermediate developers who code *with* AI assistants and want to direct them with
precision — across whatever language and stack they work in.

## Scope (in C4 terms)

The book lives at **C3 (Component) and C4 (Code)** of the C4 model — functions,
classes, modules, packages, and the relationships among them. It deliberately does
**not** cover C1–C2 (System Context, Containers): distributed-systems architecture,
deployment, scaling, and infrastructure are out of scope and have their own
literature. Our territory is the code a team reads and changes every day.

## The Thesis (extended)

The book's original claim: **design vocabulary is a communication protocol** — one
precise word ("Strategy", "Adapter", "tell, don't ask") transmits an entire
structural intent, and it is *shared* between humans and AI agents because both
learned it from the same decades of literature.

The extension that defines this book's structure:

> **Patterns and principles are the constants. The programming language is the
> variable.** Design vocabulary is language-portable — and this book *proves* it by
> realizing the same design in more than one language, rather than merely asserting
> portability.

A reader who sees the *same* Strategy, the *same* dependency diagram, the *same*
"when not to use", expressed idiomatically in two languages, internalizes the truth
the book sells: **the design is the invariant; the syntax is just the coordinate
system.**

## The Two Axes — and how each is handled

The book could vary along two axes: **language** and **domain**. They are not equal in
cost or value, so they are handled deliberately differently.

### Language axis — FULL parallel (the structural commitment)

- **Languages:** **Python** (reference idiom) and **TypeScript** now; more may be
  added later (e.g. Rust, Go, C#). Each language's own idioms and culture are
  preserved and celebrated — *Pythonic* deflation, *idiomatic TS* structural typing,
  and so on. We do not flatten to lowest-common-denominator OOP.
- **Why TS first alongside Python:** it is the dominant language of AI-assisted
  development today, and its *contrasts* with Python are pedagogically rich — most of
  all, Python forces a choice between nominal (`ABC`) and structural (`Protocol`)
  typing, while TypeScript is structural *by default*. The same pattern gains a second
  voice.
- **Mechanism:** Starlight **synced tabs** (`syncKey="lang"`) — the reader picks
  "TypeScript" once and it persists across the whole book. Native, low-friction.
- **What this proves:** that the vocabulary, not the syntax, is the portable asset —
  the book's thesis, demonstrated on every page that has code.

### Domain axis — ONE spine, held fixed

- **Decision:** a single running example — **"checkout-lite", an order-processing
  pipeline** (intake → price → pay → notify → persist) — grows across the entire book.
  No domain themes, no per-industry parallel narratives, **no domain-lens callouts.**
- **Why one spine:** the running example's power is *accumulation* — the Ch. 2 tangle
  becomes the Ch. 4 split becomes the Ch. 8 gateways becomes the Ch. 10 factory
  becomes the Ch. 11 adapter/façade. The reader builds *one* evolving mental model.
  Parallel per-domain stories would fork that effort, multiply combinatorially against
  the language axis, and — most importantly — *undercut the thesis*: the skill being
  taught is to recognize checkout-lite's Strategy in your *own* logistics or
  healthcare pipeline. **Cross-domain transfer is the lesson, not a feature to
  pre-chew.**
- **Why commerce:** order-processing is the one domain every reader already
  understands, and it naturally exercises every pattern (Strategy = pricing · State =
  order lifecycle · Observer = order events · Factory/Adapter = payment providers ·
  Façade = the checkout API).
- **Deferred, not rejected:** a future edition *could* add more domains behind a
  reader-facing **domain switcher** — but only with a real investment in the mechanism
  (the reader switches domain easily, and the narrative still flows smoothly within
  each one), never a cosmetic reskin. Out of scope now to keep cost linear and the
  single accumulating spine intact.

## What this changes structurally

(Consequences of the language axis; details to be finalized in the template/refactor.)

- **Prose goes language-neutral where the idea is universal.** The *concept*, the
  *Mermaid diagram*, *Before/After as structure*, *When NOT to Use*, *Key Takeaways*,
  and the entire *🤖 AI Collaboration* vocabulary are language-agnostic — a Strategy is
  a Strategy.
- **"Pythonic Notes" → "Language Notes."** The idiom section splits into per-language
  tabs (Pythonic | TypeScript), each carrying that language's specific moves, caveats,
  and culture. This is where language-specific nuance lives.
- **Before/After code uses synced `<Tabs>`** keyed by language. The *deflation move*
  survives and generalizes: classical class-heavy form → the idiomatic form *your
  language* prefers (Python functions + registry; TS functions + record/union; etc.).
- **Pattern Cheat Sheets** keep the canonical (classical) skeleton + UML
  language-neutral, and show the idiomatic form per language.
- **Examples split by language:** `examples/chNN/py/` and `examples/chNN/ts/`, each
  runnable and tested in its own toolchain (pytest; vitest/jest + tsc). Both are gates.
- **Voice:** the warm, pragmatic, anti-dogmatic register holds in the neutral prose;
  each language's Notes carry that language's idiom honestly. `STYLE-SAMPLES.md` will
  need TypeScript exemplars alongside the Python ones.

## What stays the same

- The **mission, audience, scope, and thesis** (now extended, not replaced).
- The **8-section chapter template**, the **GoF triad** grouping of Part III, the
  **cheat-sheet** reference cards, the **glossary-as-single-source** discipline, and
  every settled editorial decision in `AGENTS.md` except those the language axis
  forces (Pythonic Notes → Language Notes; examples layout).
- The **running example** (checkout-lite) and its chapter-by-chapter accumulation.
- **Right-sizing** as the recurring discipline; every principle paired with its
  over-application failure mode.


## Non-goals

- Distributed-systems / infrastructure architecture (C1–C2). Out of scope.
- Multiple parallel domain narratives or a domain switcher **for now** — deferred
  until the switching mechanism is worth building (see the Domain axis), not a
  near-term goal.
- Exhaustive language coverage. Two languages now; add more only when the contrast
  earns its keep.
- Teaching the languages themselves. The reader knows their language; we teach design.
