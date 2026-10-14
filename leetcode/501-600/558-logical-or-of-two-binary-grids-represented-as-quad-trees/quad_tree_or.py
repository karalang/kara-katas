# LeetCode #558: Logical OR of Two Binary Grids Represented as
# Quad-Trees -- Python mirror of the ★ arm (recursion, then a merge);
# see quad_tree_or.kara. A leaf is ("L", value) and a split is
# ("S", top_left, top_right, bottom_left, bottom_right).


def intersect(a, b):
    if a[0] == "L":
        return a if a[1] else b
    if b[0] == "L":
        return b if b[1] else a
    parts = [intersect(a[i], b[i]) for i in range(1, 5)]
    if all(p[0] == "L" for p in parts) and len({p[1] for p in parts}) == 1:
        return ("L", parts[0][1])
    return ("S", *parts)


# ---- test harness ----------------------------------------------------------


def build(grid, row, col, size):
    if size == 1:
        return ("L", grid[row][col] == 1)
    half = size // 2
    parts = [build(grid, row, col, half), build(grid, row, col + half, half),
             build(grid, row + half, col, half), build(grid, row + half, col + half, half)]
    if all(p[0] == "L" for p in parts) and len({p[1] for p in parts}) == 1:
        return ("L", parts[0][1])
    return ("S", *parts)


def construct(grid):
    return build(grid, 0, 0, len(grid))


def serialize(root):
    parts = []
    queue = [root]
    at = 0
    while at < len(queue):
        item = queue[at]
        at += 1
        if item is None:
            parts.append("null")
        elif item[0] == "L":
            parts.append(f"[1,{1 if item[1] else 0}]")
            queue.extend([None] * 4)
        else:
            parts.append("[0,1]")
            queue.extend(item[1:])
    while parts and parts[-1] == "null":
        parts.pop()
    return "[" + ",".join(parts) + "]"


class Seed:
    def __init__(self, v):
        self.v = v

    def step(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def random_grid(n, seed):
    block = 1
    j = seed.step() % 7
    while j > 0 and block < n:
        block *= 2
        j -= 1
    grid = [[0] * n for _ in range(n)]
    for br in range(n // block):
        for bc in range(n // block):
            v = seed.step() % 2
            for r in range(block):
                for c in range(block):
                    grid[br * block + r][bc * block + c] = v
    flips = seed.step() % 4
    for _ in range(flips):
        r = seed.step() % n
        c = seed.step() % n
        grid[r][c] = 1 - grid[r][c]
    return grid


def show(one, two):
    print(serialize(intersect(construct(one), construct(two))))


def main():
    show([[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
         [[1, 1, 0, 0], [1, 1, 1, 1], [1, 1, 0, 0], [1, 1, 0, 0]])
    show([[0]], [[0]])
    board = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]
    other = [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]]
    show([[1] * 4 for _ in range(4)], board)
    show(board, [[0] * 4 for _ in range(4)])
    show(board, other)
    show([[1, 0], [0, 0]], [[0, 0], [0, 1]])
    blocks = [[1, 1, 1, 1, 0, 0, 0, 0]] * 2 + [[1] * 8] * 2 + [[1, 1, 1, 1, 0, 0, 0, 0]] * 4
    show(blocks, blocks)
    left = [[0] * 64 for _ in range(64)]
    right = [[0] * 64 for _ in range(64)]
    left[37][22] = 1
    right[37][23] = 1
    show(left, right)
    seed = Seed(558)
    nodes = 0
    leaves = 0
    checksum = 0
    for _ in range(300):
        n = 1 << (seed.step() % 7)
        one = random_grid(n, seed)
        two = random_grid(n, seed)
        text = serialize(intersect(construct(one), construct(two)))
        for b in text.encode():
            checksum = (checksum * 31 + b) % 1000000007
            if b == ord("["):
                nodes += 1
        leaves += len(text.split("[1,")) - 1
    print(f"300 random pairs: {nodes - 300} nodes, {leaves} leaves, checksum {checksum}")


main()
