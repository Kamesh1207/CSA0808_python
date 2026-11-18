"""Task 12 - Day-4 Design Challenge: seasonal rates, two-decimal
analyser readings and a volume bonus.

Decision: MODIFY the original design (not a full redesign):
  * rate constants  -> a SEASON_RATE_CARDS dict selected by season
  * rate_per_litre  -> gains a season parameter
  * money           -> moved to Decimal (exact to the paisa)
  * NEW bonus()     -> Rs 0.50 per litre above 500 L in ten days
Step counting still uses round(); two-decimal readings (4.23) simply
fall to the NEAREST 0.1 % step."""

from decimal import Decimal

# --- rate cards: one place per season (Task 3 principle, extended) ---
SEASON_RATE_CARDS = {
    "normal": {"base": Decimal("30.00"), "fat": Decimal("0.40"),
               "snf": Decimal("0.30")},
    "summer": {"base": Decimal("32.00"), "fat": Decimal("0.45"),
               "snf": Decimal("0.30")},          # April - June
}
FAT_STANDARD, SNF_STANDARD, STEP = 3.5, 8.5, 0.1
BONUS_PER_LITRE = Decimal("0.50")
BONUS_THRESHOLD_LITRES = 500            # > 500 L in ten days


def rate_per_litre(fat, snf, season="normal"):
    """Return the rate per litre (Decimal, 2 dp) for the season.

    fat/snf may now carry TWO decimals from the automatic analyser;
    they are rounded to the NEAREST whole 0.1 % step."""
    card = SEASON_RATE_CARDS[season]
    fat_steps = round((fat - FAT_STANDARD) / STEP)
    snf_steps = round((snf - SNF_STANDARD) / STEP)
    rate = card["base"] + fat_steps * card["fat"] + snf_steps * card["snf"]
    return rate.quantize(Decimal("0.01"))


def bonus(litres, ten_day_litres):
    """Return the volume bonus (Decimal, 2 dp) for one entry."""
    if ten_day_litres > BONUS_THRESHOLD_LITRES:
        return (BONUS_PER_LITRE * Decimal(str(litres))
                ).quantize(Decimal("0.01"))
    return Decimal("0.00")


def payout(litres, fat, snf, season="normal", ten_day_litres=None):
    """Return the amount payable (Decimal, 2 dp), bonus included."""
    pay = (Decimal(str(litres)) * rate_per_litre(fat, snf, season)
           ).quantize(Decimal("0.01"))
    pay += bonus(litres, ten_day_litres) if ten_day_litres is not None \
        else Decimal("0.00")
    return pay


# ------------------------------------------------------------- tests
def run_tests():
    """Defence evidence: both seasons, two-decimal readings, bonus."""
    cases = [
        # (case, season, litres, fat, snf, ten_day_litres, expected)
        ("original readings, normal", "normal", 8.5, 4.2, 8.7, None, Decimal("283.90")),
        ("two-decimal reading",       "normal", 8.5, 4.23, 8.68, None, Decimal("283.90")),
        ("same entry, summer rate",   "summer", 8.5, 4.23, 8.68, None, Decimal("303.88")),
        ("two-decimal rounding down", "normal", 10,  4.24, 8.5,  None, Decimal("328.00")),
        ("bonus: 600 L in 10 days",   "normal", 60,  4.23, 8.68, 600, Decimal("2034.00")),
        ("no bonus: 480 L in 10 days","normal", 60,  4.23, 8.68, 480, Decimal("2004.00")),
    ]
    print(f"{'case':26} {'season':7} {'litres':>6} {'fat':>5} {'snf':>5} "
          f"{'10-day L':>9} {'payout':>10}  result")
    for name, season, l, f, s, tot, expected in cases:
        actual = payout(l, f, s, season, tot)
        status = "PASS" if actual == expected else "FAIL"
        print(f"{name:26} {season:7} {l:>6} {f:>5} {s:>5} "
              f"{tot if tot is not None else '-':>9} {actual:>10}  {status}")
        assert actual == expected, (name, actual, expected)
    print("\nAll Task 12 tests passed.")

    # Hand-check of the key numbers (also in the report):
    # fat 4.23 -> round((4.23-3.5)/0.1) = 7 steps; snf 8.68 -> 2 steps
    # normal : 30.00 + 7*0.40 + 2*0.30 = 33.40 -> 8.5 L = 283.90
    # summer : 32.00 + 7*0.45 + 2*0.30 = 35.75 -> 8.5 L = 303.875 -> 303.88
    # bonus  : 60 L * 33.40 = 2004.00, + 0.50*60 = 30.00 -> 2034.00


if __name__ == "__main__":
    run_tests()
