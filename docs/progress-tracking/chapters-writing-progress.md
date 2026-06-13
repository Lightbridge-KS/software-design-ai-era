# Chapter Writing Progress

Drafting status for every chapter + appendix.

**Legend:** ✅ drafted · 🚧 in progress · ⬜ stub (frontmatter + TODO only)
**Languages:** PY = Python-reference (Part I) · PY+TS = dual-language (synced `<LangTabs>`)
**Done =** `pnpm build` green · `examples/chNN/py` pytest green · (PY+TS:)
`pnpm -C examples test chNN` + `pnpm -C examples typecheck` green · glossary rows added.

New chapters are authored **dual-language from the start** (exemplar: Ch 13; multi-module
case: Ch 4). Per-chapter loop: brief → editor approval → draft → gates → commit.

## Part I — Foundations  (Python-reference)

| Ch | Title | Status | Lang |
|----|-------|--------|------|
| 1 | Design Is Communication | ✅ | PY |
| 2 | The Two Enemies: Change and Complexity | ✅ | PY |
| 3 | The Design Loop with an AI Partner | ✅ | PY |

## Part II — Principles

| Ch | Title | Status | Lang |
|----|-------|--------|------|
| 4 | Cohesion and the Single Responsibility Principle | ✅ | PY+TS |
| 5 | Coupling and the Principle of Least Knowledge | ✅ | PY+TS |
| 6 | Encapsulation and Information Hiding | ✅ | PY+TS |
| 7 | No Surprises: Least Astonishment and Contracts | ✅ | PY+TS |
| 8 | Extension Without Modification | ✅ | PY+TS |
| 9 | The Counterweights: YAGNI, KISS, and Right-Sizing | ✅ | PY+TS |

## Part III — Patterns  (GoF triad)

| Ch | Title | Family | Status | Lang |
|----|-------|--------|--------|------|
| 10 | Factories and Singleton | Creational | ✅ | PY+TS |
| 11 | Adapter and Façade | Structural | ✅ | PY+TS |
| 12 | Composite and Decorator | Structural | ✅ | PY+TS |
| 13 | Strategy and Template Method | Behavioral | ✅ | PY+TS |
| 14 | Observer and State | Behavioral | ✅ | PY+TS |
| 15 | Iterator and Visitor | Behavioral | ✅ | PY+TS |

## Part IV — Codebase Design

| Ch | Title | Status | Lang |
|----|-------|--------|------|
| 16 | Modules and Packages as Design Units | ⬜ | — |
| 17 | Dependency Direction and the Three Tiers | ⬜ | — |
| 18 | Tests as Executable Design Contracts | ⬜ | — |

## Part V — Designing with an AI Partner

| Ch | Title | Status | Lang |
|----|-------|--------|------|
| 19 | The Prompt Phrasebook | ⬜ | — |
| 20 | Encoding Conventions: AGENTS.md and Skills | ⬜ | — |
| 21 | Reviewing AI-Generated Code Through Design Lenses | ⬜ | — |
| 22 | Refactoring as a Dialogue | ⬜ | — |

## Appendices

| App | Title | Status |
|-----|-------|--------|
| A | The Design Glossary-Phrasebook (renders from `glossary.yaml`) | ⬜ |
| B | Prompt Template Library | ⬜ |
| C | Mermaid Cookbook for Design Docs | ⬜ |
| D | Building This Book (Astro Starlight setup) | ⬜ |

## Summary

- **Drafted: 14 / 22 chapters** (Part I complete · Part II complete · Part III complete 6/6).
- **Next:** Part IV (16–18) → Part V (19–22) → appendices.
- Writing order to date: 13 → 9 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 10 → 11
  (then the multi-language refactor) → 12 → 14 → 15. Appendix A assembles from `glossary.yaml`.

## Open editorial items (editor revisit)

- TypeScript prose voice across the new Language Notes tabs.
- Ch 9 `EXERCISE.md` still documents only the Python flow.
- "Two languages" intro framing appears in Ch 1, 4, and 13 — reconcile redundancy.
- Pin external citations before publication (harness engineering · parse-don't-validate
  · Ousterhout) — see memory `external-citations-to-pin`.
