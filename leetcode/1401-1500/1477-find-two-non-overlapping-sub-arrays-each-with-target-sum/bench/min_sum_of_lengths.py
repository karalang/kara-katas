# LeetCode #1477: Find Two Non-overlapping Sub-arrays Each With Target Sum
# -- bench, Python mirror of min_sum_of_lengths.kara


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


seed = 1477


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arr = [1 + next_random() % 1000 for _ in range(100000)]
    check = 0
    for p in range(400):
        arr[check % 100000] = 1 + (check // 7) % 1000
        target = 500 + check % 20000
        got = min_sum_of_lengths(arr, target)
        check = (check * 31 + got + 1 + p) % 1000000007
    print(f"400 passes over 100000 values: checksum {check}")


main()
