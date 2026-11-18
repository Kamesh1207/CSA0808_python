"""Q6 - Nested data: a railway timetable (dict -> dict -> list/tuple/set),
station queries without and with an index, at three sizes."""

import time

# ---- nested structure for 5 trains --------------------------------------
# expression for the departure time of the THIRD station of a train:
#   timetable[12627]["stops"][2][2]
timetable = {
    12627: {"name": "Karnataka Exp", "days": {1, 2, 3, 4, 5},
            "stops": [("Bangalore", None, "19:20"), ("Chennai", "23:45", "00:05"),
                      ("Vijayawada", "05:30", "05:35"), ("Delhi", "13:00", None)]},
    12628: {"name": "Karnataka Exp'", "days": {6, 7},
            "stops": [("Bangalore", None, "19:20"), ("Chennai", "23:45", "00:05"),
                      ("Delhi", "21:00", None)]},
    12657: {"name": "Chennai Mail", "days": {1, 2, 3, 4, 5, 6, 7},
            "stops": [("Chennai", None, "22:30"), ("Katpadi", "23:55", "00:02"),
                      ("Bangalore", "03:40", None)]},
    16021: {"name": "Kaveri Exp", "days": {2, 4, 6},
            "stops": [("Chennai", None, "21:15"), ("Trichy", "02:10", "02:15"),
                      ("Madurai", "04:35", None)]},
    12639: {"name": "Brindavan Exp", "days": {1, 2, 3, 4, 5, 6, 7},
            "stops": [("Bangalore", None, "07:50"), ("Katpadi", "10:53", "10:55"),
                      ("Chennai", "13:35", None)]},
}

DAYS = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}


def trains_at_scan(data, station, day):
    """Naive query: scan every train and every stop - O(total stops)."""
    result = []
    for number, info in data.items():
        if day not in info["days"]:
            continue
        for st_name, _arr, dep in info["stops"]:
            if st_name == station and dep is not None:
                result.append((number, info["name"], dep))
    return sorted(result, key=lambda t: t[2])


def build_index(data):
    """Index: station -> list of (dep, number, name, running days)."""
    index = {}
    for number, info in data.items():
        for st_name, _arr, dep in info["stops"]:
            if dep is not None:
                index.setdefault(st_name, []).append(
                    (dep, number, info["name"], info["days"]))
    for entries in index.values():
        entries.sort()
    return index


def trains_at_index(index, station, day):
    """Indexed query: only the trains AT this station - O(stops there)."""
    return [(num, name, dep) for dep, num, name, days in index.get(station, [])
            if day in days]


# neat timetable print
print(f"{'train':>6}  {'name':16} {'days':13} route")
for number, info in timetable.items():
    route = " -> ".join(f"{s}({d or '--'})" for s, _a, d in info["stops"])
    days = ",".join(DAYS[d] for d in sorted(info["days"]))
    print(f"{number:>6}  {info['name']:16} {days:13} {route}")

print("\ntrains stopping at Chennai on Monday (day 1), by departure:")
for num, name, dep in trains_at_scan(timetable, "Chennai", 1):
    print(f"  {num} {name} departs {dep}")
assert trains_at_scan(timetable, "Chennai", 1) == \
       trains_at_index(build_index(timetable), "Chennai", 1)
print("index agrees with the scan on the 5-train hand case")

print("\nunknown station:", trains_at_index(build_index(timetable), "Mysore", 1))
print("Kaveri runs {2,4,6} - not on Monday (day 1):",
      [r for r in trains_at_index(build_index(timetable), "Trichy", 1)])

# ---- timings with and without the index ---------------------------------
import random
STATIONS = ["Chennai", "Bangalore", "Katpadi", "Trichy", "Madurai", "Delhi",
            "Vijayawada", "Erode", "Salem", "Coimbatore"]
print(f"\n{'trains':>7} {'scan (s)':>10} {'indexed (s)':>12}")
for n in (100, 1_000, 10_000):
    rng = random.Random(1)
    data = {i: {"name": f"Train {i}", "days": {1, 2, 3, 4, 5, 6, 7},
                "stops": [(rng.choice(STATIONS), "00:00", "00:00")
                          for _ in range(8)]}
            for i in range(n)}
    index = build_index(data)
    start = time.perf_counter()
    for _ in range(100):
        trains_at_scan(data, "Chennai", 1)
    t_scan = (time.perf_counter() - start) / 100
    start = time.perf_counter()
    for _ in range(100):
        trains_at_index(index, "Chennai", 1)
    t_idx = (time.perf_counter() - start) / 100
    print(f"{n:>7} {t_scan:>10.5f} {t_idx:>12.6f}")

print("""
WHY: the index does the scanning work ONCE at build time; each query
then touches only the trains at that station instead of every stop of
every train. Trade-off: extra memory O(total stops) for the index and
a rebuild whenever the timetable changes. Why each structure: dict for
O(1) train lookup by number, list to preserve stop order (slicing),
tuple for the immutable (station, arr, dep) triple, set for the
running days (fast membership, no order needed).
""")
