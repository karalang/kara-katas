# LeetCode #2057: Smallest Index With Equal Value -- Python mirror of the ★
# arm's benchmark (equal.kara): the same 1000000 arrays drawn into one
# buffer, each answered by walking its indices from the front.

seed = 2057


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def smallest_equal(nums):
    for i in range(len(nums)):
        if i % 10 == nums[i]:
            return i
    return -1


def main():
    nums = []
    found = total = check = 0
    for _ in range(1000000):
        n = next_random() % 100 + 1
        rare = next_random() % 20 + 1
        nums.clear()
        for i in range(n):
            d = next_random() % 10
            nums.append((d + 1) % 10 if d == i % 10 and next_random() % rare != 0 else d)
        at = smallest_equal(nums)
        if at >= 0:
            found += 1
        total += at
        check = (check * 31 + at + 2) % 1000000007
    print(f"1000000 arrays: {found} found, sum {total}, checksum {check}")


main()
