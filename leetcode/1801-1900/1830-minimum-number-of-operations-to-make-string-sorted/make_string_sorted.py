# LeetCode #1830: Minimum Number of Operations to Make String Sorted -- the
# ★ arm in Python
MOD = 1000000007


def make_string_sorted(s):
    n = len(s)
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inverse = [1] * (n + 1)
    inverse[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n - 1, -1, -1):
        inverse[i] = inverse[i + 1] * (i + 1) % MOD
    count = [0] * 26
    operations = 0
    for i in range(n - 1, -1, -1):
        c = ord(s[i]) - ord('a')
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


print(make_string_sorted("cba"), make_string_sorted("aabaa"), make_string_sorted("cdbea"), make_string_sorted("leetcodeleetcodeleetcode"))
print(make_string_sorted("q"), make_string_sorted("abcz"), make_string_sorted("mmmm"), make_string_sorted("dcba"), make_string_sorted("za"))
backwards = "".join(chr(ord('z') - i % 26) for i in range(3000))
rand = "".join(chr(ord('a') + next_random() % 26) for _ in range(3000))
print(f"the most: {make_string_sorted(backwards)} {make_string_sorted(rand)}")
check = 0
for _ in range(3000):
    n = 1 + next_random() % 12
    s = "".join(chr(ord('a') + next_random() % 5) for _ in range(n))
    check = (check * 31 + make_string_sorted(s)) % 1000000007
print(f"3000 random strings: checksum {check}")
