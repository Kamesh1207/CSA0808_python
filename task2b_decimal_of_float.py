"""Task 2 follow-up: change Decimal(amount) to Decimal(float(amount))
and explain the new result."""

from decimal import Decimal

payments = ["33.40"] * 1000 + ["0.10"] * 3

total = Decimal("0.00")
for amount in payments:
    total += Decimal(float(amount))    # <-- float conversion sneaks back in

print("Decimal(float(amount)):", total)

# EXPLANATION
# float(amount) first converts "33.40" to the binary float 33.4, which
# cannot be stored exactly (it is really 33.399999999999998578...).
# Decimal(float) then wraps that INEXACT binary value in a Decimal - the
# error is frozen into the Decimal. Adding 1003 such values brings the
# hidden error back, so the total is no longer exactly 33400.30.
# Rule: build Decimals from STRINGS (base-10), never from floats.
