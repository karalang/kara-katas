# LeetCode #1539: Kth Missing Positive Number -- Python mirror of kth.kara
# (the ★ arm, binary search on the count of missing numbers); its output is
# byte-identical.


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


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def values(count, gap):
    arr = []
    value = 0
    for _ in range(count):
        value += next_random() % gap + 1
        arr.append(value)
    return arr


def batch(count, most, gap, top):
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        arr = values(n, gap)
        k = next_random() % top + 1
        check = mix(check, find_kth_positive(arr, k))
    print(f"{count} arrays of up to {most} values, steps up to {gap}, k up to {top}: checksum {check}")


def show(arr):
    return "[" + ", ".join(str(x) for x in arr) + "]"


def main():
    examples = [
        ([2, 3, 4, 7, 11], 5),
        ([1, 2, 3, 4], 2),
        ([1], 1),
        ([2], 1),
        ([1000], 1000),
        ([5, 6, 7], 4),
        ([5, 6, 7], 5),
    ]
    for arr, k in examples:
        print(f"{show(arr)}, k = {k} -> {find_kth_positive(arr, k)}")
    print(f"1 to 1000, k = 1000 -> {find_kth_positive(list(range(1, 1001)), 1000)}")
    odd = [2 * i + 1 for i in range(500)]
    print(f"the odd numbers to 999, k = 500 -> {find_kth_positive(odd, 500)}")
    batch(3000, 12, 4, 30)
    batch(300, 1000, 2, 1000)


main()
