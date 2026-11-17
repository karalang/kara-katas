# LeetCode #2248: Intersection of Multiple Arrays -- the benchmark's
# Python mirror of common.kara: a count for every value from 1 to 1000,
# kept where it reaches the number of arrays.


def intersection(nums):
    count = [0] * 1001
    for row in nums:
        for v in row:
            count[v] += 1
    return [v for v in range(1, 1001) if count[v] == len(nums)]


seed = 2248


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    pool = list(range(1, 151))
    for _ in range(20000):
        nums = []
        for _ in range(10):
            for i in range(100):
                j = i + next_random() % (150 - i)
                pool[i], pool[j] = pool[j], pool[i]
            nums.append(pool[:100])
        common = intersection(nums)
        acc = len(common)
        for v in common:
            acc = (acc * 1009 + v) % 1000000007
        check = (check * 31 + acc) % 1000000007
    print(f"20000 cases: checksum {check}")


main()
