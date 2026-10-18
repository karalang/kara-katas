# LeetCode 754 — Reach a Number, bench: the ★ arm (step by step),
# mirrored from reach_number.kara.


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


def main():
    rounds = 30000
    total = 0
    check = 0
    for _ in range(rounds):
        a = next_random()
        b = next_random()
        target = (a * 32768 + b) % 1000000000 + 1
        if next_random() % 2 == 0:
            target = -target
        moves = reach_number(target)
        total += moves
        check = (check * 31 + moves) % 1000000007
    print(f"{rounds} targets: {total} moves in all, checksum {check}")


main()
