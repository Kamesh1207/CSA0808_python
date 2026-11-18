"""Q1 - State Electricity Subsidy Eligibility.
Separate if statements vs if-elif-else, tested at every boundary."""

# --- predictions made BEFORE execution (evidence for the report) -----
#  units<=100 -> "full"; 101..200 + ration card -> "partial";
#  >200 only if a member is 80+ -> "senior"; otherwise "none".
PREDICTIONS = [
    ("H1", 50,  False, False, "full"),
    ("H2", 100, False, False, "full (boundary 100)"),
    ("H3", 100, True,  False, "full - BUG CASE: separate ifs may also give partial"),
    ("H4", 101, True,  False, "partial (boundary 101, card)"),
    ("H5", 200, True,  False, "partial (boundary 200, card)"),
    ("H6", 201, False, False, "none (boundary 201, no senior)"),
    ("H7", 260, False, True,  "senior (80+ member)"),
    ("H8", 300, True,  True,  "senior"),
]


def with_separate_ifs(units, ration_card, senior):
    """The developer's style: independent ifs - can give MORE THAN ONE result."""
    results = []
    if units <= 100:
        results.append("full")
    if units <= 200 and ration_card:          # note: overlap with the first rule
        results.append("partial")
    if units > 200 and senior:
        results.append("senior")
    return results or ["none"]


def with_elif(units, ration_card, senior):
    """if-elif-else: the conditions are mutually exclusive -> exactly ONE result."""
    if units <= 100:
        return "full"
    elif 101 <= units <= 200:                 # chained comparison
        return "partial" if ration_card else "none"
    else:
        return "senior" if senior else "none"


print(f"{'id':4} {'units':>5} {'card':>5} {'80+':>4}  {'predicted':~<45}")
for hid, units, card, senior, pred in PREDICTIONS:
    got_if = with_separate_ifs(units, card, senior)
    got_elif = with_elif(units, card, senior)
    flag = "  <-- TWO SUBSIDIES!" if len(got_if) > 1 else ""
    print(f"{hid:4} {units:>5} {str(card):>5} {str(senior):>4}  "
          f"{pred:45} | separate if: {got_if} | elif: {got_elif}{flag}")

print("""
WHY: separate if statements are checked INDEPENDENTLY, so two rules can
both fire for the same household (H3 gets full AND partial). An
if-elif-else chain stops at the first True condition, so exactly one
branch runs - which is what a subsidy rule needs.

DESIGN DECISION: combined Booleans (and/or) with chained comparisons
inside a single if-elif-else chain are preferred here. Nesting
(else: if:) hides the slab structure one indent deeper and forces the
reader to mentally unwind it; the flat elif chain reads exactly like
the tariff table and a rate change touches one line.
""")
