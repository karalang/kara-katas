# LeetCode #1735: Count Ways to Make Array With Product -- mirrors ways.kara
# (the ★ arm).

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


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def batch(count, most, top):
    total = 0
    check = 0
    for _ in range(count):
        q = next_random() % most + 1
        queries = []
        for _ in range(q):
            n = next_random() % top + 1
            k = next_random() % top + 1
            queries.append([n, k])
        for w in ways_to_fill_array(queries):
            total += w
            check = (check * 31 + w) % 1000000007
        check = (check * 31 + q) % 1000000007
    print(f"{count} lists of up to {most} queries up to {top}: ways sum to {total}, checksum {check}")


print(show(ways_to_fill_array([[2, 6], [5, 1], [73, 660]])))
print(show(ways_to_fill_array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]])))
print(show(ways_to_fill_array([[10000, 10000], [10000, 9973], [10000, 8192], [1, 8192]])))
batch(3000, 5, 36)
batch(300, 100, 10000)
batch(3, 10000, 10000)
