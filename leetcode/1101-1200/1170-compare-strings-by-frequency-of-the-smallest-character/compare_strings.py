# LeetCode #1170: Compare Strings by Frequency of the Smallest Character --
# the mirror of the Kāra ★ arm, counts by frequency. With `lit` as its
# argument it reads the statement literally instead: every query against
# every word, f taken as the count of min(s).
import sys


def f(s):
    smallest = ord('z') + 1
    count = 0
    for b in s.encode():
        if b < smallest:
            smallest = b
            count = 1
        elif b == smallest:
            count += 1
    return count


def num_smaller_by_frequency(queries, words):
    above = [0] * 12
    for w in words:
        above[f(w)] += 1
    for k in range(10, -1, -1):
        above[k] += above[k + 1]
    return [above[f(q) + 1] for q in queries]


def literal(queries, words):
    def freq(s):
        return s.count(min(s))
    return [sum(1 for w in words if freq(q) < freq(w)) for q in queries]


seed = [0]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def digest(xs):
    h = 0
    for x in xs:
        h = (h * 131 + x + 1) % 1000000007
    return h


def random_word(letters):
    n = 1 + next_random() % 10
    return ''.join(chr(ord('a') + next_random() % letters) for _ in range(n))


def main():
    solve = literal if sys.argv[1:] == ['lit'] else num_smaller_by_frequency

    def show(queries, words):
        got = solve(queries, words)
        print(f"{' '.join(queries)} / {' '.join(words)} -> [{', '.join(map(str, got))}]")

    show(["cbd"], ["zaaaz"])
    show(["bbb", "cc"], ["a", "aa", "aaa", "aaaa"])
    show(["ab", "aab"], ["ba", "bba", "zz"])
    show(["aaaaaaaaaa", "z"], ["bbbbbbbbbb", "a", "yzyzyzyzyz"])
    show(["zzza", "azzz", "zaza"], ["q", "qq", "qqq"])
    seed[0] = 1170
    total = 0
    check = 0
    for i in range(300):
        letters = 3 if i % 2 == 0 else 26
        nq = 1 + next_random() % 50
        nw = 1 + next_random() % 50
        queries = [random_word(letters) for _ in range(nq)]
        words = [random_word(letters) for _ in range(nw)]
        got = solve(queries, words)
        total += sum(got)
        check = (check * 31 + digest(got)) % 1000000007
    print(f"300 random lists: total {total}, checksum {check}")
    for letters in [2, 5, 26]:
        queries = [random_word(letters) for _ in range(2000)]
        words = [random_word(letters) for _ in range(2000)]
        got = solve(queries, words)
        print(f"2000 by 2000 over {letters} letters: total {sum(got)}, checksum {digest(got)}")


if __name__ == '__main__':
    main()
