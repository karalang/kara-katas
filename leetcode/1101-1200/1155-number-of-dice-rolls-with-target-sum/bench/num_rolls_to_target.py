"""LeetCode #1155 bench -- mirrors num_rolls_to_target.kara: the same 64
problems, the same passes, the ★ arm's rolling counts."""


def num_rolls_to_target(n, k, target):
    modulus = 1_000_000_007
    ways = [0] * (target + 1)
    ways[0] = 1
    for _ in range(n):
        nxt = [0] * (target + 1)
        for s in range(target + 1):
            if ways[s] != 0:
                for face in range(1, k + 1):
                    if s + face > target:
                        break
                    nxt[s + face] = (nxt[s + face] + ways[s]) % modulus
        ways = nxt
    return ways[target]


seed = 1155


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    passes = 250
    problems = []
    for _ in range(64):
        n = 1 + next_random() % 30
        k = 1 + next_random() % 30
        most = n * k if n * k < 1000 else 1000
        problems.append((n, k, n + next_random() % (most - n + 1)))
    check = 0
    for p in range(passes):
        for n, k, target in problems:
            check = (check * 31 + num_rolls_to_target(n, k, target) + p) % 1000000007
    print(f"{passes} passes over 64 problems: checksum {check}")


if __name__ == "__main__":
    main()
