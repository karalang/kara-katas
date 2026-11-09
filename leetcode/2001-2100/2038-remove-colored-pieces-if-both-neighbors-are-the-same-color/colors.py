# LeetCode #2038: Remove Colored Pieces if Both Neighbors are the Same
# Color -- the ★ arm in Python, the same algorithm and harness as
# colors.kara: each player's moves counted, one per piece inside a run of
# their color, and Alice wins exactly when she has more.


def winner_of_game(colors):
    alice = bob = 0
    for i in range(1, len(colors) - 1):
        if colors[i - 1] == colors[i] == colors[i + 1]:
            if colors[i] == "A":
                alice += 1
            else:
                bob += 1
    return alice > bob


seed = 2038


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_colors(n, stay):
    out = []
    c = "A" if next_random() % 2 == 0 else "B"
    for _ in range(n):
        if next_random() % stay == 0:
            c = "B" if c == "A" else "A"
        out.append(c)
    return "".join(out)


def show(b):
    return "true" if b else "false"


def main():
    examples = ["AAABABB", "AA", "ABBBBBBBAAA", "A", "AAA", "BBB", "AAABBB", "AAAABBB", "ABABAB"]
    for colors in examples:
        print(f"{colors} -> {show(winner_of_game(colors))}")
    wins = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 40 + 1
        stay = next_random() % 6 + 1
        bit = 1 if winner_of_game(random_colors(n, stay)) else 0
        wins += bit
        check = (check * 3 + bit + 1) % 1000000007
    print(f"2000 rows of up to 40 pieces: Alice wins {wins}, checksum {check}")
    wins = 0
    check = 0
    for r in range(4):
        stay = [2, 3, 50, 1000][r]
        bit = 1 if winner_of_game(random_colors(100000, stay)) else 0
        wins += bit
        check = (check * 3 + bit + 1) % 1000000007
    print(f"4 rows of 100000 pieces: Alice wins {wins}, checksum {check}")


main()
