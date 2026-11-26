# LeetCode #1481: Least Number of Unique Integers after K Removals --
# Python mirror of find_least_num_of_unique_ints.kara: each value counted,
# the counts sorted, and the removals spent on the rarest values first
from collections import Counter


def find_least_num_of_unique_ints(arr, k):
    counts = sorted(Counter(arr).values())
    left = k
    unique = len(counts)
    for c in counts:
        if c > left:
            break
        left -= c
        unique -= 1
    return unique


# ---- test harness ---------------------------------------------------------

seed = 1481


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def draw(n, top):
    return [1 + wide_random() % top for _ in range(n)]


def main():
    print(f"{find_least_num_of_unique_ints([5, 5, 4], 1)} {find_least_num_of_unique_ints([4, 3, 1, 1, 3, 3, 2], 3)}")
    e = [
        find_least_num_of_unique_ints([1, 2, 2, 3, 3, 3], 0),
        find_least_num_of_unique_ints([1, 2, 2, 3, 3, 3], 6),
        find_least_num_of_unique_ints([1000000000] * 8, 7),
        find_least_num_of_unique_ints([9, 8, 7, 6, 5], 2),
        find_least_num_of_unique_ints([1, 1, 2, 2, 2, 3, 3, 3, 3], 4),
    ]
    print(" ".join(map(str, e)))
    wide = draw(100000, 1000000000)
    narrow = draw(100000, 1000)
    ks = [0, 1000, 50000, 100000]
    a = [str(find_least_num_of_unique_ints(wide, k)) for k in ks]
    b = [str(find_least_num_of_unique_ints(narrow, k)) for k in ks]
    print(f"100000 values: {' '.join(a)} | {' '.join(b)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 60
        top = 1 + next_random() % 30
        arr = draw(n, top)
        k = next_random() % (n + 1)
        check = (check * 31 + find_least_num_of_unique_ints(arr, k)) % 1000000007
    print(f"3000 random arrays: checksum {check}")


main()
