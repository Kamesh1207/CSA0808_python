"""TASK B4 - Final engineering decision: sentiment at scale,
index timing, and the production decision.
Complete the Code TODO 1 below; 50 complaints scored against a
hand-read ground truth; index measured on the slowest query."""

import sqlite3
import time

POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}


def score(text):
    """+1 per positive word, -1 per negative word; a preceding negator flips it."""
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    # TODO 1: for each word find its value (+1, -1 or 0); if the previous
    # word is a negator, flip the sign; add it to the total
    for i, word in enumerate(words):
        value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0
        if value and i > 0 and words[i - 1] in NEGATORS:
            value = -value
        total += value
    return total


def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"


for c in ["Roads are clean and the bus was fast.",
          "Smoke from the factory, air is bad.",
          "The staff were not helpful.",
          "Not bad, service improved."]:
    print(f"{label(c):8} | {c}")

# ---- B4.1: 50 complaints vs hand-read ground truth ---------------------
TEMPLATES = [
    ("Roads are clean and the bus service is fast.", "positive"),
    ("The area near the depot is dirty and smells of smoke.", "negative"),
    ("Officials were helpful and the complaint was fixed.", "positive"),
    ("Trash is never collected in our street.", "negative"),
    ("Service is not slow any more, it improved.", "positive"),
    ("The staff were rude and unhelpful about the broken bin.", "negative"),
    ("Water logging near the school, roads are bad.", "negative"),
    ("New bus stand looks clean, good work by the board.", "positive"),
    ("Nothing works, the complaint portal is broken.", "negative"),
    ("Not bad at all, the new timing is helpful.", "positive"),
] * 5                                                # 50 complaints
agree = sum(1 for text, expected in TEMPLATES if label(text) == expected)
wrong = sorted({(t, label(t), e) for t, e in TEMPLATES if label(t) != e})
print(f"\nB4.1 agreement with hand reading: {agree}/{len(TEMPLATES)} "
      f"= {agree / len(TEMPLATES):.0%}")
for t, got, exp in wrong[:3]:
    print(f"  mislabelled: {t!r} -> {got}, hand label {exp}")
print("known failure (also in B2): sarcasm/double negatives - the lexicon")
print("scores 'broken portal' correctly but misses irony like 'great, smoke again'")

# ---- B4.2: index on (station, day) - effect on the slowest query -------
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, hour INT, pm25 REAL)")
rows = [("S001", f"2026-{m:02d}-{d:02d}", h, 50.0)
        for m in range(1, 13) for d in range(1, 29) for h in range(24)]
con.executemany("INSERT INTO aq VALUES (?,?,?,?)", rows * 3)   # ~0.1M rows
con.commit()


def timed(query):
    start = time.perf_counter()
    con.execute(query).fetchone()
    return time.perf_counter() - start


query = "SELECT avg(pm25) FROM aq WHERE station = 'S001' AND day = '2026-06-15'"
before = timed(query)
con.execute("CREATE INDEX aq_idx ON aq (station, day)")
con.commit()
after = timed(query)
print(f"\nB4.2 slowest query, before index: {before * 1000:.2f} ms")
print(f"                 after  index : {after * 1000:.4f} ms")
con.close()

print("""
B4.3 PRODUCTION DECISION: store cleaned readings in SQLite with an
(station, day) index and a daily incremental load (new files appended
by station); run the summary queries with GROUP BY on the database,
not in Python loops. The lexicon sentiment scorer is good enough as a
TRIAGE tool for 50,000 complaints/month (O(words) per complaint,
microseconds) with human review of the ~10% mislabelled; a trained
model is only worth it when agreement on real data drops below ~80%.
""")
