"""LeetCode #6: Zigzag Conversion — row-buffer (visit-by-row) approach.
O(n) time, O(n) space (one buffer per row, n chars total across all rows).

Algorithmic mirror of row_buffers.kara. Output format matches line-for-line
so the two can be diffed directly. See ../README.md § Output format.
"""

from __future__ import annotations


def convert(s: str, num_rows: int) -> list[str]:
    # Returns the zigzag-rewritten string as a flat list of single chars,
    # in row-major order. The caller stringifies / prints.
    n = len(s)
    # Pass-through cases: num_rows == 1 has no zigzag shape; num_rows >= n
    # means every char gets its own row and reading-by-row is the input.
    if num_rows <= 1 or num_rows >= n:
        return list(s)

    rows: list[list[str]] = [[] for _ in range(num_rows)]
    cur = 0
    going_down = False
    for c in s:
        rows[cur].append(c)
        # Flip direction at the top and bottom rails. Doing this before the
        # step (rather than after) keeps the first iteration's step downward
        # for any num_rows > 1.
        if cur == 0 or cur == num_rows - 1:
            going_down = not going_down
        cur += 1 if going_down else -1

    out: list[str] = []
    for row in rows:
        out.extend(row)
    return out


def report(s: str, num_rows: int) -> None:
    # See ../README.md § Output format. One glyph per line, then `---`
    # as a case separator. Both languages emit the same shape so the
    # outputs diff line-for-line.
    for c in convert(s, num_rows):
        print(c)
    print("---")


def main() -> None:
    report("PAYPALISHIRING", 3)   # expect: PAHNAPLSIIGYIR
    report("PAYPALISHIRING", 4)   # expect: PINALSIGYAHRPI
    report("A", 1)                # expect: A
    report("AB", 1)               # expect: AB
    report("", 3)                 # expect: <empty>
    report("ABCD", 2)             # expect: ACBD
    report("ABCDE", 4)            # expect: ABCED
    report("ABCDEFG", 100)        # expect: ABCDEFG  (num_rows >= len)
    report("ABCDEFGH", 3)         # expect: AEBDFHCG


if __name__ == "__main__":
    main()
