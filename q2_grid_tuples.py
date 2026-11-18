"""Q2 - Tuples, mutability and copying: the city bus-stop grid.
Complete the Code TODO 1 below, plus aliasing/copy demos."""

import copy
import sys
import time

rows, cols = 3, 4

bad = [[0] * cols] * rows          # every row is the SAME list object
bad[0][1] = 7

# TODO 1: create a rows x cols grid of zeros using a list comprehension
# so that every row is a SEPARATE list
good = [[0] * cols for _ in range(rows)]
good[0][1] = 7

print("bad :", bad)
print("good:", good)
print(bad[0] is bad[1], good[0] is good[1])

# Tuples are immutable, so they can be used as dictionary keys
stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
print(stops[(13.0418, 80.2341)])

# a LIST cannot be a key - hashing needs an immutable object
try:
    stops[[13.0418, 80.2341]]
except TypeError as exc:
    print("list as key ->", type(exc).__name__, "-", exc)

print("""
MEMORY DIAGRAM
  [[0]*4]*3      -> 3 names pointing at ONE row object:
                    grid[0] is grid[1] is grid[2] -> True (the bug)
  [[0]*4 for _]  -> 3 DIFFERENT row objects        -> False (correct)
""")

# --- aliasing, shallow copy, deep copy ---------------------------------
original = [[1, 2], [3, 4]]
alias = original                          # same object
shallow = original[:]                     # new outer list, SAME inner lists
shallow2 = copy.copy(original)
deep = copy.deepcopy(original)            # new outer AND new inner lists

original[0][0] = 99
print("after original[0][0] = 99:")
print("  alias  :", alias, "(changed - it IS the same list)")
print("  shallow:", shallow, "(inner list shared -> changed)")
print("  deep   :", deep, "(independent -> unchanged)")
print("  id check:", original[0] is shallow[0], original[0] is deep[0])

print("""
SHALLOW vs DEEP: a shallow copy is enough for a FLAT list of immutable
values (numbers, strings); a deep copy is needed when the list holds
mutable objects (rows, dicts) that must evolve independently. A
function that mutates a list argument changes the CALLER's list,
because the parameter is another name for the same object (aliasing).
""")

# --- unpacking tuples in a for loop -------------------------------------
for lat, lon in [(13.0827, 80.2707), (13.0418, 80.2341)]:
    print(f"stop at lat={lat}, lon={lon}")

# --- list vs tuple: memory and speed ------------------------------------
data = list(range(1_000_000))
tup = tuple(data)
print(f"\ngetsizeof list  : {sys.getsizeof(data):>10,} bytes")
print(f"getsizeof tuple : {sys.getsizeof(tup):>10,} bytes "
      "(over-allocated list growth vs exact-size tuple)")

start = time.perf_counter(); [x for x in data]; t_list = time.perf_counter() - start
start = time.perf_counter(); [x for x in tup]; t_tup = time.perf_counter() - start
print(f"iterate: list {t_list:.4f} s vs tuple {t_tup:.4f} s")

# --- changing a list stored INSIDE a tuple ------------------------------
t = ([1, 2], [3, 4])
t[0].append(99)
print("\nlist inside a tuple mutated:", t)
print("the TUPLE's references are frozen, but the objects they point to")
print("stay mutable - which is exactly why a MUTABLE value cannot be a")
print("dict key (its hash would go stale), while this tuple cannot be.")
