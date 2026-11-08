# LeetCode #2016: Maximum Difference Between Increasing Elements -- the ★
# arm's benchmark, a mirror of difference.kara.


def maximum_difference(nums):
    smallest = nums[0]
    best = -1
    for x in nums[1:]:
        if x > smallest:
            best = max(best, x - smallest)
        smallest = min(smallest, x)
    return best


seed = 2016


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for a in range(1000):
        fall = a % 11
        nums = []
        for i in range(10000):
            if i > 0 and next_random() % 10 < fall:
                step = next_random() % 1000
                nums.append(max(nums[i - 1] - step, 1))
            else:
                hi = next_random()
                nums.append((hi * 32768 + next_random()) % 1000000000 + 1)
        arrays.append(nums)
    calls = total = check = 0
    for _ in range(10):
        for nums in arrays:
            answer = maximum_difference(nums)
            calls += 1
            total += answer
            check = (check * 31 + answer + 1) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
