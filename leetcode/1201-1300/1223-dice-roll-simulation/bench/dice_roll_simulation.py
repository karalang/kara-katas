# LeetCode #1223 bench, Python mirror of the Kāra ★ arm: count the sequences
# by their last face and run length, for 50 random sets of limits at
# n = 5000; checksum of the answers.

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
    check = 0
    for _ in range(50):
        roll_max = [next_random() % 15 + 1 for _ in range(6)]
        check = (check * 131 + die_simulator(5000, roll_max)) % 1000000007
    print(f"50 sets of limits at n = 5000: checksum {check}")


main()
