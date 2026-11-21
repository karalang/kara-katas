# LeetCode #2507: Smallest Value After Replacing With Sum of Prime
# Factors -- mirror of the ★ arm (smallest.kara): the sum of n's prime
# factors by trial division, repeated until it no longer changes n.


def smallest_value(n):
    while True:
        rest = n
        total = 0
        p = 2
        while p * p <= rest:
            while rest % p == 0:
                rest //= p
                total += p
            p += 1
        if rest > 1:
            total += rest
        if total == n:
            return n
        n = total


seed = 2507


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for n in [15, 3, 2, 4, 6, 8, 12, 99991, 65536, 100000]:
        print(f"{n} -> {smallest_value(n)}")
    check = 0
    fixed = 0
    for n in range(2, 20001):
        a = smallest_value(n)
        if a == n:
            fixed += 1
        check = (check * 31 + a) % 1000000007
    print(f"2 to 20000: {fixed} already smallest, checksum {check}")
    check = 0
    fives = 0
    for _ in range(2000):
        n = (next_random() * 32768 + next_random()) % 99999 + 2
        a = smallest_value(n)
        if a == 5:
            fives += 1
        check = (check * 31 + a) % 1000000007
    print(f"2000 random to 10^5: {fives} end at 5, checksum {check}")


main()
