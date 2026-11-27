# LeetCode #1834: Single-Threaded CPU -- the bench in Python: the ★ arm over
# 50 calls on the first 50000 to 99999 of one list of 10^5 tasks, built once,
# each coming in at 1 to 10^6 and taking 1 to 10^4, each run's length drawn
# from the checksum so far. Each call copies its run, a list of two-number
# lists, as the arm takes its list by value, and the order is folded into
# the checksum.
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


def main():
    seed = 1834

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    base = []
    for _ in range(100000):
        hi = next_random()
        enqueue = 1 + (hi * 32768 + next_random()) % 1000000
        processing = 1 + next_random() % 10000
        base.append([enqueue, processing])
    check = 0
    for call in range(50):
        n = 50000 + (check + call) % 50000
        order = get_order([t[:] for t in base[:n]])
        for i in order:
            check = (check * 31 + i + 1) % 1000000007
    print(f"50 calls: checksum {check}")


main()
