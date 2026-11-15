# LeetCode #2190: Most Frequent Number Following Key In an Array -- the
# benchmark's Python mirror of follow.kara: counts in a list, the leader
# kept as met.


def most_frequent(nums, key):
    counts = [0] * 1001
    best = 0
    target = -1
    for i in range(1, len(nums)):
        if nums[i - 1] == key:
            x = nums[i]
            counts[x] += 1
            if counts[x] > best:
                best = counts[x]
                target = x
    return target


seed = 2190


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    a = next_random()
    b = next_random()
    return a * 32768 + b


def main():
    row = [next_random() % 100 + 1 for _ in range(1000000)]
    check = 0
    for _ in range(200000):
        start = big_random() % 999001
        key = row[start]
        target = most_frequent(row[start:start + 1000], key)
        check = (check * 31 + target) % 1000000007
    print(f"200000 solves: checksum {check}")


main()
