# LeetCode #2847: Smallest Number With Given Digit Product -- the Python
# mirror of the ★ arm: the largest digit that divides what is left, 9
# down to 2, and the digits smallest first.


def smallest_number(n):
    if n == 1:
        return "1"
    rest = n
    digits = []
    for d in range(9, 1, -1):
        while rest % d == 0:
            digits.append(str(d))
            rest //= d
    if rest != 1:
        return "-1"
    return "".join(reversed(digits))


# ---- the harness: the same in every arm --------------------------------

seed = 2847


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    s = smallest_number
    print(f"{s(105)} {s(7)} {s(44)} {s(1)}")
    print(f"{s(10**18)}")
    print(f"{s(1 << 59)} {s(450283905890997363)} {s(1000000007)}")
    check = 0
    none = 0
    for c in range(3300):
        n = 1
        factors = next_random() % (13 if c < 3000 else 41)
        for _ in range(factors):
            p = [2, 3, 5, 7][next_random() % 4]
            if n <= 10**18 // p:
                n *= p
        if c < 3000 and next_random() % 5 == 0:
            n *= [11, 13][next_random() % 2]
        out = s(n)
        if out == "-1":
            none += 1
        for b in out.encode():
            check = (check * 31 + b) % 1000000007
        if c == 2999:
            print(f"3000 short products: {none} with none, checksum {check}")
            none = 0
            check = 0
    print(f"300 long products: {none} with none, checksum {check}")


main()
