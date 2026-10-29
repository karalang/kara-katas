# LeetCode #1009 bench: the ★ arm (an all-ones mask) over 1,000,000 n
# below 10^9, of random lengths, drawn once; each of 50 rounds takes the
# complement of every n plus the round number and folds the round's sum
# into a checksum.


def bitwise_complement(n):
    mask = 1
    while mask < n:
        mask = mask * 2 + 1
    return mask ^ n


seed = 1009


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 1000000, 50
    values = []
    for _ in range(count):
        bits = 1 + next_random() % 30
        values.append(((next_random() * 32768 + next_random()) % (1 << bits)) % 999999000)
    check = 0
    for r in range(rounds):
        total = 0
        for k in range(count):
            total += bitwise_complement(values[k] + r)
        check = (check * 31 + total) % 1000000007
    print(f"{rounds} rounds over {count} values of n: checksum {check}")


main()
