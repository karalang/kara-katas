# LeetCode #317: Shortest Distance from All Buildings — Python mirror of the
# demo in shortest_distance.kara (one BFS per building, accumulate totals and
# reach counts). Same cases, same sink.
from collections import deque


def shortest_distance(grid, rows, cols):
    n = rows * cols
    buildings = sum(1 for v in grid if v == 1)
    total = [0] * n
    reach = [0] * n
    for src in range(n):
        if grid[src] != 1:
            continue
        dist = [-1] * n
        dist[src] = 0
        q = deque([src])
        while q:
            cell = q.popleft()
            r, c = divmod(cell, cols)
            d = dist[cell] + 1
            for nxt in ((cell - cols) if r > 0 else -1,
                        (cell + cols) if r < rows - 1 else -1,
                        (cell - 1) if c > 0 else -1,
                        (cell + 1) if c < cols - 1 else -1):
                if nxt < 0 or grid[nxt] != 0 or dist[nxt] >= 0:
                    continue
                dist[nxt] = d
                total[nxt] += d
                reach[nxt] += 1
                q.append(nxt)
    best = -1
    for i in range(n):
        if grid[i] == 0 and reach[i] == buildings:
            if best < 0 or total[i] < best:
                best = total[i]
    return best


def show(grid, rows, cols):
    return " / ".join(" ".join(str(grid[r * cols + c]) for c in range(cols))
                      for r in range(rows))


def main():
    cases = [
        ([1, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 3, 5),
        ([1, 0], 1, 2),
        ([1], 1, 1),
        ([1, 2, 0], 1, 3),
        ([1, 0, 0, 0, 1], 1, 5),
        ([1, 0, 1, 0, 0, 0, 1, 0, 1], 3, 3),
        ([1, 0, 2, 0, 2, 0, 2, 0, 1], 3, 3),
        ([0, 0, 0, 0, 1, 0, 0, 0, 0], 3, 3),
        ([1, 0, 0, 2, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0], 3, 5),
        ([2, 2, 2], 1, 3),
        ([0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 0, 1], 3, 4),
    ]
    acc = 0
    for tag, (grid, rows, cols) in enumerate(cases):
        ans = shortest_distance(grid, rows, cols)
        acc = (acc * 131 + ans + 2) % 1000000007
        print(f"case {tag}: {show(grid, rows, cols)} -> {ans}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
