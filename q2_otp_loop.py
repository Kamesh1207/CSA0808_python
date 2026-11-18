"""Q2 - OTP verification at a bank kiosk.
while and for designs; break, continue, pass and the loop-else clause.
Correct OTP is 4321; 3 attempts; blanks do not count; 3 wrong -> lock 30 min."""


def verify_while(entries, otp="4321", max_attempts=3):
    """while version: the attempt counter is updated ONLY after a real entry."""
    attempts_left = max_attempts
    i = 0
    while attempts_left > 0:
        if i >= len(entries):
            break                      # customer gave up - not a lock
        entry = entries[i]
        i += 1
        if entry == "":                # blank entry
            print("      blank -> continue (NOT counted as an attempt)")
            continue
        if entry == otp:
            print(f"      {entry!r} correct -> break")
            return "unlocked"          # break/return skips the else clause
        attempts_left -= 1             # counter updated AFTER validation
        print(f"      wrong code ({attempts_left} attempt(s) left)")
    else:
        # loop-else runs only when the WHILE CONDITION becomes false,
        # i.e. attempts were genuinely exhausted (no break happened)
        return "locked 30 minutes"
    return "gave up (session closed, not locked)"


def verify_for(entries, otp="4321", max_attempts=3):
    """for version over range(max_attempts); pass used as a placeholder."""
    for attempt in range(max_attempts):
        entry = entries[attempt] if attempt < len(entries) else None
        if entry == "":                       # blank
            print("      blank -> continue (NOT counted)")
            continue
        if entry == otp:
            print(f"      {entry!r} correct -> break")
            return "unlocked"
        if entry is None:
            pass                              # placeholder: log 'no more entries'
        else:
            print(f"      wrong code (attempt {attempt + 1})")
    else:
        return "locked 30 minutes"            # all max_attempts used, no break
    return "gave up (session closed, not locked)"


def verify_recursive(entries, otp="4321", attempts_left=3, i=0):
    """Alternative concept: recursion instead of a loop (O(a) stack!)."""
    if attempts_left == 0:
        return "locked 30 minutes"
    if i >= len(entries):
        return "gave up (session closed, not locked)"
    entry = entries[i]
    if entry == "":
        return verify_recursive(entries, otp, attempts_left, i + 1)  # blank: retry
    if entry == otp:
        return "unlocked"
    return verify_recursive(entries, otp, attempts_left - 1, i + 1)


print("CASE 1 - three wrong codes -> lock (loop-else demo):")
print("  while:", verify_while(["1111", "2222", "3333"]))
print("CASE 1b - wrong, blank, wrong, wrong (blank is free but no help):")
print("  while:", verify_while(["1111", "", "2222", "3333"]))
print("CASE 2 - correct on the 3rd real attempt:")
print("  while:", verify_while(["1111", "2222", "", "4321"]))
print("CASE 3 - customer walks away after one wrong code:")
print("  while:", verify_while(["1111"]))
print()
print("for-version checks:")
print("  lock   :", verify_for(["1111", "2222", "3333"]))
print("  success:", verify_for(["1111", "", "4321"]))
print("recursive-version checks:")
print("  lock   :", verify_recursive(["1111", "2222", "3333"]))
print("  success:", verify_recursive(["", "4321"]))

print("""
WHILE vs FOR: while is the natural shape here because the number of
rounds is NOT known in advance (blank entries consume no attempt), so
the condition 'attempts_left > 0' carries the rule. for-range(3) is
shorter but silently treats a blank as a round unless the continue is
added. BUG: if the counter were updated BEFORE validating the entry
(e.g. decremented on the blank line too), a customer with one blank
and one wrong code would be locked out after only one real attempt.

CHANGED CONDITION (2 extra attempts after a correct security answer):
the design absorbs it by parameterisation - verify_while(...,
max_attempts=5) after the question succeeds. The while condition and
the for range() are the ONLY lines that change; the lock/else logic
stays untouched.

COMPLEXITY: loop versions are O(a) time and O(1) stack; the recursive
version is O(a) time but O(a) stack frames, so a raised limit or a
loop rewrite is needed for large a.
""")
