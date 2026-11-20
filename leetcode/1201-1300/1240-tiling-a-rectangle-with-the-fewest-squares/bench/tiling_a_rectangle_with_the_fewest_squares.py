# LeetCode #1240: the benchmark, mirroring the Kāra file.


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


def main():
    total = 0
    check = 0
    for _ in range(200):
        for n in range(1, 14):
            for m in range(1, 14):
                t = tiling_rectangle(n, m)
                total += t
                check = (check * 131 + t) % 1000000007
    print(f"169 rectangles, 200 passes: total {total}, checksum {check}")


main()
