# LeetCode #2429: Minimize XOR -- the Python mirror of the ★ arm: num1's
# set bits taken from the top while bits are left to place, the rest laid
# in its clear bits from the bottom.

seed = 2429


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def minimize_xor(num1, num2):
    left = bin(num2).count("1")
    x = 0
    for bit in range(30, -1, -1):
        if left > 0 and (num1 >> bit) & 1 == 1:
            x |= 1 << bit
            left -= 1
    for bit in range(31):
        if left > 0 and (x >> bit) & 1 == 0:
            x |= 1 << bit
            left -= 1
    return x


def main():
    for a, b in [(3, 5), (1, 12), (1, 1), (1000000000, 1000000000), (1, 536870911),
                 (536870912, 536870911), (1000000000, 1), (536870911, 1)]:
        print(f"{a} {b}: {minimize_xor(a, b)}")
    for top in [1000000000, 63]:
        check = 0
        for _ in range(3000):
            r = next_random()
            a = 1 + (r * 32768 + next_random()) % top
            r = next_random()
            b = 1 + (r * 32768 + next_random()) % top
            check = (check * 31 + minimize_xor(a, b)) % 1000000007
        print(f"3000 random up to {top}: checksum {check}")


if __name__ == "__main__":
    main()
