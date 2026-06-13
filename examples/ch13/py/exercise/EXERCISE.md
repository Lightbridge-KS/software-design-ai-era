# Chapter 10 Exercise · Strategy, Right-Sized

**Starter:** `shipping.py` — a shipping-cost function with an `if/elif` chain over
four carrier options.

## Steps

1. Give your agent `shipping.py` and the **"Strategy, right-sized"** prompt from
   the chapter, with the names adapted:

   > This module selects a shipping cost with an `if/elif` chain on `carrier`.
   > Refactor to the **Strategy pattern using functions as strategies** and a
   > registry dict. Keep `shipping_cost`'s public signature unchanged. Do **not**
   > introduce classes, new dependencies, or new modules. Show the diff and
   > explain the trade-off in two sentences.

2. Grade the output with the chapter's review checklist:

   - [ ] `shipping_cost`'s public signature unchanged
   - [ ] Each carrier strategy testable alone — no dispatch needed in its tests
   - [ ] The registry is the only growth point: new carrier = one function + one entry
   - [ ] No ABC, no classes (the prompt forbade them — did the agent comply?)
   - [ ] The old `if/elif` chain is *deleted*, not duplicated alongside the registry

3. Two questions worth answering as you review:
   - Which carrier option was the **hardest** to turn into a pure function, and why?
     (Hint: look at which branches read more than one field of `Shipment`.)
   - Did the agent try to build **more** than the prompt allowed — an enum, a
     config file, a renamed function? That's the over-engineering reflex Chapter 9
     teaches you to brake.

## Stretch

Ask your agent: *"A fifth option, `drone`, is only available under 2 kg — where
does that constraint belong?"* There is more than one defensible answer; what
matters is whether the agent (and you) can articulate the trade-off.
