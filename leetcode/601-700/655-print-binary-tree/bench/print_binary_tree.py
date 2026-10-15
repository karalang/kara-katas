# Benchmark for #655: each node placed from its parent, as the Kara ★ arm.


class TreeNode:
    __slots__ = ("val", "left", "right")

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


seed = 655


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(levels, chance):
    if levels == 0:
        return None
    n = TreeNode(next_random() % 199 - 99)
    if next_random() % 100 < chance:
        n.left = random_tree(levels - 1, chance)
    if next_random() % 100 < chance:
        n.right = random_tree(levels - 1, chance)
    return n


def main():
    inputs = 8
    rounds = 10000
    trees = [random_tree(10, 85) for _ in range(inputs)]
    cells = 0
    checksum = 0
    for r in range(rounds):
        grid = print_tree(trees[(r * 3) % inputs])
        filled = 0
        chars = 0
        for row in grid:
            for cell in row:
                if len(cell) > 0:
                    filled += 1
                    chars += len(cell)
        cells += len(grid) * len(grid[0])
        checksum = (checksum * 31 + filled * 1000 + chars) % 1000000007
    print(f"{inputs} trees, {rounds} rounds: {cells} cells, checksum {checksum}")


main()
