# LeetCode #2318: Number of Distinct Roll Sequences -- the Python mirror
# of the ★ arm. The count of sequences ending in each pair of rolls, a 6
# by 6 table rolled forward once per roll.

from math import gcd

MOD = 1000000007


def distinct_sequences(n):
    if n == 1:
        return 6
    ends = [[1 if a != b and gcd(a + 1, b + 1) == 1 else 0 for b in range(6)] for a in range(6)]
    for _ in range(2, n):
        nxt = [[0] * 6 for _ in range(6)]
        for a in range(6):
            for b in range(6):
                if ends[a][b] > 0:
                    for c in range(6):
                        if c != a and c != b and gcd(b + 1, c + 1) == 1:
                            nxt[b][c] = (nxt[b][c] + ends[a][b]) % MOD
        ends = nxt
    return sum(sum(row) for row in ends) % MOD


for n in [4, 2, 1, 3, 10, 100, 10000]:
    print(f"{n}: {distinct_sequences(n)}")
check = 0
total = 0
for n in range(1, 301):
    ways = distinct_sequences(n)
    check = (check * 31 + ways) % 1000000007
    total += ways
print(f"300 counts: checksum {check}, {total} in all")
