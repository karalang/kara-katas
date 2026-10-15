# LeetCode #667: Beautiful Arrangement II -- zigzag from both ends.
# Mirrors the ★ arm (beautiful_arrangement_ii.kara) and its test harness.


def construct_array(n, k):
    out = []
    lo, hi = 1, k + 1
    while lo <= hi:
        out.append(lo)
        lo += 1
        if lo <= hi:
            out.append(hi)
            hi -= 1
    out.extend(range(k + 2, n + 1))
    return out


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def distinct_steps(a):
    seen = [False] * (len(a) + 1)
    count = 0
    for i in range(1, len(a)):
        d = abs(a[i] - a[i - 1])
        if not seen[d]:
            seen[d] = True
            count += 1
    return count


def checksum(a):
    h = 0
    for x in a:
        h = (h * 31 + x) % 1000000007
    return h


def show(n, k):
    a = construct_array(n, k)
    steps = distinct_steps(a)
    if n <= 12:
        print(f"n={n} k={k}: [{','.join(str(x) for x in a)}], distinct differences {steps}")
    else:
        print(f"n={n} k={k}: starts {a[0]},{a[1]},{a[2]}, ends {a[n - 1]}, "
              f"distinct differences {steps}, checksum {checksum(a)}")


def main():
    for n, k in [(3, 1), (3, 2), (2, 1), (6, 5), (7, 1), (8, 3), (8, 4), (12, 7),
                 (10000, 1), (10000, 5000), (10000, 9999)]:
        show(n, k)
    rng = Rng(667)
    good = 0
    total = 0
    for _ in range(1000):
        n = 2 + rng.next() % 60
        k = 1 + rng.next() % (n - 1)
        a = construct_array(n, k)
        if distinct_steps(a) == k:
            good += 1
        total = (total * 31 + checksum(a)) % 1000000007
    print(f"1000 random cases: {good} with exactly k differences, checksum {total}")


main()
