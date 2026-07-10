"""LeetCode #74: Search a 2D Matrix — flattened binary search, O(log(m*n)).

Mirror of search_a_2d_matrix.kara. The doubly-sorted matrix reads row-major as a
single ascending sequence, so one binary search over 0 .. m*n-1 finds the target;
index mid maps to a cell by (mid // cols, mid % cols). Same fourteen queries and
the same output shape (one `search(t) = true/false` per line — lowercase to match
Kāra's bool printing — then a `res:` fold of 1/0 hits) so the files diff
line-for-line. (The two-phase and staircase variants live only in Kāra; this
mirror tracks the star.)
"""

from __future__ import annotations


def search_matrix(m: list[list[int]], target: int) -> bool:
    rows = len(m)
    if rows == 0:
        return False
    cols = len(m[0])
    if cols == 0:
        return False

    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        v = m[mid // cols][mid % cols]
        if v == target:
            return True
        elif v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def report(m: list[list[int]], target: int, acc: list[str]) -> None:
    found = search_matrix(m, target)
    print(f"search({target}) = {'true' if found else 'false'}")
    acc.append("1" if found else "0")


def main() -> None:
    acc: list[str] = []

    a = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    report(a, 3, acc)
    report(a, 13, acc)
    report(a, 1, acc)
    report(a, 60, acc)
    report(a, 0, acc)
    report(a, 100, acc)
    report(a, 16, acc)
    report(a, 22, acc)

    b = [[5]]
    report(b, 5, acc)
    report(b, 4, acc)

    c = [[1, 2, 3, 4, 5]]
    report(c, 4, acc)
    report(c, 6, acc)

    d = [[1], [3], [5], [7]]
    report(d, 5, acc)
    report(d, 6, acc)

    print("res: " + " ".join(acc))


if __name__ == "__main__":
    main()
