# LeetCode #975: Odd Even Jump -- Python mirror of odd_even_jumps.kara.
# Python has no sorted map, so the keys are a sorted list searched with
# bisect, beside a dict from value to its leftmost index.
from bisect import bisect_left, bisect_right, insort


def odd_even_jumps(arr):
    n = len(arr)
    higher = [False] * n
    lower = [False] * n
    higher[n - 1] = lower[n - 1] = True
    keys = [arr[n - 1]]
    seen = {arr[n - 1]: n - 1}
    good = 1
    for i in range(n - 2, -1, -1):
        v = arr[i]
        p = bisect_left(keys, v)
        if p < len(keys):
            higher[i] = lower[seen[keys[p]]]
        q = bisect_right(keys, v)
        if q > 0:
            lower[i] = higher[seen[keys[q - 1]]]
        if v not in seen:
            insort(keys, v)
        seen[v] = i
        if higher[i]:
            good += 1
    return good


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_arr(n, top):
    return [next_random() % top for _ in range(n)]


def main():
    global seed
    cases = [
        [10, 13, 12, 14, 15],
        [2, 3, 1, 1, 4],
        [5, 1, 3, 4, 2],
        [7],
        [1, 1, 1, 1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [0, 99999, 0, 99999],
        [3, 1, 2, 3, 1, 2],
        [1, 3, 2, 3, 1],
    ]
    for arr in cases:
        print(f"{arr}: {odd_even_jumps(arr)}")
    seed = 975
    for count, most, top in [(300, 12, 5), (3000, 60, 1000), (20, 2000, 100000)]:
        total = check = 0
        for _ in range(count):
            n = most if most == 2000 else 1 + next_random() % most
            good = odd_even_jumps(random_arr(n, top))
            total += good
            check = (check * 31 + good) % 1000000007
        print(f"{count} random arrays of up to {most} values: "
              f"{total} good starts, checksum {check}")


main()
