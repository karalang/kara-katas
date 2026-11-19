# LeetCode #2334: Subarray With Elements Greater Than Varying Threshold --
# the bench, the ★ arm in Python: the nearest smaller element on either
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
        if nums[i] * width > threshold and width > best:
            best = width
    return best


def scrambled(index):
    return index * 2654435761 % 2147483647


def main():
    arrays = [[scrambled(a * 100000 + i) % 1000000000 + 1 for i in range(100000)] for a in range(10)]
    check = 0
    for p in range(5):
        for a in range(10):
            threshold = ((10 * a + p) * 7919 % 1000 + 1) * 1000000
            check = (check * 31 + valid_subarray_size(arrays[a], threshold) + 1) % 1000000007
    print(f"5 passes over 10 arrays of 10^5 values: checksum {check}")


main()
