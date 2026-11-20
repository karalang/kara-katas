# LeetCode #1240: Tiling a Rectangle with the Fewest Squares -- mirrors the
# ★ Kāra arm: backtracking on the skyline, the heights of the m columns
# filled so far. Each step finds the lowest column (the leftmost of them),
# and puts a square there of every size that fits, the largest first. A
# branch stops once it has used as many squares as the best tiling found.


def fill(heights, n, count, best):
    if count >= best[0]:
        return
    at = 0
    for j in range(1, len(heights)):
        if heights[j] < heights[at]:
            at = j
    base = heights[at]
    if base == n:
        best[0] = count
        return
    width = 0
    while at + width < len(heights) and heights[at + width] == base and width < n - base:
        width += 1
    for size in range(width, 0, -1):
        for j in range(at, at + size):
            heights[j] = base + size
        fill(heights, n, count + 1, best)
        for j in range(at, at + size):
            heights[j] = base


def tiling_rectangle(n, m):
    heights = [0] * m
    best = [n * m]
    fill(heights, n, 0, best)
    return best[0]


# ---- test harness ----------------------------------------------------------


def row(n):
    return " ".join(str(tiling_rectangle(n, m)) for m in range(1, 14))


def main():
    print(tiling_rectangle(2, 3))
    print(tiling_rectangle(5, 8))
    print(tiling_rectangle(11, 13))
    print(f"{tiling_rectangle(1, 1)} {tiling_rectangle(13, 13)} {tiling_rectangle(1, 13)} {tiling_rectangle(13, 1)}")
    print(f"11 x 1..13: {row(11)}")
    print(f"13 x 1..13: {row(13)}")
    check = 0
    total = 0
    for n in range(1, 14):
        for m in range(1, 14):
            t = tiling_rectangle(n, m)
            check = (check * 131 + t) % 1000000007
            total += t
    print(f"169 rectangles: checksum {check}, total {total}")


main()
