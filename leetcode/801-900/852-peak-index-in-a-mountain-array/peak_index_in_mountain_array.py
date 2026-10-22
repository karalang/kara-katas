# LeetCode #852: Peak Index in a Mountain Array -- Python mirror of the ★
# arm and its harness.


def peak_index_in_mountain_array(arr):
    lo = 0
    hi = len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(arr):
    print(f"{fmt(arr)} -> {peak_index_in_mountain_array(arr)}")


seed = 852


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mountain(n, peak, step):
    arr = []
    v = 0
    for i in range(n):
        if i > 0:
            if i <= peak:
                v += 1 + next_random() % step
            else:
                v -= 1 + next_random() % step
        arr.append(v)
    low = min(arr)
    return [x - low for x in arr]


def main():
    show([0, 1, 0])
    show([0, 2, 1, 0])
    show([0, 10, 5, 2])
    show([3, 5, 3, 2, 0])
    show([1, 2, 3, 4, 5, 6, 0])
    show([0, 9, 8, 7, 6, 5, 4])
    show([24, 69, 100, 99, 79, 78, 67, 36, 26, 19])
    show([1, 1000000, 0])
    show([0, 1, 2, 3, 2, 1, 0])
    show([5, 6, 7, 8, 9, 10, 4])
    n = 100000
    up = [i if i < n - 1 else 0 for i in range(n)]
    down = [0 if i == 0 else n - i for i in range(n)]
    middle = [i * 10 if i <= n // 2 else (n - i) * 10 for i in range(n)]
    print(f"rising to the second last: {peak_index_in_mountain_array(up)}")
    print(f"falling from the second: {peak_index_in_mountain_array(down)}")
    print(f"peaked in the middle: {peak_index_in_mountain_array(middle)}")
    peak = 1 + next_random() % (n - 2)
    print(f"a random mountain peaked at {peak}: {peak_index_in_mountain_array(mountain(n, peak, 10))}")
    total = 0
    check = 0
    for _ in range(600):
        n = 3 + next_random() % 40
        peak = 1 + next_random() % (n - 2)
        got = peak_index_in_mountain_array(mountain(n, peak, 1 + next_random() % 5))
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"600 random mountains: peaks sum to {total}, checksum {check}")


main()
