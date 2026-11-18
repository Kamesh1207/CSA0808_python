"""Q6 - Counting ways to climb temple steps (1 or 2 steps at a time).
Complete the Code TODO 1: memoised recursion, call counts, recursion
limit at n = 1000, and the loop alternative."""

import sys
from functools import lru_cache

calls = 0


def ways_naive(n):
    """Ways to climb n temple steps taking 1 or 2 steps at a time."""
    global calls
    calls += 1
    if n <= 1:                     # base case: one way to stand still / last step
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)   # recursive case


@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    # TODO 1: same base case and recursive case as ways_naive, but the
    # calls go to ways_memo, so each n is computed only once
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)


def ways_loop(n):
    """Alternative concept: iterative, keeps only the last two values."""
    a, b = 1, 1                     # ways(0), ways(1)
    for _ in range(max(n - 1, 0)):
        a, b = b, a + b
    return b if n >= 1 else 1


# --- correctness check against hand-worked answers --------------------
hand = {1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 6: 13}     # worked out on paper
assert all(ways_naive(n) == v for n, v in hand.items())
assert all(ways_memo(n) == v for n, v in hand.items())
print("hand check n=1..6 :", " ".join(f"{n}:{ways_naive(n)}" for n in hand))

# --- required run -----------------------------------------------------
calls = 0; print("naive:", ways_naive(25), "calls =", calls)
ways_memo.cache_clear()
calls = 0; print("memo :", ways_memo(25), "calls =", calls)

# --- growth investigation --------------------------------------------
print(f"\n{'n':>3} {'naive calls':>12} {'memo calls':>11}")
ways_memo.cache_clear()
for n in (10, 20, 25, 30):
    calls = 0; ways_naive(n); naive_calls = calls
    ways_memo.cache_clear()
    calls = 0; ways_memo(n); memo_calls = calls
    print(f"{n:>3} {naive_calls:>12} {memo_calls:>11}")

# --- deployment decision: n = 1000 ------------------------------------
print()
try:
    ways_memo.cache_clear()
    ways_memo(1000)
    print("ways_memo(1000) succeeded")
except RecursionError:
    print("ways_memo(1000) -> RecursionError, because every level waits on")
    print("the one below: the depth needed (~1000 frames) exceeds")
    print("sys.getrecursionlimit() =", sys.getrecursionlimit())
    print("raising the limit is fragile (the C stack can still overflow),")
    print("so the loop version is used for deployment:")
    result = ways_loop(1000)
    print("ways_loop(1000) =", str(result)[:60], "... ("
          f"{len(str(result))} digits)")
    assert ways_loop(30) == ways_memo(30)
    print("loop and memo agree on every n tested - DECISION: ship the loop")

print("""
CALL TREE for n=5 (plain recursion): ways(5) splits into ways(4) and
ways(3); ways(4) into ways(3), ways(2); the SAME ways(3) is therefore
computed twice, ways(2) three times - the tree recomputes every smaller
state once per occurrence, giving O(phi^n) calls (242,785 calls for
n=25 vs 26 with memoisation: one per distinct value 0..25).

COMPLEXITY: plain recursion O(phi^n) time / O(n) stack; memoised
recursion O(n) time / O(n) cache + stack; the loop O(n) time / O(1)
space (only two values kept) - measured above for n = 1000.
""")
