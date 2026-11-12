# LeetCode #1133: Largest Unique Number -- the bench in Python, the same
# algorithm and workload as largest_unique_number.kara: each array its own
# list, a list of 1001 counts per call, the same 256 arrays of 2000 values
# and 1000 rounds.


def largest_unique_number(nums):
    count = [0] * 1001
    for x in nums:
        count[x] += 1
    for v in range(1000, -1, -1):
        if count[v] == 1:
            return v
    return -1


seed = 1133


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = [[next_random() % 1001 for _ in range(2000)] for _ in range(256)]
    total = 0
    check = 0
    for rnd in range(1000):
        for j in range(256):
            at = (rnd * 7919 + j * 104729) % 2000
            arrays[j][at] = (arrays[j][at] * 7 + 13) % 1001
            r = largest_unique_number(arrays[j])
            total += r
            check = (check * 31 + r + 1) % 1000000007
    print(f"1000 rounds over 256 arrays of 2000 values: answers total {total}, checksum {check}")


main()
