# LeetCode #2117: Abbreviating the Product of a Range -- Python mirror of
# abbreviate.kara, the factors of 2 and 5 pulled out; same harness, same
# output.


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
    examples = [(1, 4), (2, 11), (371, 375), (1, 1), (10, 10), (9999, 10000), (1, 15), (1, 16)]
    for left, right in examples:
        print(f"[{left}, {right}] -> {abbreviate_product(left, right)}")
    seed = [2117]
    zeros = 0
    check = 0
    for _ in range(1000):
        left = next_random(seed) % 10000 + 1
        right = min(left + next_random(seed) % 61, 10000)
        got = abbreviate_product(left, right)
        for b in got.encode():
            check = (check * 31 + b) % 1000000007
        zeros += int(got.split("e")[-1])
    print(f"1000 ranges: {zeros} trailing zeros, checksum {check}")
    print(f"[1, 3000] -> {abbreviate_product(1, 3000)}")
    print(f"[9001, 10000] -> {abbreviate_product(9001, 10000)}")


main()
