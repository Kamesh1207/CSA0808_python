"""TASK 5 - The same utility organised four ways.
(a) one script            -> task5_single_script.py
(b) one module + main     -> reader.py/stats.py/report.py imported here
(c) three modules         -> reader.py, stats.py, report.py
(d) package attendance/   -> structure documented in task5_organisations.md

This script demonstrates (b)+(c): it imports the three modules and runs
the attendance processor; every import style is shown."""

import glob

import reader                    # style 1: import module
import reader as rd              # style 2: module under an alias
from reader import read_day      # style 3: selected names
from stats import percentage, below_75
import report

day_files = sorted(glob.glob("attendance_day*.txt"))
print("files:", day_files)

rows = {}
for path in day_files:
    try:
        for reg, _date, status in read_day(path):
            p, a = rows.get(reg, (0, 0))
            rows[reg] = (p + (status == "P"), a + (status == "A"))
    except reader.InvalidRecord as exc:        # damaged line: one file fails
        print("rejected:", exc)

summary = sorted((reg, p, a) for reg, (p, a) in rows.items())
report.print_summary(summary)
path = report.write_summary(summary)
print(f"\nsummary written to {path}")
print("students below 75%:", below_75(summary))
print("percentage(2,1) via alias import:", rd is reader,
      "| percentage(17,3) =", f"{percentage(17, 3):.1f}")
