# LeetCode #2222: Number of Ways to Select Buildings -- bench mirror of
# buildings.kara: one pass keeping the 0s and 1s behind and the pairs
# "01" and "10", each character closing the pairs it completes.


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


def main():
    # 10^5 buildings, each a 1 with chance one half
    streets = [['1' if next_random() % 2 == 1 else '0' for _ in range(100000)] for _ in range(30)]
    check = 0
    for street in streets:
        for r in range(10):
            # punch: one building is drawn again before each answer
            street[r * 9999] = '1' if next_random() % 2 == 1 else '0'
            s = "".join(street)
            check = (check * 31 + number_of_ways(s)) % 1000000007
    print(f"30 streets of 10^5, 10 punches: checksum {check}")


main()
