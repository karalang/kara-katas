# LeetCode #2071: Maximum Number of Tasks You Can Assign -- the Python
# mirror of tasks.kara (the ★ arm): a binary search on the number of
# tasks, each tested with the weakest of the strongest workers first and
# the tasks a pill brings in reach waiting in a deque.
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


# ---- test harness ----------------------------------------------------------

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
    examples = [
        ([3, 2, 1], [0, 3, 3], 1, 1),
        ([5, 4], [0, 0, 0], 1, 5),
        ([10, 15, 30], [0, 10, 10, 10, 10], 3, 10),
        ([5, 9, 8, 5, 9], [1, 6, 4, 2, 6], 1, 5),
        ([1], [0], 0, 5),
        ([1], [0], 1, 1),
        ([4, 4, 4], [1, 2, 3, 4, 5], 2, 2),
        ([1000000000], [0, 999999999], 1, 1),
    ]
    for tasks, workers, pills, strength in examples:
        print(f"{len(tasks)} tasks, {len(workers)} workers, {pills} pills of {strength} -> {max_task_assign(tasks, workers, pills, strength)}")
    seed = [2071]
    total = 0
    check = 0
    for _ in range(300):
        n = next_random(seed) % 40 + 1
        m = next_random(seed) % 40 + 1
        top = [20, 1000000000][next_random(seed) % 2]
        tasks = strengths(n, 0, top, seed)
        workers = strengths(m, 0, top, seed)
        pills = next_random(seed) % (m + 1)
        a = next_random(seed)
        b = next_random(seed)
        strength = (a * 32768 + b) % (top + 1)
        ans = max_task_assign(tasks, workers, pills, strength)
        total += ans
        check = (check * 31 + ans) % 1000000007
    print(f"300 problems: sum {total}, checksum {check}")
    tasks = strengths(50000, 0, 1000000000, seed)
    workers = strengths(50000, 0, 1000000000, seed)
    print(f"50000 tasks, 50000 workers, 1000 pills of 10000000 -> {max_task_assign(tasks, workers, 1000, 10000000)}")


main()
