# LeetCode #1361 bench -- Python: every node's parents counted, one root
# and no node with two, then a search from the root that must reach all n.


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


def random_case(n):
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
    return left, right


def main():
    # 20 sets of 5000 nodes made once; then 5000 questions, each set drawn
    # from the checksum so far, every answer folded into it
    sets = [random_case(5000) for _ in range(20)]
    check = 0
    for r in range(5000):
        left, right = sets[check % 20]
        got = validate_binary_tree_nodes(5000, left, right)
        check = (check * 31 + (1 if got else 0) + r) % 1000000007
    print(f"5000 questions: checksum {check}")


main()
