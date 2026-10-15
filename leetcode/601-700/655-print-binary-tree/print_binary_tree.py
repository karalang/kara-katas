# LeetCode #655: Print Binary Tree -- each node placed from its parent.
# Mirrors the ★ arm (print_binary_tree.kara) and its test harness.


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def print_tree(root):
    h = height(root) - 1
    columns = (1 << (h + 1)) - 1
    grid = [["" for _ in range(columns)] for _ in range(h + 1)]

    def place(node, row, column):
        if node is not None:
            grid[row][column] = str(node.val)
            if row < h:
                step = 1 << (h - row - 1)
                place(node.left, row + 1, column - step)
                place(node.right, row + 1, column + step)

    place(root, 0, (columns - 1) // 2)
    return grid


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def from_level(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(values):
        n = queue[head]
        head += 1
        if values[i] is not None:
            c = TreeNode(values[i])
            n.left = c
            queue.append(c)
        i += 1
        if i < len(values):
            if values[i] is not None:
                c = TreeNode(values[i])
                n.right = c
                queue.append(c)
            i += 1
    return root


def random_tree(levels, chance, rng):
    if levels == 0:
        return None
    n = TreeNode(rng.next() % 199 - 99)
    if rng.next() % 100 < chance:
        n.left = random_tree(levels - 1, chance, rng)
    if rng.next() % 100 < chance:
        n.right = random_tree(levels - 1, chance, rng)
    return n


def checksum(grid):
    h = 0
    for row in grid:
        for cell in row:
            for b in cell.encode():
                h = (h * 131 + b) % 1000000007
            h = (h * 131 + 44) % 1000000007
        h = (h * 131 + 10) % 1000000007
    return h


def show(values):
    grid = print_tree(from_level(values))
    print(f"{len(values)} values -> {len(grid)} rows of {len(grid[0])}")
    for row in grid:
        print("  [" + ",".join(f'"{c}"' for c in row) + "]")


def main():
    show([1, 2])
    show([1, 2, 3, None, 4])
    show([5])
    show([1, None, 2, None, 3])
    show([0, -99, 99, -1, 1, -10, 10])
    rng = Rng(655)
    filled = 0
    total = 0
    for _ in range(200):
        levels = 1 + rng.next() % 6
        chance = 40 + rng.next() % 61
        grid = print_tree(random_tree(levels, chance, rng))
        filled += sum(1 for row in grid for c in row if c)
        total = (total * 7 + checksum(grid)) % 1000000007
    print(f"200 random trees: {filled} cells filled, checksum {total}")
    grid = print_tree(random_tree(10, 100, rng))
    print(f"full, 10 levels: {len(grid)} rows of {len(grid[0])}, checksum {checksum(grid)}")
    grid = print_tree(random_tree(10, 75, rng))
    print(f"sparse, up to 10 levels: {len(grid)} rows of {len(grid[0])}, checksum {checksum(grid)}")


main()
