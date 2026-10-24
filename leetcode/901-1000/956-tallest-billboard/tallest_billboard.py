# LeetCode #956: Tallest Billboard -- the shorter side by difference.
#
# Each rod goes on the left support, on the right one, or nowhere. Track,
# for every difference d between the two sides, the tallest shorter side
# any choice so far reaches; a rod either widens the difference on the
# taller side or goes on the shorter side, which grows by the smaller of
# the rod and d. The answer is the shorter side at difference 0. O(n s)
# for n rods adding up to s.


def tallest_billboard(rods):
    total = sum(rods)
    best = [-1] * (total + 1)
    best[0] = 0
    for r in rods:
        prev = list(best)
        for d in range(total + 1):
            if prev[d] < 0:
                continue
            short = prev[d]
            if d + r <= total and short > best[d + r]:
                best[d + r] = short
            nd = abs(d - r)
            ns = short + min(d, r)
            if ns > best[nd]:
                best[nd] = ns
    return best[0]


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(rods):
    return "[" + ",".join(str(r) for r in rods) + "]"


def main():
    cases = [
        [1, 2, 3, 6],
        [1, 2, 3, 4, 5, 6],
        [1, 2],
        [1],
        [5, 5],
        [1, 1, 1, 1],
        [3, 4, 5, 6, 7],
        [100, 1, 2, 4],
        [2, 4, 8, 16],
    ]
    for rods in cases:
        print(f"{show(rods)}: {tallest_billboard(list(rods))}")
    seed = [956]
    count = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 10
        rods = [1 + next_random(seed) % 20 for _ in range(n)]
        h = tallest_billboard(rods)
        count += n
        total += h
        check = (check * 31 + h) % 1000000007
    print(f"300 random cases of {count} rods: heights adding to {total}, checksum {check}")
    wide = [1 + next_random(seed) % 250 for _ in range(20)]
    print(f"20 random rods up to 250: {tallest_billboard(wide)}")
    odd = [1 + 2 * (next_random(seed) % 125) for _ in range(20)]
    print(f"20 random odd rods up to 249: {tallest_billboard(odd)}")
    print(f"20 rods of 250: {tallest_billboard([250] * 20)}")
    print(f"rods 1 to 20: {tallest_billboard(list(range(1, 21)))}")
    print(f"rods 1 to 2048, the powers of 2: {tallest_billboard([1 << i for i in range(12)])}")
    print(f"one rod of 4981 and 19 of 1: {tallest_billboard([4981] + [1] * 19)}")


main()
