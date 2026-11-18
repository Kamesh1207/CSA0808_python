"""Task 6 - Organise the calculation into functions.
Each function: parameters in, ONE return value out, docstring attached."""

# --- constants (global names, read but never reassigned) -------------
BASE_RATE = 30.00        # Rs/litre at 3.5 % fat, 8.5 % SNF
FAT_STEP_VALUE = 0.40    # Rs per 0.1 % fat step
SNF_STEP_VALUE = 0.30    # Rs per 0.1 % SNF step
FAT_STANDARD, SNF_STANDARD, STEP = 3.5, 8.5, 0.1


def rate_per_litre(fat, snf):
    """Return the price per litre (Rs, 2 dp) for fat % and SNF %."""
    fat_steps = round((fat - FAT_STANDARD) / STEP)
    snf_steps = round((snf - SNF_STANDARD) / STEP)
    return round(BASE_RATE + fat_steps * FAT_STEP_VALUE
                 + snf_steps * SNF_STEP_VALUE, 2)


def payout(litres, fat, snf):
    """Return the amount payable (Rs, 2 dp) for one milk entry."""
    return round(litres * rate_per_litre(fat, snf), 2)


def ten_day_total(payments):
    """Return the ten-day total (Rs, 2 dp) for a list of payments."""
    return round(sum(payments), 2)


# --- demo -------------------------------------------------------------
entries = [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]

payments = [payout(*e) for e in entries]      # function returns, not prints
print("payments :", payments)
print("ten-day total :", ten_day_total(payments))

# Returning a value hands the result back to the caller, so it can be
# stored, tested with assert, or reused (ten_day_total(payments)).
# print() only writes text to the screen and returns None - a function
# that printed its result could not be composed into bigger calculations.

# --- local vs global names --------------------------------------------
def scope_demo():
    print("inside function, BASE_RATE read from global scope:", BASE_RATE)
    # BASE_RATE = 0.0        # <- UNCOMMENTING would create a NEW LOCAL
    #                        #    variable and raise UnboundLocalError
    local_only = "I exist only while this call runs"
    return local_only


print("scope_demo returns:", scope_demo())
# The constants may be READ inside functions; REASSIGNING one would
# either create a local shadow (harmless but misleading) or need a
# `global` statement, which destroys the one-place rate guarantee.

# --- dynamic typing, multiple assignment, swap -------------------------
x = 10
print("x =", x, type(x))
x = "10"                       # same name rebound to a str - dynamic typing
print("x =", x, type(x))

a, b = 1, 2
a, b = b, a                    # tuple swap without a temporary
print("after swap: a =", a, "b =", b)
