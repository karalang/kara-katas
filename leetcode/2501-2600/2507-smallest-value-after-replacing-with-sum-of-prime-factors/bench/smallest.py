# LeetCode #2507: Smallest Value After Replacing With Sum of Prime
# Factors -- benchmark mirror of the ★ arm (smallest.kara): every n from
# 2 to 10^5 asked in an order the checksum so far picks.


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


def main():
    passes = 14
    check = 0
    for p in range(passes):
        start = check % 99999
        for k in range(99999):
            n = (start + k) % 99999 + 2
            check = (check * 31 + smallest_value(n) + p) % 1000000007
    print(f"{passes} passes over 2 to 10^5: checksum {check}")


main()
