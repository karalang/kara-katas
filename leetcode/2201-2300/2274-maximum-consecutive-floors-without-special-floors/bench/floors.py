# LeetCode #2274: Maximum Consecutive Floors Without Special Floors --
# the bench, the ★ arm.


def max_consecutive(bottom, top, special):
    floors = sorted(special)
    best = max(floors[0] - bottom, top - floors[-1])
    for i in range(1, len(floors)):
        best = max(best, floors[i] - floors[i - 1] - 1)
    return best


# ---- bench harness ---------------------------------------------------------

seed = 2274


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(50):
        special = []
        f = 1 + next_random() % 20000
        while f <= 1000000000 and len(special) < 100000:
            special.append(f)
            f += 1 + next_random() % 20000
        for j in range(len(special) - 1, 0, -1):
            r = next_random() % (j + 1)
            special[j], special[r] = special[r], special[j]
        check = (check * 31 + max_consecutive(1, 1000000000, special)) % 1000000007
    print(f"50 buildings of 10^5: checksum {check}")


main()
