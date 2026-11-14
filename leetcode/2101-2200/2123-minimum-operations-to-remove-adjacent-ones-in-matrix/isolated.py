# LeetCode #2123: Minimum Operations to Remove Adjacent Ones in Matrix --
# the mirror of isolated.kara: the ones a bipartite graph by the parity
# of row plus column, the answer a maximum matching (König), grown by
# Kuhn's augmenting paths with a stamp per round.
import sys

sys.setrecursionlimit(200000)


def try_match(u, adj, partner, seen, stamp):
    for v in adj[u]:
        if seen[v] == stamp:
            continue
        seen[v] = stamp
        if partner[v] < 0 or try_match(partner[v], adj, partner, seen, stamp):
            partner[v] = u
            return True
    return False


def minimum_operations(grid):
    rows = len(grid)
    cols = len(grid[0])
    adj = [[] for _ in range(rows * cols)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0 or (r + c) % 2 != 0:
                continue
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    adj[r * cols + c].append(nr * cols + nc)
    partner = [-1] * (rows * cols)
    seen = [-1] * (rows * cols)
    matched = 0
    for u in range(rows * cols):
        if adj[u] and try_match(u, adj, partner, seen, u):
            matched += 1
    return matched


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(grid):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in grid) + "]"


def main():
    examples = [
        [[1, 1, 0], [0, 1, 1], [1, 1, 1]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 1], [1, 0]],
        [[1]],
        [[1, 1, 1, 1, 1]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    ]
    for grid in examples:
        print(f"{show(grid)} -> {minimum_operations(grid)}")
    seed = [2123]
    total = 0
    check = 0
    for rnd in range(1000):
        rows = next_random(seed) % 8 + 1
        cols = next_random(seed) % 8 + 1
        chance = [1, 2, 3][rnd % 3]
        grid = [[1 if next_random(seed) % 4 < chance else 0 for _ in range(cols)] for _ in range(rows)]
        got = minimum_operations(grid)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"1000 grids: {total} operations, checksum {check}")
    full = [[1] * 300 for _ in range(300)]
    print(f"300 by 300 ones: {minimum_operations(full)}")
    half = [[next_random(seed) % 2 for _ in range(300)] for _ in range(300)]
    print(f"300 by 300 half ones: {minimum_operations(half)}")


main()
