# LeetCode #2318: Number of Distinct Roll Sequences -- the bench, the ★
# arm in Python. The count of sequences ending in each pair of rolls, a 6
# by 6 table rolled forward once per roll, each next roll coprime with
# the last and unlike the last two. O(216 n).


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def distinct_sequences(n):
    modulus = 1000000007
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
                            nxt[b][c] = (nxt[b][c] + ends[a][b]) % modulus
        ends = nxt
    total = 0
    for a in range(6):
        for b in range(6):
            total = (total + ends[a][b]) % modulus
    return total


check = 0
for p in range(5):
    for n in range(9981, 10001):
        check = (check * 31 + distinct_sequences(n) + p) % 1000000007
print(f"5 passes over 20 counts of rolls up to 10^4: checksum {check}")
