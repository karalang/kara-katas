# LeetCode #2125: Number of Laser Beams in a Bank -- the benchmark, the
# same algorithm as beams.kara.


def number_of_beams(bank):
    prev = 0
    beams = 0
    for row in bank:
        devices = row.count(b"1")
        if devices > 0:
            beams += prev * devices
            prev = devices
    return beams


def main():
    seed = 2125

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    banks = []
    for b in range(12):
        bank = []
        for _ in range(500):
            bank.append(bytes(49 if next_random() % 4 < b % 3 + 1 else 48 for _ in range(500)))
        banks.append(bank)
    total = 0
    check = 0
    for rnd in range(500):
        for b in range(12):
            r = next_random() % 500
            c = next_random() % 500
            cells = bytearray(banks[b][r])
            cells[c] = 48 if cells[c] == 49 else 49
            banks[b][r] = bytes(cells)
            beams = number_of_beams(banks[b])
            total += beams
            check = (check * 31 + beams + rnd) % 1000000007
    print(f"6000 solves: {total} beams, checksum {check}")


main()
