# checkout-lite examples

Runnable code for the book's chapters. From Part II (Chapter 4) onward each chapter
is **multi-language**: its examples live in two sibling folders.

```
examples/chNN/
├── py/     # Python (reference idiom) — pytest, run with the dir as cwd
│   ├── before.py  after.py  models.py  test_chNN.py ...
│   └── exercise/  (some chapters)
└── ts/     # TypeScript — vitest, relative sibling imports
    ├── before.ts  after.ts  models.ts  chNN.test.ts ...
    └── exercise/  (some chapters)
```

Part I (Chapters 1–3) is Python-reference only and keeps a flat layout.

## Running the gates

**Python** (per chapter — bare-name sibling imports, so run inside the `py/` dir):

```bash
cd examples/ch13/py && uv run --with pytest pytest
# exercise subdirs (ch09, ch13):
cd examples/ch13/py/exercise && uv run --with pytest pytest
```

**TypeScript** (one standalone pnpm project for all `ts/` examples):

```bash
cd examples            # first time only:
pnpm install
pnpm test              # all ts/ tests (vitest)
pnpm test ch13         # one chapter
pnpm typecheck         # tsc --noEmit, strict, no `any`
```

This `examples/` project is intentionally separate from the Astro book at the repo
root — its dev-dependencies (vitest, tsx, typescript) never touch the site build.
