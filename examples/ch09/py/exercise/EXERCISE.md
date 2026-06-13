# Chapter 9 Exercise · The De-Engineering Audit

**Starter:** `settings.py` — a provider interface, a provider chain, a factory,
and a cached singleton, in service of three values with defaults.
**Contract:** `test_settings.py` — pins defaults, environment override, types,
and immutability, through the public `get_settings()` API only.

This exercise is inverted: success is measured in lines *deleted*.

## Steps

1. Verify the starting point: `uv run --with pytest pytest -q .` — 4 tests pass.

2. Give your agent `settings.py` and the **de-engineering audit** prompt from the
   chapter:

   > Review this module for over-engineering: interfaces with one implementation,
   > layers that only forward, DTOs that mirror entities, factories with one
   > product, a config system for constants. Propose the **simplest equivalent
   > that keeps behavior identical** — the existing tests must stay green. Show
   > what gets deleted, and report the line count before and after.

3. Run the tests against the agent's version. Green is non-negotiable.

4. Grade with the chapter's review checklist:

   - [ ] Every surviving abstraction has ≥2 users today
   - [ ] No layer that only forwards (is the provider chain gone?)
   - [ ] Well over half the lines are gone
   - [ ] `get_settings()` survived — the brake never deletes the public API
   - [ ] The tests were not modified to make life easier

5. Questions worth answering as you review:
   - The tests deliberately pin *behavior*, not *structure*. Which classes did
     that free your agent to delete? What would have happened if a test had
     asserted `isinstance(provider, ChainedSettingsProvider)`?
   - Did the agent keep the singleton cache? `get_settings()` is called a handful
     of times per process on three environment variables — what evidence would
     justify caching?
   - Each deleted class speculated about a future (files, vaults, services).
     What *evidence* would have to appear in this project before any of them
     earns its way back in?

## Stretch

Tell your agent: *"Settings may soon also come from a `settings.toml` file —
product has confirmed it for next quarter."* That is **evidence**, not
speculation. Where does the design land now — and is it the cathedral, or
something smaller that still honors the new requirement?
