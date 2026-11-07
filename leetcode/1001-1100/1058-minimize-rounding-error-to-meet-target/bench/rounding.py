# LeetCode #1058: Minimize Rounding Error to Meet Target -- the benchmark,
# the same algorithm as rounding.kara.


def thousandths(p):
    value = 0
    for c in p:
        if c != '.':
            value = value * 10 + (ord(c) - 48)
    return value


def minimize_error(prices, target):
    floor_sum = 0
    fractions = []
    for p in prices:
        t = thousandths(p)
        floor_sum += t // 1000
        if t % 1000 != 0:
            fractions.append(t % 1000)
    up = target - floor_sum
    if up < 0 or up > len(fractions):
        return "-1"
    fractions.sort(reverse=True)
    error = 0
    for k, f in enumerate(fractions):
        error += 1000 - f if k < up else f
    return f"{error // 1000}.{error % 1000:03}"


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_price(rng):
    whole = rng.next() % 1000
    part = 0 if rng.next() % 4 == 0 else rng.next() % 999 + 1
    return f"{whole}.{part:03}"


def main():
    rng = Rng(1058)
    lists = [[random_price(rng) for _ in range(500)] for _ in range(40)]
    calls = 0
    check = 0
    for _ in range(8):
        for prices in lists:
            floor_sum = 0
            with_fraction = 0
            for p in prices:
                t = thousandths(p)
                floor_sum += t // 1000
                if t % 1000 != 0:
                    with_fraction += 1
            for target in range(floor_sum - 1, floor_sum + with_fraction + 2):
                answer = minimize_error(prices, target)
                for c in answer:
                    check = (check * 131 + ord(c)) % 1000000007
                calls += 1
    print(f"{calls} calls: checksum {check}")


main()
