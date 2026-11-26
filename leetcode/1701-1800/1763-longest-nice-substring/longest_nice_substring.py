# LeetCode #1763: Longest Nice Substring -- the ★ arm in Python, with the
# same harness.
def longest_nice_substring(s):
    for i, c in enumerate(s):
        if c.swapcase() not in s:
            left = longest_nice_substring(s[:i])
            right = longest_nice_substring(s[i + 1:])
            return right if len(right) > len(left) else left
    return s


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters, upper):
    out = []
    for _ in range(n):
        base = 65 if next_random() % 100 < upper else 97
        out.append(chr(base + next_random() % letters))
    return "".join(out)


def main():
    global seed
    print(" ".join(f'"{longest_nice_substring(s)}"' for s in ["YazaAay", "Bb", "c", "dDzeE"]))
    print(" ".join(f'"{longest_nice_substring(s)}"' for s in ["abcABx", "aAbBcC", "aAxbB", "qwertyEe", "aXXXXA"]))
    seed = 1763
    few = random_text(100, 3, 50)
    many = random_text(100, 26, 50)
    doubled = "aA" * 50
    print(f"100 letters: {len(longest_nice_substring(few))} {len(longest_nice_substring(many))} {len(longest_nice_substring(doubled))}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        letters = 1 + next_random() % 5
        upper = next_random() % 101
        s = random_text(n, letters, upper)
        nice = longest_nice_substring(s)
        first = s.find(nice) if nice else 0
        check = (check * 31 + len(nice) * 100 + first) % 1000000007
    print(f"3000 random strings: checksum {check}")


main()
