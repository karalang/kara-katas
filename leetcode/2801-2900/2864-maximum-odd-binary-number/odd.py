# LeetCode #2864: Maximum Odd Binary Number -- the Python mirror of the
# ★ arm (odd.kara): the ones less one, then the zeros, then the last one.


def maximum_odd_binary_number(s):
    ones = s.count("1")
    zeros = len(s) - ones
    return "1" * (ones - 1) + "0" * zeros + "1"


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(s, check):
    for b in s.encode():
        check = (check * 31 + b) % 1000000007
    return check


def main():
    global seed
    print(f"{maximum_odd_binary_number('010')} {maximum_odd_binary_number('0101')} {maximum_odd_binary_number('1')}")
    ones = "1" * 100
    front = "1" + "0" * 99
    t = "true" if maximum_odd_binary_number(ones) == ones else "false"
    u = "true" if maximum_odd_binary_number(front).endswith("01") else "false"
    print(f"{t} {u}")
    seed = 2864
    check = 0
    ones_total = 0
    for c in range(6000):
        n = next_random() % 8 + 1 if c < 3000 else next_random() % 100 + 1
        bits = ["1" if next_random() % 3 == 0 else "0" for _ in range(n)]
        bits[next_random() % n] = "1"
        best = maximum_odd_binary_number("".join(bits))
        ones_total += best.count("1")
        check = fold(best, check)
        if c == 2999:
            print(f"3000 short strings: {ones_total} ones, checksum {check}")
            ones_total = 0
            check = 0
    print(f"3000 long strings: {ones_total} ones, checksum {check}")


main()
