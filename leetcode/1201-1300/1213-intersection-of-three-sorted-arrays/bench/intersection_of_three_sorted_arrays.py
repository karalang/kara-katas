# LeetCode #1213 bench, in Python: the ★ arm (three pointers, all three
# stepping on when the values agree and otherwise only those at the least
# value) on 1000 triples of arrays of 600 to 950 values drawn once, then 10
# rounds over the triples, every answer's length and last value folded
# into a checksum.

seed = 1213


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def random_sorted(percent):
    return [v for v in range(1, 2001) if next_random() % 100 < percent]


def main():
    triples = []
    for _ in range(1000):
        a = random_sorted(33 + next_random() % 12)
        b = random_sorted(33 + next_random() % 12)
        c = random_sorted(33 + next_random() % 12)
        triples.append((a, b, c))
    check = 0
    for rnd in range(10):
        for a, b, c in triples:
            answer = arrays_intersection(a, b, c)
            last = answer[-1] if answer else 0
            check = (check * 131 + len(answer) + last + rnd) % 1000000007
    print(f"10 rounds over 1000 triples of 600 to 950 values: checksum {check}")


main()
