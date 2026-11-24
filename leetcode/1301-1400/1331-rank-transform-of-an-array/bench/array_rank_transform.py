# LeetCode #1331 bench, Python mirror of the Kāra bench: the ★ arm (the
# values sorted, their repeats removed, and each value's rank found by
# binary search) on 20 arrays of 10^5 values, the constraints' longest,
# each from 1 to 10^9 or from a narrower spread with many repeats, built
# once. Then 15 passes, each setting one value of every array from the
# checksum so far, answering it and folding two of its ranks plus the pass
# into the checksum.
from bisect import bisect_left


def array_rank_transform(arr):
    distinct = sorted(set(arr))
    return [bisect_left(distinct, x) + 1 for x in arr]


seed = 1331


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    arrays = []
    for t in range(20):
        spread = 1000000000 if t % 2 == 0 else 1000
        arr = []
        for _ in range(n):
            a = next_random()
            b = next_random()
            arr.append((a * 61036 + b) % spread + 1)
        arrays.append(arr)
    check = 0
    for p in range(15):
        for t in range(20):
            at = check % n
            arrays[t][at] = check // 7 % 1000000000 + 1
            ranks = array_rank_transform(arrays[t])
            check = (check * 31 + ranks[at] + ranks[n - 1] + p) % 1000000007
    print(f"15 passes over 20 arrays of 10^5: checksum {check}")


main()
