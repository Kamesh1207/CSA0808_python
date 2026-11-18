"""TASK 3 - Exceptions in the attendance processor.
Complete the Code TODO 1 and TODO 2: custom exception, complete try
statement, missing-file handling, and the LBF-vs-EAFP experiment."""

import os
import tempfile


class InvalidRecord(Exception):
    """Raised when a line of the attendance file is not in the expected format."""


def parse_line(line):
    """'192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P')"""
    parts = line.strip().split(",")
    # TODO 1: raise InvalidRecord if there are not exactly 3 fields or the
    # status is not P or A; otherwise return the 3 fields as a tuple
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    reg, day, status = parts
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")
    return reg, day, status


def summarise(path):
    present, absent, errors = 0, 0, []
    # TODO 2: open the file with a with statement, parse each line inside
    # try/except InvalidRecord, count P and A, record (line no, message)
    try:
        with open(path, encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:                       # try / except / else / finally
                    reg, day, status = parse_line(line)
                except InvalidRecord as exc:
                    errors.append((line_no, str(exc)))
                else:
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
                finally:
                    pass                   # runs every line: audit hook point
    except FileNotFoundError as exc:
        print(f"handled inside summarise: {exc}")
        raise
    return present, absent, errors


# ---- the required run -------------------------------------------------
data = ("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
        "192311003,2026-10-08\n192311004,2026-10-08,L\n")
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                 encoding="utf-8") as tmp:
    tmp.write(data)
print(summarise(tmp.name))
os.remove(tmp.name)

# ---- missing file: handled inside summarise ---------------------------
print("\nmissing-file experiment:")
try:
    summarise("no_such_folder/no_such_file.csv")
except FileNotFoundError:
    print("caller saw the re-raised FileNotFoundError - logged and reported")

# ---- raise ... from ... keeps the original cause ----------------------
print("\nraise ... from ... demonstration:")
try:
    try:
        int("12a")                      # the ORIGINAL failure
    except ValueError as cause:
        raise InvalidRecord("bad number in record") from cause
except InvalidRecord as e:
    print("caught:", e)
    print("  __cause__:", type(e.__cause__).__name__, "-", e.__cause__)

# ---- Task 3.4 misuse experiment ---------------------------------------
print("\nmisuse experiment: except Exception: pass hides everything")


def misuse_demo():
    try:
        total = 0
        total = totel + 1               # NameError: 'totel' typo, undefined
        return total
    except Exception:
        pass                            # 'harmless' handler


print("misuse_demo() returned:", misuse_demo(),
      "- the NameError typo was swallowed, the function returned None")
print("With specific handlers (except InvalidRecord / FileNotFoundError)")
print("the NameError would STOP the program and point at line of the typo;")
print("`except Exception: pass` hides real bugs -> never use it.")
print("""
FAILURE TABLE (Task 3.1)
  missing folder/file  -> FileNotFoundError
  permission denied    -> PermissionError
  wrong encoding       -> UnicodeDecodeError
  damaged line fields  -> InvalidRecord (custom), IndexError/ValueError inside
  empty file           -> no exception: 0, 0, [] (documented behaviour)
""")
