# LeetCode #1178: Number of Valid Words for Each Puzzle -- a Python mirror
# of the ★ arm (valid_words.kara): each word's set of letters as a bit mask,
# counted in a dict, and each puzzle's subsets of its other six letters
# walked with `sub = (sub - 1) & rest`. With `lit` it instead checks every
# puzzle against every distinct set of letters the words have, as the
# statement reads, and prints the same.
import sys
from collections import Counter

LIT = len(sys.argv) > 1 and sys.argv[1] == "lit"


def mask_of(w):
    m = 0
    for c in w:
        m |= 1 << (ord(c) - 97)
    return m


def find_num_of_valid_words(words, puzzles):
    count = Counter(mask_of(w) for w in words)
    answer = []
    for p in puzzles:
        first = 1 << (ord(p[0]) - 97)
        rest = 0
        for c in p[1:]:
            rest |= 1 << (ord(c) - 97)
        total = 0
        sub = rest
        while True:
            total += count.get(sub | first, 0)
            if sub == 0:
                break
            sub = (sub - 1) & rest
        answer.append(total)
    return answer


def literal(words, puzzles):
    count = Counter(mask_of(w) for w in words)
    answer = []
    for p in puzzles:
        first = 1 << (ord(p[0]) - 97)
        allowed = mask_of(p)
        answer.append(sum(n for m, n in count.items() if m & first and m & ~allowed == 0))
    return answer


solve = literal if LIT else find_num_of_valid_words
seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def distinct(m, k):
    letters = [chr(97 + i) for i in range(m)]
    for i in range(k):
        j = i + next_random() % (m - i)
        letters[i], letters[j] = letters[j], letters[i]
    return letters[:k]


def word(m, longest):
    s = distinct(m, 1 + next_random() % 7)
    n = 4 + next_random() % (longest - 3)
    return "".join(s[next_random() % len(s)] for _ in range(n))


def puzzle(m):
    return "".join(distinct(m, 7))


def show(a):
    return "[" + ", ".join(str(x) for x in a) + "]"


def main():
    global seed
    words = ["aaaa", "asas", "able", "ability", "actt", "actor", "access"]
    puzzles = ["aboveyz", "abrodyz", "abslute", "absoryz", "actresz", "gaswxyz"]
    print(f"example 1: {show(solve(words, puzzles))}")
    words = ["apple", "pleas", "please"]
    puzzles = ["aelwxyz", "aelpxyz", "aelpsxy", "saelpxy", "xaelpsy"]
    print(f"example 2: {show(solve(words, puzzles))}")
    words = ["aaaa", "aaab", "abcz", "bbbb", "bbbb", "bbbb", "abcdefg"]
    puzzles = ["abcdefg", "bacdefg", "zabcdef", "gfedcba", "hijklmn"]
    print(f"small: {show(solve(words, puzzles))}")
    seed = 1178
    total = 0
    check = 0
    for _ in range(300):
        words = [word(9, 12) for _ in range(1 + next_random() % 30)]
        puzzles = [puzzle(10) for _ in range(1 + next_random() % 10)]
        for a in solve(words, puzzles):
            total += a
            check = (check * 131 + a + 1) % 1000000007
    print(f"300 random problems: {total} valid in all, checksum {check}")
    words = [word(12, 50) for _ in range(100000)]
    puzzles = [puzzle(12) for _ in range(10000)]
    answer = solve(words, puzzles)
    check = 0
    for a in answer:
        check = (check * 131 + a + 1) % 1000000007
    print(f"100000 words, 10000 puzzles: {sum(answer)} valid in all, checksum {check}")


main()
