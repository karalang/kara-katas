# LeetCode #2222: Number of Ways to Select Buildings -- mirror of
# buildings.kara: one pass keeping the 0s and 1s behind and the pairs
# "01" and "10", each character closing the pairs it completes. O(n).


def number_of_ways(s):
    zeros = ones = zero_ones = one_zeros = ways = 0
    for c in s:
        if c == '0':
            ways += zero_ones
            one_zeros += ones
            zeros += 1
        else:
            ways += one_zeros
            zero_ones += zeros
            ones += 1
    return ways


seed = 2222


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n characters, each '1' with chance ones in 10
def draw_street(n, ones):
    return "".join('1' if next_random() % 10 < ones else '0' for _ in range(n))


def show(s):
    print(f"\"{s}\" -> {number_of_ways(s)}")


def main():
    # LeetCode's two examples, then four more: too short, one pattern,
    # the other, and all alike
    show("001101")
    show("11100")
    show("01")
    show("010")
    show("101")
    show("0000")
    # 3000 random streets of 1 to 40 buildings, ones with chance 1, 5
    # and 9 in 10 in turn
    check = 0
    for c in range(3000):
        n = next_random() % 40 + 1
        s = draw_street(n, [1, 5, 9][c % 3])
        check = (check * 31 + number_of_ways(s)) % 1000000007
    print(f"3000 streets: checksum {check}")
    # the constraints' largest: 10^5 random, and 10^5 alternating, whose
    # count passes i32
    wide = draw_street(100000, 5)
    alternating = "".join('0' if i % 2 == 0 else '1' for i in range(100000))
    print(f"10^5 random: {number_of_ways(wide)}; 10^5 alternating: {number_of_ways(alternating)}")


main()
