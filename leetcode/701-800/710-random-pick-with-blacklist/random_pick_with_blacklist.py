# LeetCode #710: Random Pick with Blacklist -- remap the blacklisted
# numbers below the line.
#
# A mirror of random_pick_with_blacklist.kara (the ★ arm) and its
# harness.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_below(seed, bound):
    hi = next_random(seed)
    lo = next_random(seed)
    return (hi * 32768 + lo) % bound


class Solution:
    def __init__(self, n, blacklist, seed):
        self.bound = n - len(blacklist)
        high = {b for b in blacklist if b >= self.bound}
        self.remap = {}
        last = n - 1
        for b in blacklist:
            if b < self.bound:
                while last in high:
                    last -= 1
                self.remap[b] = last
                last -= 1
        self.seed = [seed]

    def pick_from(self, r):
        return self.remap.get(r, r)

    def pick(self):
        return self.pick_from(random_below(self.seed, self.bound))


def random_blacklist(n, count, seed):
    seen = set()
    out = []
    while len(out) < count:
        x = random_below(seed, n)
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def run(n, blacklist, picks, seed):
    s = Solution(n, list(blacklist), seed)
    black = set(blacklist)
    bound = n - len(blacklist)
    out = f"n = {n}, {len(blacklist)} blacklisted"
    if n <= 300000:
        got = sorted(s.pick_from(r) for r in range(bound))
        want = [x for x in range(n) if x not in black]
        if got == want:
            out += ", every draw a different allowed number"
        else:
            out += ", the draws do NOT cover the allowed numbers"
    else:
        draws = {b for b in blacklist if b < bound}
        draws.update(range(bound - 1000, bound))
        got = set()
        ok = True
        for r in draws:
            x = s.pick_from(r)
            if x < 0 or x >= n or x in black or x in got:
                ok = False
            got.add(x)
        verdict = "each" if ok else "NOT each"
        out += f", {len(draws)} draws, {verdict} allowed, all different"
    counts = {}
    bad = 0
    for _ in range(picks):
        x = s.pick()
        if x < 0 or x >= n or x in black:
            bad += 1
        counts[x] = counts.get(x, 0) + 1
    total = 0
    for c in sorted(counts.values()):
        total = (total * 131 + c) % 1000000007
    return (f"{out}; {picks} picks: {bad} not allowed, "
            f"{len(counts)} seen, counts {total}")


def main():
    print(run(7, [2, 3, 5], 7, 1))
    print(run(7, [2, 3, 5], 10000, 2))
    print(run(1, [], 100, 3))
    print(run(2, [0], 100, 4))
    print(run(2, [1], 100, 5))
    print(run(10, [], 10000, 6))
    print(run(10, [0, 1, 2, 3, 5, 6, 7, 8, 9], 1000, 7))
    print(run(10, [9, 8, 7, 6, 5], 1000, 8))
    print(run(10, [0, 1, 2, 3, 4], 1000, 9))
    print(run(1000000000, [0, 999999999], 20000, 10))
    seed = [710]
    big = random_blacklist(1000000000, 100000, seed)
    print(run(1000000000, big, 20000, 11))
    half = random_blacklist(200000, 100000, seed)
    print(run(200000, half, 20000, 12))
    most = random_blacklist(300000, 299990, seed)
    print(run(300000, most, 20000, 13))
    total = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 60
        count = next_random(seed) % n
        blacklist = random_blacklist(n, count, seed)
        line = run(n, blacklist, 200, next_random(seed))
        for b in line.encode():
            total = (total * 131 + b) % 1000000007
    print(f"300 random cases: checksum {total}")


main()
