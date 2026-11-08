# LeetCode #1064: Fixed Point -- the benchmark, the same binary search as
# fixed.kara. A suffix is searched through its start, as a slice copy
# would cost more than the search.
seed = 1064


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_sorted(n, first):
    arr = []
    x = first
    for _ in range(n):
        arr.append(x)
        x += 1 + next_random() % 2
    return arr


def fixed_point(arr, start):
    # the suffix arr[start:]: arr[start + i] < i for every i below lo
    lo, hi = 0, len(arr) - start
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[start + mid] < mid:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo < len(arr) - start and arr[start + lo] == lo else -1


def main():
    # 8 arrays of 1000000 numbers, built once, then each answered on its
    # first 500000 suffixes
    arrays = [random_sorted(1000000, -100000 * a) for a in range(8)]
    calls = found = check = 0
    for arr in arrays:
        for p in range(500000):
            answer = fixed_point(arr, p)
            if answer >= 0:
                found += 1
            check = (check * 31 + answer + 1) % 1000000007
            calls += 1
    print(f"{calls} calls: {found} found, checksum {check}")


main()
