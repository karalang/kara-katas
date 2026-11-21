class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def minimum_operations(root):
    total = 0
    level = [root] if root is not None else []
    while level:
        values = [n.val for n in level]
        target = {v: i for i, v in enumerate(sorted(values))}
        seen = [False] * len(values)
        for i in range(len(values)):
            length = 0
            at = i
            while not seen[at]:
                seen[at] = True
                at = target[values[at]]
                length += 1
            if length > 1:
                total += length - 1
        nxt = []
        for n in level:
            if n.left is not None:
                nxt.append(n.left)
            if n.right is not None:
                nxt.append(n.right)
        level = nxt
    return total


# ---- test harness ---------------------------------------------------------

seed = 2471


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def parse(text):
    items = [None if s == "null" else int(s) for s in text[1:-1].split(",")]
    root = TreeNode(items[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(items):
        node = queue[head]
        head += 1
        if items[i] is not None:
            node.left = TreeNode(items[i])
            queue.append(node.left)
        i += 1
        if i < len(items):
            if items[i] is not None:
                node.right = TreeNode(items[i])
                queue.append(node.right)
            i += 1
    return root


def random_tree(n):
    values = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        high = next_random()
        j = (high * 32768 + next_random()) % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = [TreeNode(v) for v in values]
    for k in range(1, n):
        high = next_random()
        at = nodes[(high * 32768 + next_random()) % k]
        while True:
            if next_random() % 2 == 0:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = nodes[k]
                    break
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = nodes[k]
                    break
    return nodes[0]


def complete_tree(n):
    values = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        high = next_random()
        j = (high * 32768 + next_random()) % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = [TreeNode(v) for v in values]
    for k in range(1, n):
        parent = nodes[(k - 1) // 2]
        if k % 2 == 1:
            parent.left = nodes[k]
        else:
            parent.right = nodes[k]
    return nodes[0]


def main():
    for text in ["[1,4,3,7,6,8,5,null,null,null,null,9,null,10]", "[1,3,2,7,6,5,4]", "[1,2,3,4,5,6]", "[5]", "[1,3,2]", "[1,2,3,5,null,6,4]", "[10,2,9,null,8,null,1,7,null,3]"]:
        print(f"{text} -> {minimum_operations(parse(text))}")
    chain = [TreeNode(100000 - i) for i in range(100000)]
    for i in range(1, 100000):
        chain[i - 1].right = chain[i]
    print(f"path of 10^5 -> {minimum_operations(chain[0])}")
    print(f"complete tree of 10^5 -> {minimum_operations(complete_tree(100000))}")
    print(f"random tree of 10^5 -> {minimum_operations(random_tree(100000))}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 40
        check = (check * 31 + minimum_operations(random_tree(n))) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
