"""TASK B2 - Adversarial data: broken files and SQL injection.
Complete the Code TODO 1 and TODO 2, then the four adversarial files."""

import sqlite3

readings = [("Adyar", "2026-10-01", 48.0), ("Guindy", "2026-10-01", 95.0),
            ("Guindy", "2026-10-03", 121.0), ("Adyar", "2026-10-04", 60.0)]

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")

# TODO 1: insert all readings with ONE executemany call using ?
# placeholders, then commit
con.executemany("INSERT INTO aq VALUES (?, ?, ?)", readings)
con.commit()


def station_average(name):
    # TODO 2: average pm25 of one station using a parameterised SELECT
    row = con.execute("SELECT avg(pm25) FROM aq WHERE station = ?",
                      (name,)).fetchone()
    return row[0]


print(station_average("Adyar"), station_average("Guindy"))
print(station_average("Adyar' OR '1'='1"))      # an injection attempt finds nothing
con.close()

# ---- adversarial files -------------------------------------------------
print("\n--- adversarial CSV files ---")


def try_read(title, content, delimiter=",", encoding="utf-8"):
    """Answer one adversarial file and report the design's response."""
    import csv
    import io
    print(f"\n{title}")
    try:
        rows = list(csv.DictReader(io.StringIO(content),
                                   delimiter=delimiter))
        if not rows or not rows[0].get("pm25"):
            print("  -> empty file / missing column detected: 0 valid rows")
            return
        good = [(r["station"], r["pm25"]) for r in rows
                if r["pm25"] not in ("", "NA")
                and 0 <= float(r["pm25"]) <= 999]
        print(f"  -> parsed {len(good)} valid rows: {good}")
    except (KeyError, ValueError, UnicodeDecodeError) as exc:
        print(f"  -> rejected with {type(exc).__name__}: {exc}")


try_read("1) missing column (no pm25):",
         "station,date\nAdyar,2026-10-01\n")
try_read("2) wrong delimiter (semicolon):",
         "station;date;pm25\nAdyar;2026-10-01;48\n")
try_read("3) wrong encoding (utf-8 bytes of latin-1 text):",
         "station,date,pm25\nAdy\xe1r,2026-10-01,48\n".encode("latin-1")
         .decode("utf-8", errors="replace"))
try_read("4) empty file:", "")

# ---- quote in the station name: + concatenation vs ? placeholder ------
print("\n--- SQL built with + vs ? placeholder ---")
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
con.executemany("INSERT INTO aq VALUES (?, ?, ?)", readings)
con.commit()

evil = "Adyar' OR '1'='1"
try:
    built = con.execute(
        f"SELECT avg(pm25) FROM aq WHERE station = '{evil}'").fetchone()
    print("f-string/+ version :", built[0],
          "- the injected OR matched EVERY row (classic SQL injection)")
except sqlite3.OperationalError as exc:
    print("f-string/+ version : sqlite error:", exc)

safe = con.execute(
    "SELECT avg(pm25) FROM aq WHERE station = ?", (evil,)).fetchone()
print("? placeholder version:", safe[0],
      "- the whole string is one literal station name -> no rows -> None")
con.close()

# ---- adversarial sentiment inputs (B2 third bullet) --------------------
print("\n--- adversarial sentiment inputs ---")


def score(text, POSITIVE, NEGATIVE, NEGATORS):
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    for i, w in enumerate(words):
        value = 1 if w in POSITIVE else -1 if w in NEGATIVE else 0
        if value and i > 0 and words[i - 1] in NEGATORS:
            value = -value
        total += value
    return total


P = {"good", "clean", "fast", "helpful", "improved"}
N = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEG = {"not", "never", "no"}
for text in ["The app is so good (sarcasm: it crashes daily).",
             "It is not never clean.", "Good roads but bad smoke."]:
    print(f"  score {score(text, P, N, NEG):>2} <- {text}")
print("  sarcasm and subtle double negatives defeat the lexicon -> logged")
