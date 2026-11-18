"""TASK 5(a) - the SAME utility as one single script (no functions split
into modules). Compare with task5_main.py: when the second report
(absent for 3 consecutive days) is required, THIS file must be edited
in place, risking the working code; the module organisation just adds
a function to stats.py and one import line to the main script."""

import glob

rows = {}
for path in sorted(glob.glob("attendance_day*.txt")):
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3 and parts[2] in ("P", "A"):
                p, a = rows.get(parts[0], (0, 0))
                rows[parts[0]] = (p + (parts[2] == "P"), a + (parts[2] == "A"))

for reg in sorted(rows):
    p, a = rows[reg]
    print(f"{reg}: present={p} absent={a} pct={100.0 * p / (p + a):.1f}")

if __name__ == "__main__":
    pass    # the script IS the main program; the guard documents it
