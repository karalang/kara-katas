# Benchmark for #494: Python mirror of the ★ arm (counting ways by running
# sum); see target_sum.kara.


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


def main():
    # 40,000 arrays of 20 numbers from 0 to 50 (the problem's most numbers
    # and at most its largest sum), each with a target from -100 to 100,
    # built once, then each solved once.
    seed = 494

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    targets = []
    for _ in range(40000):
        arrays.append([next_random() % 51 for _ in range(20)])
        targets.append(next_random() % 201 - 100)
    reachable = 0
    checksum = 0
    for k in range(len(arrays)):
        ways = find_target_sum_ways(arrays[k], targets[k])
        if ways > 0:
            reachable += 1
        checksum = (checksum * 31 + ways) % 1000000007
    print(f"40000 arrays of 20: {reachable} reachable, checksum {checksum}")


main()
