"""Q4 - Sets: elective registration clash detection.
Complete the Code TODO 1 with set operators, then the method version,
then membership timings."""

ai_elective = {"192311001", "192311004", "192311007", "192311009"}
iot_elective = {"192311002", "192311004", "192311009", "192311010"}
all_students = {f"1923110{i:02d}" for i in range(1, 11)}

# TODO 1: set operators - both, exactly one, neither
both = ai_elective & iot_elective                    # intersection
exactly_one = ai_elective ^ iot_elective             # symmetric difference
neither = all_students - (ai_elective | iot_elective)  # union, difference

print("clash      :", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither    :", sorted(neither))

# same results with the METHOD names
assert both == ai_elective.intersection(iot_elective)
assert exactly_one == ai_elective.symmetric_difference(iot_elective)
assert neither == all_students.difference(
    ai_elective.union(iot_elective))
print("method version (intersection / symmetric_difference / difference")
print("/ union) gives identical results - verified with asserts")

# duplicates vanish because a set stores each hashable value once
dup_register = {"192311001", "192311001", "192311004"}
print("\nduplicates removed:", dup_register, "len =", len(dup_register))

# --- membership timing: list vs set -------------------------------------
import time

print(f"\n{'n':>9} {'x in list (s)':>13} {'x in set (s)':>13}")
for n in (10_000, 100_000, 1_000_000):
    absent_value = n                       # guaranteed NOT in the container
    data = list(range(n))
    s = set(data)

    start = time.perf_counter()
    for _ in range(1_000):
        absent_value in data
    t1 = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(1_000):
        absent_value in s
    t2 = time.perf_counter() - start

    print(f"{n:>9} {t1:>13.5f} {t2:>13.7f}")

# nested loops vs & for finding common students
list_a, list_b = list(ai_elective), list(iot_elective)
start = time.perf_counter()
slow = [a for a in list_a for b in list_b if a == b]
t_loops = time.perf_counter() - start
start = time.perf_counter()
fast = ai_elective & iot_elective
t_set = time.perf_counter() - start
print(f"\nnested loops O(n*m): {t_loops:.6f} s   set &  O(n+m): {t_set:.7f} s")

print("""
WHY: a set hashes each element, so `x in s` checks one slot (O(1)
average); a list must compare x with every element (O(n)). Sets refuse
LISTS because lists are unhashable (mutable), but accept TUPLES of
immutable values - the same rule that allows tuples as dict keys.

CONVERT list -> set when you need fast membership or uniqueness; you
lose ORDER and duplicates (and only hashable items can be stored).
""")
