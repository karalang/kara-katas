# LeetCode #1681: Minimum Incompatibility -- the bench's Python mirror: the
# ★ arm on 300 arrays of 16 values from 1 to 16, each with a random k that
# divides 16, all drawn first, each answered 4 times.


def minimum_incompatibility(nums, k):
    n = len(nums)
    size = n // k
    full = (1 << n) - 1
    cost = [-1] * (1 << n)
    for s in range(full + 1):
        if bin(s).count("1") != size:
            continue
        seen = 0
        lo = 2**31 - 1
        hi = -(2**31)
        ok = True
        for i in range(n):
            if s >> i & 1 == 1:
                bit = 1 << nums[i]
                if seen & bit:
                    ok = False
                    break
                seen |= bit
                lo = min(lo, nums[i])
                hi = max(hi, nums[i])
        if ok:
            cost[s] = hi - lo
    unreached = 2**31 - 1
    best = [unreached] * (1 << n)
    best[0] = 0
    for m in range(full):
        if best[m] == unreached or bin(m).count("1") % size != 0:
            continue
        free = full ^ m
        lowest = free & -free
        s = free
        while s > 0:
            if s & lowest and cost[s] >= 0:
                best[m | s] = min(best[m | s], best[m] + cost[s])
            s = (s - 1) & free
    return -1 if best[full] == unreached else best[full]


seed = 1681


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays, n, rounds = 300, 16, 4
    ks = [1, 2, 4, 8, 16]
    cases = []
    for _ in range(arrays):
        nums = [next_random() % n + 1 for _ in range(n)]
        k = ks[next_random() % 5]
        cases.append((nums, k))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, k in cases:
            answer = minimum_incompatibility(nums, k)
            total += answer
            check = (check * 31 + answer + 1 + r) % 1000000007
    print(f"{arrays} arrays of {n} values, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
