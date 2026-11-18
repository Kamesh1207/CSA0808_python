"""TASK B1 - Cleaning pipeline + SQLite storage.
Complete the Code TODO 1 and TODO 2 below, plus the >999 rule and
SQL queries for the board's questions (A1.3)."""

import csv
import io
import sqlite3

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Guindy,2026-10-04,5000
"""


def load_clean(text):
    """Returns (station, date, pm25) tuples for valid, non-negative readings only."""
    rows = []
    # TODO 1: read the text with csv.DictReader; skip rows whose pm25 is
    # empty, 'NA' or negative (or above 999 - impossible sensor fault);
    # convert pm25 to float
    for row in csv.DictReader(io.StringIO(text)):
        raw = (row["pm25"] or "").strip()
        if raw in ("", "NA", "N/A"):          # missing values
            continue
        value = float(raw)
        if value < 0 or value > 999:          # impossible values
            continue
        rows.append((row["station"], row["date"], value))
    return rows


def min_max(values):
    # TODO 2: scale each value to 0-1 using (v - min) / (max - min)
    lo, hi = min(values), max(values)
    return [round((v - lo) / (hi - lo), 3) for v in values]


clean = load_clean(RAW)
print("raw rows: 8 -> clean rows:", len(clean))
print(clean)
print(min_max([pm for _, _, pm in clean]))

# ---- store in SQLite and answer the board's questions -----------------
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
con.executemany("INSERT INTO aq VALUES (?, ?, ?)", clean)
con.commit()

print("\nboard questions answered with SQL:")
q1 = con.execute("SELECT avg(pm25) FROM aq WHERE station = ?",
                 ("Adyar",)).fetchone()[0]
print(f"1) avg PM2.5 of Adyar        : {q1}")
q2 = con.execute("SELECT station, day, pm25 FROM aq "
                  "ORDER BY pm25 DESC LIMIT 1").fetchone()
print(f"2) worst reading city-wide   : {q2}")
q3 = con.execute("SELECT station, COUNT(*), avg(pm25) FROM aq "
                  "GROUP BY station").fetchall()
print(f"3) valid readings per station: {q3}")
con.close()

# matplotlib charts are produced by task_b1_charts.py when the library
# is installed; interpretation is in README.md (A3.1 choices).
