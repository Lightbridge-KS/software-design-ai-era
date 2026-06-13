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

- [x] examples/ch13 → `py/` (14 pytest) + `ts/` (14 vitest, tsc strict, exercise/) 
- [x] MDX: imports, Before/After `###`+`####`/LangTabs, Language Notes, 2 cheat sheets dual-lang, paths
- [x] STYLE-SAMPLES: harvested approved TS voice (Excerpt 5)
- [x] All gates green; editor-reviewed; committed

**Phase 1 complete.** Pilot locked the pattern: synced `<LangTabs>`, `####` Before/After
for paired-pattern chapters, dual-language cheat sheets, `examples/chNN/{py,ts}` split.

## Phase 2 — Pattern chapters

- [x] Ch 11 (Adapter & Façade) — `###`/`####` decomposition, dual cheat sheets — committed `4c0f46c`
- [x] Ch 10 (Factories & Singleton) — bilingual demoted Singleton — committed `cfbd7f1`

## Phase 3 — Part II principle chapters

- [x] Ch 5 (Coupling) `2d8fec1` · [x] Ch 6 (Encapsulation) `79331f4` · [x] Ch 7 (Contracts) `483bd59` · [x] Ch 8 (Extension) `2903846`
- [x] Ch 4 (Cohesion & SRP) — multi-module split; first dual-language chapter (intro aside) — `e7cf982`
- [x] Ch 9 (Counterweights) — cathedral + exercise subdir — `619b199`

**Phase 3 complete.**

## Part I — Python-reference (no py/ts split)

- [x] Ch 1 carries the reader note ("Part I is Python; dual-language from Part II"). Ch 2, 3 unchanged (one note at the entry point suffices).

## Next up (new drafting, not refactor)

Drafted so far: Ch 1–11, 13. **Stubs remaining:** Ch 12 (Composite & Decorator),
14 (Observer & State), 15 (Iterator & Visitor); Part IV (16–18); Part V (19–22).
**Next:** draft **Ch 12** — a Part III pattern chapter, authored **dual-language
from the start** (follow the Ch 13 exemplar + AGENTS.md rules; per-chapter loop:
brief → editor approval → draft → gates → commit). Editorial revisit items
(editor): TS prose voice in Language Notes tabs; Ch 9 EXERCISE.md (Python-only);
intro-aside redundancy across Ch 1/4/13; pin external citations.

## Multi-language refactor status: COMPLETE

All Part II + III drafted chapters (4–11, 13) are dual-language; Part I (1–3) is
Python-reference with the entry note. Gates per chapter: `pnpm build` ·
`examples/chNN/py` pytest · `pnpm -C examples test chNN` · `pnpm -C examples typecheck`.
Deferred (unchanged): examples CI; the TS-voice review (editor to revisit prose).

## Notes / decisions

- TS runner: **vitest** (+ tsx). `examples/` is a separate pnpm project from the Astro book.
- `<LangTabs>` labels are exactly **"Python"** then **"TypeScript"** (synced tabs match by label).
- Before/After: sequential `###` subsections, each a `<LangTabs>` (one tab dimension = language).
- "Pythonic Notes" → "Language Notes" (per-language tabs, prose+code).
- Cheat sheets: neutral mermaid/intent/when; per-language Canonical+idiom; dual `Runnable:` paths.
- CI for examples: **deferred** (local gates only; Netlify stays build-only).
