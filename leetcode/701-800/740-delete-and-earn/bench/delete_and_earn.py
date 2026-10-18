# LeetCode #740: Delete and Earn -- house robber over values.
# Benchmark mirror of the Kara star arm: total the points each value is
# worth in a table as long as the largest value, then walk the values
# in order keeping the best total with the last value taken and with
# it left.


def delete_and_earn(nums):
    top = 0
    for x in nums:
        if x > top:
            top = x
    points = []
    for _ in range(top + 1):
        points.append(0)
    for x in nums:
        points[x] += x
    take = 0
    skip = 0
    for v in range(top + 1):
        taken = skip + points[v]
        skip = take if take > skip else skip
        take = taken
    return take if take > skip else skip


def main():
    seed = 740
    n = 20000

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    nums = [1 + next_random() % 10000 for _ in range(n)]
    total = 0
    for _ in range(5000):
        for _ in range(20):
            j = next_random() % n
            nums[j] = 1 + next_random() % 10000
        total += delete_and_earn(nums)
    print(f"5000 rounds of 20000 numbers: {total} points in all")


main()
