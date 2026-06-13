# Multi-Language Refactor — Progress Tracker

Tracks the Python → Python+TypeScript refactor. North star: `VISION.md`.
Full plan: `/Users/kittipos/.claude/plans/let-s-tackle-the-refactoring-frolicking-dahl.md`.

Python is the reference idiom; TypeScript is the parallel track (synced `<LangTabs>`).
**Part I (Ch 1–3) stays Python-reference** (process-focused); full parallel from Part II.

## Gates (per chapter)

- [ ] `pnpm build` (repo root) passes
- [ ] `cd examples/chNN/py && uv run --with pytest pytest` green (+ `…/py/exercise` where present)
- [ ] `cd examples && pnpm test chNN` green
- [ ] `cd examples && pnpm typecheck` green (strict, no `any`)

## Phase 0 — Infra + conventions

- [x] `src/components/LangTabs.astro` (syncKey="lang" wrapper)
- [x] `examples/` standalone TS project: `package.json`, `tsconfig.json`, `vitest.config.ts`, `README.md`
- [x] `pnpm install` in `examples/` (vitest + tsx + typescript); lockfile committed
- [x] root `tsconfig.json` excludes `examples`
- [x] this progress tracker created
- [x] `AGENTS.md` updated (Code/Structure rules; Settled Decision 2 note; vitest + label convention)
- [x] `docs/chapter-template.mdx` updated (Before/After `###`+LangTabs; Language Notes; cheat-sheet dual-lang)
- [x] `docs/book-design-software-design-for-humans-and-ai.md` structural sections updated
- [x] `docs/STYLE-SAMPLES.md` — TS exemplars pending note
- [x] Phase 0 gate: `pnpm build` passes; `pnpm -C examples test` + `typecheck` green

**Phase 0 complete** — committed `271e0d0`.

## Phase 1 — Pilot: Ch 13 (Strategy & Template Method)

- [ ] examples/ch13 → `py/` + `ts/` (idiomatic TS twins + vitest tests)
- [ ] MDX: imports, Before/After `###`+LangTabs, Language Notes, 2 cheat sheets dual-lang, paths
- [ ] STYLE-SAMPLES: harvest approved TS voice exemplars
- [ ] All gates green; editor review of rendered page; commit

## Phase 2 — Pattern chapters

- [ ] Ch 11 (Adapter & Façade) — validates multi-pattern Before/After decomposition
- [ ] Ch 10 (Factories & Singleton) — module-level value in both languages

## Phase 3 — Part II principle chapters

- [ ] Ch 5 (Coupling)  ·  [ ] Ch 6 (Encapsulation)  ·  [ ] Ch 7 (Contracts)  ·  [ ] Ch 8 (Extension)
- [ ] Ch 4 (Cohesion & SRP) — multi-module split
- [ ] Ch 9 (Counterweights) — cathedral + exercise subdir

## Part I — Python-reference (no py/ts split)

- [ ] Ch 1, 2, 3 — add a one-line reader note that dual-language begins in Part II

## Notes / decisions

- TS runner: **vitest** (+ tsx). `examples/` is a separate pnpm project from the Astro book.
- `<LangTabs>` labels are exactly **"Python"** then **"TypeScript"** (synced tabs match by label).
- Before/After: sequential `###` subsections, each a `<LangTabs>` (one tab dimension = language).
- "Pythonic Notes" → "Language Notes" (per-language tabs, prose+code).
- Cheat sheets: neutral mermaid/intent/when; per-language Canonical+idiom; dual `Runnable:` paths.
- CI for examples: **deferred** (local gates only; Netlify stays build-only).
