# LeetCode #2844: Minimum Operations to Make a Special Number -- the
# Python mirror of the ★ arm: one pass from the right, ending the
# number at the first 0 or 5 after a 0, or 2 or 7 after a 5.


def minimum_operations(num):
    n = len(num)
    zero = False
    five = False
    for i in range(n - 1, -1, -1):
        d = num[i]
        if (zero and d in "05") or (five and d in "27"):
            return n - i - 2
        if d == "0":
            zero = True
        if d == "5":
            five = True
    return n - 1 if zero else n


# ---- the harness: the same in every arm --------------------------------

seed = 2844


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def number(n, kinds):
    order = "0527134689"
    digits = []
    for i in range(n):
        d = order[next_random() % kinds]
        while i == 0 and n > 1 and d == "0":
            d = order[next_random() % kinds]
        digits.append(d)
    return "".join(digits)


def main():
    m = minimum_operations
    print(f"{m('2245047')} {m('2908305')} {m('10')}")
    print(f"{m('0')} {m('5')} {m('25')} {m('75')} {m('57')}")
    print(f"{m('1' * 100)} {m('9' * 98 + '25')}")
    check = 0
    total = 0
    for c in range(3300):
        short = c < 3000
        n = next_random() % 8 + 1 if short else next_random() % 100 + 1
        kinds = 4 + next_random() % 3 if short else 10
        ops = m(number(n, kinds))
        total += ops
        check = (check * 31 + ops) % 1000000007
        if c == 2999:
            print(f"3000 short numbers: {total} operations, checksum {check}")
            total = 0
            check = 0
    print(f"300 long numbers: {total} operations, checksum {check}")


main()
