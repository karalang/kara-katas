# LeetCode #2768: Number of Black Blocks -- the ★ arm in Python
# (blocks.kara): each black cell counted into every block it lies in, in
# a dict keyed by the block's top-left corner; every other block has
# none.


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


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def shuffle(cells):
    for i in range(len(cells) - 1, 0, -1):
        j = wide() % (i + 1)
        cells[i], cells[j] = cells[j], cells[i]


def fold(counts, sums, check):
    for i in range(5):
        sums[i] += counts[i]
        check = (check * 31 + counts[i] % 1000000007 + 1) % 1000000007
    return check


def main():
    print(count_black_blocks(3, 3, [[0, 0]]))
    print(count_black_blocks(3, 3, [[0, 0], [1, 1], [0, 2]]))
    print(count_black_blocks(100000, 100000, []))
    print(count_black_blocks(100000, 100000, [[0, 0], [0, 99999], [99999, 0], [99999, 99999]]))
    full = [[x, y] for x in range(100) for y in range(100)]
    board = [[x, y] for x in range(100) for y in range(100) if (x + y) % 2 == 0]
    print(count_black_blocks(100, 100, full))
    print(count_black_blocks(100, 100, board))
    sums = [0] * 5
    check = 0
    for _ in range(3000):
        m = next_random() % 5 + 2
        n = next_random() % 5 + 2
        density = next_random() % 4 + 1
        cells = []
        for x in range(m):
            for y in range(n):
                if next_random() % 5 < density:
                    cells.append([x, y])
        shuffle(cells)
        check = fold(count_black_blocks(m, n, cells), sums, check)
    print(f"3000 small grids: counts sum to {sums}, checksum {check}")
    sums = [0] * 5
    check = 0
    for _ in range(10):
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
        check = fold(count_black_blocks(m, n, cells), sums, check)
    print(f"10 grids of 10^4 cells: counts sum to {sums}, checksum {check}")


main()
