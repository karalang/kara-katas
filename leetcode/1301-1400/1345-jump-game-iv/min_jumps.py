# LeetCode #1345: Jump Game IV -- Python mirror of the ★ arm: a
# breadth-first search from index 0 over i - 1, i + 1 and the indices of
# the same value, each value's list emptied the first time it is used.
from collections import deque


def min_jumps(arr):
    n = len(arr)
    places = {}
    for i, v in enumerate(arr):
        places.setdefault(v, []).append(i)
    steps = [-1] * n
    steps[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        if i == n - 1:
            return steps[i]
        nxt = places.pop(arr[i], [])
        nxt.append(i - 1)
        nxt.append(i + 1)
        for j in nxt:
            if 0 <= j < n and steps[j] < 0:
                steps[j] = steps[i] + 1
                queue.append(j)
    return steps[n - 1]


seed = 1345


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    e1 = min_jumps([100, -23, -23, 404, 100, 23, 23, 23, 3, 404])
    e2 = min_jumps([7])
    e3 = min_jumps([7, 6, 9, 6, 9, 6, 9, 7])
    n = 50000
    same = [5] * n
    rising = list(range(n))
    thousand = []
    kinds = []
    spread = [-100000000]
    for _ in range(300):
        a = next_random()
        b = next_random()
        kinds.append((a * 65536 + b) % 200000001 - 100000000)
    for i in range(n):
        thousand.append(1 + next_random() % 1000)
        if 0 < i < n - 1:
            spread.append(kinds[next_random() % 300])
    spread.append(100000000)
    print(f"{e1} {e2} {e3} {min_jumps(same)} {min_jumps(rising)} {min_jumps(thousand)} {min_jumps(spread)}")
    check = 0
    for t in range(1000):
        length = 1 + next_random() % 500 if t % 10 == 0 else 1 + next_random() % 30
        top = 3 if t % 3 == 0 else 20 if t % 3 == 1 else 10000
        arr = [1 + next_random() % top for _ in range(length)]
        check = (check * 131 + min_jumps(arr)) % 1000000007
    print(f"1000 random arrays: checksum {check}")


main()
