"""Task 2 - Complete the Code: exact money totals with Decimal."""
from decimal import Decimal

# 1,000 payments of Rs 33.40 and three small adjustments of Rs 0.10
payments = ["33.40"] * 1000 + ["0.10"] * 3


def total_float(items):
    """Naive float total - accumulates binary rounding error."""
    total = 0.0
    for amount in items:
        total += float(amount)
    return total


def total_decimal(items):
    """TODO 1: Add the amounts exactly by creating a Decimal from each
    string, and return the Decimal total."""
    total = Decimal("0.00")
    for amount in items:
        total += Decimal(amount)     # Decimal(str) is EXACT (base-10)
    return total


print("float  :", total_float(payments))
print("Decimal:", total_decimal(payments))
print(0.1 + 0.2 == 0.3, Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))

# Expected output:
# float  : 33400.30000000061
# Decimal: 33400.30
# False True
