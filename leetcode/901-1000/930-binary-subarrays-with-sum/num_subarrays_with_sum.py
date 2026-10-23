# LeetCode #930: Binary Subarrays With Sum -- prefix sums counted in an
# array (Python mirror).


def num_subarrays_with_sum(nums, goal):
    n = len(nums)
    seen = [0] * (n + 1)
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


def show(nums, goal):
    print(f"[{','.join(str(v) for v in nums)}], goal {goal}: {num_subarrays_with_sum(nums, goal)}")


def main():
    show([1, 0, 1, 0, 1], 2)
    show([0, 0, 0, 0, 0], 0)
    show([1], 1)
    show([0], 1)
    show([1, 1, 1], 0)
    show([1, 0, 1], 3)
    show([1, 1, 1, 1], 2)
    show([0, 1, 0, 0, 1, 0], 0)
    show([0, 0, 1, 1, 0], 2)
    show([0, 1, 0, 1, 0, 1, 0], 3)
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 2000
        lean = 1 + next_random() % 99
        nums = []
        ones = 0
        for _ in range(n):
            v = 1 if next_random() % 100 < lean else 0
            ones += v
            nums.append(v)
        goal = next_random() % (ones + 2)
        a = num_subarrays_with_sum(nums, goal)
        total += a
        check = (check * 1000003 + a) % 1000000007
    print(f"300 random arrays: answers summing to {total}, checksum {check}")
    zeros = [0] * 30000
    ones = [1] * 30000
    alternating = [i % 2 for i in range(30000)]
    a = num_subarrays_with_sum(zeros, 0)
    b = num_subarrays_with_sum(ones, 15000)
    c = num_subarrays_with_sum(alternating, 7500)
    print(f"30000 elements: all 0s {a}, all 1s {b}, alternating {c}")


main()
