# LeetCode #2196: Create Binary Tree From Descriptions -- Python mirror of
# create.kara (the ★ arm): one pass over the descriptions, each value's
# node made the first time it is named and kept in a dict, the child hung
# on its parent's side, and every child put in a set; the root is the one
# parent never named as a child. O(n).


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def node_of(nodes, v):
    if v in nodes:
        return nodes[v]
    n = TreeNode(v)
    nodes[v] = n
    return n


def create_binary_tree(descriptions):
    nodes = {}
    children = set()
    for d in descriptions:
        parent = node_of(nodes, d[0])
        child = node_of(nodes, d[1])
        if d[2] == 1:
            parent.left = child
        else:
            parent.right = child
        children.add(d[1])
    for d in descriptions:
        if d[0] not in children:
            return nodes[d[0]]
    return None


# ---- test harness ---------------------------------------------------------

seed = 2196


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def level_order(root):
    items = []
    queue = [root]
    head = 0
    while head < len(queue):
        at = queue[head]
        head += 1
        if at is not None:
            items.append(str(at.val))
            queue.append(at.left)
            queue.append(at.right)
        else:
            items.append("null")
    while items and items[-1] == "null":
        items.pop()
    return "[" + ",".join(items) + "]"


def random_descriptions(n, top):
    used = set()
    values = []
    while len(values) < n:
        v = wide_random() % top + 1
        if v not in used:
            used.add(v)
            values.append(v)
    free = [(0, 1), (0, 0)]
    descriptions = []
    for k in range(1, n):
        pick = wide_random() % len(free)
        p, side = free[pick]
        free[pick] = free[-1]
        free.pop()
        descriptions.append([values[p], values[k], side])
        free.append((k, 1))
        free.append((k, 0))
    for i in range(len(descriptions) - 1, 0, -1):
        j = wide_random() % (i + 1)
        descriptions[i], descriptions[j] = descriptions[j], descriptions[i]
    return descriptions


def show(descriptions):
    text = "[" + ", ".join("[" + ", ".join(str(x) for x in d) + "]" for d in descriptions) + "]"
    print(f"{text} -> {level_order(create_binary_tree(descriptions))}")


def checksum(text, check=0):
    for c in text:
        check = (check * 31 + ord(c)) % 1000000007
    return check


def main():
    show([[20, 15, 1], [20, 17, 0], [50, 20, 1], [50, 80, 0], [80, 19, 1]])
    show([[1, 2, 1], [2, 3, 0], [3, 4, 1]])
    show([[7, 3, 0]])
    show([[1, 2, 0], [2, 3, 0], [3, 4, 0], [4, 5, 0]])
    show([[2, 4, 1], [2, 5, 0], [3, 6, 1], [3, 7, 0], [1, 2, 1], [1, 3, 0]])
    show([[9, 8, 1], [8, 7, 0], [7, 6, 1], [6, 5, 0]])
    check = 0
    nodes = 0
    for rnd in range(2000):
        n = next_random() % 59 + 2
        top = 100 if rnd % 2 == 0 else 100000
        text = level_order(create_binary_tree(random_descriptions(n, top)))
        nodes += n
        check = checksum(text, check)
    print(f"2000 trees of {nodes} nodes: checksum {check}")
    big = level_order(create_binary_tree(random_descriptions(10001, 100000)))
    print(f"10^4 random descriptions: {len(big)} characters, checksum {checksum(big)}")
    chain = [[v, v + 1, v % 2] for v in range(10000, 0, -1)]
    long = level_order(create_binary_tree(chain))
    print(f"a chain of 10^4: {len(long)} characters, starts {long[:12]}, ends {long[-12:]}")


main()
