# LeetCode #1055: Shortest Way to Form String -- one pass over the source
# per piece. The Python mirror of shortest_way.kara; its output is
# byte-identical.


def shortest_way(source, target):
    pieces = 0
    i = 0
    while i < len(target):
        start = i
        for c in source:
            if i < len(target) and target[i] == c:
                i += 1
        if i == start:
            return -1
        pieces += 1
    return pieces


# ---- test harness ----

class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_word(n, letters, rng):
    return "".join(chr(97 + rng.next() % letters) for _ in range(n))


def trial(count, longest, letters, rng):
    formed = 0
    total = 0
    check = 0
    for _ in range(count):
        source = random_word(rng.next() % longest + 1, letters, rng)
        target = random_word(rng.next() % longest + 1, letters, rng)
        answer = shortest_way(source, target)
        if answer > 0:
            formed += 1
            total += answer
        check = (check * 131 + answer + 2) % 1000000007
    return formed, total, check


def main():
    examples = [
        ("abc", "abcbc"),
        ("abc", "acdbc"),
        ("xyz", "xzyxz"),
        ("a", "aaaa"),
        ("abc", "cba"),
        ("aaa", "aaaa"),
        ("abcab", "bacab"),
        ("ab", "ba"),
        ("source", "source"),
        ("xy", "z"),
    ]
    for source, target in examples:
        print(f"{source} {target} -> {shortest_way(source, target)}")
    rng = Rng(1055)
    formed, total, check = trial(3000, 8, 3, rng)
    print(f"3000 random pairs of 1 to 8 letters of 3: {formed} formed, total {total}, checksum {check}")
    formed, total, check = trial(300, 1000, 26, rng)
    print(f"300 random pairs of 1 to 1000 letters of 26: {formed} formed, total {total}, checksum {check}")
    source = random_word(1000, 25, rng)
    backwards = source[::-1]
    repeated = "y" * 1000
    print(f"1000 letters, the source reversed: {shortest_way(source, backwards)}")
    print(f"1000 letters, the source itself: {shortest_way(source, source)}")
    print(f"1000 letters, 1000 y: {shortest_way(source, repeated)}")
    print(f"1000 letters, a z at the end: {shortest_way(source, backwards + 'z')}")


main()
