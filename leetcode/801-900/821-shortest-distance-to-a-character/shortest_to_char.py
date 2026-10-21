# LeetCode 821 — Shortest Distance to a Character, by two sweeps.
#
# Mirrors shortest_to_char.kara: a sweep from the left keeps the last `c`
# seen and a sweep from the right the first, and each place keeps the
# nearer of the two.


def shortest_to_char(s, c):
    n = len(s)
    answer = [0] * n
    last = -n
    for i in range(n):
        if s[i] == c:
            last = i
        answer[i] = i - last
    last = 2 * n
    for i in range(n - 1, -1, -1):
        if s[i] == c:
            last = i
        answer[i] = min(answer[i], last - i)
    return answer


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(s, c):
    print(f"{s} {c} -> [{', '.join(map(str, shortest_to_char(s, c)))}]")


def summary(label, s, c):
    answer = shortest_to_char(s, c)
    print(f"{label}: {len(answer)} places, total {sum(answer)}, farthest {max(answer)}")


def main():
    show("loveleetcode", "e")
    show("aaab", "b")
    show("a", "a")
    show("ab", "a")
    show("baaab", "b")
    show("abcde", "c")
    show("eeee", "e")
    show("xaaaaaaxaax", "x")
    rng = Random(821)
    letters = "".join(chr(ord("a") + rng.next() % 26) for _ in range(10000))
    summary("random letters, q", letters, "q")
    summary("one z at the end", "a" * 9999 + "z", "z")
    summary("one z in the middle", "a" * 5000 + "z" + "a" * 4999, "z")
    total = 0
    check = 0
    for _ in range(300):
        length = 1 + rng.next() % 40
        s = "".join(chr(ord("a") + rng.next() % 3) for _ in range(length))
        c = chr(ord("a") + rng.next() % 3)
        at = rng.next() % (length + 1)
        with_c = s[:at] + c + s[at:]
        for d in shortest_to_char(with_c, c):
            total += d
            check = (check * 131 + d) % 1000000007
    print(f"300 random strings: total {total}, checksum {check}")


main()
