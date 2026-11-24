# LeetCode #1298 bench: the ★ arm (a breadth-first walk over the boxes that
# can be opened, each queued once, when it is both held and open) over 100
# cases of 1000 boxes, built once; then 5000 passes, each flipping one box of
# every case between open and locked, chosen from the checksum so far,
# answering it, and folding the answer into the checksum.
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
    seed = 1298
    cases = []
    for t in range(100):
        cases.append(make_case(1000, 10 + t % 40, 5 + t % 20, 60 + t % 40, 1 + t % 4))
    check = 0
    for p in range(5000):
        for t in range(len(cases)):
            status, candies, keys, contained, initial = cases[t]
            b = check % 1000
            status[b] = 1 - status[b]
            got = max_candies(status, candies, keys, contained, initial)
            check = (check * 31 + got + p) % 1000000007
    print(f"5000 passes over 100 cases of 1000 boxes: checksum {check}")


main()
