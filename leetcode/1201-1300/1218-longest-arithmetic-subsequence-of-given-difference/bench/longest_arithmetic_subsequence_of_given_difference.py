# LeetCode #1218 bench, in Python: the ★ arm (a dict from each value to
# the longest subsequence ending with it) on 16 arrays of 10^5 values from
# -10^4 to 10^4 drawn once, each asked with the differences -3 to 3;
# every answer folded into a checksum.

seed = 1218


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def longest_subsequence(arr, difference):
    ending = {}
    best = 0
    for x in arr:
        length = ending.get(x - difference, 0) + 1
        ending[x] = length
        if length > best:
            best = length
    return best


def main():
    arrays = [[next_random() % 20001 - 10000 for _ in range(100000)] for _ in range(16)]
    check = 0
    for arr in arrays:
        for d in range(-3, 4):
            check = (check * 131 + longest_subsequence(arr, d) + d + 3) % 1000000007
    print(f"16 arrays of 10^5 values, differences -3 to 3: checksum {check}")


main()
