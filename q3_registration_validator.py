"""Q3 - Vehicle registration number validator (string methods only, no re).
Complete the Code: TODO 1 and TODO 2 below, plus a receipt formatter."""


def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    # TODO 1: remove spaces and hyphens and convert to upper case
    return text.replace(" ", "").replace("-", "").strip().upper()


def is_valid(reg):
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    # TODO 2: length 9 or 10, then slice each part and test with
    # isalpha()/isdigit()
    if len(reg) not in (9, 10):
        return False
    return (reg[:2].isalpha()          # 2 state letters
            and reg[2:4].isdigit()     # 2 district digits
            and reg[4:-4].isalpha()    # 1 or 2 series letters
            and reg[-4:].isdigit())    # 4 serial digits


def format_reg(reg):
    """'TN09AB1234' -> 'TN 09 AB 1234' for the receipt."""
    return f"{reg[:2]} {reg[2:4]} {reg[4:-4]} {reg[-4:]}"


# predictions before execution:
#   'tn 09 ab 1234' -> valid; 'KA-01-M-0007' -> valid;
#   'TN9AB1234' (district part wrong) -> INVALID; 'TN 22 1234 AB' -> INVALID
for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
    reg = normalise(raw)
    print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")

print()
print("receipt  :", format_reg("TN09AB1234"))
print("receipt10:", format_reg("TN09ABC1234"))

print("""
IMMUTABILITY AND SLICING:
  text = 'tn 09'; text.upper() returns a NEW string 'TN 09' - the object
  text refers to never changes, because str objects are immutable
  (they can be shared safely and used as dict keys). Every 'change'
  method returns a new object.
  s[-4:]  -> the LAST 4 characters (the serial digits) for any length.
  9-char  'TN09AB1234' : s[4:-4] -> 'AB'  (1 series letter)
  10-char 'TN09ABC1234': s[4:-4] -> 'ABC' (2 series letters)
""")
