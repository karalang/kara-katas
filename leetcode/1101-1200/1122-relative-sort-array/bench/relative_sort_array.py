# LeetCode #1122: Relative Sort Array -- the bench in Python: the ★ arm
# over 4 problems of 1000 values, each round swapping two values of each
# `arr1` and two of each `arr2` and sorting it again.

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
    ones, twos = [], []
    for top in [1000, 500, 100, 10]:
        arr1 = [next_random() % (top + 1) for _ in range(1000)]
        distinct = sorted(set(arr1))
        for j in range(len(distinct) - 1, 0, -1):
            k = next_random() % (j + 1)
            distinct[j], distinct[k] = distinct[k], distinct[j]
        twos.append(distinct[:(len(distinct) + 1) // 2])
        ones.append(arr1)
    check = 0
    for rnd in range(5000):
        for j in range(4):
            a, t = ones[j], twos[j]
            m = len(t)
            p, q = rnd * 7919 % 1000, rnd * 104729 % 1000
            a[p], a[q] = a[q], a[p]
            p, q = rnd * 31 % m, rnd * 17 % m
            t[p], t[q] = t[q], t[p]
            for x in relative_sort_array(a, t):
                check = (check * 31 + x) % 1000000007
    print(f"5000 rounds over 4 problems of 1000 values: checksum {check}")


main()
