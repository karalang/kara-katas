# LeetCode #878 bench: Python mirror of nth_magical_number.kara (the ★
# arm, binary search on the answer) on the same 1,000,000 cases.


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def nth_magical_number(n, a, b):
    lcm = a // gcd(a, b) * b
    lo = 1
    hi = n * min(a, b)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if mid // a + mid // b - mid // lcm >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo % 1000000007


seed = 878


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def up_to(limit):
    x = next_random()
    y = next_random()
    return (x * 32768 + y) % limit + 1


def main():
    total = 0
    check = 0
    for _ in range(1000000):
        n = up_to(1000000000)
        a = up_to(39999) + 1
        b = up_to(39999) + 1
        answer = nth_magical_number(n, a, b)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"1000000 cases: answers sum to {total}, checksum {check}")


main()
