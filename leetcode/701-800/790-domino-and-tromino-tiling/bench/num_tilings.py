# LeetCode 790 — Domino and Tromino Tiling: the bench, in Python.
# Mirrors num_tilings.kara: two growing tables of counts, full and
# ragged ends, for 300,000 random n.

MOD = 1000000007


def num_tilings(n):
    full = [1, 1]
    ragged = [0, 1]
    for i in range(2, n + 1):
        full.append((full[i - 1] + full[i - 2] + 2 * ragged[i - 2]) % MOD)
        ragged.append((ragged[i - 1] + full[i - 1]) % MOD)
    return full[n]


seed = 790


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 300000
    total = 0
    check = 0
    for _ in range(rounds):
        n = 1 + next_random() % 1000
        ways = num_tilings(n)
        total = (total + ways) % MOD
        check = (check * 31 + ways) % MOD
    print(f"{rounds} rounds of n up to 1000: answers sum to {total}, checksum {check}")


main()
