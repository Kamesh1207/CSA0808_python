"""Task 9 - Implement and Test the Milk Payment Calculator.

Run:  python3 task9_calculator.py
Prints a test table (expected vs actual) and passes all assert checks.
The interactive keyboard version is in main() at the bottom."""

FAT_STANDARD, SNF_STANDARD, STEP = 3.5, 8.5, 0.1
BASE_RATE, FAT_STEP_VALUE, SNF_STEP_VALUE = 30.00, 0.40, 0.30
FAT_MIN, FAT_MAX = 2.0, 7.0
SNF_MIN, SNF_MAX = 6.0, 9.5          # assumed instrument limits


def read_number(text):
    """Convert clerk text to float; return None when invalid."""
    text = text.strip().replace(",", ".")
    if not text.replace(".", "", 1).replace("-", "", 1).isdigit():
        return None
    return float(text)


def valid_entry(litres, fat, snf):
    """Return (True, 'ok') or (False, reason) for one entry."""
    if litres is None or litres <= 0:
        return False, "quantity must be positive"
    if fat is None or not (FAT_MIN <= fat <= FAT_MAX):
        return False, f"fat outside {FAT_MIN}-{FAT_MAX}"
    if snf is None or not (SNF_MIN <= snf <= SNF_MAX):
        return False, f"snf outside {SNF_MIN}-{SNF_MAX}"
    return True, "ok"


def rate_per_litre(fat, snf):
    """Return the price per litre (Rs, 2 dp)."""
    fat_steps = round((fat - FAT_STANDARD) / STEP)
    snf_steps = round((snf - SNF_STANDARD) / STEP)
    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
    return round(rate, 2)


def payout(litres, fat, snf):
    """Return the amount payable (Rs, 2 dp) for one valid entry."""
    return round(litres * rate_per_litre(fat, snf), 2)


def ten_day_total(payments):
    """Return the ten-day total (Rs, 2 dp) for a list of payments."""
    return round(sum(payments), 2)


# ---------------------------------------------------------------- tests
def run_tests():
    """Test table: normal, boundary, invalid and a hand-calculated total."""
    cases = [
        # (case, litres, fat, snf, expected payout or None if rejected)
        ("normal, at standard",  10,  3.5, 8.5, 300.00),
        ("normal, above std",    8.5, 4.2, 8.7, 283.90),
        ("normal, below std",    12,  3.1, 8.3, 333.60),
        ("boundary: lowest fat", 5,   2.0, 8.5, 120.00),
        ("boundary: highest fat",7,   7.0, 9.0, 318.50),
        ("invalid: text qty",    None,4.0, 8.5, "rejected"),
        ("invalid: negative qty",-3,  4.0, 8.5, "rejected"),
        ("invalid: fat 8.0",     10,  8.0, 8.5, "rejected"),
        ("invalid: snf 5.0",     10,  4.0, 5.0, "rejected"),
    ]

    print(f"{'case':22} {'input (L, fat, snf)':22} "
          f"{'expected':>9} {'actual':>9}  result")
    for name, l, f, s, expected in cases:
        ok, reason = valid_entry(l, f, s)
        actual = payout(l, f, s) if ok else "rejected"
        status = "PASS" if actual == expected else "FAIL"
        print(f"{name:22} {str((l, f, s)):22} "
              f"{expected!s:>9} {actual!s:>9}  {status}")
        assert actual == expected, (name, actual, expected)

    # hand-calculated 5-entry set (worked out on paper):
    # 300.00 + 283.90 + 333.60 + 120.00 + 318.50 = 1356.00
    five = [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3),
            (5, 2.0, 8.5), (7, 7.0, 9.0)]
    total = ten_day_total([payout(*e) for e in five])
    print(f"{'hand total of 5 entries':22} {'':22} "
          f"{1356.00:>9} {total:>9}  "
          f"{'PASS' if total == 1356.00 else 'FAIL'}")
    assert total == 1356.00
    print("\nAll tests passed.")


def main():
    """Interactive version used in the lab: read entries from the clerk."""
    payments = []
    while True:
        raw = input("litres fat snf (or 'done'): ").strip()
        if raw.lower() == "done":
            break
        parts = raw.split()
        litres, fat, snf = (read_number(p) for p in parts)
        ok, reason = valid_entry(litres, fat, snf)
        if ok:
            pay = payout(litres, fat, snf)
            payments.append(pay)
            print(f"  accepted  rate {rate_per_litre(fat, snf):6.2f} "
                  f"amount {pay:8.2f}")
        else:
            print(f"  rejected: {reason}")
    print(f"ten-day total: {ten_day_total(payments):.2f}")


if __name__ == "__main__":
    run_tests()
    # main()   # uncomment to enter entries from the keyboard
