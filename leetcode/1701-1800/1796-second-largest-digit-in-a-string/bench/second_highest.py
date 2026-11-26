# LeetCode #1796: Second Largest Digit in a String -- the bench in Python:
# the ★ arm over 1000 random strings of 100 characters built once, 1000000
# calls.


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


def main():
    texts = []
    for _ in range(1000):
        digits = 1 + next_random() % 9
        s = []
        for _ in range(100):
            if next_random() % 10 < digits:
                s.append(str(next_random() % 10))
            else:
                s.append("abcdef"[next_random() % 6])
        texts.append("".join(s))
    check = 0
    for call in range(1000000):
        s = texts[(check + call) % 1000]
        check = (check * 31 + second_highest(s) + 1) % 1000000007
    print(f"1000000 calls over 1000 strings: checksum {check}")


main()
