# LeetCode #2511: Maximum Enemy Forts That Can Be Captured -- Python
# mirror of the ★ arm (forts.kara): one pass that keeps the place of the
# last fort that is not 0, and its harness, line for line.


def capture_forts(forts):
    best = 0
    last = -1
    for i in range(len(forts)):
        if forts[i] != 0:
            if last >= 0 and forts[last] == -forts[i]:
                best = max(best, i - last - 1)
            last = i
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_forts(n, zeros):
    out = []
    for _ in range(n):
        r = next_random() % (zeros + 2)
        out.append(0 if r < zeros else (1 if r == zeros else -1))
    return out


def fmt(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    global seed
    cases = [
        [1, 0, 0, -1, 0, 0, 0, 0, 1],
        [0, 0, 1, -1],
        [1],
        [-1, 0, 0, 0],
        [1, 0, 0, 1, 0, -1],
        [-1, 0, 0, 0, 1, 0, 0, 0, 0, -1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [0, -1, 0, 1, 0, 0, -1, 0, 0, 0, 1, 1, -1],
    ]
    for forts in cases:
        print(f"{fmt(forts)} -> {capture_forts(forts)}")
    seed = 2511
    for zeros in [1, 18]:
        check = 0
        none = 0
        for _ in range(2000):
            n = next_random() % 30 + 1
            a = capture_forts(random_forts(n, zeros))
            if a == 0:
                none += 1
            check = (check * 31 + a) % 1000000007
        print(f"2000 random, zeros {zeros} in {zeros + 2}: {none} capture nothing, checksum {check}")
    wide = [0] * 1000
    wide[0] = 1
    wide[999] = -1
    print(f"1000 forts, 998 between: {capture_forts(wide)}")
    wide[999] = 1
    print(f"1000 forts, both ends ours: {capture_forts(wide)}")
    turns = [-1 if i % 2 == 0 else 1 for i in range(1000)]
    print(f"1000 forts, -1 and 1 in turn: {capture_forts(turns)}")
    print(f"1000 random forts: {capture_forts(random_forts(1000, 38))}")


main()
