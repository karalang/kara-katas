# LeetCode #1306: Jump Game III -- the Python mirror of the ★ arm (a
# breadth-first walk from the start, each place queued once), with the same
# harness.
from collections import deque


def can_reach(arr, start):
    n = len(arr)
    seen = [False] * n
    queue = deque([start])
    seen[start] = True
    while queue:
        i = queue.popleft()
        if arr[i] == 0:
            return True
        for j in (i + arr[i], i - arr[i]):
            if 0 <= j < n and not seen[j]:
                seen[j] = True
                queue.append(j)
    return False


seed = 1306


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(b):
    return "true" if b else "false"


def main():
    e1 = can_reach([4, 2, 3, 0, 3, 1, 2], 5)
    e2 = can_reach([4, 2, 3, 0, 3, 1, 2], 0)
    e3 = can_reach([3, 0, 2, 1, 2], 2)
    one = can_reach([0], 0)
    none = can_reach([1, 1], 0)
    line = [1] * 50000
    line[49999] = 0
    long = can_reach(line, 0)
    print(" ".join(show(b) for b in (e1, e2, e3, one, none, long)))
    reached = 0
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 300
        arr = [1 + next_random() % (n - 1) if n > 1 else 0 for _ in range(n)]
        zeros = next_random() % 4
        for _ in range(zeros):
            arr[next_random() % n] = 0
        start = next_random() % n
        got = can_reach(arr, start)
        if got:
            reached += 1
        check = (check * 3 + (1 if got else 0)) % 1000000007
    print(f"3000 random arrays: {reached} reach a 0, checksum {check}")


main()
