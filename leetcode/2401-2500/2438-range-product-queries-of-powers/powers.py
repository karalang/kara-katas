# LeetCode #2438: Range Product Queries of Powers -- the Python mirror of
# the ★ arm: the exponents' prefix sums, and two to each range's sum by
# squaring modulo 10^9 + 7.

MOD = 1000000007
seed = 2438


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def power_of_two(exponent):
    result = 1
    base = 2
    e = exponent
    while e > 0:
        if e % 2 == 1:
            result = result * base % MOD
        base = base * base % MOD
        e //= 2
    return result


def product_queries(n, queries):
    prefix = [0]
    for bit in range(31):
        if (n >> bit) & 1 == 1:
            prefix.append(prefix[-1] + bit)
    return [power_of_two(prefix[q[1] + 1] - prefix[q[0]]) for q in queries]


def set_bits(n):
    return bin(n).count("1")


def every_query(n):
    k = set_bits(n)
    return [[l, r] for l in range(k) for r in range(l, k)]


def fold(values):
    check = 0
    for v in values:
        check = (check * 31 + v) % 1000000007
    return check


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    cases = [
        (15, [[0, 1], [2, 2], [0, 3]]),
        (2, [[0, 0]]),
        (1, [[0, 0]]),
        (536870911, [[0, 28], [28, 28], [10, 20]]),
    ]
    for n, queries in cases:
        print(f"{n}: {show(product_queries(n, queries))}")
    for n in [536870911, 1000000000]:
        print(f"{n}, every query: checksum {fold(product_queries(n, every_query(n)))}")
    k = set_bits(999999999)
    many = []
    for _ in range(100000):
        a = next_random() % k
        b = next_random() % k
        many.append([min(a, b), max(a, b)])
    print(f"999999999, 10^5 random queries: checksum {fold(product_queries(999999999, many))}")
    check = 0
    for _ in range(3000):
        r = next_random()
        n = 1 + (r * 32768 + next_random()) % 1000000000
        k = set_bits(n)
        queries = []
        for _ in range(5):
            a = next_random() % k
            b = next_random() % k
            queries.append([min(a, b), max(a, b)])
        check = (check * 31 + fold(product_queries(n, queries))) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
