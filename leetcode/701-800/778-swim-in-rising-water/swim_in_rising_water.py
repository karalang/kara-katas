# LeetCode 778 — Swim in Rising Water, Dijkstra on the highest square.
# Mirrors swim_in_rising_water.kara (the ★ arm) and its harness.
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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(n):
    values = list(range(n * n))
    i = n * n - 1
    while i > 0:
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
        i -= 1
    return [values[r * n:(r + 1) * n] for r in range(n)]


def snake(n):
    return [[r * n + c if r % 2 == 0 else r * n + n - 1 - c for c in range(n)] for r in range(n)]


def show(grid):
    print(f"{grid} -> {swim_in_water(grid)}")


def main():
    global seed
    show([[0, 2], [1, 3]])
    show([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]])
    show([[0]])
    show([[3, 0], [1, 2]])
    show([[0, 3], [2, 1]])
    show([[0, 8, 7], [1, 6, 5], [2, 3, 4]])
    show([[0, 7, 8], [6, 1, 2], [5, 4, 3]])
    seed = 778
    print(f"random 50 x 50 -> {swim_in_water(random_grid(50))}")
    print(f"snake 50 x 50 -> {swim_in_water(snake(50))}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 20
        answer = swim_in_water(random_grid(n))
        total += answer
        check = (check * 31 + answer * 50 + n) % 1000000007
    print(f"300 random grids: answers sum to {total}, checksum {check}")


main()
