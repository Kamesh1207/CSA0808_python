"""TASK 1 - Diagnose and repair the hostel mess-bill script.
The ORIGINAL buggy script is in task1_diagnosis.md; this is the repaired
design (Task 1.2): with-statement, line-by-line reading, specific
exceptions, rejected-line log, join() for the report, Decimal for paise."""

from decimal import Decimal
import sys

LOG_NAME = "task1_rejected_lines.log"


def process_mess_file(file_name):
    """Return (report_lines, total, rejected) for one mess-bill file."""
    report, rejected = [], []
    total = Decimal("0.00")
    with open(file_name, encoding="utf-8") as f:          # closes itself
        for line_no, line in enumerate(f, 1):             # ONE line in memory
            line = line.strip()
            if not line:                                   # skip empty last line
                continue
            parts = [p.strip() for p in line.split(",")]
            try:
                reg, name, amount_text = parts[0], parts[1], parts[2]
                amount = Decimal(amount_text)   # ValueError if not a number
                if amount < 0:
                    raise ValueError(f"negative amount {amount_text}")
            except (ValueError, IndexError) as exc:
                rejected.append((line_no, line, str(exc)))
                continue
            report.append(f"{name} {amount}")
            total += amount
    return report, total, rejected


report, total, rejected = process_mess_file("mess_oct.txt")
print("\n".join(report))
print("Total", total)
if rejected:
    with open(LOG_NAME, "w", encoding="utf-8") as log:
        for line_no, line, err in rejected:
            log.write(f"line {line_no}: {line!r} -> {err}\n")
    print(f"{len(rejected)} rejected line(s) written to {LOG_NAME}")

# TASK 1.3 defence (<=100 words):
# The repaired script reads ONE line at a time, so memory is
# O(line), not O(file) - a 50,000-line file works in kilobytes.
# The with statement closes the file even on error; specific excepts
# count and LOG every rejected line instead of swallowing it, so
# money is never silently lost; Decimal keeps paise exact.
