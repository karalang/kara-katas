# LeetCode #2125: Number of Laser Beams in a Bank -- the mirror of
# beams.kara: each row with devices adds its count times the count of the
# last such row above it.


def number_of_beams(bank):
    prev = 0
    beams = 0
    for row in bank:
        devices = sum(1 for c in row if c == "1")
        if devices > 0:
            beams += prev * devices
            prev = devices
    return beams


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_bank(seed, m, n, quarters):
    bank = []
    for _ in range(m):
        row = []
        for _ in range(n):
            row.append("1" if next_random(seed) % 4 < quarters else "0")
        bank.append("".join(row))
    return bank


def main():
    examples = [
        "011001 000000 010100 001000",
        "000 111 000",
        "10101",
        "11 11",
        "1 0 0 1 0 1",
        "000 000",
    ]
    for text in examples:
        print(f"{text} -> {number_of_beams(text.split(' '))}")
    seed = [2125]
    total = 0
    check = 0
    for rnd in range(2000):
        m = next_random(seed) % 10 + 1
        n = next_random(seed) % 10 + 1
        beams = number_of_beams(random_bank(seed, m, n, rnd % 3 + 1))
        total += beams
        check = (check * 31 + beams) % 1000000007
    print(f"2000 banks: {total} beams, checksum {check}")
    full = random_bank(seed, 500, 500, 4)
    half = random_bank(seed, 500, 500, 2)
    print(f"500 by 500: {number_of_beams(full)} beams all devices, {number_of_beams(half)} half")


main()
