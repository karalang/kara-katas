"""LeetCode #1155: Number of Dice Rolls With Target Sum -- the Python
mirror of num_rolls_to_target.kara.

Dice added one at a time: `ways[s]` counts the rolls of the dice so far
that sum to `s`, and a new die moves each count up by each of its faces."""

MOD = 1_000_000_007


def num_rolls_to_target(n, k, target):
    ways = [0] * (target + 1)
    ways[0] = 1
    for _ in range(n):
        nxt = [0] * (target + 1)
        for s in range(target + 1):
            if ways[s] != 0:
                for face in range(1, k + 1):
                    if s + face > target:
                        break
                    nxt[s + face] = (nxt[s + face] + ways[s]) % MOD
        ways = nxt
    return ways[target]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(n, k, target):
    print(f"n = {n}, k = {k}, target = {target}  ->  {num_rolls_to_target(n, k, target)}")


def main():
    global seed
    for n, k, t in [(1, 6, 3), (2, 6, 7), (30, 30, 500), (1, 1, 1), (1, 1, 2), (2, 5, 1),
                    (3, 4, 12), (3, 4, 13), (30, 1, 30), (30, 30, 30), (30, 30, 900),
                    (30, 30, 1000), (30, 30, 465), (10, 30, 1000)]:
        show(n, k, t)
    seed = 1155
    nonzero = 0
    check = 0
    for i in range(1000):
        n = 1 + next_random() % 30
        k = 1 + next_random() % 30
        target = 1 + next_random() % 1000 if i < 500 else n + next_random() % (n * k - n + 1)
        ways = num_rolls_to_target(n, k, target)
        if ways != 0:
            nonzero += 1
        check = (check * 31 + ways) % 1000000007
    print(f"1000 random problems: {nonzero} with a roll, checksum {check}")


if __name__ == "__main__":
    main()
