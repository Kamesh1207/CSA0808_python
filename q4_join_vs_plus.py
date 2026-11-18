"""Q4 - Building long text: repeated += vs str.join().
Complete the Code TODO 1, then measurements at three sizes (3 runs each)."""

import time

items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]


def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text


def build_join(parts):
    # TODO 1: build the same text using a single str.join() call
    return ";".join(parts) + ";"


# --- required run on the 200,000-line list ---------------------------
start = time.perf_counter(); a = build_plus(items); t_plus = time.perf_counter() - start
start = time.perf_counter(); b = build_join(items); t_join = time.perf_counter() - start
print("same text:", a == b, "| length:", len(b))
print(f"+= time: {t_plus:.4f} s   join time: {t_join:.4f} s")

# --- average of three runs at 1,000 / 10,000 / 200,000 lines ---------
print(f"\n{'lines':>7} {'+= avg (s)':>12} {'join avg (s)':>13}")
for n in (1_000, 10_000, 200_000):
    subset = items[:n]
    t1 = t2 = 0.0
    for _ in range(3):
        start = time.perf_counter(); build_plus(subset); t1 += time.perf_counter() - start
        start = time.perf_counter(); build_join(subset); t2 += time.perf_counter() - start
    print(f"{n:>7} {t1 / 3:>12.5f} {t2 / 3:>13.5f}")

print("""
EXPLANATION (string immutability): a str cannot be extended in place.
Every += must allocate a NEW string and copy the old characters plus
the new one, so one pass costs 1+2+3+...+n characters = O(n^2) copying
in the worst case. CPython sometimes reuses the buffer when the
reference count is 1, which hides part of the cost - but that is an
implementation detail, not a guarantee (other interpreters show the
full quadratic behaviour). str.join() computes the total size once,
allocates ONE string and copies each part exactly once: O(n) copying.
That is why join() stays the recommended practice.

ALTERNATIVE: writing each line with print/write to a file streams in
O(n) time and O(1) extra memory but locks the text into the file;
io.StringIO also builds in one pass, O(n) time and O(n) memory, and
keeps the text in process. join() needs O(total size) memory but
returns a real str that can be returned and reused.
""")
