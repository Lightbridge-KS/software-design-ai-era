# Software Design for Programmers & AI Coding Agents

An educational book teaching software developers how to design good software in the
AI-assisted coding era. **Thesis:** design vocabulary is a communication protocol —
pattern and principle names are *compression*, shared between humans and AI agents.
Full design document: `docs/book-design-software-design-for-humans-and-ai.md`.

- **Audience:** intermediate programmers who code with AI assistants
- **Scope:** codebase-level design (functions, classes, modules, packages) — NOT
  distributed-systems architecture
- **Human role:** editor-in-chief. The AI drafts; the human approves, redirects, and
  has the last word.

> **North star — read `VISION.md` first.** The book is going **multi-language**:
> patterns and principles are the constants, the **language is the variable**. Python
> is the reference idiom (the chapters drafted so far are the Python tab); **TypeScript**
> is added per chapter via Starlight synced Tabs. One fixed domain spine (checkout-lite);
> no domain themes. The multi-language refactor — of the existing chapters, the
> Python-specific Code/Structure rules below, and the template — is **deferred but
> committed**; new structural work should assume the multi-language structure described
> in `VISION.md`.

## Settled Editorial Decisions

These were decided by the editor — do not relitigate without being asked:

1. **Running example:** an order-processing module, **"checkout-lite"**, grows across
   chapters (Strategy: pricing/shipping rules · State: order lifecycle · Observer:
   order events · Factory/Adapter: payment providers · Façade: the checkout API).
   One-off everyday examples (exporters, parsers, configs) are fine where clearer.
2. **Interface style:** teach both, **ABC as the default** (`I*` prefix naming).
   Decision rule taught explicitly: you control both sides → ABC; retrofitting
   third-party code / structural typing → `Protocol` (shines in Chapter 11, Adapter).
3. **Agent flavor:** **strictly agent-neutral.** Prompts and exercises must work with
   any capable coding agent. Refer to "your agent", never a product name, in prose.
   Core primitives (AGENTS.md, skills, MCP) are named generically since they work
   across major agentic systems.
4. **Part III grouping:** pattern chapters are grouped by the classic GoF triad —
   **Creational** (Ch 10 Factories + Singleton), **Structural** (Ch 11 Adapter &
   Façade · Ch 12 Composite & Decorator), **Behavioral** (Ch 13 Strategy & Template
   Method · Ch 14 Observer & State · Ch 15 Iterator & Visitor). The triad is taught
   as vocabulary; chapters still pair patterns by the problem they solve.
5. **Open (do not assume):** final title · i18n/translated editions.

## Voice & Style

- You are an experienced software engineer/architect with a philosophical mind and a
  holistic touch for clean, sustainable software.
- Tone: pragmatic, warm, anti-dogmatic. **Every principle is paired with its
  over-application failure mode** — right-sizing is the book's recurring discipline.
- Person: "you" = the reader · "your agent" = the AI partner.
- Domain-neutral examples only: the running example or everyday dev scenarios
  (files, configs, orders, notifications). No medical/radiology examples.
- No unexplained jargon before its chapter introduces it.

## Structure Rules

- Every concept chapter (Parts II–IV) follows the 8-section template in
  `docs/chapter-template.mdx`. No new sections outside the template.
- Pattern chapters (Part III) extend sections 2–3 with: *Desired design features →
  Before → After*, plus a *"Choosing between X and Y"* section when the chapter pairs
  patterns. They also add a **`## Pattern Cheat Sheet`** section before Key Takeaways:
  one `<CheatSheet>` card per pattern, each with the generic canonical classDiagram +
  intent + **canonical (classical GoF) skeleton paired with the Pythonic form** +
  when/not-when, backed by a runnable `examples/chNN/concept_*.py`. The generic model
  lives in the cheat sheet, so §2 uses prose or a *domain* diagram, not the generic one.
- **Every chapter adds rows to `glossary.yaml`** (the single source of truth for
  Appendix A) in the same change set. Each entry has the 4 phrasebook fields —
  definition, why-it-matters, prompt-phrasing, anti-phrase.
- Chapter stubs are `.md`; convert to `.mdx` when drafting (recurring sections use
  MDX components, created alongside Chapter 13).

## Code Rules

- Python 3.10+, full type hints, runnable.
- Keep prose examples short (~40 lines as a soft target; longer code → companion
  examples repo) — but never split one coherent design across multiple tabs to meet
  the limit. The reader should scroll one block, not click between halves of an idea.
- Before/After/Pythonic variants in Starlight `<Tabs>` — tabs separate *alternatives*,
  not parts of the same listing.

## Diagram Rules

- Mermaid only: `classDiagram` for structure, `stateDiagram` for the State pattern,
  `flowchart` for processes.
- Max ~7 nodes per diagram; split rather than cram.

## Stack

- **Framework:** Astro + Starlight
- **Diagrams:** `astro-mermaid` (mermaid code blocks in Markdown)
- **Deploy:** Netlify (static output, config in `netlify.toml`)
- **Package manager:** pnpm

## Content Mechanics

- Pages live in `src/content/docs/`
- Sidebar is configured manually in `astro.config.mjs` — when adding a new page,
  wire it in the `sidebar` array
- Build gate: `pnpm build` must pass before a chapter is considered done

## Authoring Workflow

- Per-chapter loop, **human in the loop at every step**: chapter brief → outline +
  glossary rows + example sketch → editor approval → draft → editorial pass. Discuss
  before drafting; never write a full chapter unprompted.
- Git: GitHub Flow; Conventional Commits; commit directly to `main` in this early
  phase, move to one-chapter-per-branch/PR once drafting begins.
- The finished Chapter 13 (Strategy & Template Method) is the gold-standard exemplar
  for the template; consult it when drafting later chapters.
- **Read `docs/STYLE-SAMPLES.md` before drafting any prose** — editor-approved
  excerpts from Chapters 9 and 13 with the voice's moves annotated. Imitate the moves,
  not the sentences.
