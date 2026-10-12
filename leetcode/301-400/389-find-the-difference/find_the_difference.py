# LeetCode #389: Find the Difference -- XOR of every byte.
# Mirrors find_the_difference.kara.


def find_the_difference(s, t):
    x = 0
    for b in s.encode():
        x ^= b
    for b in t.encode():
        x ^= b
    return chr(x)


def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    for s, t in [("abcd", "abcde"), ("", "y"), ("a", "aa"), ("ae", "aea"), ("zzz", "zzzz"), ("abc", "zcba")]:
        print(f'"{s}", "{t}" -> {find_the_difference(s, t)}')
    seed = [389]
    right = checksum = 0
    for _ in range(3000):
        n = step(seed) % 61
        letters = [chr(step(seed) % 26 + 97) for _ in range(n)]
        s = "".join(letters)
        added = chr(step(seed) % 26 + 97)
        at = step(seed) % (n + 1)
        letters.insert(at, added)
        i = len(letters) - 1
        while i > 0:
            j = step(seed) % (i + 1)
            letters[i], letters[j] = letters[j], letters[i]
            i -= 1
        t = "".join(letters)
        got = find_the_difference(s, t)
        if got == added:
            right += 1
        checksum = (checksum * 31 + ord(got)) % 1000000007
    print(f"3000 random pairs: {right} right, checksum {checksum}")


main()
