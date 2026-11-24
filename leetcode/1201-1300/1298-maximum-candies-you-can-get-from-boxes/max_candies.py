# LeetCode #1298: Maximum Candies You Can Get from Boxes -- Python mirror of
# the ★ arm (a breadth-first walk over the boxes that can be opened, each
# queued once, when it is both held and open).
from collections import deque


def max_candies(status, candies, keys, contained_boxes, initial_boxes):
    n = len(status)
    open_ = [s == 1 for s in status]
    held = [False] * n
    queued = [False] * n
    queue = deque()
    for b in initial_boxes:
        held[b] = True
        if open_[b] and not queued[b]:
            queued[b] = True
            queue.append(b)
    total = 0
    while queue:
        b = queue.popleft()
        total += candies[b]
        for k in keys[b]:
            open_[k] = True
            if held[k] and not queued[k]:
                queued[k] = True
                queue.append(k)
        for c in contained_boxes[b]:
            held[c] = True
            if open_[c] and not queued[c]:
                queued[c] = True
                queue.append(c)
    return total


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def make_case(n, open_in, initial_in, nest, max_keys):
    order = list(range(n))
    for i in range(n):
        j = i + next_random() % (n - i)
        order[i], order[j] = order[j], order[i]
    status = [0] * n
    candies = [0] * n
    keys = [[] for _ in range(n)]
    contained = [[] for _ in range(n)]
    initial = []
    for i in range(n):
        b = order[i]
        roll = next_random() % 100
        if i > 0 and roll < nest:
            parent = order[next_random() % i]
            contained[parent].append(b)
        elif next_random() % 100 < initial_in:
            initial.append(b)
        if next_random() % 100 < open_in:
            status[b] = 1
        candies[b] = 1 + next_random() % 1000
        count = next_random() % (max_keys + 1)
        for _ in range(count):
            k = next_random() % n
            if k not in keys[b]:
                keys[b].append(k)
    return status, candies, keys, contained, initial


def main():
    global seed
    e1 = max_candies([1, 0, 1, 0], [7, 5, 4, 100], [[], [], [1], []], [[1, 2], [3], [], []], [0])
    e2 = max_candies([1, 0, 0, 0, 0, 0], [1] * 6, [[1, 2, 3, 4, 5], [], [], [], [], []], [[1, 2, 3, 4, 5], [], [], [], [], []], [0])
    none = max_candies([1, 1], [5, 6], [[], []], [[], []], [])
    early = max_candies([1, 1, 0], [1, 10, 100], [[2], [], []], [[1], [2], []], [0])
    inside = max_candies([1, 0], [1, 10], [[], [1]], [[1], []], [0])
    print(f"{e1} {e2} {none} {early} {inside}")
    seed = 1298
    total = 0
    check = 0
    for i in range(3002):
        n = 1 + next_random() % 60 if i < 3000 else 1000
        open_in = next_random() % 101
        initial_in = next_random() % 101
        nest = next_random() % 101
        max_keys = next_random() % 6
        got = max_candies(*make_case(n, open_in, initial_in, nest, max_keys))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"3002 random cases: candies total {total}, checksum {check}")


main()
