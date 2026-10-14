# LeetCode #564: Find the Closest Palindrome -- Python mirror of the ★
# arm (five candidates); see nearest_palindromic.kara.


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


# ---- test harness ---------------------------------------------------------

seed = 564


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(n):
    print(f"{n} -> {nearest_palindromic(n)}")


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
    for n in ["123", "1", "9", "10", "11", "99", "100", "101", "1000", "1001",
              "1991", "12932", "99800", "100000000000000000",
              "807045053224792883", "999999999999999998", "999999999999999999"]:
        show(n)
    checksum = 0
    for v in range(1, 3001):
        checksum = (checksum * 31 + int(nearest_palindromic(str(v)))) % 1000000007
    print(f"1 to 3000: checksum {checksum}")
    checksum = 0
    longer = 0
    for t in range(300):
        n = random_number(t)
        got = nearest_palindromic(n)
        if len(got) != len(n):
            longer += 1
        checksum = (checksum * 31 + int(got)) % 1000000007
    print(f"300 random numbers: {longer} answers of another length, checksum {checksum}")


main()
