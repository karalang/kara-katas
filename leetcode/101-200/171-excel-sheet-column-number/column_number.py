# LeetCode #171: Excel Sheet Column Number — reference oracle.
#
# Map an Excel column title to its 1-based number: A->1, B->2, ..., Z->26,
# AA->27, AB->28, ..., ZY->701. This is *bijective* base-26 (no zero digit) —
# the parse direction, char -> value, exactly the self-hosted lexer's
# `from_str_radix` accumulation but with a 1-offset alphabet:
#
#   n = n * 26 + (c - 'A' + 1)        for each title char, most-significant first
#
# The round-trip render below (the LeetCode #168 direction, value -> title)
# doubles as a second oracle: to_title(to_number(s)) must reproduce s. It is the
# same digit-table render as #405/#415 — `"ABC...Z"[d]` — over bijective base-26,
# where each emitted digit subtracts one before the modulus.

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def to_number(title):
    n = 0
    for c in title:
        n = n * 26 + (ord(c) - ord("A") + 1)
    return n


def to_title(num):
    out = []
    n = num
    while n > 0:
        n -= 1                       # bijective: shift into 0..25 before the mod
        out.append(LETTERS[n % 26])
        n //= 26
    return "".join(reversed(out))


def main():
    titles = ["A", "B", "Z", "AA", "AB", "AZ", "BA", "ZY", "ZZ", "AAA",
              "FXSHRXW"]

    # Parse direction (#171): title -> number.
    for t in titles:
        print(f'"{t}" -> {to_number(t)}')

    # Round-trip render (#168 direction): number -> title, must reproduce input.
    print("--- round-trip ---")
    for t in titles:
        n = to_number(t)
        print(f'{n} -> "{to_title(n)}"')


main()
