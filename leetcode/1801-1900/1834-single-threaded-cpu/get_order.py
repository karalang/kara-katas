# LeetCode #1834: Single-Threaded CPU -- the ★ arm in Python, with heapq as
# the queue of (processing time, index)
import heapq


def get_order(tasks):
    n = len(tasks)
    coming = sorted(range(n), key=lambda i: tasks[i][0])
    ready = []
    order = []
    clock = 0
    nxt = 0
    while len(order) < n:
        if not ready and clock < tasks[coming[nxt]][0]:
            clock = tasks[coming[nxt]][0]
        while nxt < n and tasks[coming[nxt]][0] <= clock:
            i = coming[nxt]
            heapq.heappush(ready, (tasks[i][1], i))
            nxt += 1
        processing, i = heapq.heappop(ready)
        clock += processing
        order.append(i)
    return order


seed = 1834


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def fold(order):
    check = len(order)
    for i in order:
        check = (check * 31 + i) % 1000000007
    return check


def big():
    hi = next_random()
    return hi * 32768 + next_random()


print(show(get_order([(1, 2), (2, 4), (3, 2), (4, 1)])), show(get_order([(7, 10), (7, 12), (7, 5), (7, 4), (7, 2)])))
print(show(get_order([(5, 3)])), show(get_order([(1, 1), (10, 1), (3, 1)])), show(get_order([(1, 5), (2, 3), (2, 3), (3, 1)])), show(get_order([(4, 4), (4, 4), (4, 4)])), show(get_order([(1, 1000000000), (2, 1000000000), (3, 1000000000), (1000000000, 1)])))
spread = []
for _ in range(100000):
    a = 1 + big() % 1000000000
    spread.append((a, 1 + big() % 1000000000))
once = [(1, 1 + next_random() % 1000) for _ in range(100000)]
print(f"the most: {fold(get_order(spread))} {fold(get_order(once))}")
check = 0
for _ in range(3000):
    n = 1 + next_random() % 8
    tasks = []
    for _ in range(n):
        a = 1 + next_random() % 10
        tasks.append((a, 1 + next_random() % 5))
    check = (check * 31 + fold(get_order(tasks))) % 1000000007
print(f"3000 random cases: checksum {check}")
