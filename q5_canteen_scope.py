"""Q5 - Functions, parameters and scope: the mutable default bug.
Complete the Code TODO 1, plus multi-value returns and scope demos."""

GST_RATE = 0.05                      # global constant, only READ below


def add_item_buggy(item, order=[]):
    """Default list is created ONCE at definition - every call shares it."""
    order.append(item)
    return order


def bill(orders):
    """Return TWO values as a tuple (total, gst)."""
    total = round(sum(orders), 2)
    return total, round(total * GST_RATE, 2)


def add_item(item, order=None):
    """TODO 1: create a new list when order is None, append, return it."""
    if order is None:
        order = []                   # a FRESH list per call
    order.append(item)
    return order


print(add_item_buggy("Tea"), add_item_buggy("Vada"))
print(add_item("Tea"), add_item("Vada"))
print("add_item_buggy.__defaults__ =", add_item_buggy.__defaults__)
# The default VALUE object lives on the function object and is the SAME
# list in every call (the tuple above holds one list that has grown).

# --- three customers in sequence: orders stay independent ------------
PRICES = {"Tea": 10.0, "Vada": 15.0, "Idli": 25.0}

print()
for customer in ("Ananya", "Balu", "Chitra"):
    order = []
    for item in ("Tea", "Vada", "Idli"):
        add_item(item, order)
    total, gst = bill([PRICES[item] for item in order])
    print(f"{customer:8} order={order}  total=Rs{total:.2f}  gst=Rs{gst:.2f}")

print("""
POSITIONAL / KEYWORD / DEFAULT: positional for the primary data
(add_item('Tea')), keyword for clarity at the call site
(add_item('Tea', order=my_order)), default for configuration used in
almost every call (GST_RATE-like parameters, order=None). Never use a
mutable default (list/dict/set) - use None and create it inside.

RETURN vs PRINT: bill() RETURNS (total, gst), so the caller can keep
computing with them; a printed value is just text on the screen.
""")

# --- local / global / nonlocal ---------------------------------------
counter = 0                                    # global


def serve():
    global counter                             # needed to REBIND a global
    counter += 1


def counter_closure():
    count = 0                                  # enclosing-scope name

    def step():
        nonlocal count                         # needed to REBIND non-local
        count += 1
        return count

    step()
    step()
    return count


serve(); serve()
print("global counter        :", counter, "(changed with 'global')")
print("nonlocal count        :", counter_closure(), "(changed with 'nonlocal')")
print("""
Reading a global inside a function needs no keyword; only REBINDING
needs global (or nonlocal for enclosing scopes) - and both are usually
avoided by passing values in and returning values out, which keeps
functions testable.
""")
