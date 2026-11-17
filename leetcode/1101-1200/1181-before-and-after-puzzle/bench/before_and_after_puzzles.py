# LeetCode #1181: Before and After Puzzle -- the ★ arm in Python: the
# phrases' indices grouped by first word in a dict, each phrase's last word
# looking up the phrases that start with it, the puzzles gathered in a set
# and sorted.


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


seed = 1181


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    vocabulary = ["a", "be", "cat", "dog", "eel", "fig", "go", "hat"]
    problems = []
    for _ in range(100):
        m = 2 + next_random() % 7
        phrases = []
        for _ in range(100):
            n = 1 + next_random() % 25
            phrases.append(" ".join(vocabulary[next_random() % m] for _ in range(n)))
        problems.append(phrases)
    rounds = 5
    check = 0
    for _ in range(rounds):
        for phrases in problems:
            puzzles = before_and_after_puzzles(phrases)
            check = (check * 131 + len(puzzles)) % 1000000007
            for p in puzzles:
                check = (check * 31 + len(p)) % 1000000007
    print(f"{rounds} rounds of 100 problems: checksum {check}")


main()
