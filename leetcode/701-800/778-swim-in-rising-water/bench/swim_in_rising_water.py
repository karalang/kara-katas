# Benchmark for #778: Swim in Rising Water -- mirror of the ★ arm
# (Dijkstra on the highest square), with the same workload as the Kāra
# program.
import heapq


def swim_in_water(grid):
    n = len(grid)
    done = [False] * (n * n)
    queue = [(grid[0][0], 0)]
    while queue:
        t, at = heapq.heappop(queue)
        if done[at]:
            continue
        done[at] = True
        r, c = divmod(at, n)
        if r == n - 1 and c == n - 1:
            return t
        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not done[nr * n + nc]:
                h = grid[nr][nc]
                heapq.heappush(queue, (h if h > t else t, nr * n + nc))
    return -1


seed = 778


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n = 64, 50
    grids = []
    for g in range(count):
        values = [r * n + n - 1 - c if g % 4 == 2 and r % 2 == 1 else r * n + c for r in range(n) for c in range(n)]
        if g % 4 < 2:
            i = n * n - 1
            while i > 0:
                j = next_random() % (i + 1)
                values[i], values[j] = values[j], values[i]
                i -= 1
        else:
            for _ in range(50):
                i = next_random() % (n * n)
                j = next_random() % (n * n)
                values[i], values[j] = values[j], values[i]
        grids.append([values[r * n:(r + 1) * n] for r in range(n)])
    total = 0
    checksum = 0
    for rnd in range(3000):
        g = (rnd * 7) % count
        answer = swim_in_water(grids[g])
        total += answer
        checksum = (checksum * 31 + answer + g) % 1000000007
    print(f"3000 rounds of 50 x 50 grids: answers sum to {total}, checksum {checksum}")


main()
