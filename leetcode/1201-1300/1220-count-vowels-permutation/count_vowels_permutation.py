# LeetCode #1220: Count Vowels Permutation -- the Python mirror of the ★
# arm: five running counts, the strings of the length so far that end in
# each vowel; a letter's next count is the sum over the letters that may
# come before it. O(n).


def count_vowel_permutation(n):
    modulus = 1_000_000_007
    a = e = i = o = u = 1
    for _ in range(1, n):
        a, e, i, o, u = (e + i + u) % modulus, (a + i) % modulus, (e + o) % modulus, i, (i + o) % modulus
    return (a + e + i + o + u) % modulus


def main():
    for n in [1, 2, 5, 144]:
        print(f"n = {n}: {count_vowel_permutation(n)}")
    check = 0
    for n in range(1, 201):
        check = (check * 131 + count_vowel_permutation(n)) % 1000000007
    print(f"n from 1 to 200: checksum {check}")
    print(f"n = 10^4: {count_vowel_permutation(10000)}")
    print(f"n = 2 * 10^4: {count_vowel_permutation(20000)}")


main()
