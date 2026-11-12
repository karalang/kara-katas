# LeetCode #1134: Armstrong Number -- the bench in Python, the same
# algorithm and workload as is_armstrong.kara: every number from 1 to
# 15000000 asked in turn.


def is_armstrong(n):
    k = 0
    m = n
    while m > 0:
        k += 1
        m //= 10
    total = 0
    m = n
    while m > 0:
        d = m % 10
        p = 1
        for _ in range(k):
            p *= d
        total += p
        m //= 10
    return total == n


def main():
    count = 0
    total = 0
    check = 0
    for n in range(1, 15000001):
        if is_armstrong(n):
            count += 1
            total += n
            check = (check * 31 + n) % 1000000007
    print(f"1 to 15000000: {count} Armstrong numbers, summing to {total}, checksum {check}")


main()
