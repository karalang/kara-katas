# LeetCode #2871: Split Array Into Maximum Number of Subarrays -- the
# bench, as split.kara: 50 arrays of 10^5 values, each answered 10 times
# by the greedy arm.

def max_subarrays(nums):
    parts = 0
    running = -1
    for v in nums:
        running &= v
        if running == 0:
            parts += 1
            running = -1
    return max(parts, 1)


seed = 2871


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 50, 10, 100000
    arrays = []
    for c in range(count):
        if c % 2 == 0:
            arrays.append([wide() % 1000001 for _ in range(n)])
        else:
            arrays.append([(wide() | wide()) % 1000001 for _ in range(n)])
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            parts = max_subarrays(nums)
            total += parts
            check = (check * 31 + parts + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: {total} subarrays, checksum {check}")


main()
