# LeetCode #1213: Intersection of Three Sorted Arrays -- a Python mirror of
# the ★ arm: three pointers, all three stepping on when the values agree
# and otherwise only those at the least value.


def arrays_intersection(arr1, arr2, arr3):
    out = []
    i = j = k = 0
    while i < len(arr1) and j < len(arr2) and k < len(arr3):
        a, b, c = arr1[i], arr2[j], arr3[k]
        if a == b == c:
            out.append(a)
            i += 1
            j += 1
            k += 1
        else:
            least = min(a, b, c)
            if a == least:
                i += 1
            if b == least:
                j += 1
            if c == least:
                k += 1
    return out


seed = 1213


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_sorted(top, percent):
    out = [v for v in range(1, top + 1) if next_random() % 100 < percent]
    if not out:
        out.append(next_random() % top + 1)
    return out


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    cases = [
        ([1, 2, 3, 4, 5], [1, 2, 5, 7, 9], [1, 3, 4, 5, 8]),
        ([197, 418, 523, 876, 1356], [501, 880, 1593, 1710, 1870], [521, 682, 1337, 1395, 1764]),
        ([1], [1], [1]),
        ([1], [2], [1]),
        ([1, 2, 3], [1, 2, 3], [1, 2, 3]),
        ([2000], [1, 2000], [1, 1000, 2000]),
        ([1, 3, 5, 7], [2, 4, 6, 8], [1, 2, 3, 4, 5, 6, 7, 8]),
    ]
    for a, b, c in cases:
        print(f"{show(a)} {show(b)} {show(c)}: {show(arrays_intersection(a, b, c))}")
    kept = check = 0
    for _ in range(1000):
        top = next_random() % 20 + 1
        a = random_sorted(top, next_random() % 100)
        b = random_sorted(top, next_random() % 100)
        c = random_sorted(top, next_random() % 100)
        answer = arrays_intersection(a, b, c)
        kept += len(answer)
        for v in answer:
            check = (check * 131 + v) % 1000000007
        check = (check * 131 + len(answer)) % 1000000007
    print(f"1000 small cases: {kept} values kept, checksum {check}")
    a = random_sorted(2000, 45)
    b = random_sorted(2000, 45)
    c = random_sorted(2000, 45)
    answer = arrays_intersection(a, b, c)
    print(f"{len(a)}, {len(b)} and {len(c)} of 1 to 2000: {len(answer)} kept, the first {answer[0]}, the last {answer[-1]}")
    evens = [2 * v for v in range(1, 1001)]
    odds = [2 * v + 1 for v in range(1000)]
    allv = list(range(1001, 2001))
    print(f"1000 evens, 1000 odds, 1001 to 2000: {len(arrays_intersection(evens, odds, allv))} kept")
    print(f"1000 evens three times over: {len(arrays_intersection(evens, evens, evens))} kept")
    print(f"1000 evens, 1001 to 2000 twice: {len(arrays_intersection(evens, allv, allv))} kept")


main()
