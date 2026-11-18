"""Q7 - Contact merging from first principles.
Design: dict keyed by the NORMALISED primary number; sets for the
numbers and e-mails; names normalised to catch re-spellings."""

import time


def normalise_number(raw):
    """'+91 98400 12345' -> '919840012345'->last 10 ->'9840012345'.
    Two contacts are the SAME person if they share any normalised number."""
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    if len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    return digits


def normalise_name(raw):
    """'Dr. Ravi ' -> 'ravi' (honorifics stripped, lower, single spaces)."""
    name = raw.lower().strip()
    for title in ("dr.", "dr", "mr.", "mr", "mrs.", "mrs", "ms.", "ms"):
        if name.startswith(title + " "):
            name = name[len(title) + 1:].strip()
    return " ".join(name.split())


def merge_contacts(contact_lists):
    """Merge lists of dicts {name, phone, email} keyed by normalised number."""
    merged = {}
    for contacts in contact_lists:
        for c in contacts:
            key = normalise_number(c.get("phone", ""))
            if not key:
                continue
            entry = merged.setdefault(
                key, {"names": set(), "numbers": set(), "emails": set()})
            if c.get("name"):
                entry["names"].add(normalise_name(c["name"]))
            if c.get("phone"):
                entry["numbers"].add(normalise_number(c["phone"]))
            if c.get("email"):
                entry["emails"].add(c["email"].lower())
    return merged


# --- hand-verifiable small case -----------------------------------------
phone_a = [{"name": "Dr. Ravi", "phone": "+91 98400 12345",
            "email": "ravi@gmail.com"},
           {"name": "Meena", "phone": "98400 77777", "email": None}]
phone_b = [{"name": "ravi kumar", "phone": "9840012345",
            "email": "R.KUMAR@gmail.com"},
           {"name": "Meena S", "phone": "+919840077777",
            "email": "meena@outlook.com"}]
sim = [{"name": "Ravi Kumar", "phone": "09840012345", "email": None}]

merged = merge_contacts([phone_a, phone_b, sim])
print(f"{'key (number)':14} {'names':24} {'numbers':28} emails")
for key, entry in sorted(merged.items()):
    print(f"{key:14} {sorted(entry['names'])!s:24} "
          f"{sorted(entry['numbers'])!s:28} {sorted(entry['emails'])}")

# hand check: 3 records of Ravi collapse to ONE entry (key 9840012345)
# with BOTH spellings ('ravi', 'ravi kumar') and BOTH e-mails kept;
# Meena keeps her own key (9840077777); 2 distinct people in total
assert len(merged) == 2
assert merged["9840012345"]["emails"] == {"ravi@gmail.com", "r.kumar@gmail.com"}
assert merged["9840012345"]["names"] == {"ravi", "ravi kumar"}
assert merged["9840077777"]["numbers"] == {"9840077777"}
print("\nhand verification passed: 5 input records -> 2 merged contacts")

# --- measurement: dict grouping vs pairwise comparison -------------------
def make_contacts(n, seed=1):
    import random
    rng = random.Random(seed)
    names = ["Ravi Kumar", "Dr. Ravi", "Meena", "Arun", "Priya", "Kumar"]
    return [{"name": rng.choice(names),
             "phone": f"+91 98{rng.randrange(10**8):08d}",
             "email": f"user{rng.randrange(10**6)}@mail.com"}
            for _ in range(n)]


print(f"\n{'n':>8} {'pairwise O(n^2) (s)':>20} {'dict O(n) (s)':>14}")
for n in (1_000, 100_000):
    contacts = make_contacts(n)

    start = time.perf_counter()
    merged_dict = merge_contacts([contacts])
    t_dict = time.perf_counter() - start

    t_pair = None
    if n <= 1_000:                      # n^2 = 10^6 pairs is the practical cap
        start = time.perf_counter()
        seen = []
        for i in range(n):
            for j in range(i + 1, n):
                if normalise_number(contacts[i]["phone"]) == \
                        normalise_number(contacts[j]["phone"]):
                    seen.append(j)
        t_pair = time.perf_counter() - start
    print(f"{n:>8} {f'{t_pair:.4f}' if t_pair else 'off scale (~8 h)':>20} "
          f"{t_dict:>14.4f}")

print("""
DEFENCE: the dictionary solves duplicate detection by HASHING - one
lookup per record, O(n) average, versus comparing every pair O(n^2)
(100,000 contacts -> 5,000,000,000 pair tests). Two DIFFERENT people
with the same normalised name stay separate because the KEY is the
number, not the name; the same person with several numbers appears
under each number key (a further union-find/merge pass on shared
numbers would join multi-number people). Remaining limitation: entries
with NO phone at all cannot be keyed - an e-mail-keyed fallback would
be needed.
""")
