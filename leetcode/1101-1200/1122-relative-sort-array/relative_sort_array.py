# LeetCode #1122: Relative Sort Array -- Python mirror of the ★ arm.

seed = 1122


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def relative_sort_array(arr1, arr2):
    count = [0] * 1001
    for x in arr1:
        count[x] += 1
    out = []
    for x in arr2:
        out += [x] * count[x]
        count[x] = 0
    for v in range(1001):
        out += [v] * count[v]
    return out


def main():
    cases = [([2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]), ([28, 6, 22, 8, 44, 17], [22, 28, 8, 6]),
             ([3, 1, 2, 1], [2, 1, 3]), ([5, 4, 3, 2, 1, 3], [3]), ([7], [7]), ([1000, 0, 500, 0, 1000], [1000]),
             ([9, 8, 9, 8, 1], [1])]
    for arr1, arr2 in cases:
        print(f"{arr1}, {arr2} -> {relative_sort_array(arr1, arr2)}")
    placed = check = 0
    for _ in range(2000):
        n = next_random() % 1000 + 1
        top = next_random() % 1001
        arr1 = [next_random() % (top + 1) for _ in range(n)]
        distinct = sorted(set(arr1))
        for j in range(len(distinct) - 1, 0, -1):
            k = next_random() % (j + 1)
            distinct[j], distinct[k] = distinct[k], distinct[j]
        m = next_random() % len(distinct) + 1
        arr2 = distinct[:m]
        r = relative_sort_array(arr1, arr2)
        s2 = set(arr2)
        placed += sum(1 for x in r if x in s2)
        for x in r:
            check = (check * 31 + x) % 1000000007
    print(f"2000 random problems: {placed} values placed by arr2, checksum {check}")


main()
