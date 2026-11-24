# LeetCode #1347 -- Python mirror of the ★ arm: one count per letter, up
# for s and down for t, the positive counts summed.


def min_steps(s, t):
    count = [0] * 26
    for ch in s:
        count[ord(ch) - 97] += 1
    for ch in t:
        count[ord(ch) - 97] -= 1
    return sum(c for c in count if c > 0)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_word(seed, n, letters):
    return "".join(chr(97 + next_random(seed) % letters) for _ in range(n))


def main():
    e1 = min_steps("bab", "aba")
    e2 = min_steps("leetcode", "practice")
    e3 = min_steps("anagram", "mangaar")
    same = min_steps("q", "q")
    differ = min_steps("a", "z")
    seed = [1347]
    s = random_word(seed, 50000, 26)
    t = random_word(seed, 50000, 26)
    print(e1, e2, e3, same, differ, min_steps("a" * 50000, "b" * 50000), min_steps(s, t))
    total = 0
    check = 0
    for c in range(2000):
        if c % 10 == 0:
            n = 1 + next_random(seed) % 300
        else:
            n = 1 + next_random(seed) % 12
        letters = 2 if c % 3 == 0 else 5 if c % 3 == 1 else 26
        s = random_word(seed, n, letters)
        t = random_word(seed, n, letters)
        got = min_steps(s, t)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random pairs: {total} steps in all, checksum {check}")


main()
