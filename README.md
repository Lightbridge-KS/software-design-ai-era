# Software Design for Programmers in era of Agentic Coding

[![Netlify Status](https://api.netlify.com/api/v1/badges/fc2bb3ef-c5c7-498c-8c05-c9667fbc49a8/deploy-status)](https://app.netlify.com/projects/software-design-ai-era/deploys)

> A shared vocabulary for building clean, sustainable codebases — with humans and AI as partners.

An educational book that teaches **codebase-level software design** for the AI-coding
era: how to recognize the patterns an AI agent generates, and how to brainstorm,
judge, and *direct* that agent using the correct, time-tested vocabulary of design
principles and patterns.

**Live site:** https://software-design-ai-era.netlify.app

## The thesis

**Design vocabulary is a communication protocol.** One precise word — "Strategy",
"Adapter", "tell, don't ask" — transmits an entire structural intent, and it is
*shared* between humans and AI agents because both learned it from the same decades of
literature. Two ideas follow:

- **Patterns and principles are the constants; the language is the variable.** Every
  design is shown in **Python** and **TypeScript** side by side — proof that the
  vocabulary, not the syntax, is the portable asset.
- **Right-sizing is the recurring discipline.** Agents' most common design sin is
  over-engineering, so every principle is paired with its over-application failure mode
  and a "when *not* to use".

Scope is **C3–C4 of the C4 model** (components and code) — functions, classes, modules,
packages — not distributed-systems architecture.

## Status

11 / 22 chapters drafted. Part I (Foundations) and Part II (Principles) are complete;
Part III (Patterns) is in progress. See
[`docs/progress-tracking/chapters-writing-progress.md`](docs/progress-tracking/chapters-writing-progress.md).

## Tech stack

- **[Astro](https://astro.build) + [Starlight](https://starlight.astro.build)** — the docs site
- **[astro-mermaid](https://www.npmjs.com/package/astro-mermaid)** — diagrams from fenced ` ```mermaid ` blocks
- **pnpm** · deployed on **Netlify** (static output)
- Runnable examples: **Python** (pytest, via `uv`) and **TypeScript** (vitest + `tsc`)

## Run the book locally

```bash
pnpm install
pnpm dev      # local dev server
pnpm build    # production build to dist/  (the Netlify build gate)
```

## Run the examples

Each chapter's runnable code lives in `examples/chNN/`. From Part II on it is
dual-language: `py/` (Python) and `ts/` (TypeScript).

```bash
# Python — bare-name sibling imports, so run inside the chapter's py/ dir
cd examples/ch13/py && uv run --with pytest pytest

# TypeScript — one standalone project for all ts/ examples
cd examples && pnpm install      # first time only
pnpm test                        # all vitest suites
pnpm typecheck                   # tsc --noEmit (strict, no `any`)
```

## Repository layout

```
src/content/docs/   # the book (MDX), grouped by Part; sidebar in astro.config.mjs
src/components/      # MDX components: LangTabs, AICollab, VocabTable, PromptCard, TryIt, CheatSheet
examples/chNN/       # runnable code per chapter: py/ + ts/
glossary.yaml        # single source of truth for the Appendix A phrasebook
docs/                # design doc, chapter template, style samples, progress trackers
VISION.md            # the project's north star
AGENTS.md            # conventions for AI coding agents working in this repo (CLAUDE.md -> AGENTS.md)
```

## How this book is written

The book is its own case study: it is drafted by an AI coding agent with the human as
**editor-in-chief** (the agent drafts; the human approves, redirects, and has the last
word), following the conventions in [`AGENTS.md`](AGENTS.md) and the north star in
[`VISION.md`](VISION.md).

## License

© 2026 Lightbridge-KS. License TBD.
