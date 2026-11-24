# LeetCode #1345 bench in Python: the ★ arm (a breadth-first search over
# i - 1, i + 1 and the indices of the same value, each value's list
# emptied the first time it is used) on the same 10 arrays of 5 * 10^4
# values and 30 passes.
from collections import deque


def min_jumps(arr):
    n = len(arr)
    places = {}
    for i in range(n):
        places.setdefault(arr[i], []).append(i)
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
    n = 50000
    arrays = []
    for a in range(10):
        if a % 2 == 0:
            arrays.append([1 + next_random() % 1000 for _ in range(n)])
        else:
            arrays.append([i // 2 for i in range(n)])
    check = 0
    for pass_ in range(30):
        for a in range(10):
            arr = arrays[a]
            arr[check % n] = (check // 7) % 25000
            answer = min_jumps(arr)
            check = (check * 31 + answer + pass_) % 1000000007
    print(f"30 passes over 10 arrays of 5 * 10^4: checksum {check}")


main()
