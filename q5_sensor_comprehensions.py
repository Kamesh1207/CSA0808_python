"""Q5 - List comprehension: cleaning cold-storage sensor readings.
Three implementations of the same pipeline + timings + memory."""

import sys
import time

RAW = [4.2, -50.0, 51.5, 6.0, 7.5, -60.0, 3.1, 8.9, 0.0, 49.9]
LOW, HIGH = -50.0, 50.0          # sensor-validity band


def clean_loop(readings):
    """(a) for loop with append - the baseline."""
    valid, fahrenheit, alarms = [], [], []
    for minute, c in enumerate(readings):
        if LOW <= c <= HIGH:
            valid.append(c)
            fahrenheit.append(c * 9 / 5 + 32)
            if not (2 <= c <= 8):            # outside the vaccine band
                alarms.append(minute)
    return valid, fahrenheit, alarms


def clean_comprehension(readings):
    """(b) list comprehensions with conditions."""
    valid = [c for c in readings if LOW <= c <= HIGH]
    fahrenheit = [c * 9 / 5 + 32 for c in valid]
    alarms = [m for m, c in enumerate(readings)
              if LOW <= c <= HIGH and not 2 <= c <= 8]
    return valid, fahrenheit, alarms


def clean_map_filter(readings):
    """(c) map() and filter() with lambda."""
    valid = list(filter(lambda c: LOW <= c <= HIGH, readings))
    fahrenheit = list(map(lambda c: c * 9 / 5 + 32, valid))
    alarms = [m for m, c in enumerate(readings)
              if LOW <= c <= HIGH and not 2 <= c <= 8]
    return valid, fahrenheit, alarms


a, b, c = clean_loop(RAW), clean_comprehension(RAW), clean_map_filter(RAW)
assert a == b == c
print("valid     :", b[0])
print("fahrenheit:", [round(f, 1) for f in b[1]])
print("alarm mins:", b[2])

# dict comprehension (minute -> C) and set comprehension (distinct ints)
c_to_f = {m: round(v * 9 / 5 + 32, 1) for m, v in enumerate(RAW)
          if LOW <= v <= HIGH}
distinct_ints = {int(v) for v in RAW if LOW <= v <= HIGH}
print("dict comp :", dict(list(c_to_f.items())[:5]), "...")
print("set comp  :", distinct_ints)

# generator expression: O(1) memory instead of O(n)
big = list(range(100_000))
gen = (c for c in big if c % 2 == 0)
lst = [c for c in big if c % 2 == 0]
print(f"\ngetsizeof list comp (100k results): {sys.getsizeof(lst):,} bytes (grows with n)")
print(f"getsizeof genexpr                 : {sys.getsizeof(gen):,} bytes (constant, O(1))")

# --- timings -------------------------------------------------------------
print(f"\n{'n':>9} {'loop':>9} {'comprehension':>14} {'map/filter':>11}")
for n in (10_000, 100_000, 1_000_000):
    data = [(i * 37 % 110) - 50 for i in range(n)]
    t = []
    for fn in (clean_loop, clean_comprehension, clean_map_filter):
        start = time.perf_counter(); fn(data); t.append(time.perf_counter() - start)
    print(f"{n:>9} {t[0]:>9.4f} {t[1]:>14.4f} {t[2]:>11.4f}")

# --- edge cases -----------------------------------------------------------
assert clean_comprehension([]) == ([], [], [])
assert clean_comprehension([99, -99]) == ([], [], [])   # all invalid
assert clean_comprehension([5, 6]) == ([5, 6], [41.0, 42.8], [])
print("\nedge cases pass: empty, all-invalid, all-valid")

print("""
GENERAL FORM: [expression for x in iterable if condition]
A comprehension is harder to read than a loop when it nests >1 for,
chains >1 condition, or needs side effects. It is NOT always best:
the generator expression wins when the result is consumed once
(O(1) memory - measured above), the plain loop wins when logic is
complex; timings show comprehension/map-filter marginally faster than
loop+append at every size, all O(n).
""")
