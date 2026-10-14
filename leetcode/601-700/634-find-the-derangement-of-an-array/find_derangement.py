# LeetCode #634: Find the Derangement of An Array -- Python mirror of the
# ★ arm.
#
# D(n) = (n - 1) * (D(n - 1) + D(n - 2)) modulo 10^9 + 7, kept in two
# variables.
MOD = 1000000007


def find_derangement(n):
    before, last = 1, 0
    for i in range(2, n + 1):
        before, last = last, (i - 1) * ((last + before) % MOD) % MOD
    return last


for n in [3, 2, 1, 4, 5, 6, 10, 12, 13, 20, 1000, 99999, 1000000]:
    print(f"n = {n} -> {find_derangement(n)}")
total = checksum = 0
for n in range(1, 2001):
    d = find_derangement(n)
    total = (total + d) % MOD
    checksum = (checksum * 31 + d) % MOD
print(f"1 to 2000: total {total}, checksum {checksum}")
