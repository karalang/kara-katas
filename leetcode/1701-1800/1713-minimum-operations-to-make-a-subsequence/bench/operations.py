# LeetCode #1713: Minimum Operations to Make a Subsequence -- the Python
# mirror of the bench (operations.kara): a dict of the target's places and
# the smallest tail of each rising run, found with `bisect`, on 20 random
# problems of 100000 values, each answered 5 times.

from bisect import bisect_left


def min_operations(target, arr):
    place = {}
    for i, v in enumerate(target):
        place[v] = i
    tails = []
    for a in arr:
        p = place.get(a)
        if p is None:
            continue
        i = bisect_left(tails, p)
        if i == len(tails):
            tails.append(p)
        else:
            tails[i] = p
    return len(target) - len(tails)


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def wide(state):
    a = next_random(state)
    return a * 32768 + next_random(state)


def main():
    count = 20
    rounds = 5
    n = 100000
    seed = [1713]
    problems = []
    for _ in range(count):
        target = list(range(n))
        for i in range(n - 1, 0, -1):
            j = wide(seed) % (i + 1)
            target[i], target[j] = target[j], target[i]
        for i in range(n):
            target[i] = target[i] * 10000 + next_random(seed) % 10000
        arr = []
        for _ in range(n):
            if next_random(seed) % 2 == 0:
                arr.append(target[wide(seed) % n])
            else:
                arr.append(wide(seed) % 1000000000)
        problems.append((target, arr))
    total = 0
    check = 0
    for r in range(rounds):
        for target, arr in problems:
            answer = min_operations(target, arr)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of {n} values, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
