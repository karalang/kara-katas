# LeetCode #2038: Remove Colored Pieces if Both Neighbors are the Same
# Color -- the ★ arm in Python, the same algorithm and workload as
# colors.kara: each row written out as a fresh string, its pieces listed,
# each player's moves counted, Alice winning with more.


def winner_of_game(colors):
    c = list(colors)
    alice = bob = 0
    for i in range(1, len(c) - 1):
        if c[i - 1] == c[i] == c[i + 1]:
            if c[i] == "A":
                alice += 1
            else:
                bob += 1
    return alice > bob


seed = 2038


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rows = []
    for r in range(4):
        stay = [2, 3, 50, 1000][r]
        c = "A" if next_random() % 2 == 0 else "B"
        row = []
        for _ in range(100000):
            if next_random() % stay == 0:
                c = "B" if c == "A" else "A"
            row.append(c)
        rows.append(row)
    calls = 0
    wins = 0
    check = 0
    for rnd in range(100):
        for r in range(4):
            at = (rnd * 7919 + r * 104729) % 100000
            rows[r][at] = "B" if rows[r][at] == "A" else "A"
            bit = 1 if winner_of_game("".join(rows[r])) else 0
            calls += 1
            wins += bit
            check = (check * 3 + bit + 1) % 1000000007
    print(f"{calls} calls: Alice wins {wins}, checksum {check}")


main()
