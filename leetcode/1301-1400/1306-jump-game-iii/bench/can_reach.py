# LeetCode #1306 bench in Python: the ★ arm (a breadth-first walk from the
# start in a `collections.deque`, each place queued once) on the same 10
# arrays and 300 passes.
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


def main():
    n = 50000
    arrays = []
    for _ in range(10):
        arr = [1 + next_random() % 10 for _ in range(n)]
        arr[next_random() % n] = 0
        arrays.append(arr)
    check = 0
    for pass_no in range(300):
        for a in range(10):
            arrays[a][check % n] = (check // 7) % 11
            start = (check // 13) % n
            got = can_reach(arrays[a], start)
            check = (check * 31 + (1 if got else 2) + pass_no) % 1000000007
    print(f"300 passes over 10 arrays of 5 * 10^4: checksum {check}")


main()
