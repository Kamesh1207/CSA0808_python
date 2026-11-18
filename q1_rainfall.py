"""Q1 - Lists and slicing: daily rainfall records."""

import random
import time

# --- data -------------------------------------------------------------
random.seed(42)                       # reproducible "measurements"
readings = [random.choice([0, 0, 0, 1, 2, 5, 8, 12, 20, 35, 60])
            for _ in range(365)]

# --- weekly totals with slicing ---------------------------------------
weekly = [sum(readings[i:i + 7]) for i in range(0, len(readings) - 6, 7)]
print(f"52 full weeks + {len(readings) % 7} extra day(s); "
      f"weekly totals (first 5): {weekly[:5]}")

# --- max / min with positions -----------------------------------------
wettest, driest = max(weekly), min(weekly)
print(f"wettest week #{weekly.index(wettest) + 1}: {wettest} mm | "
      f"driest week #{weekly.index(driest) + 1}: {driest} mm")
flat_max, flat_min = max(readings), min(readings)
print(f"max day {readings.index(flat_max) + 1}: {flat_max} mm | "
      f"min day {readings.index(flat_min) + 1}: {flat_min} mm")

# --- moving average: naive vs running sum ------------------------------
# Pseudocode (SIMATS standard):
#   NAIVE:   FOR start FROM 0 TO n-7: total <- 0;
#            FOR j FROM start TO start+6: total <- total + r[j];
#            APPEND total/7
#   RUNNING: window <- sum(r[0..6]); APPEND window/7;
#            FOR start FROM 1 TO n-7:
#                window <- window + r[start+6] - r[start-1]; APPEND window/7


def moving_avg_naive(r, w=7):
    return [sum(r[i:i + w]) / w for i in range(len(r) - w + 1)]


def moving_avg_running(r, w=7):
    if len(r) < w:
        return []
    out, window = [], sum(r[:w])
    out.append(window / w)
    for i in range(1, len(r) - w + 1):
        window += r[i + w - 1] - r[i - 1]      # add the new day, drop the old
        out.append(window / w)
    return out


assert moving_avg_naive(readings) == moving_avg_running(readings)

# --- dry days -----------------------------------------------------------
dry = [i + 1 for i, r in enumerate(readings) if r == 0]
print(f"dry days (0 mm): {len(dry)} days, first 10: {dry[:10]}")

# --- slicing questions ---------------------------------------------------
print("\nreadings[7:14] -> days 8-14 (the SECOND week):",
      readings[7:14])
print("readings[-7:]  -> the LAST week               :",
      readings[-7:])
print("readings[::7]  -> every 7th day (a sampling, NOT weeks):",
      readings[::7][:5], "...")

# --- timings: naive vs running sum --------------------------------------
print(f"\n{'n':>7} {'naive (s)':>10} {'running (s)':>12} "
      f"{'naive adds':>11} {'running adds':>13}")
for n in (365, 36_500, 365_000):
    data = [random.random() * 60 for _ in range(n)]
    start = time.perf_counter(); moving_avg_naive(data); t1 = time.perf_counter() - start
    start = time.perf_counter(); moving_avg_running(data); t2 = time.perf_counter() - start
    naive_adds = 7 * (n - 6)           # 7 additions per window
    run_adds = 7 + 2 * (n - 7)         # 1 first window + 2 per slide
    print(f"{n:>7} {t1:>10.4f} {t2:>12.4f} {naive_adds:>11,} {run_adds:>13,}")

# --- edge cases -----------------------------------------------------------
assert moving_avg_naive([]) == [] and moving_avg_running([]) == []
assert moving_avg_naive([3, 5]) == []          # shorter than the window
print("\nedge cases: empty list -> [], list shorter than 7 -> [] - handled")

print("""
LIST COSTS: append O(1)*, pop() O(1), pop(0)/insert(i,x) O(n) (every
later element shifts), sort O(n log n). A list is the right structure
for a fixed daily log; inserting a LATE reading at its date costs
O(n) shifting, acceptable once a day but a linked structure/dict keyed
by date would avoid it if late arrivals were frequent.

ALTERNATIVE: collections.deque(maxlen=7) keeps the window in O(1) per
slide (auto-drop) - same O(n) overall for the average; a dict keyed by
date gives O(1) date access but loses the ordered slicing the weekly
totals rely on, so the list remains the right choice here.
""")
