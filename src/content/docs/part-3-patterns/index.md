---
title: "Part III - Patterns"
description: "A curated, Pythonic phrasebook of design patterns, grouped by the classic Creational / Structural / Behavioral triad."
---

Part II gave you the grammar of design. Part III gives you the phrasebook: named
patterns, each a crystallized application of those principles (Chapter 8 already
hinted that the patterns *are* the principles, named). Knowing a pattern's name is
leverage — it is the compression that lets you ask your agent for an entire structure
in three words, and the shared vocabulary that lets it answer precisely.

## The three families

The patterns sort into the three families the literature has used since the
Gang of Four — themselves a piece of vocabulary worth owning, because naming the
family is itself compression ("I need a structural pattern to make these two
interfaces fit"):

- **Creational** — patterns about *making objects*: who decides which concrete type
  to build, and how. (Chapter 10: Factories, and the demoted Singleton.)
- **Structural** — patterns about *composing objects* into larger shapes without
  rigid coupling. (Chapter 11: Adapter & Façade · Chapter 12: Composite & Decorator.)
- **Behavioral** — patterns about *assigning responsibility* and coordinating how
  objects collaborate. (Chapter 13: Strategy & Template Method · Chapter 14:
  Observer & State · Chapter 15: Iterator & Visitor.)

| Family | Chapter | Patterns |
|---|---|---|
| Creational | 10 | Factory function · Factory Method · Abstract Factory · Singleton (demoted) |
| Structural | 11 | Adapter · Façade |
| Structural | 12 | Composite · Decorator |
| Behavioral | 13 | Strategy · Template Method |
| Behavioral | 14 | Observer · State |
| Behavioral | 15 | Iterator · Visitor |

## How these chapters are organized

Within each family we pair patterns by the *problem they solve*, so you meet
alternatives side by side — Strategy next to Template Method, Adapter next to Façade —
and learn to choose, not just to apply. Every pattern is taught Pythonic-first: the
classical class-based form, then the lighter form Python's functions, protocols,
generators, and `match` often make better, then the decision rule for which to reach
for. And every pattern carries its counterweight — the over-application failure mode
this book never lets out of its sight.
