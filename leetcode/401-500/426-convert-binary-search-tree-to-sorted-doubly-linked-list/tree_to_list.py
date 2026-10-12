# LeetCode #426: Convert Binary Search Tree to Sorted Doubly Linked List
# -- mirror of tree_to_list.kara (in-order recursion).


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def tree_to_doubly_list(root):
    first = None
    last = None

    def link(node):
        nonlocal first, last
        if node is None:
            return
        link(node.left)
        if last is not None:
            last.right = node
            node.left = last
        else:
            first = node
        last = node
        link(node.right)

    link(root)
    if first is None:
        return None
    first.left = last
    last.right = first
    return first


seed = 426


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def insert(root, val):
    if root is None:
        return Node(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root


def read(head, n):
    forward = []
    backward = []
    ok = True
    if head is not None:
        cur = head
        for _ in range(n):
            forward.append(str(cur.val))
            nxt = cur.right
            if nxt.left is None or nxt.left.val != cur.val:
                ok = False
            cur = nxt
        if cur.val != head.val:
            ok = False
        for _ in range(n):
            cur = cur.left
            backward.append(str(cur.val))
        if cur.val != head.val:
            ok = False
    elif n != 0:
        ok = False
    mark = "" if ok else " BROKEN"
    return f"[{' '.join(forward)}] back from the tail [{' '.join(backward)}]{mark}"


def show(text):
    root = None
    n = 0
    for word in text.split():
        root = insert(root, int(word))
        n += 1
    print(f"{text}: {read(tree_to_doubly_list(root), n)}")


show("4 2 5 1 3")
show("2 1 3")
show("")
show("1")
show("1 2 3 4 5")
show("5 4 3 2 1")
show("-7 100 0")
show("8 4 12 2 6 10 14 1 3 5 7 9 11 13 15")
show("3 1 2")
show("1 3 2")
total = 0
checksum = 0
for _ in range(2000):
    n = step() % 41
    used = set()
    root = None
    count = 0
    while count < n:
        v = step() % 1000 - 500
        if v not in used:
            used.add(v)
            root = insert(root, v)
            count += 1
    line = read(tree_to_doubly_list(root), n)
    total += n
    for ch in line:
        checksum = (checksum * 31 + ord(ch)) % 1000000007
print(f"2000 random trees, {total} nodes: checksum {checksum}")
