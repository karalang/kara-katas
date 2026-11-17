# LeetCode #2229: Check if an Array Is Consecutive -- the mirror of
# consecutive.kara: largest less smallest one less than the count, and a
# set to find a repeat.


def is_consecutive(nums):
    seen = set()
    smallest = nums[0]
    largest = nums[0]
    for x in nums:
        if x in seen:
            return False
        seen.add(x)
        smallest = min(smallest, x)
        largest = max(largest, x)
    return largest - smallest + 1 == len(nums)


seed = 2229


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def shuffled_run(low, n):
    nums = list(range(low, low + n))
    for i in range(n - 1, 0, -1):
        j = wide_random() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


def b(v):
    return "true" if v else "false"


def show(nums):
    print(f"[{', '.join(str(x) for x in nums)}] -> {b(is_consecutive(nums))}")


def main():
    show([1, 3, 4, 2])
    show([1, 3])
    show([3, 5, 4])
    show([7])
    show([2, 2])
    show([0, 100000])
    show([5, 9, 6, 8, 4])
    check = 0
    yes = 0
    for c in range(3000):
        n = next_random() % 20 + 1
        low = wide_random() % (100001 - n)
        nums = shuffled_run(low, n)
        if c % 3 != 0:
            at = next_random() % n
            nums[at] = min(max(low + next_random() % (n + 2) - 1, 0), 100000)
        answer = is_consecutive(nums)
        if answer:
            yes += 1
        check = (check * 31 + (1 if answer else 2)) % 1000000007
    print(f"3000 cases: {yes} consecutive, checksum {check}")
    nums = shuffled_run(0, 100000)
    print(f"10^5 numbers: {b(is_consecutive(nums))}")
    at = wide_random() % 100000
    kept = nums[at]
    nums[at] = 100000
    print(f"10^5 numbers: {b(is_consecutive(nums))}")
    nums[at] = (kept + 1) % 100000
    print(f"10^5 numbers: {b(is_consecutive(nums))}")


main()
