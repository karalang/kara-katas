# Benchmark for #848: Shifting Letters -- Python twin of the Kāra ★ arm
# (suffix sums, from the back).


def shifting_letters(s, shifts):
    b = bytearray(s.encode())
    shift = 0
    for i in range(len(b) - 1, -1, -1):
        shift = (shift + shifts[i]) % 26
        b[i] = 97 + (b[i] - 97 + shift) % 26
    return b.decode()


seed = 848


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 64
    rounds = 2000
    n = 100000
    texts = []
    all_shifts = []
    for _ in range(count):
        s = []
        shifts = []
        for _ in range(n):
            s.append(chr(97 + next_random() % 26))
            shifts.append(next_random() * 4657 % 1000000001)
        texts.append(''.join(s))
        all_shifts.append(shifts)
    checksum = 0
    for round_ in range(rounds):
        out = shifting_letters(texts[round_ % count], all_shifts[round_ % count])
        checksum = (checksum * 31 + ord(out[0]) + ord(out[n // 2]) * 7 + ord(out[n - 1]) * 13) % 1000000007
    print(f"{rounds} rounds of {count} strings: checksum {checksum}")


main()
