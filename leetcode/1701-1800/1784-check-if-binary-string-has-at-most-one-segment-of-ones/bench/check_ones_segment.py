# LeetCode #1784: Check if Binary String Has at Most One Segment of Ones --
# the bench in Python, mirroring check_ones_segment.kara: a search for
# "01".


def check_ones_segment(s):
    return "01" not in s


seed = 1784


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    strings = []
    for k in range(4000):
        ones = 1 + next_random() % 100
        s = "1" * ones + "0" * (100 - ones)
        if k % 2 == 1 and ones < 100:
            at = ones + next_random() % (100 - ones)
            s = s[:at] + "1" + s[at + 1:]
        strings.append(s)
    check = 0
    for call in range(4000000):
        s = strings[(check + call) % 4000]
        check = (check * 31 + (2 if check_ones_segment(s) else 1)) % 1000000007
    print(f"4000000 calls over 4000 strings: checksum {check}")


main()
