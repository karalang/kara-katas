# LeetCode #1361: Validate Binary Tree Nodes -- Python mirror of the ★ arm:
# every node's parents counted, exactly one root and no node with two, then
# a search from the root must reach all n nodes, none twice.


def validate_binary_tree_nodes(n, left_child, right_child):
    parents = [0] * n
    for i in range(n):
        for child in (left_child[i], right_child[i]):
            if child != -1:
                parents[child] += 1
    root = -1
    for i in range(n):
        if parents[i] > 1:
            return False
        if parents[i] == 0:
            if root != -1:
                return False
            root = i
    if root == -1:
        return False
    seen = [False] * n
    queue = [root]
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        if seen[node]:
            return False
        seen[node] = True
        for child in (left_child[node], right_child[node]):
            if child != -1:
                queue.append(child)
    return head == n


seed = 1361


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_case():
    n = 1 + next_random() % 40
    left = [-1] * n
    right = [-1] * n
    order = list(range(n))
    for i in range(1, n):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    for i in range(1, n):
        while True:
            parent = order[next_random() % i]
            if next_random() % 2 == 0:
                if left[parent] == -1:
                    left[parent] = order[i]
                    break
            elif right[parent] == -1:
                right[parent] = order[i]
                break
    node = next_random() % n
    other = next_random() % n
    kind = next_random() % 6
    if kind == 0:
        if left[node] == -1:
            left[node] = other
        elif right[node] == -1:
            right[node] = other
    elif kind == 1:
        left[node] = -1
    elif kind == 2:
        if right[node] != -1:
            right[node] = other
    return n, left, right


def b(x):
    return "true" if x else "false"


def main():
    v = validate_binary_tree_nodes
    print(" ".join(b(x) for x in [
        v(4, [1, -1, 3, -1], [2, -1, -1, -1]),
        v(4, [1, -1, 3, -1], [2, 3, -1, -1]),
        v(2, [1, 0], [-1, -1]),
        v(1, [-1], [-1]),
        v(3, [1, -1, -1], [2, 2, -1]),
        v(2, [-1, -1], [-1, -1]),
        v(2, [1, -1], [-1, 1]),
        v(4, [1, 2, -1, -1], [-1, -1, 1, -1]),
    ]))
    valid = 0
    check = 0
    for _ in range(2000):
        n, left, right = random_case()
        got = v(n, left, right)
        if got:
            valid += 1
        check = (check * 131 + n + (1 if got else 0)) % 1000000007
    print(f"2000 random cases: {valid} valid, checksum {check}")


main()
