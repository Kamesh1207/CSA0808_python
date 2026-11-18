"""Q3 - Dictionaries: Kisan call-centre complaint analysis.
Complete the Code TODO 1 and TODO 2, then the experimental comparison."""

import collections
import random
import time

calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]
STOP = {"not", "high"}


def frequencies(texts, stop):
    # TODO 1: word -> count for every word not in stop, using dict.get()
    counts = {}
    for text in texts:
        for word in text.lower().split():
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts


def top(counts, k):
    # TODO 2: k most frequent (word, count), highest first, then A-Z
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]


print(top(frequencies(calls, STOP), 3))
# 'price' comes before 'received': both count 2, and the sort key
# (-count, word) falls back to the alphabetical word for ties.

# group complaints by district into a dict of lists (setdefault)
district_calls = [
    ("Erode", calls[0]), ("Salem", calls[1]), ("Erode", calls[2])]
by_district = {}
for district, text in district_calls:
    by_district.setdefault(district, []).append(text)
print("\ncomplaints by district:", {k: len(v) for k, v in by_district.items()})

# --- experimental investigation ----------------------------------------
BASE = ["seeds not received on time", "fertiliser price very high",
        "subsidy delayed for seeds", "soil health card needed",
        "crop insurance not credited"]


def make_complaints(n):
    rng = random.Random(7)
    words = ["seeds", "fertiliser", "subsidy", "price", "delayed", "soil",
             "crop", "insurance", "card", "received"]
    return [" ".join(rng.choice(BASE).split()[:2] + [
        rng.choice(words) for _ in range(5)]) for _ in range(n)]


def count_with_list_count(words):
    """O(n*d): one full pass over the words per DISTINCT word."""
    distinct = set(words)
    return {w: words.count(w) for w in distinct}


print(f"\n{'n texts':>8} {'words':>9} {'dict loop':>11} "
      f"{'list.count':>11} {'Counter':>9}")
for n in (1_000, 10_000, 100_000):
    texts = make_complaints(n)
    words = " ".join(texts).split()

    start = time.perf_counter(); c1 = frequencies(texts, STOP); t1 = time.perf_counter() - start
    start = time.perf_counter(); c2 = count_with_list_count(words); t2 = time.perf_counter() - start
    start = time.perf_counter(); c3 = collections.Counter(
        w for w in words if w not in STOP); t3 = time.perf_counter() - start

    assert top(c1, 3) == top(dict(c3), 3) or sorted(c1) == sorted(c3)
    print(f"{n:>8} {len(words):>9} {t1:>11.4f} {t2:>11.4f} {t3:>9.4f}")

print("""
DICT LOOKUP: a dictionary hashes the key and jumps straight to a
slot, so the AVERAGE lookup is O(1) - independent of the size.
Counting with list.count() per distinct word costs O(n*d) (d distinct
words) - quadratic-ish as the vocabulary grows. Insertion order is
preserved since Python 3.7 (dict is an ordered mapping). Views:
keys()/values()/items() are live views, not copies.

ENGINEERING DECISION: deploy the dict loop (or Counter, which is a
tuned C implementation of the same idea). O(n) per day scales to
100,000 complaints; list.count() does not.
""")
