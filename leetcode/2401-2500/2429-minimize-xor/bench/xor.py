# LeetCode #2429: Minimize XOR -- the bench, the ★ arm: num1's set bits
# taken from the top while bits are left to place, the rest laid in its
# clear bits from the bottom.

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
    firsts = []
    seconds = []
    for _ in range(100000):
        r = next_random()
        firsts.append(1 + (r * 32768 + next_random()) % 1000000000)
        r = next_random()
        seconds.append(1 + (r * 32768 + next_random()) % 1000000000)
    check = 0
    for p in range(10):
        for i in range(len(firsts)):
            check = (check * 31 + minimize_xor(firsts[i], seconds[i] ^ (p + 1)) + p) % 1000000007
    print(f"10 passes over 10^5 pairs: checksum {check}")


main()
