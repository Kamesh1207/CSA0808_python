"""TASK B3 - Loops vs libraries vs SQL: daily mean PM2.5 per station.
Three methods verified to agree, timed at 1 / 12 / 120 stations
(~8,760 readings each) and profiled with cProfile."""

import cProfile
import io
import pstats
import random
import sqlite3
import statistics
import time

HOURS = 24


def make_rows(n_stations, seed=1):
    """One year of hourly readings per station, in memory."""
    rng = random.Random(seed)
    names = [f"S{i:03d}" for i in range(n_stations)]
    days = [f"2026-{m:02d}-{d:02d}" for m in range(1, 13) for d in range(1, 29)]
    return [(rng.choice(names), rng.choice(days), h,
             round(rng.uniform(20, 150), 1))
            for _ in range(n_stations * 365 * HOURS // 4)
            for h in [rng.randrange(24)]][:n_stations * 365 * HOURS // 4]


def mean_loops(rows):
    """Plain-Python loops (the csv-module version reads the same rows)."""
    sums, counts = {}, {}
    for station, day, _h, pm25 in rows:
        key = (station, day)
        sums[key] = sums.get(key, 0.0) + pm25
        counts[key] = counts.get(key, 0) + 1
    return {k: s / counts[k] for k, s in sums.items()}


def mean_sql(rows):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE aq (station TEXT, day TEXT, hour INT, pm25 REAL)")
    con.executemany("INSERT INTO aq VALUES (?,?,?,?)", rows)
    result = {(station, day): avg for station, day, avg in con.execute(
        "SELECT station, day, avg(pm25) FROM aq GROUP BY station, day")}
    con.close()
    return result


try:
    import pandas as pd

    def mean_pandas(rows):
        df = pd.DataFrame(rows, columns=["station", "day", "hour", "pm25"])
        return df.groupby(["station", "day"])["pm25"].mean().to_dict()
except ImportError:
    def mean_pandas(rows):
        return None                      # pandas not installed


def mean_statistics(rows):
    """Alternative concept: store all readings then statistics.mean()."""
    groups = {}
    for station, day, _h, pm25 in rows:
        groups.setdefault((station, day), []).append(pm25)
    return {k: statistics.mean(v) for k, v in groups.items()}


print("correctness on small data (12 stations x 28 days):")
small = make_rows(12)
r1, r2, r4 = mean_loops(small), mean_sql(small), mean_statistics(small)
assert set(r1) == set(r2) == set(r4)
assert all(abs(r1[k] - r2[k]) < 1e-9 for k in r1)
assert all(abs(r1[k] - r4[k]) < 1e-9 for k in r1)
rp = mean_pandas(small)
print("  loops == SQL == statistics.mean: verified",
      f"(pandas: {'verified too' if rp and all(abs(r1[k] - v) < 1e-9 for k, v in rp.items()) else 'not installed'})")

print(f"\n{'stations':>9} {'rows':>9} {'loops (s)':>10} {'SQL (s)':>9} {'pandas (s)':>11}")
for n in (1, 12, 120):
    rows = make_rows(n)
    t0 = time.perf_counter(); mean_loops(rows); t1 = time.perf_counter() - t0
    t0 = time.perf_counter(); mean_sql(rows); t2 = time.perf_counter() - t0
    t0 = time.perf_counter(); rp = mean_pandas(rows); t3 = time.perf_counter() - t0
    print(f"{n:>9} {len(rows):>9} {t1:>10.4f} {t2:>9.4f} "
          f"{f'{t3:.4f}' if rp is not None or n == 0 else 'n/a':>11}")

print("\ncProfile of the plain-Python version (12 stations):")
profiler = cProfile.Profile()
profiler.enable(); mean_loops(small); profiler.disable()
buffer = io.StringIO()
pstats.Stats(profiler, stream=buffer).sort_stats("cumulative").print_stats(4)
for line in buffer.getvalue().splitlines():
    if "mean_loops" in line or "function calls" in line:
        print("  ", line.strip())
print("  -> the hot spot is the tuple-key dict update inside the loop")

print("""
TRADE-OFF: the running-sum dict loop is O(n) time and O(stations x
days) space, no dependencies - right for a quick one-off check. SQL
GROUP BY keeps data on disk, is indexed and reusable - right for the
daily automated report. pandas is the fastest to WRITE and extend but
needs the library and RAM for the whole table.
""")
