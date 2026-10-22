# LeetCode #864: Shortest Path to Get All Keys -- Python mirror of the ★
# arm (breadth-first search over (cell, keys held) states) and its harness.
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


def show(grid):
    print(f"{' / '.join(grid)} -> {shortest_path_all_keys(grid)}")


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_grid(rng, rows, cols, keys, walls):
    size = rows * cols
    cells = []
    order = []
    for i in range(size):
        cells.append("#" if rng.next() % 100 < walls else ".")
        order.append(i)
    for i in range(1, size):
        j = rng.next() % (i + 1)
        order[i], order[j] = order[j], order[i]
    cells[order[0]] = "@"
    for i in range(keys):
        cells[order[1 + i]] = chr(ord("a") + i)
        cells[order[1 + keys + i]] = chr(ord("A") + i)
    return ["".join(cells[r * cols:(r + 1) * cols]) for r in range(rows)]


def main():
    show(["@.a..", "###.#", "b.A.B"])
    show(["@..aA", "..B#.", "....b"])
    show(["@Aa"])
    show(["@aA"])
    show(["Aa@"])
    show(["@#a", "A.."])
    show(["a.@.b", "#####", "A...B"])
    show(["@.....", "#####.", "a.A..b", "######", "B....."])
    show(["b.@.a", ".###.", "..A..", ".#B#."])
    show(["@abcdef", "ABCDEF."])
    show(["fedcba@", "FEDCBA#"])
    show(["@.#ab", ".#.##", "...BA"])
    rng = Rng(864)
    for walls in (0, 20, 30, 40):
        grid = random_grid(rng, 30, 30, 6, walls)
        print(f"30 by 30, walls {walls} in 100, six keys: {shortest_path_all_keys(grid)}")
    reached = total = check = 0
    for _ in range(1000):
        rows = 1 + rng.next() % 8
        cols = 1 + rng.next() % 8
        most = (rows * cols - 1) // 2
        if most == 0:
            continue
        keys = 1 + rng.next() % min(most, 6)
        walls = rng.next() % 40
        moves = shortest_path_all_keys(random_grid(rng, rows, cols, keys, walls))
        if moves >= 0:
            reached += 1
            total += moves
        check = (check * 31 + moves + 2) % 1000000007
    print(f"1000 random grids: {reached} with every key reached, moves sum to {total}, checksum {check}")


main()
