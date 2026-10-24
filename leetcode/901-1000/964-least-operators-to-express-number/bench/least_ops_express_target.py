# Benchmark: LeetCode #964 Least Operators to Express Number -- the ★
# arm, digit DP, on every x from 2 to 100 and 2000 targets below 2 * 10^8.
# Mirrors least_ops_express_target.kara.


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


def main():
    rounds = 80
    total = 0
    check = 0
    for r in range(rounds):
        for x in range(2, 101):
            for j in range(2000):
                n = least_ops_express_target(x, 200000000 - 99991 * j - r)
                total += n
                check = (check * 31 + n) % 1000000007
    print(f"{rounds} rounds over x from 2 to 100 and 2000 targets: {total} operators, checksum {check}")


main()
