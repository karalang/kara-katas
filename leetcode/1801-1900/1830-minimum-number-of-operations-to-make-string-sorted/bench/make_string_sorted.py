# LeetCode #1830: Minimum Number of Operations to Make String Sorted -- the
# bench in Python: the ★ arm over 500 calls on runs of 1500 to 2999 letters
# cut from one string of 4500 random letters, built once, each run's start and
# length drawn from the checksum so far. Each call makes its run a string of
# its own.
MOD = 1000000007


def power(base, exp):
    result = 1
    b = base % MOD
    e = exp
    while e > 0:
        if e % 2 == 1:
            result = result * b % MOD
        b = b * b % MOD
        e //= 2
    return result


def make_string_sorted(s):
    letters = s.encode()
    n = len(letters)
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inverse = [1] * (n + 1)
    inverse[n] = power(fact[n], MOD - 2)
    for i in range(n - 1, -1, -1):
        inverse[i] = inverse[i + 1] * (i + 1) % MOD
    count = [0] * 26
    operations = 0
    for i in range(n - 1, -1, -1):
        c = letters[i] - 97
        count[c] += 1
        smaller = sum(count[:c])
        ways = fact[n - 1 - i] * smaller % MOD
        for k in count:
            ways = ways * inverse[k] % MOD
        operations = (operations + ways) % MOD
    return operations


seed = 1830


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


letters = bytes(97 + next_random() % 26 for _ in range(4500))
check = 0
for call in range(500):
    start = (check + call) % 1500
    length = 1500 + (check * 7 + call) % 1500
    s = letters[start:start + length].decode()
    check = (check * 31 + make_string_sorted(s)) % 1000000007
print(f"500 calls: checksum {check}")
