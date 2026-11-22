# LeetCode #2768: Number of Black Blocks -- the bench in Python: the ★ arm
# over 100 grids of 10^4 black cells, all drawn first, then each answered
# 5 times.
from math import gcd


def count_black_blocks(m, n, coordinates):
    blocks = {}
    for x, y in coordinates:
        for bx in range(max(x - 1, 0), min(x, m - 2) + 1):
            for by in range(max(y - 1, 0), min(y, n - 2) + 1):
                blocks[(bx, by)] = blocks.get((bx, by), 0) + 1
    counts = [0] * 5
    for black in blocks.values():
        counts[black] += 1
    counts[0] = (m - 1) * (n - 1) - len(blocks)
    return counts


seed = 2768


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count = 100
    rounds = 5
    grids = []
    for _ in range(count):
        side = wide() % 900 + 101
        area = side * side
        m = side + wide() % (100001 - side)
        n = side + wide() % (100001 - side)
        x0 = wide() % (m - side + 1)
        y0 = wide() % (n - side + 1)
        stride = wide() % area
        while gcd(stride, area) != 1:
            stride = wide() % area
        start = wide() % area
        cells = []
        for k in range(10000):
            at = (start + k * stride) % area
            cells.append([x0 + at // side, y0 + at % side])
        grids.append((m, n, cells))
    sums = [0] * 5
    check = 0
    for r in range(rounds):
        for m, n, cells in grids:
            counts = count_black_blocks(m, n, cells)
            for i in range(5):
                sums[i] += counts[i]
                check = (check * 31 + counts[i] % 1000000007 + r + 1) % 1000000007
    print(f"{count} grids of 10^4 cells, {rounds} rounds: counts sum to {sums}, checksum {check}")


main()
