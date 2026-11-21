# LeetCode #2415: Reverse Odd Levels of Binary Tree -- the Python mirror of
# the ★ arm: mirror pairs walked down together, the values of each pair on
# an odd level swapped.


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def swap_pairs(a, b, odd):
    if a is not None and b is not None:
        if odd:
            a.val, b.val = b.val, a.val
        swap_pairs(a.left, b.right, not odd)
        swap_pairs(a.right, b.left, not odd)


def reverse_odd_levels(root):
    if root is not None:
        swap_pairs(root.left, root.right, True)
    return root


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values):
    nodes = [TreeNode(v) for v in values]
    for i in range(len(nodes) // 2):
        nodes[i].left = nodes[2 * i + 1]
        nodes[i].right = nodes[2 * i + 2]
    return nodes[0]


def levels(root):
    queue = [root] if root is not None else []
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return [n.val for n in queue]


def show(values):
    return "[" + ",".join(str(v) for v in values) + "]"


def answer(values):
    return levels(reverse_odd_levels(build(values)))


def random_values(depth, top):
    return [(next_random() * 32768 + next_random()) % top for _ in range((1 << (depth + 1)) - 1)]


def digest(values):
    h = 0
    for v in values:
        h = (h * 31 + v) % 1000000007
    return h


def main():
    global seed
    print(show(answer([2, 3, 5, 8, 13, 21, 34])))
    print(show(answer([7, 13, 11])))
    print(show(answer([0, 1, 2, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2])))
    print(show(answer([5])))
    print(show(answer(list(range(15)))))
    seed = 2415
    print(f"{digest(answer(random_values(13, 100001)))} {digest(answer(list(range(16383))))}")
    check = 0
    total = 0
    for _ in range(2000):
        depth = next_random() % 7
        top = 1 + next_random() % 50
        got = answer(random_values(depth, top))
        if len(got) > 1:
            total += got[1] - got[2]
        check = (check * 31 + digest(got)) % 1000000007
    print(f"2000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
