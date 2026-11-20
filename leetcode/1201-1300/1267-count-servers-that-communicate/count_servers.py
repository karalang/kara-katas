# LeetCode #1267: Count Servers that Communicate -- Python mirror of the ★
# arm (servers counted per row and column, then a server communicates when
# its row or column holds another), with the same harness.


def count_servers(grid):
    m, n = len(grid), len(grid[0])
    rows = [sum(r) for r in grid]
    cols = [sum(grid[r][c] for r in range(m)) for c in range(n)]
    return sum(1 for r in range(m) for c in range(n) if grid[r][c] == 1 and (rows[r] > 1 or cols[c] > 1))


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_grid(m, n, odds, rng):
    return [[1 if rng.next() % odds == 0 else 0 for _ in range(n)] for _ in range(m)]


def main():
    one = count_servers([[1, 0], [0, 1]])
    two = count_servers([[1, 0], [1, 1]])
    three = count_servers([[1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    print(f"{one} {two} {three}")
    rng = Rng(1267)
    total = check = 0
    for _ in range(2000):
        m = rng.next() % 12 + 1
        n = rng.next() % 12 + 1
        odds = rng.next() % 8 + 2
        got = count_servers(random_grid(m, n, odds, rng))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random grids: {total} servers communicate, checksum {check}")
    full = [[1] * 250 for _ in range(250)]
    diagonal = [[1 if r == c else 0 for c in range(250)] for r in range(250)]
    print(f"{count_servers(full)} {count_servers(diagonal)} {count_servers(random_grid(250, 250, 30, rng))}")


main()
