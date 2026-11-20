# LeetCode #1220 bench, Python mirror of the Kāra ★ arm: five running
# counts, the strings of the length so far that end in each vowel, for
# every n from 1 to 8000; checksum of the answers.


def count_vowel_permutation(n):
    modulus = 1_000_000_007
    a = e = i = o = u = 1
    for _ in range(1, n):
        a, e, i, o, u = (e + i + u) % modulus, (a + i) % modulus, (e + o) % modulus, i, (i + o) % modulus
    return (a + e + i + o + u) % modulus


check = 0
for n in range(1, 8001):
    check = (check * 131 + count_vowel_permutation(n)) % 1000000007
print(f"every n from 1 to 8000: checksum {check}")
