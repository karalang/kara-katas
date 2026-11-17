# LeetCode #1181: Before and After Puzzle -- a Python mirror of the ★ arm
# (before_and_after_puzzles.kara): the phrases' indices grouped by first
# word, each phrase's last word looking up the phrases that start with it,
# the puzzles gathered into a set and sorted. With `lit` it instead joins
# every ordered pair of different phrases split into words, as the
# statement reads, and prints the same.
import sys

LIT = len(sys.argv) > 1 and sys.argv[1] == "lit"


def before_and_after_puzzles(phrases):
    starting = {}
    for i, p in enumerate(phrases):
        starting.setdefault(p.split(" ", 1)[0], []).append(i)
    puzzles = set()
    for i, p in enumerate(phrases):
        last = p.rsplit(" ", 1)[-1]
        for j in starting.get(last, []):
            if j != i:
                rest = phrases[j].split(" ", 1)
                puzzles.add(p + (" " + rest[1] if len(rest) > 1 else ""))
    return sorted(puzzles)


def literal(phrases):
    found = set()
    for i, a in enumerate(phrases):
        for j, b in enumerate(phrases):
            wa, wb = a.split(" "), b.split(" ")
            if i != j and wa[-1] == wb[0]:
                found.add(" ".join(wa + wb[1:]))
    return sorted(found)


solve = literal if LIT else before_and_after_puzzles
seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(puzzles):
    return f"{len(puzzles)} [{' / '.join(puzzles)}]"


VOCABULARY = ["a", "be", "cat", "dog", "eel", "fig", "go", "hat"]


def phrase(m, most):
    n = 1 + next_random() % most
    return " ".join(VOCABULARY[next_random() % m] for _ in range(n))


def fold(check, puzzles):
    check = (check * 131 + len(puzzles)) % 1000000007
    for p in puzzles:
        for c in p:
            v = 27 if c == " " else ord(c) - 96
            check = (check * 31 + v) % 1000000007
    return check


def main():
    global seed
    print(f"example 1: {show(solve(['writing code', 'code rocks']))}")
    phrases = [
        "mission statement", "a quick bite to eat", "a chip off the old block", "chocolate bar",
        "mission impossible", "a man on a mission", "block party", "eat my words", "bar of soap",
    ]
    print(f"example 2: {show(solve(phrases))}")
    print(f"example 3: {show(solve(['a', 'b', 'a']))}")
    print(f"small 1: {show(solve(['go go']))}")
    print(f"small 2: {show(solve(['go fig go', 'go fig go']))}")
    print(f"small 3: {show(solve(['eel', 'eel', 'eel cat']))}")
    print(f"small 4: {show(solve(['a be', 'be cat', 'cat a']))}")
    seed = 1181
    total = 0
    check = 0
    for _ in range(300):
        m = 1 + next_random() % 5
        count = 1 + next_random() % 12
        puzzles = solve([phrase(m, 4) for _ in range(count)])
        total += len(puzzles)
        check = fold(check, puzzles)
    print(f"300 random problems: {total} puzzles, checksum {check}")
    phrases = [phrase(8, 25) for _ in range(100)]
    puzzles = solve(phrases)
    print(f"100 phrases: {len(puzzles)} puzzles, checksum {fold(0, puzzles)}")


main()
