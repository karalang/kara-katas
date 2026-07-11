"""LeetCode #89: Gray Code — direct XOR formula.

Mirror of gray_code.kara. The i-th binary-reflected Gray code is i ^ (i >> 1); emit it
for i in 0..2**n. Same six cases and output shape (an `n=<n>: [...]` line per case,
then a `sink:` fold of length + values) so the files diff line-for-line.
"""

from __future__ import annotations


def gray_code(n: int) -> list[int]:
    total = 1 << n
    return [i ^ (i >> 1) for i in range(total)]


def show(g: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in g) + "]"


def report(n: int, acc: list[int]) -> None:
    g = gray_code(n)
    print(f"n={n}: {show(g)}")
    a = (acc[0] * 131 + (len(g) + 1)) % 1000000007
    for x in g:
        a = (a * 131 + (x + 1)) % 1000000007
    acc[0] = a


def main() -> None:
    acc = [0]
    report(0, acc)
    report(1, acc)
    report(2, acc)
    report(3, acc)
    report(4, acc)
    report(5, acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
