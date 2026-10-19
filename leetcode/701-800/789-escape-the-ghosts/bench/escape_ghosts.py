# LeetCode 789 — Escape The Ghosts: the bench, in Python.
# Mirrors escape_ghosts.kara: every ghost's distance to the target
# against yours, stopping at the first that is no farther.


def escape_ghosts(ghosts, target):
    mine = abs(target[0]) + abs(target[1])
    for g in ghosts:
        if abs(g[0] - target[0]) + abs(g[1] - target[1]) <= mine:
            return False
    return True


seed = 789


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    boards = []
    for _ in range(64):
        ghosts = []
        for _ in range(100):
            x = next_random() % 20001 - 10000
            y = next_random() % 20001 - 10000
            ghosts.append([x, y])
        boards.append(ghosts)
    rounds = 10000000
    escapes = 0
    check = 0
    for r in range(rounds):
        x = next_random() % 2001 - 1000
        y = next_random() % 2001 - 1000
        if escape_ghosts(boards[r % 64], [x, y]):
            escapes += 1
            check = (check * 31 + r % 1000) % 1000000007
    print(f"{rounds} rounds of 100-ghost boards: {escapes} escapes, checksum {check}")


main()
