# LeetCode #2185: Counting Words With a Given Prefix -- the Python mirror
# of prefix_count.kara: each word asked whether it starts with the
# prefix.


def prefix_count(words, pref):
    return sum(1 for w in words if w.startswith(pref))


# ---- test harness ---------------------------------------------------------

seed = 2185


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def show(words, pref):
    quoted = ", ".join(f"\"{w}\"" for w in words)
    print(f"[{quoted}], \"{pref}\" -> {prefix_count(words, pref)}")


def main():
    show(["pay", "attention", "practice", "attend"], "at")
    show(["leetcode", "win", "loops", "success"], "code")
    show(["a"], "a")
    show(["ab", "abc", "a"], "abc")
    show(["xyz", "xy", "x", "xyzw"], "x")
    show(["ba", "ab", "aba"], "ab")
    total = 0
    check = 0
    for rnd in range(2000):
        letters = [2, 3, 26][rnd % 3]
        n = next_random() % 20 + 1
        words = [random_word(next_random() % 6 + 1, letters) for _ in range(n)]
        pref = random_word(next_random() % 3 + 1, letters)
        found = prefix_count(words, pref)
        total += found
        check = (check * 31 + found + n) % 1000000007
    print(f"2000 lists: {total} words in all, checksum {check}")
    long_word = "a" * 100
    words = [long_word] * 50 + ["a" * 99 + "b"] * 50
    print(f"100 words of 100 letters: {prefix_count(words, long_word)} {prefix_count(words, 'a' * 99)} {prefix_count(words, 'b')}")


main()
