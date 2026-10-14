# Benchmark for #564: Python mirror of the ★ arm (five candidates); see
# nearest_palindromic.kara.


def mirrored(half, length):
    text = str(half)
    return int(text + text[: min(length // 2, len(text))][::-1])


def nearest_palindromic(n):
    value = int(n)
    length = len(n)
    half = int(n[: (length + 1) // 2])
    candidates = [10 ** (length - 1) - 1, 10**length + 1]
    for h in [half - 1, half, half + 1]:
        candidates.append(mirrored(h, length))
    best = -1
    for c in candidates:
        if c == value or c < 0:
            continue
        d = abs(c - value)
        bd = abs(best - value)
        if best == -1 or d < bd or (d == bd and c < best):
            best = c
    return str(best)


# ---- benchmark ---------------------------------------------------------------

seed = 564


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_number(t):
    length = 1 + step() % 18
    digits = [1 + step() % 9]
    for _ in range(1, length):
        digits.append(step() % 10)
    if t % 3 == 1:
        for i in range(length // 2):
            digits[length - 1 - i] = digits[i]
    value = 0
    for d in digits:
        value = value * 10 + d
    if t % 3 == 2:
        value = 10 ** (length - 1) + step() % 7 - 3
        if value < 1:
            value = 1
    return str(value)


def main():
    count = 10000
    rounds = 300
    numbers = [random_number(t) for t in range(count)]
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            got = int(nearest_palindromic(numbers[(rnd * 7 + g) % count]))
            checksum = (checksum * 31 + got % 1000000007) % 1000000007
    print(f"{count} numbers, {rounds} rounds: checksum {checksum}")


main()
