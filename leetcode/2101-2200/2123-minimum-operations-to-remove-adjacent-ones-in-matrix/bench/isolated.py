# LeetCode #2123: Minimum Operations to Remove Adjacent Ones in Matrix --
# the benchmark, the same algorithm as isolated.kara: the ones a bipartite
# graph by the parity of row plus column, the answer a maximum matching
# grown by Kuhn's augmenting paths.
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


def main():
    seed = [2123]
    grids = []
    for g in range(12):
        chance = [1, 2, 3][g % 3]
        grids.append([[1 if next_random(seed) % 4 < chance else 0 for _ in range(300)] for _ in range(300)])
    total = 0
    check = 0
    for rnd in range(10):
        for g in range(12):
            cell = (rnd * 7919 + g * 104729) % 90000
            grids[g][cell // 300][cell % 300] = 1 - grids[g][cell // 300][cell % 300]
            got = minimum_operations(grids[g])
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"120 solves: {total} operations, checksum {check}")


main()
