"""Task 10 - Expectation vs execution: float vs Decimal totals and speed,
plus the rate-table (dict) alternative benchmark."""

import time
from decimal import Decimal

PAYMENT = "33.40"   # Rs per simulated payment


def total_float(items):
    t = 0.0
    for a in items:
        t += float(a)
    return t


def total_float_round_each(items):
    t = 0.0
    for a in items:
        t += round(float(a), 2)     # round after every addition
    return t


def total_decimal(items):
    t = Decimal("0.00")
    for a in items:
        t += Decimal(a)
    return t


print("float vs Decimal for n identical payments of Rs 33.40")
print(f"{'n':>8} {'float total':>22} {'Decimal total':>14} "
      f"{'diff (Rs)':>10}  {'t_float':>9} {'t_round':>9} {'t_dec':>9}")
for n in (300, 6_000, 150_000):
    payments = [PAYMENT] * n

    t0 = time.perf_counter()
    tf = total_float(payments)
    t1 = time.perf_counter()
    tr = total_float_round_each(payments)
    t2 = time.perf_counter()
    td = total_decimal(payments)
    t3 = time.perf_counter()

    print(f"{n:>8} {tf:>22} {td:>14} {tf - float(td):>10.6f}  "
          f"{t1 - t0:>9.4f} {t2 - t1:>9.4f} {t3 - t2:>9.4f}")

print()
print("round-each-payment vs round-only-the-total (n = 150000):")
print(" float rounded each addition :", round(tr, 2),
      "-> equals the Decimal bank total only after a final round")
print(" float rounded once at end   :", round(tf, 2),
      "-> same 2-dp result here, but the paise can be off in general")
print(" Decimal                     :", td, "-> exact bank amount")
# The errors come from binary floats: 33.4 is really
# 33.399999999999998578..., so each addition can be off by ~1e-14 and
# these accumulate linearly with n. Decimal digits are exact.

# ---------------------------------------------------------------
# Alternative concept: rate TABLE (dict lookup) vs recomputation
# ---------------------------------------------------------------
print()
print("rate table (dict) vs recomputing the rate for every entry")

pairs = [(3.5, 8.5), (4.2, 8.7), (3.1, 8.3)]
entries = [pairs[i % 3] for i in range(150_000)]


def rate_float(fat, snf):
    return round(30.0 + round((fat - 3.5) / 0.1) * 0.40
                 + round((snf - 8.5) / 0.1) * 0.30, 2)


t0 = time.perf_counter()
recomputed = [rate_float(f, s) for f, s in entries]
t1 = time.perf_counter()

rate_table = {p: rate_float(*p) for p in pairs}          # k entries, O(k) space
t2 = time.perf_counter()
looked_up = [rate_table[p] for p in entries]             # O(1) per lookup
t3 = time.perf_counter()

print(f"recompute : {t1 - t0:.4f} s   (recalculates for every entry)")
print(f"dict look : {t3 - t2:.4f} s   (plus {t2 - t1:.4f} s one-time build)")
print(f"space     : table holds k={len(rate_table)} rates "
      f"(O(k)) instead of recalculating")
print("same rates:", recomputed == looked_up)
