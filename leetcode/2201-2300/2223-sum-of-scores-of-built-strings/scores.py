# LeetCode #2223: Sum of Scores of Built Strings -- mirror of
# scores.kara: the Z-function by the Z-algorithm, z[0] = n, summed.
# O(n).


def sum_scores(s):
    n = len(s)
    z = [0] * n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l = i
            r = i + z[i]
    return sum(z)


seed = 2223


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n letters from the first `letters` of the alphabet
def draw_word(n, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return "".join(alphabet[next_random() % letters] for _ in range(n))


def show(s):
    print(f"\"{s}\" -> {sum_scores(s)}")


def main():
    # LeetCode's two examples, then four more: one letter, one letter
    # throughout, all different, and a repeated pair
    show("babab")
    show("azbazbzaz")
    show("a")
    show("aaaa")
    show("abcd")
    show("abab")
    # 3000 random strings of 1 to 40 letters from 1, 2 and 26 letters in
    # turn
    check = 0
    for c in range(3000):
        n = next_random() % 40 + 1
        s = draw_word(n, [1, 2, 26][c % 3])
        check = (check * 31 + sum_scores(s)) % 1000000007
    print(f"3000 strings: checksum {check}")
    # the constraints' largest: 10^5 of one letter, whose sum passes
    # i32, and 10^5 random from two letters
    same = "a" * 100000
    wide = draw_word(100000, 2)
    print(f"10^5 alike: {sum_scores(same)}; 10^5 of two letters: {sum_scores(wide)}")


main()
