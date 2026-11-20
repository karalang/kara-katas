# LeetCode #1735: Count Ways to Make Array With Product -- the bench
# (ways.kara): the product over k's primes of C(n + e - 1, e), read off
# factorials and their inverses.

MOD = 1000000007


def ways_to_fill_array(queries):
    top = max(q[0] for q in queries) + 14
    fact = [1] * (top + 1)
    for i in range(1, top + 1):
        fact[i] = fact[i - 1] * i % MOD
    inverse = [1] * (top + 1)
    inverse[top] = pow(fact[top], MOD - 2, MOD)
    for i in range(top, 0, -1):
        inverse[i - 1] = inverse[i] * i % MOD

    def choose(m, r):
        return fact[m] * inverse[r] % MOD * inverse[m - r] % MOD

    answers = []
    for n, k in queries:
        ways = 1
        p = 2
        while p * p <= k:
            e = 0
            while k % p == 0:
                k //= p
                e += 1
            ways = ways * choose(n + e - 1, e) % MOD
            p += 1
        if k > 1:
            ways = ways * n % MOD
        answers.append(ways)
    return answers


seed = 1735


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count = 10
rounds = 60
q = 10000
problems = []
for _ in range(count):
    queries = []
    for _ in range(q):
        n = next_random() % 10000 + 1
        k = next_random() % 10000 + 1
        queries.append([n, k])
    problems.append(queries)
total = 0
check = 0
for r in range(rounds):
    for queries in problems:
        answers = ways_to_fill_array(queries)
        total += answers[0]
        check = (check * 31 + answers[0] + answers[q // 2] + answers[q - 1] + r) % 1000000007
print(f"{count} lists of {q} queries, {rounds} rounds: first answers sum to {total}, checksum {check}")
