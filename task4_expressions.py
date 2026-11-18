"""Task 4 - Correct expressions for steps, rate and amount,
plus three surprising results and their explanations."""

import math

# ---- the correct expressions ---------------------------------------
fat, snf, litres = 4.2, 8.7, 8.5          # one clerk entry

fat_steps = round((fat - 3.5) / 0.1)      # 0.1 % steps of fat from 3.5
snf_steps = round((snf - 8.5) / 0.1)      # 0.1 % steps of SNF from 8.5
rate = round(30.00 + fat_steps * 0.40 + snf_steps * 0.30, 2)
amount = round(litres * rate, 2)

print("fat_steps =", fat_steps)          # 7
print("snf_steps =", snf_steps)          # 2
print("rate      =", rate)               # 33.4
print("amount    =", amount)             # 283.9

# Precedence / associativity notes:
#   ** is evaluated before * / and binds tighter than unary minus,
#   so -3 ** 2 is -(3**2) = -9.  ** is RIGHT-associative:
#   2 ** 3 ** 2 == 2 ** 9 == 512.
print(-3 ** 2, 2 ** 3 ** 2)

# Comparison chaining and Boolean operators:
print(2.0 <= fat <= 7.0, fat > 3.0 and snf > 8.0)

print()
print("---- three surprising results ----")

# SURPRISE 1: float subtraction/division is not exact
s1 = (4.2 - 3.5) / 0.1
print("(4.2 - 3.5) / 0.1 =", s1)
# 4.2-3.5 is stored as 0.7000000000000002 and dividing by 0.1 gives
# 7.000000000000001, not 7. round() fixes the step count: round(s1) == 7.

# SURPRISE 2: equality of float sums fails
print("0.1 + 0.2 == 0.3 ->", 0.1 + 0.2 == 0.3)
# 0.1 and 0.2 have no exact binary representation; the sum is
# 0.30000000000000004. Use round(x, 2) or the decimal module for money.

# SURPRISE 3: round()/int()/floor() disagree on negatives and .5
print("int(-2.7)   =", int(-2.7))    # -2  truncates TOWARD ZERO
print("floor(-2.7) =", math.floor(-2.7))  # -3  largest integer <= x
print("round(-2.7) =", round(-2.7))    # -3  nearest
print("round(-2.5) =", round(-2.5))    # -2  BANKER'S rounding (to even)
print("round( 2.5) =", round(2.5))     #  2  (int() and floor() give 2 / 2)
# int() truncation would give the WRONG rate for milk below the standard
# (e.g. fat = 3.1 would count -3 steps instead of -4), so round() is used.

# ---- Alternative concept: int()/floor() instead of round() ---------
print()
print("---- int()/floor() vs round() for the fat step count ----")
for f in (4.2, 3.1):
    r = round((f - 3.5) / 0.1)          # correct
    t = int((f - 3.5) / 0.1)            # truncation toward zero
    fl = math.floor((f - 3.5) / 0.1)    # floor
    rr = round(30.0 + r * 0.40, 2)
    tr = round(30.0 + t * 0.40, 2)
    fr = round(30.0 + fl * 0.40, 2)
    print(f"fat={f}: round steps={r:>3} rate={rr:6.2f} | "
          f"int steps={t:>3} rate={tr:6.2f} | floor steps={fl:>3} rate={fr:6.2f}")
# fat = 3.1: true steps = -4, but int()/-floor() give -3 (floor of -4.0
# is right, yet floating noise like -3.9999999999999996 makes floor give
# -4 while int gives -3) -> rate 28.40 instead of 28.00 for 3.1.
# All three run in O(1) time and O(1) space; only round() is correct.
