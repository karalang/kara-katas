# LeetCode #1177: Can Make Palindrome from Substring -- the Python mirror
# of the ★ arm: one bit per letter, the parity masks of every prefix, and a
# query holds when the odd letters of its substring, halved, are at most
# k. With `lit` each substring's letters are counted afresh instead.
import sys

LIT = len(sys.argv) > 1 and sys.argv[1] == "lit"


def can_make_pali_queries(s, queries):
    if LIT:
        out = []
        for left, right, k in queries:
            count = [0] * 26
            for c in s[left:right + 1]:
                count[ord(c) - ord("a")] += 1
            odd = sum(1 for n in count if n % 2 == 1)
            out.append(odd // 2 <= k)
        return out
    masks = [0]
    for c in s:
        masks.append(masks[-1] ^ (1 << (ord(c) - ord("a"))))
    return [bin(masks[r + 1] ^ masks[l]).count("1") // 2 <= k for l, r, k in queries]


seed = 1177


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(length, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(length))


def random_queries(n, count, span, most):
    queries = []
    for _ in range(count):
        left = next_random() % n
        right = min(left + next_random() % span, n - 1)
        queries.append([left, right, next_random() % (most + 1)])
    return queries


def tally(answers):
    yes = 0
    check = 0
    for a in answers:
        bit = 1 if a else 0
        yes += bit
        check = (check * 3 + bit + 1) % 1000000007
    return yes, check


def show(v):
    return "[" + ", ".join("true" if a else "false" for a in v) + "]"


print(f"example 1: {show(can_make_pali_queries('abcda', [[3, 3, 0], [1, 2, 0], [0, 3, 1], [0, 3, 2], [0, 4, 1]]))}")
print(f"example 2: {show(can_make_pali_queries('lyb', [[0, 1, 0], [2, 2, 1]]))}")
print(f"small: {show(can_make_pali_queries('a', [[0, 0, 0]]))} {show(can_make_pali_queries('racecar', [[0, 6, 0], [1, 5, 0], [0, 5, 0]]))} {show(can_make_pali_queries('ab', [[0, 1, 0], [0, 1, 1], [0, 1, 100000]]))}")
alphabet = "abcdefghijklmnopqrstuvwxyz"
print(f"alphabet: {show(can_make_pali_queries(alphabet, [[0, 25, 12], [0, 25, 13], [0, 24, 12], [0, 24, 11]]))}")
yes = 0
check = 0
for _ in range(300):
    n = 1 + next_random() % 40
    s = letters(n, 1 + next_random() % 26)
    queries = random_queries(n, 20, n, 7)
    y, c = tally(can_make_pali_queries(s, queries))
    yes += y
    check = (check * 131 + c) % 1000000007
print(f"300 random strings: {yes} of 6000 true, checksum {check}")
s = letters(100000, 26)
queries = random_queries(100000, 99900, 64, 13)
queries += random_queries(100000, 100, 100000, 26)
y, c = tally(can_make_pali_queries(s, queries))
print(f"100000 letters, 100000 queries: {y} true, checksum {c}")
