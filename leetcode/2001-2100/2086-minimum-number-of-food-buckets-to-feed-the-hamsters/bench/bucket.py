# LeetCode #2086: Minimum Number of Food Buckets to Feed the Hamsters --
# Python mirror of the ★ arm's benchmark (bucket.kara): the same street and
# 3000 windows, each a copied slice, served by the same greedy.

seed = 2086


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def minimum_buckets(hamsters):
    n = len(hamsters)
    bucket = [False] * n
    count = 0
    for i in range(n):
        if hamsters[i] != "H":
            continue
        if i > 0 and bucket[i - 1]:
            continue
        if i + 1 < n and hamsters[i + 1] == ".":
            bucket[i + 1] = True
            count += 1
        elif i > 0 and hamsters[i - 1] == ".":
            bucket[i - 1] = True
            count += 1
        else:
            return -1
    return count


def main():
    pieces = [".", "H.", ".H", "H.H", ".H.H.", "..H"]
    parts = []
    length = 0
    while length < 1000000:
        p = pieces[next_random() % 6]
        parts.append(p)
        length += len(p)
    street = "".join(parts)
    total = impossible = check = 0
    for _ in range(3000):
        hi = next_random()
        start = (hi * 32768 + next_random()) % 900000
        a = minimum_buckets(street[start:start + 100000])
        if a < 0:
            impossible += 1
        else:
            total += a
        check = (check * 31 + a + 1) % 1000000007
    print(f"3000 windows: sum {total}, {impossible} impossible, checksum {check}")


main()
