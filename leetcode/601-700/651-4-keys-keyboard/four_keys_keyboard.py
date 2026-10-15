# LeetCode #651: 4 Keys Keyboard -- the best for every count of presses.
# Mirrors the ★ arm (four_keys_keyboard.kara) and its test harness.


def max_a(n):
    best = [0] * (n + 1)
    for i in range(1, n + 1):
        best[i] = best[i - 1] + 1
        for j in range(1, i - 2):
            best[i] = max(best[i], best[j] * (i - j - 1))
    return best[n]


def show(n):
    print(f"{n} -> {max_a(n)}")


def main():
    for n in [3, 7, 1, 6, 8, 9, 10, 11, 15, 20, 31, 42, 50]:
        show(n)
    total = 0
    checksum = 0
    for n in range(1, 51):
        a = max_a(n)
        total += a
        checksum = (checksum * 31 + a) % 1000000007
    print(f"1 to 50: total {total}, checksum {checksum}")


main()
