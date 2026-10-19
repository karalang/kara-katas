# LeetCode 795 -- Number of Subarrays with Bounded Maximum, one pass.
# Python mirror of the ★ arm and its harness.


def num_subarray_bounded_max(nums, left, right):
    too_big = -1
    in_range = -1
    count = 0
    for i, x in enumerate(nums):
        if x > right:
            too_big = i
        elif x >= left:
            in_range = i
        if in_range > too_big:
            count += in_range - too_big
    return count


seed = 795


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums, left, right):
    answer = num_subarray_bounded_max(nums, left, right)
    print(f"nums = [{', '.join(map(str, nums))}], left = {left}, right = {right} -> {answer}")


def main():
    show([2, 1, 4, 3], 2, 3)
    show([2, 9, 2, 5, 6], 2, 8)
    show([5], 5, 5)
    show([1, 1, 1], 2, 3)
    show([3, 3, 3, 3], 0, 1000000000)
    show([0, 1000000000, 0], 1000000000, 1000000000)
    show([7, 1, 7, 1, 7], 7, 7)
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 200
        top = 1 + next_random() % 20
        nums = [next_random() % top for _ in range(n)]
        a = next_random() % top
        b = next_random() % top
        answer = num_subarray_bounded_max(nums, min(a, b), max(a, b))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"300 random cases: {total} subarrays, checksum {check}")


main()
