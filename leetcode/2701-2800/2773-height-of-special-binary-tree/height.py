# LeetCode #2773: Height of Special Binary Tree -- the ★ arm in Python
# (height.kara): a child is a real child unless it points straight back,
# and the height is found by recursion over the real children.
import sys

sys.setrecursionlimit(100000)


def depth(u, left, right):
    best = 0
    l = left[u]
    if l >= 0 and right[l] != u:
        best = max(best, depth(l, left, right) + 1)
    r = right[u]
    if r >= 0 and left[r] != u:
        best = max(best, depth(r, left, right) + 1)
    return best


def height_of_tree(left, right, root):
    return depth(root, left, right)


seed = 2773


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def joined(left, right, root):
    leaves = []
    stack = [root]
    while stack:
        u = stack.pop()
        if left[u] < 0 and right[u] < 0:
            leaves.append(u)
        if right[u] >= 0:
            stack.append(right[u])
        if left[u] >= 0:
            stack.append(left[u])
    l = list(left)
    r = list(right)
    k = len(leaves)
    for i in range(k):
        r[leaves[i]] = leaves[(i + 1) % k]
        l[leaves[i]] = leaves[(i + k - 1) % k]
    return l, r


def level(lst):
    n = sum(1 for v in lst if v >= 0)
    left = [-1] * n
    right = [-1] * n
    queue = [0]
    head = 0
    nxt = 1
    at = 1
    while head < len(queue):
        u = queue[head]
        head += 1
        for side in range(2):
            if at < len(lst):
                if lst[at] >= 0:
                    if side == 0:
                        left[u] = nxt
                    else:
                        right[u] = nxt
                    queue.append(nxt)
                    nxt += 1
                at += 1
    return joined(left, right, 0)


def grown(n, reach):
    left = [-1] * n
    right = [-1] * n
    for k in range(1, n):
        p = k - 1 - next_random() % min(reach, k)
        while left[p] >= 0 and right[p] >= 0:
            p = next_random() % k
        if left[p] >= 0:
            go_left = False
        elif right[p] >= 0:
            go_left = True
        else:
            go_left = next_random() % 2 == 0
        if go_left:
            left[p] = k
        else:
            right[p] = k
    return joined(left, right, 0)


def main():
    for lst in [[1, 2, 3, -1, -1, 4, 5], [1, 2], [1, 2, 3, -1, -1, 4, -1, 5, 6]]:
        left, right = level(lst)
        print(height_of_tree(left, right, 0))
    n = 10000
    chain_left = [i + 1 if i + 1 < n else -1 for i in range(n)]
    left, right = joined(chain_left, [-1] * n, 0)
    print(height_of_tree(left, right, 0))
    left = [-1] * n
    right = [-1] * n
    top = n - 8191
    for i in range(top):
        left[i] = i + 1
    for k in range(8191):
        if 2 * k + 1 < 8191:
            left[top + k] = top + 2 * k + 1
            right[top + k] = top + 2 * k + 2
    left, right = joined(left, right, 0)
    print(height_of_tree(left, right, 0))
    total = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 19 + 2
        reach = next_random() % m + 1
        left, right = grown(m, reach)
        h = height_of_tree(left, right, 0)
        total += h
        check = (check * 31 + h) % 1000000007
    print(f"3000 small trees: heights sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(20):
        reach = next_random() % 50 + 1
        left, right = grown(n, reach)
        h = height_of_tree(left, right, 0)
        total += h
        check = (check * 31 + h) % 1000000007
    print(f"20 trees of 10^4: heights sum to {total}, checksum {check}")


main()
