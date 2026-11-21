# LeetCode #2496: Maximum Value of a String in an Array -- benchmark
# mirror of the ★ arm (value.kara): 2000 lists of 100 strings, built
# once, then the passes; each puts the checksum so far, written in
# digits, in place of one string of every list, asks, and puts it back.


def maximum_value(strs):
    best = 0
    for s in strs:
        number = 0
        digits = True
        for c in s:
            if "0" <= c <= "9":
                number = number * 10 + (ord(c) - ord("0"))
            else:
                digits = False
        worth = number if digits else len(s)
        best = max(best, worth)
    return best


seed = 2496


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    passes = 90
    lists = []
    for _ in range(2000):
        strs = []
        for _ in range(100):
            length = next_random() % 9 + 1
            s = []
            for _ in range(length):
                k = next_random()
                if k % 2 == 0:
                    s.append(chr(ord("0") + k // 2 % 10))
                else:
                    s.append(chr(ord("a") + k // 2 % 26))
            strs.append("".join(s))
        lists.append(strs)
    check = 0
    for p in range(passes):
        for strs in lists:
            at = check % 100
            was = strs[at]
            strs[at] = f"{check % 1000000000}"
            check = (check * 31 + maximum_value(strs) + p) % 1000000007
            strs[at] = was
    print(f"{passes} passes over 2000 lists of 100: checksum {check}")


main()
