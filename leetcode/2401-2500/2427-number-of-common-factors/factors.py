# LeetCode #2427: Number of Common Factors -- the Python mirror of the ★
# arm: the divisors of gcd(a, b), counted in pairs up to its square root.

seed = 2427


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def common_factors(a, b):
    g = gcd(a, b)
    count = 0
    d = 1
    while d * d <= g:
        if g % d == 0:
            count += 1 if d * d == g else 2
        d += 1
    return count


def main():
    for a, b in [(12, 6), (25, 30), (1, 1), (1000, 1000), (997, 991), (7, 994), (720, 840)]:
        print(f"{a} {b}: {common_factors(a, b)}")
    check = 0
    total = 0
    for a in range(1, 201):
        for b in range(1, 201):
            answer = common_factors(a, b)
            check = (check * 31 + answer) % 1000000007
            total += answer
    print(f"pairs to 200: checksum {check}, total {total}")
    check = 0
    total = 0
    for _ in range(3000):
        a = 1 + next_random() % 1000
        if next_random() % 2 == 0:
            b = 1 + next_random() % 1000
        else:
            f = 1 + next_random() % a
            b = f * (1 + next_random() % (1000 // f))
        answer = common_factors(a, b)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
