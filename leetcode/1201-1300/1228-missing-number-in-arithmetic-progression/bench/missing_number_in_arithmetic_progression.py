# LeetCode #1228 bench: the ★ arm in Python, over the same 2000 random
# progressions and 2000 passes as the Kāra bench.


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


def main():
    seed = 1228

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    for _ in range(2000):
        first = next_random() % 100001
        low = -(first // 1000)
        high = (100000 - first) // 1000
        step = low + next_random() % (high - low + 1)
        gone = next_random() % 999 + 1
        arrays.append([first + i * step for i in range(1001) if i != gone])
    check = 0
    for _ in range(2000):
        for arr in arrays:
            check = (check * 131 + missing_number(arr)) % 1000000007
    print(f"2000 progressions of 1000 values, 2000 passes: checksum {check}")


main()
