"""LeetCode #66: Plus One — reverse scan with early return, O(n) time, O(1) extra.

Mirror of plus_one.kara: walk the digits from least-significant; the first digit
below 9 absorbs the +1 and we stop, otherwise a 9 becomes 0 and the carry ripples
left. If every digit is a 9 the result grows one place to [1, 0, ..., 0]. Same
twelve cases and the same output shape (one bracketed digit list per line, then a
`sums:` fold of the positional checksums) so the files diff line-for-line.
"""

from __future__ import annotations


def plus_one(digits: list[int]) -> list[int]:
    out = digits[:]  # private copy; caller's array untouched
    i = len(out) - 1
    while i >= 0:
        if out[i] < 9:
            out[i] += 1
            return out
        out[i] = 0  # 9 + 1 = 10: write 0, carry left
        i -= 1
    return [1] + [0] * len(digits)  # all nines: one place wider


def report(digits: list[int], acc: list[str]) -> None:
    out = plus_one(digits)
    chk = sum((k + 1) * v for k, v in enumerate(out))
    print("[" + ", ".join(str(v) for v in out) + "]")
    acc.append(str(chk))


def main() -> None:
    acc: list[str] = []
    report([1, 2, 3], acc)              # [1, 2, 4]
    report([4, 3, 2, 1], acc)           # [4, 3, 2, 2]
    report([9], acc)                    # [1, 0]
    report([9, 9], acc)                 # [1, 0, 0]
    report([9, 9, 9], acc)              # [1, 0, 0, 0]
    report([1, 9, 9], acc)              # [2, 0, 0]
    report([0], acc)                    # [1]
    report([8, 9, 9, 9], acc)           # [9, 0, 0, 0]
    report([1, 0, 0, 0], acc)           # [1, 0, 0, 1]
    report([2, 9], acc)                 # [3, 0]
    report([5, 4, 3, 2, 1], acc)        # [5, 4, 3, 2, 2]
    report([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], acc)  # [9, 8, 7, 6, 5, 4, 3, 2, 1, 1]
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()
