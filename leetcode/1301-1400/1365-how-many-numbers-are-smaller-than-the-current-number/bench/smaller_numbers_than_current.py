# LeetCode #1365 bench -- Python: the values counted and the counts summed,
# so below[v] holds how many values are less than v.


def smaller_numbers_than_current(nums):
    below = [0] * 102
    for x in nums:
        below[x + 1] += 1
    for v in range(1, 102):
        below[v] += below[v - 1]
    return [below[x] for x in nums]


seed = 1365


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 arrays of 500 values from 0 to 100, the constraints' most, built
    # once; then 2 * 10^5 rounds, each setting one value of one array, both
    # drawn from the checksum so far, and folding three of the answers
    # into the checksum
    arrays = [[next_random() % 101 for _ in range(500)] for _ in range(20)]
    check = 0
    for r in range(200000):
        k = check % 20
        arrays[k][(check // 20) % 500] = (check // 10000) % 101
        got = smaller_numbers_than_current(arrays[k])
        check = (check * 31 + got[0] + got[check % 500] * 7 + got[499] * 13 + r) % 1000000007
    print(f"200000 rounds over 20 arrays of 500 values: checksum {check}")


main()
