# LeetCode #2117: Abbreviating the Product of a Range -- the benchmark,
# the same algorithm as abbreviate.kara: the factors of 2 and 5 pulled
# out, the rest modulo 100000 and capped at 10^11, and a float of the
# leading digits.


def abbreviate_product(left, right):
    cap = 100000000000
    twos = 0
    fives = 0
    last = 1
    exact = 1
    lead = 1.0
    for i in range(left, right + 1):
        x = i
        while x % 2 == 0:
            x //= 2
            twos += 1
        while x % 5 == 0:
            x //= 5
            fives += 1
        last = last * x % 100000
        exact = cap if exact > cap // x else exact * x
        lead *= float(i)
        while lead >= 1e12:
            lead /= 10.0
    zeros = min(twos, fives)
    for _ in range(twos - zeros):
        last = last * 2 % 100000
        exact = cap if exact > cap // 2 else exact * 2
    for _ in range(fives - zeros):
        last = last * 5 % 100000
        exact = cap if exact > cap // 5 else exact * 5
    if exact < 10000000000:
        return f"{exact}e{zeros}"
    while lead >= 1e5:
        lead /= 10.0
    return f"{int(lead)}...{last:05}e{zeros}"


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [2117]
    long = 0
    check = 0
    for _ in range(40000):
        left = next_random(seed) % 10000 + 1
        right = min(left + next_random(seed) % 3000, 10000)
        got = abbreviate_product(left, right)
        if "..." in got:
            long += 1
        for b in got.encode():
            check = (check * 31 + b) % 1000000007
    print(f"40000 solves: {long} long answers, checksum {check}")


main()
