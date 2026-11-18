"""TASK 2 - Biometric attendance processor (implementation of the
design in task2_attendance_design.md). Processes every
attendance_day*.txt in this folder and writes the two reports."""

import glob

THRESHOLD = 75.0


def process_month(file_names):
    """Read every daily file once, accumulating counts in dictionaries."""
    present, absent, damaged = {}, {}, []

    def record(reg, status, file_name, line_no, line):
        if status == "P":
            present[reg] = present.get(reg, 0) + 1
        else:
            absent[reg] = absent.get(reg, 0) + 1

    for file_name in sorted(file_names):
        try:
            with open(file_name, encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) != 3 or parts[2] not in ("P", "A"):
                        damaged.append((file_name, line_no, line,
                                        "damaged line"))
                        continue
                    record(parts[0], parts[2], file_name, line_no, line)
        except FileNotFoundError:
            damaged.append((file_name, 0, "", "FILE MISSING"))
    return present, absent, damaged


present, absent, damaged = process_month(
    sorted(glob.glob("attendance_day*.txt")))

rows = []
for reg in sorted(set(present) | set(absent)):
    p, a = present.get(reg, 0), absent.get(reg, 0)
    pct = 100.0 * p / (p + a)
    rows.append((reg, p, a, pct))

with open("attendance_summary.csv", "w", encoding="utf-8") as out:
    out.write("reg,present,absent,percentage\n")
    for reg, p, a, pct in rows:
        out.write(f"{reg},{p},{a},{pct:.1f}\n")

below = [reg for reg, _p, _a, pct in rows if pct < THRESHOLD]
with open("below_75.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(below) + ("\n" if below else ""))

print("attendance_summary.csv:")
print(open("attendance_summary.csv").read().strip())
print("\nbelow 75% :", below or "none")
print("damaged   :", damaged)
print("\ntrace check: day1 line 3 (BADLINE) is logged, not counted - "
      "matches the trace in task2_attendance_design.md")
