# LeetCode #2111: Minimum Operations to Make the Array K-Increasing --
# the Python mirror of increasing.kara (the ★ arm): each of the `k`
# chains keeps its longest non-decreasing subsequence, its length from
# patience piles with `bisect_right`, and changes the rest. O(n log n).

from bisect import bisect_right


def k_increasing(arr, k):
    changes = 0
    for r in range(k):
        tails = []
        length = 0
        for i in range(r, len(arr), k):
            x = arr[i]
            at = bisect_right(tails, x)
            if at == len(tails):
                tails.append(x)
            else:
                tails[at] = x
            length += 1
        changes += length - len(tails)
    return changes


# ---- test harness ----------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    examples = [
        ([5, 4, 3, 2, 1], 1),
        ([4, 1, 5, 2, 6, 2], 2),
        ([4, 1, 5, 2, 6, 2], 3),
        ([1], 1),
        ([2, 2, 2], 1),
        ([3, 1, 2], 3),
        ([10, 9, 8, 7, 6, 5], 2),
    ]
    for arr, k in examples:
        print(f"{arr}, k = {k} -> {k_increasing(arr, k)}")
    seed = [2111]
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random(seed) % 40 + 1
        arr = [next_random(seed) % 10 + 1 for _ in range(n)]
        k = next_random(seed) % n + 1
        got = k_increasing(arr, k)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"3000 arrays: {total} operations, checksum {check}")
    falling = [100000 - i for i in range(100000)]
    seed = [7]
    random = []
    for _ in range(100000):
        hi = next_random(seed)
        lo = next_random(seed)
        random.append((hi * 32768 + lo) % 100000 + 1)
    print(f"falling, k = 1 -> {k_increasing(falling, 1)}")
    print(f"random, k = 7 -> {k_increasing(random, 7)}")
    print(f"random, k = n -> {k_increasing(random, 100000)}")


main()
