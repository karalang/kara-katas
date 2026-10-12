# LeetCode #404: Sum of Left Leaves -- mirror of sum_of_left_leaves.kara
# (recursion over the index pool, carrying whether a node is a left child).

NULL = None


def visit(nodes, node, is_left):
    if node == -1:
        return 0
    val, left, right = nodes[node]
    if left == -1 and right == -1:
        return val if is_left else 0
    return visit(nodes, left, True) + visit(nodes, right, False)


def sum_of_left_leaves(nodes):
    if not nodes:
        return 0
    return visit(nodes, 0, False)


def build(vals):
    nodes = []
    if not vals or vals[0] is NULL:
        return nodes
    nodes.append([vals[0], -1, -1])
    queue = [0]
    head = 0
    i = 1
    while head < len(queue) and i < len(vals):
        cur = queue[head]
        head += 1
        if vals[i] is not NULL:
            nodes.append([vals[i], -1, -1])
            nodes[cur][1] = len(nodes) - 1
            queue.append(len(nodes) - 1)
        i += 1
        if i < len(vals) and vals[i] is not NULL:
            nodes.append([vals[i], -1, -1])
            nodes[cur][2] = len(nodes) - 1
            queue.append(len(nodes) - 1)
        i += 1
    return nodes


seed = 404


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(vals):
    text = "[" + ", ".join("null" if v is NULL else str(v) for v in vals) + "]"
    print(f"{text}: {sum_of_left_leaves(build(vals))}")


show([3, 9, 20, NULL, NULL, 15, 7])
show([1])
show([])
show([1, 2])
show([1, NULL, 2])
show([1, 2, 3, 4, 5])
show([1, NULL, 2, NULL, 3])
show([1, 2, NULL, 3, NULL, 4])
show([1, NULL, 2, 3])
show([-1, -2, -3, -4, NULL, -5, -6])
show(list(range(1, 16)))
total = 0
checksum = 0
for case in range(2000):
    n = 1 + step() % 60
    nodes = [[step() % 201 - 100, -1, -1]]
    for i in range(1, n):
        while True:
            p = step() % i
            side = 1 + step() % 2
            if nodes[p][side] == -1:
                break
        nodes.append([step() % 201 - 100, -1, -1])
        nodes[p][side] = i
    s = sum_of_left_leaves(nodes)
    total += s
    checksum = (checksum * 31 + s + 10000) % 1000000007
print(f"2000 random trees: total {total}, checksum {checksum}")
