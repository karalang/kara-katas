# LeetCode #1058: Minimize Rounding Error to Meet Target -- mirror of
# rounding.kara: the largest fractions rounded up, in thousandths.


def thousandths(p):
    value = 0
    for c in p:
        if c != '.':
            value = value * 10 + int(c)
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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_price(most, fractions, seed):
    whole = next_random(seed) % most
    if next_random(seed) % 4 == 0:
        part = 0
    else:
        part = (next_random(seed) % fractions + 1) * (999 // fractions)
    return f"{whole}.{part:03}"


def trial(count, most, below, fractions, seed):
    reached = 0
    total = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        prices = []
        floor_sum = 0
        for _ in range(n):
            p = random_price(below, fractions, seed)
            floor_sum += thousandths(p) // 1000
            prices.append(p)
        target = floor_sum - 1 + next_random(seed) % (n + 3)
        answer = minimize_error(prices, target)
        if answer != "-1":
            reached += 1
            total += thousandths(answer)
        for c in answer:
            check = (check * 131 + ord(c)) % 1000000007
    return reached, total, check


def show(prices):
    return "[" + ", ".join(prices) + "]"


def main():
    examples = [
        (["0.700", "2.800", "4.900"], 8),
        (["1.500", "2.500", "3.500"], 10),
        (["1.500", "2.500", "3.500"], 9),
        (["0.000"], 0),
        (["0.000", "1.000"], 2),
        (["0.001", "999.999"], 1000),
        (["0.500", "0.500"], 1),
        (["1000.000", "0.250", "0.750"], 1001),
    ]
    for prices, target in examples:
        print(f"{show(prices)} {target} -> {minimize_error(prices, target)}")
    seed = [1058]
    reached, total, check = trial(3000, 8, 10, 4, seed)
    print(f"3000 problems of 1 to 8 prices below 10: {reached} reached, total {total}, checksum {check}")
    reached, total, check = trial(300, 500, 1000, 999, seed)
    print(f"300 problems of 1 to 500 prices below 1000: {reached} reached, total {total}, checksum {check}")
    prices = []
    floor_sum = 0
    with_fraction = 0
    for _ in range(500):
        p = random_price(1000, 999, seed)
        t = thousandths(p)
        floor_sum += t // 1000
        if t % 1000 != 0:
            with_fraction += 1
        prices.append(p)
    check = 0
    least = 1000000000
    most = 0
    for target in range(floor_sum - 1, floor_sum + with_fraction + 2):
        answer = minimize_error(prices, target)
        for c in answer:
            check = (check * 131 + ord(c)) % 1000000007
        if answer != "-1":
            least = min(least, thousandths(answer))
            most = max(most, thousandths(answer))
    print(f"500 prices, {with_fraction + 3} targets: checksum {check}, least {least}, most {most}")
    print(f"one past each end: {minimize_error(prices, floor_sum - 1)} {minimize_error(prices, floor_sum + with_fraction + 1)}")


main()
