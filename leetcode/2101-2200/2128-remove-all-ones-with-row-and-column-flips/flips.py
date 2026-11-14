# LeetCode #2128: Remove All Ones With Row and Column Flips -- the mirror
# of flips.kara: every row the first row or its complement, checked cell
# by cell against the first column.


def remove_ones(grid):
    first = grid[0]
    for row in grid:
        for j in range(len(row)):
            if row[j] ^ row[0] != first[j] ^ first[0]:
                return False
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def text(b):
    return "true" if b else "false"


def show(grid):
    rows = ", ".join("[" + ", ".join(map(str, r)) + "]" for r in grid)
    print(f"[{rows}] -> {text(remove_ones(grid))}")


def main():
    show([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    show([[1, 1, 0], [0, 0, 0], [0, 0, 0]])
    show([[0]])
    show([[1, 0, 1, 1]])
    show([[1], [0], [1]])
    show([[1, 1], [1, 1]])
    show([[1, 0], [0, 0]])
    seed = [2128]
    cleared = 0
    check = 0
    for rnd in range(3000):
        m = next_random(seed) % 6 + 1
        n = next_random(seed) % 6 + 1
        grid = []
        if rnd % 2 == 0:
            for _ in range(m):
                grid.append([next_random(seed) % 2 for _ in range(n)])
        else:
            columns = [next_random(seed) % 2 for _ in range(n)]
            for _ in range(m):
                r = next_random(seed) % 2
                grid.append([c ^ r for c in columns])
            if next_random(seed) % 3 == 0:
                i = next_random(seed) % m
                j = next_random(seed) % n
                grid[i][j] = 1 - grid[i][j]
        if remove_ones(grid):
            cleared += 1
            check = (check * 31 + rnd) % 1000000007
    print(f"3000 grids: {cleared} cleared, checksum {check}")
    columns = [next_random(seed) % 2 for _ in range(300)]
    big = []
    for _ in range(300):
        r = next_random(seed) % 2
        big.append([c ^ r for c in columns])
    a = remove_ones(big)
    big[299][299] = 1 - big[299][299]
    b = remove_ones(big)
    big[299][299] = 1 - big[299][299]
    big[0][0] = 1 - big[0][0]
    c = remove_ones(big)
    print(f"300 by 300: {text(a)} flipped, {text(b)} with the last cell changed, {text(c)} with the first")


main()
