# LeetCode #650: 2 Keys Keyboard -- the sum of the prime factors.
# Mirrors the ★ arm (keys_keyboard.kara) and its test harness.


def min_steps(n):
    rest = n
    steps = 0
    p = 2
    while p * p <= rest:
        while rest % p == 0:
            steps += p
            rest //= p
        p += 1
    if rest > 1:
        steps += rest
    return steps


def show(n):
    print(f"{n} -> {min_steps(n)}")


def main():
    for n in [3, 1, 2, 16, 27, 6, 35, 49, 997, 961, 768, 999, 1000]:
        show(n)
    total = 0
    checksum = 0
    for n in range(1, 201):
        s = min_steps(n)
        total += s
        checksum = (checksum * 31 + s) % 1000000007
    print(f"1 to 200: total {total}, checksum {checksum}")


main()
