# Multi-Language Refactor — COMPLETE

The Python → (Python + TypeScript) refactor is done. This file is a historical
record; live drafting status lives in `chapters-writing-progress.md`.

## Outcome

- **Infra:** `src/components/LangTabs.astro` (synced `syncKey="lang"`); a standalone
  `examples/` TS project (vitest + tsx + strict tsconfig); conventions recorded in
  `AGENTS.md`, `docs/chapter-template.mdx`, and `docs/STYLE-SAMPLES.md`.
- **Chapters:** all drafted Part II + III chapters (4–11, 13) are dual-language
  (synced `<LangTabs>`, examples split into `examples/chNN/{py,ts}`). Part I (1–3) is
  Python-reference, with an entry note in Ch 1.
- **Gates** (per chapter): `pnpm build` · `examples/chNN/py` pytest ·
  `pnpm -C examples test chNN` · `pnpm -C examples typecheck` (strict, no `any`).
- New chapters are authored **dual-language from the start** (exemplar: Ch 13;
  multi-module case: Ch 4).

## Phase commits

- Phase 0 (infra + conventions): `271e0d0`
- Phase 1 (pilot, Ch 13): `da8dd17`
- Phase 2 (patterns): Ch 11 `4c0f46c` · Ch 10 `cfbd7f1`
- Phase 3 (principles): Ch 5 `2d8fec1` · Ch 6 `79331f4` · Ch 7 `483bd59` ·
  Ch 8 `2903846` · Ch 4 `e7cf982` · Ch 9 `619b199`

Deferred (unchanged): examples CI. Editor-revisit items (TS prose voice, etc.) are
tracked in `chapters-writing-progress.md`.
