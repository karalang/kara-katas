#!/usr/bin/env python3
"""LeetCode #43: Multiply Strings — known-correct reference oracle.

Pure digit arithmetic (the grid form), no int() conversion of the operands and
no bignum shortcut, so the output is the answer the kara styles must match
byte-for-byte. We *do* use Python ints only to verify the grid against the
language's native bignum at the bottom.
"""


def multiply(a: str, b: str) -> str:
    m, n = len(a), len(b)
    res = [0] * (m + n)
    for i in range(m - 1, -1, -1):
        d1 = ord(a[i]) - ord("0")
        for j in range(n - 1, -1, -1):
            d2 = ord(b[j]) - ord("0")
            lo, hi = i + j + 1, i + j
            s = d1 * d2 + res[lo]
            res[lo] = s % 10
            res[hi] += s // 10
    out = "".join(str(d) for d in res).lstrip("0")
    return out if out else "0"


CASES = [
    ("2", "3"),
    ("123", "456"),
    ("0", "0"),
    ("0", "52"),
    ("99", "0"),
    ("9", "9"),
    ("99", "99"),
    ("999", "999"),
    ("9999", "9999"),
    ("123", "7"),
    ("6", "123456"),
    ("25", "4"),
    ("10", "10"),
    ("100", "1000"),
    ("123456789", "987654321"),
    ("99999999999999999999", "99999999999999999999"),
    ("12345678901234567890", "98765432109876543210"),
]


if __name__ == "__main__":
    for a, b in CASES:
        got = multiply(a, b)
        assert got == str(int(a) * int(b)), (a, b, got)
        print(f'"{a}" * "{b}" -> "{got}"')
