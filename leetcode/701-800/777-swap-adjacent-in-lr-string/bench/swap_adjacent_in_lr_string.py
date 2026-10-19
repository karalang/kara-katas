# Benchmark for #777: Swap Adjacent in LR String -- mirror of the ★ arm
# (two pointers), with the same workload as the Kāra program.


def can_transform(start, end):
    s = start
    e = end
    n = len(s)
    if len(e) != n:
        return False
    i = 0
    j = 0
    while True:
        while i < n and s[i] == "X":
            i += 1
        while j < n and e[j] == "X":
            j += 1
        if i == n or j == n:
            return i == n and j == n
        if s[i] != e[j]:
            return False
        if s[i] == "L" and i < j:
            return False
        if s[i] == "R" and i > j:
            return False
        i += 1
        j += 1


def main():
    count = 64
    n = 10000
    seed = 777

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    starts = []
    ends = []
    for g in range(count):
        s = []
        for _ in range(n):
            r = next_random() % 4
            s.append("X" if r < 2 else "L" if r == 2 else "R")
        e = list(s)
        if g % 4 < 2:
            for _ in range(100000):
                i = next_random() % (n - 1)
                if (e[i] == "X" and e[i + 1] == "L") or (e[i] == "R" and e[i + 1] == "X"):
                    e[i], e[i + 1] = e[i + 1], e[i]
        else:
            k = n - 2 if g % 4 == 2 else next_random() % (n - 1)
            while not (e[k] == "X" and e[k + 1] == "R"):
                k = n - 2 if k == 0 else k - 1
            e[k], e[k + 1] = e[k + 1], e[k]
        starts.append("".join(s))
        ends.append("".join(e))
    yes = 0
    checksum = 0
    for rnd in range(20000):
        g = (rnd * 7) % count
        if can_transform(starts[g], ends[g]):
            yes += 1
            checksum = (checksum * 31 + g + 1) % 1000000007
        else:
            checksum = (checksum * 31 + 7) % 1000000007
    print(f"20000 rounds of {n} letters: {yes} reachable, checksum {checksum}")


main()
