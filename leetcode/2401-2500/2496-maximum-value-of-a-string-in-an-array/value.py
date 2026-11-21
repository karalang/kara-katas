# LeetCode #2496: Maximum Value of a String in an Array -- Python mirror of
# the ★ arm (value.kara): one pass over each string's characters builds
# its number and notes whether any is not a digit.


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


# ---- test harness -----------------------------------------------------------

seed = 2496


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_string(digit_in):
    length = next_random() % 9 + 1
    s = []
    for _ in range(length):
        k = next_random()
        if k % 8 < digit_in:
            s.append(chr(ord("0") + k // 8 % 10))
        else:
            s.append(chr(ord("a") + k // 8 % 26))
    return "".join(s)


def main():
    cases = [
        ["alic3", "bob", "3", "4", "00000"],
        ["1", "01", "001", "0001"],
        ["a"],
        ["0"],
        ["0000", "a"],
        ["999999999", "abcdefghi"],
        ["12a", "7", "ab"],
        ["000000012", "11", "abcdefghi"],
        ["x1", "1x", "10"],
    ]
    for strs in cases:
        print(f"{len(strs)} strings, first {strs[0]} -> {maximum_value(strs)}")
    for digit_in in range(9):
        check = 0
        for _ in range(2000):
            count = next_random() % 100 + 1
            strs = [random_string(digit_in) for _ in range(count)]
            check = (check * 31 + maximum_value(strs)) % 1000000007
        print(f"2000 random, digits {digit_in} in 8: checksum {check}")
    nines = ["999999999"] * 100
    letters = ["abcdefghi" if i % 2 == 0 else "12345678z" for i in range(100)]
    last = ["a99999999"] * 99 + ["100000000"]
    for name, strs in [("nines", nines), ("letters", letters), ("last", last)]:
        print(f"100 {name} -> {maximum_value(strs)}")


if __name__ == "__main__":
    main()
