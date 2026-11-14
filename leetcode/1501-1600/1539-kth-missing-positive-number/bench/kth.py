# LeetCode #1539: Kth Missing Positive Number -- bench: the ★ arm (binary
# search on the count of missing numbers) over 1000 arrays of 1 to 1000
# values and 1000 values of k, built once, every pair asked 5 times. Python
# mirror of kth.kara.


def find_kth_positive(arr, k):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] - mid - 1 < k:
            lo = mid + 1
        else:
            hi = mid
    return lo + k


seed = 1539


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(1000):
        n = next_random() % 1000 + 1
        gap = next_random() % 4 + 1
        arr = []
        value = 0
        for _ in range(n):
            value += next_random() % gap + 1
            arr.append(value)
        arrays.append(arr)
    ks = [next_random() % 2000 + 1 for _ in range(1000)]
    check = 0
    for _ in range(5):
        for arr in arrays:
            for k in ks:
                check = (check * 31 + find_kth_positive(arr, k) + 1) % 1000000007
    print(f"5 passes over 1000 arrays of up to 1000 values and 1000 values of k: checksum {check}")


main()
