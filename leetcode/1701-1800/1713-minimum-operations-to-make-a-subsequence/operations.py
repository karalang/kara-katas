# LeetCode #1713: Minimum Operations to Make a Subsequence -- the Python
# mirror of the ★ arm (operations.kara): the array's values read as their
# places in the target, and the longest rising run of places kept by the
# tails of each length, found with a binary search.

from bisect import bisect_left


def min_operations(target, arr):
    place = {v: i for i, v in enumerate(target)}
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


def batch(count, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        values = list(range(1, top + 1))
        for i in range(top - 1, 0, -1):
            a = next_random(seed)
            j = (a * 32768 + next_random(seed)) % (i + 1)
            values[i], values[j] = values[j], values[i]
        t = (next_random(seed) * 32768 + next_random(seed)) % min(most, top) + 1
        target = values[:t]
        n = (next_random(seed) * 32768 + next_random(seed)) % most + 1
        arr = []
        for _ in range(n):
            a = next_random(seed)
            arr.append((a * 32768 + next_random(seed)) % top + 1)
        answer = min_operations(target, arr)
        total += answer
        check = (check * 31 + answer + t + n) % 1000000007
    print(f"{count} problems of up to {most} values from 1 to {top}: answers sum to {total}, checksum {check}")


def main():
    # LeetCode's two examples, then a target already there, one with
    # nothing in common, and an array that holds the target backwards
    print(min_operations([5, 1, 3], [9, 4, 2, 3, 4]))
    print(min_operations([6, 4, 8, 1, 3, 2], [4, 7, 6, 2, 3, 8, 6, 1]))
    print(min_operations([1, 2, 3], [1, 5, 2, 5, 3]))
    print(min_operations([1, 2], [3, 4, 5]))
    print(min_operations([1, 2, 3, 4], [4, 3, 2, 1]))
    seed = [1713]
    batch(3000, 10, 12, seed)
    batch(300, 1000, 1500, seed)
    batch(10, 100000, 120000, seed)


main()
