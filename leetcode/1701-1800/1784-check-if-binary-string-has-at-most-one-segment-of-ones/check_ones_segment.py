# LeetCode #1784: Check if Binary String Has at Most One Segment of Ones --
# the ★ arm in Python: "01" appears exactly when a second segment begins.


def check_ones_segment(s):
    return "01" not in s


seed = 1784


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_binary(n, zeros):
    s = "1"
    for _ in range(1, n):
        s += "0" if next_random() % 4 < zeros else "1"
    return s


def show(b):
    return "true" if b else "false"


def main():
    f = check_ones_segment
    print(f"{show(f('1001'))} {show(f('110'))}")
    print(f"{show(f('1'))} {show(f('10'))} {show(f('101'))} {show(f('111'))} {show(f('1000001'))}")
    ones = "1" * 100
    half = "1" * 50 + "0" * 50
    ends = "1" + "0" * 98 + "1"
    print(f"the most: {show(f(ones))} {show(f(half))} {show(f(ends))}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        zeros = next_random() % 4
        s = random_binary(n, zeros)
        check = (check * 31 + (2 if f(s) else 1)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
