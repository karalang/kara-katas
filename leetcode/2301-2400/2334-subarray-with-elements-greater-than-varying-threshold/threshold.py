# LeetCode #2334: Subarray With Elements Greater Than Varying Threshold --
# the Python mirror of the ★ arm: the nearest smaller element on either
# side from a monotonic stack, and the widest run whose least element
# times its width exceeds the threshold.


def valid_subarray_size(nums, threshold):
    n = len(nums)
    left = [-1] * n
    right = [n] * n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] >= nums[i]:
            right[stack.pop()] = i
        if stack:
            left[i] = stack[-1]
        stack.append(i)
    best = -1
    for i in range(n):
        width = right[i] - left[i] - 1
        if nums[i] * width > threshold:
            best = max(best, width)
    return best


SEED = [2334]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def random_nums(n, top):
    nums = []
    for _ in range(n):
        draw = next_random() * 32768
        draw += next_random()
        nums.append(draw % top + 1)
    return nums


def main():
    print(valid_subarray_size([1, 3, 4, 3, 1], 6))
    print(valid_subarray_size([6, 5, 6, 5, 8], 7))
    print(valid_subarray_size([1, 1, 1], 10))
    print(valid_subarray_size([1000000000], 1000000000))
    print(valid_subarray_size([1000000000], 999999999))
    print(valid_subarray_size(list(range(1, 101)), 2500))
    big = random_nums(2000, 1000000000)
    print(valid_subarray_size(big, 1000000000))
    check = 0
    found = 0
    for _ in range(2000):
        n = next_random() % 12 + 1
        nums = random_nums(n, 20)
        threshold = next_random() % 60 + 1
        size = valid_subarray_size(nums, threshold)
        check = (check * 31 + size + 1) % 1000000007
        if size > 0:
            found += 1
    print(f"2000 cases: checksum {check}, {found} with a size")


main()
