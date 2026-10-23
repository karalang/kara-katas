# LeetCode #878: Nth Magical Number -- Python mirror of the ★ arm (binary
# search on the answer) and its test harness; prints the same output as
# nth_magical_number.kara.


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


# ---- test harness ----------------------------------------------------------

seed = 878


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def up_to(limit):
    x = next_random()
    y = next_random()
    return (x * 32768 + y) % limit + 1


def show(n, a, b):
    print(f"n = {n}, a = {a}, b = {b} -> {nth_magical_number(n, a, b)}")


def main():
    show(1, 2, 3)
    show(4, 2, 3)
    show(5, 2, 4)
    show(3, 6, 4)
    show(1, 40000, 40000)
    show(1000000000, 40000, 40000)
    show(1000000000, 2, 3)
    show(1000000000, 39999, 40000)
    show(999999999, 2, 2)
    show(123456789, 210, 330)
    total = 0
    for _ in range(3000):
        n = next_random() % 100 + 1
        a = next_random() % 19 + 2
        b = next_random() % 19 + 2
        total += nth_magical_number(n, a, b)
    print(f"3000 cases with n up to 100 and a, b up to 20: answers sum to {total}")
    total = 0
    check = 0
    for k in range(200):
        n = up_to(1000000000)
        a = up_to(39999 if k % 2 == 0 else 199) + 1
        b = a * (next_random() % 3 + 1) if k % 5 == 0 else up_to(39999) + 1
        answer = nth_magical_number(n, a, min(b, 40000))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"200 cases with n up to 10^9 and a, b up to 4 * 10^4: answers sum to {total}, checksum {check}")


main()
