"""Benchmark lane for LeetCode 317 — Python mirror of bench/shortest_distance.kara.

Build the grid once (20% obstacles, BUILDINGS buildings on corner-reachable
empty cells), then PASSES one-BFS-per-building passes, each after relocating one
building to an empty cell chosen from the checksum (moved back after).
"""

ROWS = 360
COLS = 360
BUILDINGS = 20
OBSTACLE_PCT = 20
PASSES = 30
MASK = 1073741823


def lcg(s):
    return (s * 1103515245 + 12345) & 0x7FFFFFFF


def shortest_distance(grid, rows, cols):
    n = rows * cols
    total = [0] * n
    reach = [0] * n
    seen = [0] * n
    dist = [0] * n
    b = 0
    for src in range(n):
        if grid[src] != 1:
            continue
        b += 1
        seen[src] = b
        dist[src] = 0
        q = [src]
        head = 0
        while head < len(q):
            cell = q[head]
            head += 1
            r, c = divmod(cell, cols)
            d = dist[cell] + 1
            if r > 0:
                nb = cell - cols
                if grid[nb] == 0 and seen[nb] != b:
                    seen[nb] = b; dist[nb] = d; total[nb] += d; reach[nb] += 1; q.append(nb)
            if r < rows - 1:
                nb = cell + cols
                if grid[nb] == 0 and seen[nb] != b:
                    seen[nb] = b; dist[nb] = d; total[nb] += d; reach[nb] += 1; q.append(nb)
            if c > 0:
                nb = cell - 1
                if grid[nb] == 0 and seen[nb] != b:
                    seen[nb] = b; dist[nb] = d; total[nb] += d; reach[nb] += 1; q.append(nb)
            if c < cols - 1:
                nb = cell + 1
                if grid[nb] == 0 and seen[nb] != b:
                    seen[nb] = b; dist[nb] = d; total[nb] += d; reach[nb] += 1; q.append(nb)
    best = -1
    for i in range(n):
        if grid[i] == 0 and reach[i] == b and (best < 0 or total[i] < best):
            best = total[i]
    return best


def main():
    n = ROWS * COLS
    seed = 317
    grid = [0] * n
    for i in range(n):
        seed = lcg(seed)
        grid[i] = 2 if (seed // 65536) % 100 < OBSTACLE_PCT else 0
    grid[0] = 0

    reachable = [False] * n
    q = [0]
    reachable[0] = True
    head = 0
    while head < len(q):
        cell = q[head]
        head += 1
        r, c = divmod(cell, COLS)
        if r > 0 and grid[cell - COLS] != 2 and not reachable[cell - COLS]:
            reachable[cell - COLS] = True; q.append(cell - COLS)
        if r < ROWS - 1 and grid[cell + COLS] != 2 and not reachable[cell + COLS]:
            reachable[cell + COLS] = True; q.append(cell + COLS)
        if c > 0 and grid[cell - 1] != 2 and not reachable[cell - 1]:
            reachable[cell - 1] = True; q.append(cell - 1)
        if c < COLS - 1 and grid[cell + 1] != 2 and not reachable[cell + 1]:
            reachable[cell + 1] = True; q.append(cell + 1)

    sites = []
    while len(sites) < BUILDINGS:
        seed = lcg(seed)
        p = (seed // 256) % n
        if grid[p] == 0 and reachable[p]:
            grid[p] = 1
            sites.append(p)

    checksum = 0
    for pass_ in range(PASSES):
        old = sites[pass_ % BUILDINGS]
        i = checksum % n
        while grid[i] != 0:
            i = (i + 1) % n
        grid[old] = 0
        grid[i] = 1
        ans = shortest_distance(grid, ROWS, COLS)
        checksum = (checksum * 31 + ans + 7) & MASK
        grid[i] = 0
        grid[old] = 1
    print(f"checksum {checksum}")


if __name__ == "__main__":
    main()
