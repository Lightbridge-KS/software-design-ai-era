"""Chapter 2 · Change amplification, made literal.

One requirement arrives: "We're expanding to Canada (country code CA)."
Watch how many places in checkout() must change — and, worse, how one place
changes *silently* without anyone deciding it should.

Run: `python demonstrate_amplification.py`
"""

from models import Customer, LineItem, Order
import checkout_tangle


def main() -> None:
    canada_order = Order(
        customer=Customer("Marie", "marie@example.ca"),
        items=[LineItem("notebook", 20.00)],
        country="CA",
    )

    print("Requirement: support Canada (CA).")
    print("Edit sites a developer must find and reason about:\n")
    print("  1. tax branch     — no CA case exists; CA is charged 0% tax.")
    print("                       Is that legal? Nobody decided it. (unknown unknown)")
    print("  2. shipping branch — CA is not US, not in (DE, FR, NL), so it")
    print("                       falls through to the `else`: 24.90.")
    print("                       A neighbor charged the rest-of-world rate,")
    print("                       silently, with no line of code naming Canada.\n")

    total = checkout_tangle.checkout(canada_order, "tok_demo", send_email=False)
    print(f"  Computed total for a 20.00 Canadian order: {total:.2f}")
    print("  (20.00 subtotal + 0.00 tax + 24.90 shipping — both probably wrong.)\n")

    print("Two edit sites for one requirement is change amplification.")
    print("The silent `else` that priced Canada without being asked is an")
    print("unknown unknown — the symptom you cannot grep for.")


if __name__ == "__main__":
    main()
