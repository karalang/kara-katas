# LeetCode #1781: Sum of Beauty of All Substrings -- the ★ arm in Python:
# from each start, the letters' counts grown one letter at a time.


def beauty_sum(s):
    n = len(s)
    total = 0
    for i in range(n):
        counts = [0] * 26
        for j in range(i, n):
            counts[ord(s[j]) - 97] += 1
            most, fewest = 0, n
            for c in counts:
                if c > 0:
                    most = max(most, c)
                    fewest = min(fewest, c)
            total += most - fewest
    return total


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def main():
    global seed
    print(f"{beauty_sum('aabcb')} {beauty_sum('aabcbaa')}")
    print(f"{beauty_sum('z')} {beauty_sum('aaaa')} {beauty_sum('abcdefghijklmnopqrstuvwxyz')} {beauty_sum('abababab')} {beauty_sum('aaaaab')}")
    seed = 1781
    wide = random_word(500, 26)
    two = random_word(500, 2)
    same = "q" * 500
    print(f"the most: {beauty_sum(wide)} {beauty_sum(two)} {beauty_sum(same)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        letters = 1 + next_random() % 6
        check = (check * 31 + beauty_sum(random_word(n, letters))) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
