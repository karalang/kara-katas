# LeetCode #1228: Missing Number In Arithmetic Progression -- Python mirror
# of the ★ arm: the step from the first and last values, then a binary
# search for the first element out of place.


def missing_number(arr):
    n = len(arr)
    step = int((arr[n - 1] - arr[0]) / n)
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == arr[0] + mid * step:
            lo = mid + 1
        else:
            hi = mid
    return arr[0] + lo * step


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def progression(seed, length):
    first = next_random(seed) % 100001
    low = -(first // (length - 1))
    high = (100000 - first) // (length - 1)
    step = low + next_random(seed) % (high - low + 1)
    gone = next_random(seed) % (length - 2) + 1
    arr = [first + i * step for i in range(length) if i != gone]
    return arr, first + gone * step


def main():
    print(missing_number([5, 7, 11, 13]))
    print(missing_number([15, 13, 12]))
    print(missing_number([7, 7, 7]))
    seed = [1228]
    check = 0
    right = 0
    for _ in range(1000):
        length = next_random(seed) % 998 + 4
        arr, removed = progression(seed, length)
        answer = missing_number(arr)
        check = (check * 131 + answer) % 1000000007
        if answer == removed:
            right += 1
    print(f"1000 random progressions: checksum {check}, {right} right")
    big = [v for v in (i * 100 for i in range(1000)) if v != 50000]
    print(f"1000 values: {missing_number(big)}")


main()
