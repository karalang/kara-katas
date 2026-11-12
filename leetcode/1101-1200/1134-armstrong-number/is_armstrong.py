# LeetCode #1134: Armstrong Number -- the Python mirror of the ★ arm: the
# digits counted by dividing by 10, then each digit's k-th power summed by
# repeated multiplication, and the sum compared with n.


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


seed = 1134


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def b(x):
    return "true" if x else "false"


def main():
    for n in [153, 123, 1, 9, 10, 370, 371, 9474, 9475, 100000000, 88593477, 24678050]:
        print(f"{n} -> {b(is_armstrong(n))}")
    found = [n for n in range(1, 20001) if is_armstrong(n)]
    print(f"Armstrong numbers to 20000: [{', '.join(str(n) for n in found)}]")
    known = [1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474, 54748, 92727,
             93084, 548834, 1741725, 4210818, 9800817, 9926315, 24678050, 24678051, 88593477]
    yes = sum(1 for n in known if is_armstrong(n))
    near = sum(1 for n in known for m in (n - 1, n + 1) if m >= 1 and m not in known and is_armstrong(m))
    print(f"{yes} of the {len(known)} up to 10^8 accepted, {near} of their other neighbours")
    count = 0
    check = 0
    for _ in range(2000):
        n = (next_random() * 32768 + next_random()) % 100000000 + 1
        a = is_armstrong(n)
        if a:
            count += 1
        check = (check * 31 + n % 1000 + (1 if a else 0)) % 1000000007
    print(f"2000 random numbers to 10^8: {count} accepted, checksum {check}")


main()
