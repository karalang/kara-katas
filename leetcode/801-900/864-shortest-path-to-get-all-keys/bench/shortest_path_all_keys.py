# LeetCode #864: Shortest Path to Get All Keys -- Python mirror of the
# bench program (the ★ arm, breadth-first search over (cell, keys held)
# states).
from collections import deque


def shortest_path_all_keys(grid):
    rows, cols = len(grid), len(grid[0])
    cells = "".join(grid)
    size = len(cells)
    start, keys = 0, 0
    for i, ch in enumerate(cells):
        if ch == "@":
            start = i
        elif "a" <= ch <= "f":
            keys += 1
    full = (1 << keys) - 1
    seen = [False] * (size << keys)
    queue = deque()
    seen[start] = True
    queue.append((start, 0, 0))
    while queue:
        cell, held, steps = queue.popleft()
        if held == full:
            return steps
        r, c = divmod(cell, cols)
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            nxt = nr * cols + nc
            b = cells[nxt]
            if b == "#":
                continue
            if "A" <= b <= "F" and held & (1 << (ord(b) - ord("A"))) == 0:
                continue
            now = held
            if "a" <= b <= "f":
                now = held | (1 << (ord(b) - ord("a")))
            if not seen[now * size + nxt]:
                seen[now * size + nxt] = True
                queue.append((nxt, now, steps + 1))
    return -1


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    rows, cols, rounds = 30, 30, 1000
    rng = Rng(864)
    cells = ["#" if rng.next() % 100 < 20 else "." for _ in range(rows * cols)]
    for i in range(12):
        at = rng.next() % (rows * cols)
        while cells[at] != ".":
            at = rng.next() % (rows * cols)
        cells[at] = chr(ord("a") + i) if i < 6 else chr(ord("A") + i - 6)
    reached = total = check = 0
    for _ in range(rounds):
        start = rng.next() % (rows * cols)
        while cells[start] != ".":
            start = rng.next() % (rows * cols)
        cells[start] = "@"
        grid = ["".join(cells[r * cols:(r + 1) * cols]) for r in range(rows)]
        cells[start] = "."
        moves = shortest_path_all_keys(grid)
        if moves >= 0:
            reached += 1
            total += moves
        check = (check * 31 + moves + 2) % 1000000007
    print(f"{rounds} starts on a 30 by 30 grid: {reached} reach every key, moves sum to {total}, checksum {check}")


main()
