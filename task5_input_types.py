"""Task 5 - Reading clerk input and converting types.
Runs a non-interactive demo on sample entries so the output can be
shown; the same read_number() function is used unchanged when the
text comes from input() in the lab."""

STEP_TEXTS = ["8.5", " 8.5 ", "8,5", "eight", "-3", "12"]


def read_number(text):
    """Convert raw clerk text to float or None when invalid.

    input() ALWAYS returns a str, so the text must be converted with
    int()/float() before arithmetic. The string is cleaned first
    (strip spaces, accept a decimal comma) and then validated with str
    methods BEFORE converting, so "eight" or "8,5" never reaches
    float() and no exception escapes to the user."""

    text = text.strip()               # " 8.5 " -> "8.5"
    text = text.replace(",", ".")     # "8,5"   -> "8.5"  (decimal comma)
    if not text.replace(".", "", 1).replace("-", "", 1).isdigit():
        return None                   # "eight" fails the digit test
    return float(text)                # safe to convert now


# Alternative concept (discussed in the report): try float(text) inside
# try/except ValueError - same O(1) test, slightly faster for valid
# input, and it accepts "1e3" style exponents, but it silently accepts
# values like "  nan  " unless checked, so the str check is clearer.
def read_number_try(text):
    try:
        return float(text.strip().replace(",", "."))
    except ValueError:
        return None


print("Entry   read_number()  read_number_try()  type ok?")
for t in STEP_TEXTS:
    a, b = read_number(t), read_number_try(t)
    print(f"{t!r:>9}  {a!s:>13}  {b!s:>16}   {type(a) is float}")

# f-string formatting with width and precision: {amount:8.2f} reserves
# 8 columns and prints exactly 2 decimals, so the rupee columns align.
print()
print("litres   fat    snf    rate    amount")
for litres, fat, snf in [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]:
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)
    rate = round(30.00 + fat_steps * 0.40 + snf_steps * 0.30, 2)
    amount = round(litres * rate, 2)
    print(f"{litres:6.1f}  {fat:5.2f}  {snf:5.2f}  {rate:6.2f}  {amount:8.2f}")

# In the lab the same function is fed from the keyboard:
#   raw = input("litres fat snf: ")          # always a str
#   litres = read_number(raw.split()[0])     # etc.
