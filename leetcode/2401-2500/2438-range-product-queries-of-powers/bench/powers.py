# LeetCode #2438: Range Product Queries of Powers -- the bench, the ★ arm:
# the exponents' prefix sums, and two to each range's sum by squaring
# modulo 10^9 + 7.

MOD = 1000000007


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
    answers = []
    for q in queries:
        answers.append(power_of_two(prefix[q[1] + 1] - prefix[q[0]]))
    return answers


seed = 2438


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    values = []
    every = []
    for _ in range(100):
        r = next_random()
        n = 1 + (r * 32768 + next_random()) % 1000000000
        k = bin(n).count("1")
        queries = []
        for _ in range(10000):
            a = next_random() % k
            b = next_random() % k
            queries.append([min(a, b), max(a, b)])
        values.append(n)
        every.append(queries)
    check = 0
    for p in range(10):
        for c in range(len(values)):
            answers = product_queries(values[c], every[c])
            m = len(answers)
            for i in range(m):
                check = (check * 31 + answers[(i + p) % m] + p) % 1000000007
    print(f"10 passes over 100 values of 10^4 queries: checksum {check}")


main()
