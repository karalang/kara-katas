"""LeetCode 302 — Smallest Rectangle Enclosing Black Pixels (binary search).

Mirror of smallest_rectangle.kara: same algorithm, same output.

The connectivity precondition makes the row and column projections contiguous,
so each of the four edges is binary-searchable from the seed pixel. See the
Kara file's header for why that is true and what it costs when it isn't.
"""


def row_has_black(img, w, h, r):
    return any(img[r * w + c] for c in range(w))


def col_has_black(img, w, h, c):
    return any(img[r * w + c] for r in range(h))


def _bisect(lo, hi, pred):
    """First index in [lo, hi) where pred is True (pred is monotone)."""
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def min_area(img, w, h, x, y):
    top = _bisect(0, x + 1, lambda r: row_has_black(img, w, h, r))
    bottom = _bisect(x + 1, h, lambda r: not row_has_black(img, w, h, r))
    left = _bisect(0, y + 1, lambda c: col_has_black(img, w, h, c))
    right = _bisect(y + 1, w, lambda c: not col_has_black(img, w, h, c))
    return (bottom - top) * (right - left)


def image_of(rows):
    h = len(rows)
    w = len(rows[0]) if h else 0
    return [1 if ch == "1" else 0 for row in rows for ch in row], w, h


def report(rows, x, y):
    img, w, h = image_of(rows)
    print(f"seed ({x},{y}) -> area {min_area(img, w, h, x, y)}")


def main():
    report(["0010", "0110", "0100"], 0, 2)
    report(["1"], 0, 0)
    report(["11", "11"], 1, 1)
    report(["0000", "0100", "0000"], 1, 1)
    report(["111"], 0, 1)


if __name__ == "__main__":
    main()
