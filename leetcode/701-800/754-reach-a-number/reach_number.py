# LeetCode 754 — Reach a Number, mirror of the ★ arm (step by step) and
# its harness.


def reach_number(target):
    t = abs(target)
    k = 0
    s = 0
    while s < t or (s - t) % 2 != 0:
        k += 1
        s += k
    return k


seed = 754


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(target):
    print(f"target = {target} -> {reach_number(target)}")


def main():
    for t in [2, 3, 1, -1, 4, 5, -6, 1000000000, -1000000000, 999961560, 999961561]:
        show(t)
    total = 0
    check = 0
    for _ in range(1000):
        target = next_random() * 32768 + next_random()
        target = target % 1000000000 + 1
        if next_random() % 2 == 0:
            target = -target
        moves = reach_number(target)
        total += moves
        check = (check * 31 + moves) % 1000000007
    print(f"1000 random targets: {total} moves in all, checksum {check}")


main()
