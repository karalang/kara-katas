# LeetCode 789 — Escape The Ghosts, comparing distances to the target.
# Mirrors escape_ghosts.kara (the ★ arm) and its harness.


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


def show(ghosts, target):
    answer = "true" if escape_ghosts(ghosts, target) else "false"
    print(f"ghosts = {ghosts}, target = {target} -> {answer}")


def main():
    show([[1, 0], [0, 3]], [0, 1])
    show([[1, 0]], [2, 0])
    show([[2, 0]], [1, 0])
    show([[5, 0], [-10, 8]], [3, 7])
    show([[0, 0]], [0, 0])
    show([[1, 1]], [0, 0])
    show([[-1, 0], [0, 1], [-1, 0], [0, 1], [-1, 0]], [0, 0])
    show([[10000, 10000], [-10000, -10000]], [10000, -10000])
    show([[10000, 10000], [-10000, -10000]], [9999, -10000])
    escapes = 0
    check = 0
    for _ in range(300):
        count = 1 + next_random() % 10
        ghosts = []
        for _ in range(count):
            x = next_random() % 41 - 20
            y = next_random() % 41 - 20
            ghosts.append([x, y])
        tx = next_random() % 41 - 20
        ty = next_random() % 41 - 20
        answer = escape_ghosts(ghosts, [tx, ty])
        if answer:
            escapes += 1
        check = (check * 31 + (7 if answer else 3) + count) % 1000000007
    print(f"300 random boards: {escapes} escapes, checksum {check}")


main()
