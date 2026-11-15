# LeetCode #2207: Maximize Number of Subsequences in a String -- Python
# mirror of the ★ arm: one pass counting the first letter so far, each
# second letter adding that count; the added letter is best a first letter
# at the front or a second letter at the end, whichever is more common.


def maximum_subsequence_count(text, pattern):
    first, second = pattern[0], pattern[1]
    firsts = seconds = pairs = 0
    for ch in text:
        if ch == second:
            pairs += firsts
            seconds += 1
        if ch == first:
            firsts += 1
    return pairs + max(firsts, seconds)


# ---- test harness ---------------------------------------------------------

seed = 2207


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def show(text, pattern):
    print(f'"{text}", "{pattern}" -> {maximum_subsequence_count(text, pattern)}')


def main():
    show("abdcdbc", "ac")
    show("aabb", "ab")
    show("aaa", "aa")
    show("xyz", "ab")
    show("bbb", "ab")
    show("bbaa", "ab")
    best = 0
    check = 0
    for c in range(3000):
        letters = [2, 3, 26][c % 3]
        n = next_random() % 30 + 1
        text = random_word(n, letters)
        pattern = random_word(2, letters)
        got = maximum_subsequence_count(text, pattern)
        best = max(best, got)
        check = (check * 31 + got) % 1000000007
    print(f"3000 texts: most {best}, checksum {check}")
    half = "a" * 50000 + "b" * 50000
    print(f'50000 a then 50000 b, "ab" -> {maximum_subsequence_count(half, "ab")}')
    same = "a" * 100000
    print(f'10^5 a, "aa" -> {maximum_subsequence_count(same, "aa")}')
    print(f'10^5 a, "ba" -> {maximum_subsequence_count(same, "ba")}')


main()
