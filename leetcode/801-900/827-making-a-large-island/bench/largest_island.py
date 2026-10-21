# Benchmark for #827: Making A Large Island -- the ★ arm (label, then try each 0).
#
# Mirrors largest_island.kara: a breadth-first search on a deque gives
# every island a label and records its size, and each 0 adds 1 to the
# sizes of the distinct labels around it.

from collections import deque


def largest_island(grid):
    n = len(grid)
    label = [[0] * n for _ in range(n)]
    size = []
    dr = (-1, 1, 0, 0)
    dc = (0, 0, -1, 1)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1 and label[r][c] == 0:
                ident = len(size) + 1
                label[r][c] = ident
                queue = deque([(r, c)])
                count = 0
                while queue:
                    cr, cc = queue.popleft()
                    count += 1
                    for k in range(4):
                        nr = cr + dr[k]
                        nc = cc + dc[k]
                        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1 and label[nr][nc] == 0:
                            label[nr][nc] = ident
                            queue.append((nr, nc))
                size.append(count)
    best = max(size, default=0)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                seen = []
                made = 1
                for k in range(4):
                    nr = r + dr[k]
                    nc = c + dc[k]
                    if 0 <= nr < n and 0 <= nc < n:
                        ident = label[nr][nc]
                        if ident > 0 and ident not in seen:
                            seen.append(ident)
                            made += size[ident - 1]
                best = max(best, made)
    return best


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    count = 16
    rounds = 200
    n = 500
    rng = Random(827)
    grids = []
    for _ in range(count):
        grids.append([[1 if rng.next() % 100 < 55 else 0 for _ in range(n)] for _ in range(n)])
    total = 0
    checksum = 0
    for r in range(rounds):
        res = largest_island(grids[r % count])
        total += res
        checksum = (checksum * 131 + res) % 1000000007
    print(f"{rounds} rounds of {count} grids: total {total}, checksum {checksum}")


main()
