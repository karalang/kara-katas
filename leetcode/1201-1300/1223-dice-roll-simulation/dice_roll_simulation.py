# LeetCode #1223: Dice Roll Simulation -- the Python mirror of the ★ arm:
# count the sequences by their last face and how many times in a row it
# has come up; a roll of the same face lengthens the run while it stays
# within that face's limit, and any other face starts a run of one.

seed = 1223


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def die_simulator(n, roll_max):
    modulus = 1_000_000_007
    count = [[0] * 15 for _ in range(6)]
    for f in range(6):
        count[f][0] = 1
    for _ in range(1, n):
        nxt = [[0] * 15 for _ in range(6)]
        for f in range(6):
            for r in range(roll_max[f]):
                c = count[f][r]
                if c == 0:
                    continue
                for g in range(6):
                    if g != f:
                        nxt[g][0] = (nxt[g][0] + c) % modulus
                    elif r + 1 < roll_max[f]:
                        nxt[f][r + 1] = (nxt[f][r + 1] + c) % modulus
        count = nxt
    total = 0
    for f in range(6):
        for r in range(15):
            total = (total + count[f][r]) % modulus
    return total


def main():
    print(die_simulator(2, [1, 1, 2, 2, 2, 3]))
    print(die_simulator(2, [1, 1, 1, 1, 1, 1]))
    print(die_simulator(3, [1, 1, 1, 2, 2, 3]))
    print(die_simulator(1, [1, 1, 1, 1, 1, 1]))
    check = 0
    for _ in range(300):
        n = next_random() % 60 + 1
        roll_max = [next_random() % 15 + 1 for _ in range(6)]
        check = (check * 131 + die_simulator(n, roll_max)) % 1000000007
    print(f"300 random cases with n up to 60: checksum {check}")
    wide = [next_random() % 15 + 1 for _ in range(6)]
    print(f"n = 5000: no face twice {die_simulator(5000, [1] * 6)}, up to 15 {die_simulator(5000, [15] * 6)}, {wide}: {die_simulator(5000, wide)}")


main()
