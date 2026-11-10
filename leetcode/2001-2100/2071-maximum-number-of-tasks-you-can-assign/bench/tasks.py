# LeetCode #2071: Maximum Number of Tasks You Can Assign -- Python mirror of
# the ★ arm's benchmark (tasks.kara): 12 problems of 50000 tasks and 50000
# workers, strengths up to 1000000000, 0 to 11000 pills of strength
# 10000000.
from collections import deque


def can_do(tasks, workers, k, pills, strength):
    left = pills
    waiting = deque()
    nxt = 0
    for w in workers[len(workers) - k:]:
        while nxt < k and tasks[nxt] <= w + strength:
            waiting.append(tasks[nxt])
            nxt += 1
        if not waiting:
            return False
        if waiting[0] <= w:
            waiting.popleft()
        else:
            if left == 0:
                return False
            left -= 1
            waiting.pop()
    return True


def max_task_assign(tasks, workers, pills, strength):
    tasks = sorted(tasks)
    workers = sorted(workers)
    lo, hi = 0, min(len(tasks), len(workers))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can_do(tasks, workers, mid, pills, strength):
            lo = mid
        else:
            hi = mid - 1
    return lo


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def strengths(n, low, high, seed):
    out = []
    for _ in range(n):
        a = next_random(seed)
        b = next_random(seed)
        out.append(low + (a * 32768 + b) % (high - low + 1))
    return out


def main():
    seed = [2071]
    total = 0
    check = 0
    for t in range(12):
        tasks = strengths(50000, 0, 1000000000, seed)
        workers = strengths(50000, 0, 1000000000, seed)
        a = max_task_assign(tasks, workers, t * 1000, 10000000)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"12 problems: sum {total}, checksum {check}")


main()
