# LeetCode #1145: Binary Tree Coloring Game -- the Python mirror of
# btree_game_winning_move.kara: one walk counting every subtree; at the
# first player's node its two sides and the rest of the tree are the
# three parts blue can take, and blue wins when one holds more than half.
import sys

sys.setrecursionlimit(10000)
seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def parse(text):
    inner = text[1:-1]
    if not inner:
        return None
    items = [None if s == "null" else int(s) for s in inner.split(",")]
    root = TreeNode(items[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(items):
        node = queue[head]
        head += 1
        if items[i] is not None:
            c = TreeNode(items[i])
            node.left = c
            queue.append(c)
        i += 1
        if i < len(items):
            if items[i] is not None:
                c = TreeNode(items[i])
                node.right = c
                queue.append(c)
            i += 1
    return root


def random_tree(count_, deep):
    pool = list(range(1, count_ + 1))
    for j in range(len(pool) - 1, 0, -1):
        k = next_random() % (j + 1)
        pool[j], pool[k] = pool[k], pool[j]
    root = TreeNode(pool[0])
    nodes = [root]
    for i in range(1, count_):
        c = TreeNode(pool[i])
        while True:
            if deep and next_random() % 2 == 0:
                at = nodes[-1]
            else:
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


def full_tree(count_):
    return "[" + ",".join(str(v) for v in range(1, count_ + 1)) + "]"


def chain(count_):
    root = TreeNode(1)
    at = root
    for v in range(2, count_ + 1):
        c = TreeNode(v)
        at.left = c
        at = c
    return root


def b(v):
    return "true" if v else "false"


def main():
    global seed
    cases = [
        ("[1,2,3,4,5,6,7,8,9,10,11]", 11, 3),
        ("[1,2,3]", 3, 1),
        ("[1]", 1, 1),
        ("[1,2,null,3,null,4,null,5]", 5, 3),
        ("[1,2,null,3,null,4,null,5]", 5, 1),
        ("[1,2,3,4,5,6,7]", 7, 1),
        ("[1,2,3,4,5,6,7]", 7, 2),
    ]
    for tree, n, x in cases:
        print(f"{tree} n = {n} x = {x} -> {b(btree_game_winning_move(parse(tree), n, x))}")
    seed = 1145
    wins = 0
    check = 0
    for t in range(2000):
        n = 2 * (next_random() % 50) + 1
        root = random_tree(n, t % 2 == 1)
        x = next_random() % n + 1
        answer = btree_game_winning_move(root, n, x)
        if answer:
            wins += 1
        check = (check * 31 + x + (1 if answer else 0)) % 1000000007
    print(f"2000 random trees: blue wins {wins}, checksum {check}")
    print(f"99 full, x = 1: {b(btree_game_winning_move(parse(full_tree(99)), 99, 1))}")
    print(f"99 full, x = 2: {b(btree_game_winning_move(parse(full_tree(99)), 99, 2))}")
    print(f"99 in a chain, x = 50: {b(btree_game_winning_move(chain(99), 99, 50))}")
    big = random_tree(99, False)
    losing = [x for x in range(1, 100) if not btree_game_winning_move(big, 99, x)]
    print(f"99 random, x from 1 to 99: blue loses only at [{', '.join(map(str, losing))}]")


main()
