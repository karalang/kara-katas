"""LeetCode 296 - Best Meeting Point.

Mirror of best_meeting_point.kara: same separability, same median, same
free-sort trick - the row coordinates come out ascending because the outer
loop is the row, and the column coordinates come out ascending because the
second pass makes the column the outer loop. No sort() call anywhere, in
either language, which is the whole point of scanning twice.
"""


def at(data: list[int], w: int, r: int, c: int) -> int:
    return data[r * w + c]


def row_coords(data: list[int], h: int, w: int) -> list[int]:
    return [r for r in range(h) for c in range(w) if at(data, w, r, c)]


def col_coords(data: list[int], h: int, w: int) -> list[int]:
    return [c for c in range(w) for r in range(h) if at(data, w, r, c)]


def min_deviation(xs: list[int]) -> int:
    """Minimum of sum |x - p| for an ASCENDING list; the median attains it."""
    if not xs:
        return 0
    m = xs[len(xs) // 2]
    return sum(abs(x - m) for x in xs)


def min_total_distance(data: list[int], h: int, w: int) -> int:
    return min_deviation(row_coords(data, h, w)) + min_deviation(col_coords(data, h, w))


def meeting_point(data: list[int], h: int, w: int) -> tuple[int, int]:
    rows = row_coords(data, h, w)
    cols = col_coords(data, h, w)
    if not rows:
        return (0, 0)
    return (rows[len(rows) // 2], cols[len(cols) // 2])


def parse(rows: list[str]) -> tuple[list[int], int, int]:
    h = len(rows)
    w = len(rows[0]) if h else 0
    data = [1 if rows[r][c] == "1" else 0 for r in range(h) for c in range(w)]
    return data, h, w


def report(label: str, grid: list[str]) -> None:
    data, h, w = parse(grid)
    mr, mc = meeting_point(data, h, w)
    print(f"{label} -> {min_total_distance(data, h, w)}  (meet at {mr},{mc})")


def main() -> None:
    report("cross      ", ["10001", "00000", "00100"])
    report("single     ", ["0100"])
    report("pair-row   ", ["1001"])
    report("pair-col   ", ["1", "0", "0", "1"])
    report("all-ones   ", ["111", "111", "111"])
    report("diagonal   ", ["100", "010", "001"])
    report("corners    ", ["101", "000", "101"])
    report("empty      ", ["000", "000"])
    report("column     ", ["1", "1", "1", "1", "1"])
    report("sparse-wide", ["1000000001"])


if __name__ == "__main__":
    main()
