"""TASK 6 - Design challenge: College Fest Registration Desk.
Reads every fest_*.txt department file (one is deliberately missing),
validates each line, removes duplicates with a set, and writes:
master list, event-wise lists, summary report and an error log.
The program never stops on a bad line or a missing file."""

import glob

VALID_EVENTS = {"Dance", "Music", "Drama", "Solo"}


def valid_email(email):
    """String-method validation: one '@', a '.' after it, no spaces."""
    if email.count("@") != 1 or " " in email:
        return False
    domain = email.split("@")[1]
    return "." in domain and domain.split(".")[-1].isalpha()


def valid_line(parts):
    """(reg, name, dept, email, events) validity checks in order."""
    if len(parts) != 5:
        return False, f"expected 5 fields, found {len(parts)}"
    reg, name, _dept, email, events = (p.strip() for p in parts)
    if not reg.isdigit() or not name.replace(" ", "").isalpha():
        return False, "bad register number or name"
    if not valid_email(email):
        return False, f"invalid e-mail '{email}'"
    if not events or not all(e in VALID_EVENTS for e in events.split(";")):
        return False, "unknown or empty event list"
    return True, ""


files = sorted(glob.glob("fest_*.txt")) + ["fest_mech.txt"]  # mech file does NOT exist
master, events, seen, errors = [], {}, set(), []

for file_name in files:
    try:
        with open(file_name, encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                ok, reason = valid_line(line.split(","))
                if not ok:
                    errors.append(f"{file_name}:{line_no}: {reason} | {line}")
                    continue
                reg, name, dept, email, ev = (p.strip() for p in line.split(","))
                if reg in seen:
                    errors.append(f"{file_name}:{line_no}: duplicate reg {reg}")
                    continue
                seen.add(reg)
                master.append((reg, name, dept, email, ev))
                for event in ev.split(";"):
                    events.setdefault(event, []).append(reg)
    except FileNotFoundError as exc:
        errors.append(f"{file_name}: MISSING FILE ({exc})")

with open("fest_master.csv", "w", encoding="utf-8") as out:
    out.write("reg,name,dept,email,events\n")
    for row in master:
        out.write(",".join(row) + "\n")
for event, regs in events.items():
    with open(f"event_{event}.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(regs) + "\n")
with open("fest_errors.log", "w", encoding="utf-8") as out:
    out.write("\n".join(errors) + "\n")

print(f"clean registrations : {len(master)}")
for row in master:
    print("  ", row)
print("\nevent-wise lists:")
for event, regs in sorted(events.items()):
    print(f"  {event:6}: {len(regs)} participants -> event_{event}.txt")
print("\nerror log:")
print(open("fest_errors.log", encoding="utf-8").read().strip())
print("\nThe program never stopped: the missing department file and every")
print("bad line were captured in fest_errors.log (evidence for Stage 5).")
