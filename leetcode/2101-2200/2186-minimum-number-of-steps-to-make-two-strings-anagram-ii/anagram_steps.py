# LeetCode #2186: Minimum Number of Steps to Make Two Strings Anagram II
# -- the Python mirror of anagram_steps.kara: each letter counted up in s
# and down in t, and the counts' sizes summed.


def min_steps(s, t):
    balance = [0] * 26
    for b in s.encode():
        balance[b - 97] += 1
    for b in t.encode():
        balance[b - 97] -= 1
    steps = 0
    for d in balance:
        steps += abs(d)
    return steps


# ---- test harness ---------------------------------------------------------

seed = 2186


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def show(s, t):
    print(f"\"{s}\", \"{t}\" -> {min_steps(s, t)}")


def main():
    show("leetcode", "coats")
    show("night", "thing")
    show("a", "a")
    show("a", "b")
    show("aaab", "ab")
    show("abcde", "edcba")
    total = 0
    check = 0
    for rnd in range(2000):
        letters = [3, 26][rnd % 2]
        a = next_random() % 30 + 1
        b = next_random() % 30 + 1
        s = random_word(a, letters)
        t = random_word(b, letters)
        steps = min_steps(s, t)
        total += steps
        check = (check * 31 + steps + a) % 1000000007
    print(f"2000 pairs: {total} steps in all, checksum {check}")
    all_a = "a" * 200000
    all_z = "z" * 200000
    s = random_word(200000, 26)
    t = random_word(200000, 26)
    back = s[::-1]
    print(f"2 * 10^5 letters: {min_steps(all_a, all_z)} {min_steps(s, t)} {min_steps(s, back)}")


main()
