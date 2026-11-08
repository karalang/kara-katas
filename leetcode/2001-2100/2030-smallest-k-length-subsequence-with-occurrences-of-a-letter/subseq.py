# LeetCode #2030: Smallest K-Length Subsequence With Occurrences of a Letter
# -- Python mirror of the ★ arm (subseq.kara). A stack of the answer so
# far: a character pops the larger ones above it while enough characters
# are left to refill the stack to k and enough copies of `letter` are left
# to keep `repetition`; it goes on the stack while there is room that the
# letters still owed do not need. O(n).


def smallest_subsequence(s, k, letter, repetition):
    n = len(s)
    remain = s.count(letter)
    stack = []
    have = 0
    for i, c in enumerate(s):
        while (stack and stack[-1] > c and len(stack) - 1 + n - i >= k
               and (stack[-1] != letter or have - 1 + remain >= repetition)):
            if stack.pop() == letter:
                have -= 1
        if len(stack) < k:
            if c == letter:
                stack.append(c)
                have += 1
            elif k - len(stack) > repetition - have:
                stack.append(c)
        if c == letter:
            remain -= 1
    return "".join(stack)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(check, text):
    for b in text.encode():
        check = (check * 31 + b) % 1000000007
    return check


# `n` letters from the first `a` of the alphabet, each a step from the last
# with odds `climb` in 10 of going up
def draw(n, a, climb):
    out = []
    c = next_random() % a
    for _ in range(n):
        r = next_random() % 10
        if r < climb:
            c = (c + 1) % a
        elif r < climb + 3:
            c = next_random() % a
        out.append(chr(97 + c))
    return "".join(out)


def problem(s):
    k = next_random() % len(s) + 1
    letter = s[next_random() % len(s)]
    have = s.count(letter)
    repetition = next_random() % min(k, have) + 1
    return k, letter, repetition


def main():
    global seed
    examples = [
        ("leet", 3, "e", 1),
        ("leetcode", 4, "e", 2),
        ("bb", 2, "b", 2),
        ("aaabbbcccddd", 3, "b", 2),
        ("zyxwvutsrqponmlkjihgfedcba", 5, "z", 1),
        ("bacbacbac", 4, "c", 3),
        ("abcabcabc", 9, "a", 3),
        ("mississippi", 4, "s", 3),
    ]
    for s, k, letter, repetition in examples:
        print(f"{s} {k} {letter} {repetition} -> {smallest_subsequence(s, k, letter, repetition)}")
    seed = 2030
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 20 + 1
        a = next_random() % 6 + 1
        s = draw(n, a, next_random() % 6)
        k, letter, repetition = problem(s)
        got = smallest_subsequence(s, k, letter, repetition)
        total += got.count(letter)
        check = fold(check, got)
    print(f"3000 problems of up to 20 letters: {total} letters kept, checksum {check}")
    total = 0
    check = 0
    for a in range(6):
        n = [50000, 50000, 50000, 50000, 2000, 2000][a]
        s = draw(n, [26, 3, 26, 2, 26, 5][a], [2, 5, 7, 4, 3, 6][a])
        k = [49990, 20, 49900, 7, 1000, 1500][a]
        letter = s[next_random() % n]
        repetition = min(k, s.count(letter), [5, 3, 49000, 7, 300, 900][a])
        got = smallest_subsequence(s, k, letter, repetition)
        total += got.count(letter)
        check = fold(check, got)
    print(f"6 problems of up to 50000 letters: {total} letters kept, checksum {check}")


main()
