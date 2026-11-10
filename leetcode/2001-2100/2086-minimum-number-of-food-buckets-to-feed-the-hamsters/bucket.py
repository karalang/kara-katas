# LeetCode #2086: Minimum Number of Food Buckets to Feed the Hamsters --
# Python mirror of the ★ arm (bucket.kara): the same greedy, left to right,
# the bucket on a hamster's right when it can go there.

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


def random_street(n, odds):
    return "".join("H" if next_random() % 10 < odds else "." for _ in range(n))


def main():
    for s in ["H..H", ".H.H.", ".HHH.", "H", ".", "H.H.H", "HH.HH.H"]:
        print(f"{s} -> {minimum_buckets(s)}")
    total = impossible = check = 0
    for _ in range(2000):
        n = next_random() % 30 + 1
        odds = next_random() % 5 + 1
        s = random_street(n, odds)
        a = minimum_buckets(s)
        if a < 0:
            impossible += 1
        else:
            total += a
        check = (check * 31 + a + 1) % 1000000007
    print(f"2000 streets: sum {total}, {impossible} impossible, checksum {check}")
    pieces = [".", "H.", ".H", "H.H", ".H.H.", "..H"]
    s = ""
    parts = []
    length = 0
    while length < 99995:
        p = pieces[next_random() % 6]
        parts.append(p)
        length += len(p)
    s = "".join(parts) + "." * (100000 - length)
    print(f"10^5 cells, served: {minimum_buckets(s)}")
    print(f"10^5 cells, H.H.: {minimum_buckets('H.' * 50000)}")


main()
