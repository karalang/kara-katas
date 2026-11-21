# LeetCode #2481: Minimum Cuts to Divide a Circle -- Python mirror of
# cuts.kara: by parity.


def number_of_cuts(n):
    if n == 1:
        return 0
    elif n % 2 == 0:
        return n // 2
    else:
        return n


seed = 2481


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for n in [4, 3, 1, 2, 99, 100]:
        print(f"{n} -> {number_of_cuts(n)}")
    every = [number_of_cuts(n) for n in range(1, 101)]
    print(f"1 to 100 -> [{', '.join(str(v) for v in every)}]")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 100
        check = (check * 31 + number_of_cuts(n)) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
