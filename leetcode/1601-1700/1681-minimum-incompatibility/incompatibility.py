# LeetCode #1681: Minimum Incompatibility -- the Python mirror of the ★ arm:
# a table over the sets of values already placed, filled a subset at a
# time.


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


def batch(count, most):
    total = 0
    impossible = 0
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        nums = [next_random() % n + 1 for _ in range(n)]
        divisors = [d for d in range(1, n + 1) if n % d == 0]
        k = divisors[next_random() % len(divisors)]
        answer = minimum_incompatibility(nums, k)
        if answer < 0:
            impossible += 1
        else:
            total += answer
        check = (check * 31 + answer + 1 + n) % 1000000007
    print(f"{count} arrays of up to {most} values: answers sum to {total}, {impossible} impossible, checksum {check}")


print(minimum_incompatibility([1, 2, 1, 4], 2))
print(minimum_incompatibility([6, 3, 8, 1, 3, 1, 2, 2], 4))
print(minimum_incompatibility([5, 3, 3, 6, 3, 3], 3))
print(minimum_incompatibility([3, 1, 2], 3))
print(minimum_incompatibility([3, 1, 2], 1))
print(minimum_incompatibility([1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8], 4))
batch(3000, 8)
batch(300, 12)
batch(20, 16)
