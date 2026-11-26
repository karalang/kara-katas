# LeetCode #1796: Second Largest Digit in a String -- the ★ arm in Python:
# one pass keeping the largest digit and the largest below it.


def second_highest(s):
    first = second = -1
    for c in s:
        if c.isdigit():
            d = int(c)
            if d > first:
                second = first
                first = d
            elif first > d > second:
                second = d
    return second


seed = 1796


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, digits):
    s = []
    for _ in range(n):
        if next_random() % 10 < digits:
            s.append(str(next_random() % 10))
        else:
            s.append("abcdef"[next_random() % 6])
    return "".join(s)


def main():
    print(f"{second_highest('dfa12321afd')} {second_highest('abc1111')}")
    print(" ".join(str(second_highest(s)) for s in ["a", "abc", "7777", "09", "0123456789", "9a8b7c"]))
    nines = "9" * 500
    eights = "9" + "8" * 499
    wide = random_text(500, 5)
    print(f"the most: {second_highest(nines)} {second_highest(eights)} {second_highest(wide)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        digits = next_random() % 10
        s = random_text(n, digits)
        check = (check * 31 + second_highest(s) + 1) % 1000000007
    print(f"3000 random strings: checksum {check}")


main()
