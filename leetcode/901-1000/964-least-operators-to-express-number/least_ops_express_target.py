# LeetCode #964: Least Operators to Express Number -- digit DP.
#
# Mirrors least_ops_express_target.kara: target's base-x digits settled
# from the lowest, each made as d copies of x^k (pos) or as x - d copies
# subtracted from a carried x^(k+1) (neg); x^k costs k operators, 1 costs
# 2, and the first term's sign comes off the end.


def least_ops_express_target(x, target):
    t = target
    pos = neg = k = 0
    while t > 0:
        cur = t % x
        t //= x
        if k > 0:
            pos, neg = min(cur * k + pos, (cur + 1) * k + neg), min((x - cur) * k + pos, (x - cur - 1) * k + neg)
        else:
            pos, neg = cur * 2, (x - cur) * 2
        k += 1
    return min(pos, k + neg) - 1


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    cases = [(3, 19), (5, 501), (100, 100000000), (2, 1), (2, 2), (3, 2), (100, 1), (100, 99), (100, 50), (2, 3),
             (7, 343), (7, 342)]
    for x, target in cases:
        print(f"x = {x}, target = {target}: {least_ops_express_target(x, target)}")
    total = 0
    check = 0
    for x in range(2, 13):
        for target in range(1, 301):
            n = least_ops_express_target(x, target)
            total += n
            check = (check * 31 + n) % 1000000007
    print(f"targets 1 to 300 for x from 2 to 12: {total} operators, checksum {check}")
    seed = 964
    total = 0
    check = 0
    for _ in range(300):
        x = 2 + next_random() % 99
        target = 1 + (next_random() * 32768 + next_random()) % 200000000
        n = least_ops_express_target(x, target)
        total += n
        check = (check * 31 + n) % 1000000007
    print(f"300 random cases up to 2 * 10^8: {total} operators, checksum {check}")
    for x, target in [(2, 200000000), (100, 200000000), (99, 199999999), (2, 134217728), (2, 134217727), (3, 129140163),
                      (10, 100000000), (10, 99999999)]:
        print(f"x = {x}, target = {target}: {least_ops_express_target(x, target)}")


main()
