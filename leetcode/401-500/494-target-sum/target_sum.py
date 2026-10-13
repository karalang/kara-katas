# LeetCode #494: Target Sum -- Python mirror of the ★ arm (counting ways
# by running sum); see target_sum.kara.


def find_target_sum_ways(nums, target):
    total = 0
    for x in nums:
        total += x
    if target > total or target < -total:
        return 0
    width = 2 * total + 1
    ways = [0] * width
    ways[total] = 1
    for x in nums:
        nxt = [0] * width
        for s in range(width):
            if ways[s] > 0:
                nxt[s + x] += ways[s]
                nxt[s - x] += ways[s]
        ways = nxt
    return ways[target + total]


def show(name, nums, target):
    print(f"{name}: {nums} to {target} -> {find_target_sum_ways(nums, target)}")


seed = 494


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("example 1", [1, 1, 1, 1, 1], 3)
    show("example 2", [1], 1)
    show("zeros", [0, 0, 0, 1], 1)
    show("out of reach", [2, 3], 6)
    show("wrong parity", [2, 4], 1)
    show("a negative target", [1, 2, 3, 4], -2)
    show("all minus", [5, 5, 5], -15)
    # 300 random arrays of 1 to 14 numbers from 0 to 20, each with a
    # target from -30 to 30.
    count = 300
    total = 0
    reachable = 0
    checksum = 0
    for _ in range(count):
        size = 1 + next_random() % 14
        nums = [next_random() % 21 for _ in range(size)]
        target = next_random() % 61 - 30
        ways = find_target_sum_ways(nums, target)
        total += ways
        if ways > 0:
            reachable += 1
        checksum = (checksum * 31 + ways) % 1000000007
    print(f"{count} random arrays: {reachable} reachable, {total} ways, checksum {checksum}")


main()
