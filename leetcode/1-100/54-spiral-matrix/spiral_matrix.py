"""LeetCode #54: Spiral Matrix — algorithmic mirror of spiral_boundary.kara (the ★ solver).

Boundary shrinking: hold four walls `top / bottom / left / right`, walk the top row left→right,
the right column top→bottom, the bottom row right→left, the left column bottom→top, and shrink
the corresponding wall after each pass. The two `if top <= bottom` / `if left <= right` guards
before the bottom-row and left-column passes are what keep a single leftover row or column from
being emitted twice. Prints one bracketed spiral per test case plus a `sums:` line of per-case
positional checksums (`Σ (k+1)·seq[k]`), so this oracle diffs byte-for-byte against `karac run`
/ `karac build` output for all three .kara solvers (which all reach the identical order).
"""

from __future__ import annotations


def spiral_order(m: list[list[int]]) -> list[int]:
    out: list[int] = []
    top, bottom = 0, len(m) - 1
    left, right = 0, len(m[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):        # top row, left → right
            out.append(m[top][c])
        top += 1
        for r in range(top, bottom + 1):        # right column, top → bottom
            out.append(m[r][right])
        right -= 1
        if top <= bottom:                       # bottom row, right → left
            for c in range(right, left - 1, -1):
                out.append(m[bottom][c])
            bottom -= 1
        if left <= right:                       # left column, bottom → top
            for r in range(bottom, top - 1, -1):
                out.append(m[r][left])
            left += 1
    return out


CASES: list[list[list[int]]] = [
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],                     # 3×3 square
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],         # 3×4 wide
    [[1]],                                                  # 1×1
    [[1, 2], [3, 4]],                                       # 2×2
    [[1, 2, 3, 4, 5]],                                      # 1×5 single row
    [[1], [2], [3], [4]],                                   # 4×1 single column
    [[7, 9, 6]],                                            # 1×3 single row
    [[1, 2], [3, 4], [5, 6], [7, 8]],                       # 4×2 tall
    [[1, 2, 3, 4, 5],                                       # 5×5 deep spiral
     [16, 17, 18, 19, 6],
     [15, 24, 25, 20, 7],
     [14, 23, 22, 21, 8],
     [13, 12, 11, 10, 9]],
    [[-1, -2], [-3, -4]],                                   # 2×2 negatives
    [[1, 2, 3], [4, 5, 6]],                                 # 2×3 wide
    [[3], [2]],                                             # 2×1 tall
]


def main() -> None:
    parts = ["sums:"]
    for m in CASES:
        seq = spiral_order(m)
        print("[" + ", ".join(str(x) for x in seq) + "]")
        chk = sum((k + 1) * v for k, v in enumerate(seq))
        parts.append(str(chk))
    print(" ".join(parts))


if __name__ == "__main__":
    main()
