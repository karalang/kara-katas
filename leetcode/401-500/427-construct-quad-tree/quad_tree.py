# LeetCode #427: Construct Quad Tree -- mirror of quad_tree.kara
# (divide, then merge). A leaf is ("leaf", value), a split is
# ("split", top_left, top_right, bottom_left, bottom_right).


def build(grid, row, col, size):
    if size == 1:
        return ("leaf", grid[row][col] == 1)
    half = size // 2
    top_left = build(grid, row, col, half)
    top_right = build(grid, row, col + half, half)
    bottom_left = build(grid, row + half, col, half)
    bottom_right = build(grid, row + half, col + half, half)
    parts = (top_left, top_right, bottom_left, bottom_right)
    if all(p[0] == "leaf" for p in parts):
        if top_left[1] == top_right[1] == bottom_left[1] == bottom_right[1]:
            return ("leaf", top_left[1])
    return ("split",) + parts


def construct(grid):
    return build(grid, 0, 0, len(grid))


# ---- test harness ---------------------------------------------------------


def serialize(root):
    parts = []
    queue = [root]
    at = 0
    while at < len(queue):
        item = queue[at]
        at += 1
        if item is None:
            parts.append("null")
        elif item[0] == "leaf":
            parts.append(f"[1,{1 if item[1] else 0}]")
            queue.extend([None] * 4)
        else:
            parts.append("[0,1]")
            queue.extend(item[1:])
    while parts and parts[-1] == "null":
        parts.pop()
    return "[" + ",".join(parts) + "]"


seed = 427


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(n):
    block = 1
    j = step() % 7
    while j > 0 and block < n:
        block *= 2
        j -= 1
    grid = [[0] * n for _ in range(n)]
    for br in range(n // block):
        for bc in range(n // block):
            v = step() % 2
            for r in range(block):
                for c in range(block):
                    grid[br * block + r][bc * block + c] = v
    flips = step() % 4
    for _ in range(flips):
        r = step() % n
        c = step() % n
        grid[r][c] = 1 - grid[r][c]
    return grid


def main():
    print(serialize(construct([[0, 1], [1, 0]])))
    print(serialize(construct([
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0],
    ])))
    print(serialize(construct([[0]])))
    print(serialize(construct([[1]])))
    print(serialize(construct([[1, 1], [1, 1]])))
    print(serialize(construct([[1, 1], [1, 0]])))
    print(serialize(construct([
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0],
    ])))
    print(serialize(construct([
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 1],
    ])))
    one = [[0] * 64 for _ in range(64)]
    one[37][22] = 1
    print(serialize(construct(one)))
    nodes = 0
    leaves = 0
    checksum = 0
    for _ in range(300):
        n = 1 << (step() % 7)
        text = serialize(construct(random_grid(n)))
        for b in text.encode():
            checksum = (checksum * 31 + b) % 1000000007
            if b == ord("["):
                nodes += 1
        leaves += len(text.split("[1,")) - 1
    print(f"300 random grids: {nodes - 300} nodes, {leaves} leaves, checksum {checksum}")


main()
