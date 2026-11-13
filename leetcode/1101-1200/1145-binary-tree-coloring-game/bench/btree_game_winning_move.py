# LeetCode #1145: Binary Tree Coloring Game -- the Python mirror of
# btree_game_winning_move.kara: one walk counting every subtree; at the
# first player's node its two sides and the rest of the tree are the
# three parts blue can take, and blue wins when one holds more than half.


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def count(node, x, sides):
    if node is None:
        return 0
    l = count(node.left, x, sides)
    r = count(node.right, x, sides)
    if node.val == x:
        sides[0], sides[1] = l, r
    return l + r + 1


def btree_game_winning_move(root, n, x):
    sides = [0, 0]
    count(root, x, sides)
    l, r = sides
    above = n - 1 - l - r
    return max(l, r, above) * 2 > n


seed = 1145


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(count_):
    pool = list(range(1, count_ + 1))
    for j in range(len(pool) - 1, 0, -1):
        k = next_random() % (j + 1)
        pool[j], pool[k] = pool[k], pool[j]
    root = TreeNode(pool[0])
    nodes = [root]
    for i in range(1, count_):
        c = TreeNode(pool[i])
        while True:
            at = nodes[next_random() % len(nodes)]
            if next_random() % 2 == 0:
                if at.left is None:
                    at.left = c
                    break
            elif at.right is None:
                at.right = c
                break
        nodes.append(c)
    return root


def main():
    # 20 trees of 99 nodes, built once. Each of 1000 rounds asks every tree
    # about 99 first moves drawn at random.
    trees = [random_tree(99) for _ in range(20)]
    wins = 0
    check = 0
    for _ in range(1000):
        for t in trees:
            for _ in range(99):
                x = next_random() % 99 + 1
                answer = btree_game_winning_move(t, 99, x)
                if answer:
                    wins += 1
                check = (check * 31 + x + (1 if answer else 0)) % 1000000007
    print(f"1000 rounds over 20 trees of 99 nodes: blue wins {wins}, checksum {check}")


main()
