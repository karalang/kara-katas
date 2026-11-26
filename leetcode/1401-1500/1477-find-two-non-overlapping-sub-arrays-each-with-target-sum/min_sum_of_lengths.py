# LeetCode #1477: Find Two Non-overlapping Sub-arrays Each With Target Sum
# -- Python mirror of min_sum_of_lengths.kara: one sliding window, and the
# shortest window of the target sum ending at or before each place


def min_sum_of_lengths(arr, target):
    n = len(arr)
    none = n + 1
    shortest = [none] * n
    best = 2 * none
    total = 0
    left = 0
    for right in range(n):
        total += arr[right]
        while total > target:
            total -= arr[left]
            left += 1
        here = none
        if total == target:
            here = right - left + 1
            if left > 0 and shortest[left - 1] < none:
                best = min(best, here + shortest[left - 1])
        shortest[right] = min(shortest[right - 1], here) if right > 0 else here
    return -1 if best >= 2 * none else best


# ---- test harness ---------------------------------------------------------

seed = 1477


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, top):
    return [1 + next_random() % top for _ in range(n)]


def main():
    print(f"{min_sum_of_lengths([3, 2, 2, 4, 3], 3)} {min_sum_of_lengths([7, 3, 4, 7], 7)} {min_sum_of_lengths([4, 3, 2, 6, 2, 3, 4], 6)}")
    e = [
        min_sum_of_lengths([5], 5),
        min_sum_of_lengths([5, 5], 5),
        min_sum_of_lengths([1] * 6, 2),
        min_sum_of_lengths([1, 2, 1], 3),
        min_sum_of_lengths([1, 2, 3], 7),
        min_sum_of_lengths([3, 1, 1, 1, 5, 1, 2, 1], 3),
        min_sum_of_lengths([1, 1, 1, 2, 2, 2, 4, 4], 6),
    ]
    print(" ".join(map(str, e)))
    big = draw(100000, 1000)
    most = [str(min_sum_of_lengths(big, t)) for t in [1000, 5000, 100000, 100000000]]
    print(f"100000 values: {' '.join(most)}")
    check = 0
    none = 0
    for _ in range(3000):
        n = 1 + next_random() % 60
        top = 1 + next_random() % 20
        arr = draw(n, top)
        target = 1 + next_random() % 40
        got = min_sum_of_lengths(arr, target)
        if got == -1:
            none += 1
        check = (check * 31 + got + 1) % 1000000007
    print(f"3000 random arrays: {none} with no pair, checksum {check}")


main()
