# LeetCode #930: Binary Subarrays With Sum -- bench: prefix sums counted
# in an array. Mirrors num_subarrays_with_sum.kara.


def num_subarrays_with_sum(nums, goal):
    seen = [0] * (len(nums) + 1)
    seen[0] = 1
    total = 0
    count = 0
    for v in nums:
        total += v
        if total >= goal:
            count += seen[total - goal]
        seen[total] += 1
    return count


seed = 930


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 100, 100, 30000
    # count arrays of n elements, built once, each leaning from 0 to 1 by
    # a random amount, with a goal from 0 to the number of 1s
    arrays = []
    goals = []
    for _ in range(count):
        lean = 1 + next_random() % 99
        nums = []
        ones = 0
        for _ in range(n):
            v = 1 if next_random() % 100 < lean else 0
            ones += v
            nums.append(v)
        goals.append(next_random() % (ones + 1))
        arrays.append(nums)
    total = 0
    check = 0
    for r in range(rounds):
        # each round visits every array, starting from a different one
        for i in range(count):
            p = (r + i) % count
            a = num_subarrays_with_sum(arrays[p], goals[p])
            total += a
            check = (check * 1000003 + a) % 1000000007
    print(f"{rounds} rounds over {count} arrays of {n}: answers summing to {total}, checksum {check}")


main()
