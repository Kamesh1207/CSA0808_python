"""TASK 4 - File and exception forensics: the library returns.log bugs.
Part A reproduces the defects; Part B is the repaired version."""

# ---- original defective program (from the brief) ----------------------
def save_returns_buggy(books):
    log = open("returns.log", "w")          # defect 1: "w" wipes the file
    for b in books:
        log.write(b)                        # defect 2: no newline separator
    log.close()                             # defect 3: never closed if write fails


def process_buggy(day_file):
    try:
        books = open(day_file).read().split("\n")
        save_returns_buggy(books)
    except FileNotFoundError:
        print("missing")                    # defect 4: error not logged


# ---- Task 4.2: construct evidence over three days ----------------------
for day in (1, 2, 3):
    with open(f"books_day{day}.txt", "w", encoding="utf-8") as f:
        f.write(f"BOOK-MON-{day} (Monday returns)\n"
                f"BOOK-TUE-{day} (Tuesday returns)")

for day in (1, 2, 3):
    process_buggy(f"books_day{day}.txt")

log_after = open("returns.log", encoding="utf-8").read()
print("\nlog after the BUGGY runs (3 days):")
print(repr(log_after))
print("-> only day 3 survived: mode 'w' TRUNCATES the file every call;")
print("-> both books of one day are joined on one line (no newline);")
print("-> if write() raised, log.close() would never run (no with).")

# ---- Task 4.3: repaired program ---------------------------------------
def save_returns(books, mode="a"):
    with open("returns.log", mode, encoding="utf-8") as log:
        for b in books:
            log.write(b.rstrip("\n") + "\n")   # one book per line


def process(day_file):
    books = []
    try:
        with open(day_file, encoding="utf-8") as f:
            books = [line for line in f.read().split("\n") if line]
        save_returns(books)
    except FileNotFoundError as exc:
        with open("task4_error.log", "a", encoding="utf-8") as err:
            err.write(f"{day_file}: {exc}\n")
        print(f"logged: {day_file} missing")


open("returns.log", "w").close()            # fresh log for the repaired run
process("books_day1.txt")
process("books_day2.txt")
process("books_day3.txt")
process("books_missing.txt")                # missing file -> logged, no crash

log = open("returns.log", encoding="utf-8").read().splitlines()
print(f"\nlog after the REPAIRED runs: {len(log)} lines")
for line in log:
    print("  ", line)
assert len(log) == 6 and len(set(log)) == 6
print("all three days are present, one book per line - defects fixed")
print("\nerror log:", open("task4_error.log").read().strip())

print("""
TASK 4.4 - prevention rules
  1. ALWAYS open with `with open(...)` - it closes on error, so no
     open file handle leaks and buffers are flushed.
  2. Choose the mode deliberately: 'a' to grow a log, 'w' only for
     reports you mean to replace; write complete lines ending in a
     newline character.
""")
