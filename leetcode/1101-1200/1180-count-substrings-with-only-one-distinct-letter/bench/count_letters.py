# LeetCode #1180: Count Substrings with Only One Distinct Letter -- the ★
# arm's bench in Python: one pass, the run of equal letters ending at each
# position added at every step. The same strings and the same 100 rounds.


def count_letters(s):
    total = 0
    run = 0
    last = 0
    for c in s:
        if c == last:
            run += 1
        else:
            run = 1
            last = c
        total += run
    return total


seed = 1180


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    strings = []
    for _ in range(1000):
        m = 1 + next_random() % 4
        strings.append(bytes(97 + next_random() % m for _ in range(1000)))
    rounds = 100
    check = 0
    for _ in range(rounds):
        for s in strings:
            check = (check * 131 + count_letters(s)) % 1000000007
    print(f"{rounds} rounds of 1000 strings: checksum {check}")


main()
