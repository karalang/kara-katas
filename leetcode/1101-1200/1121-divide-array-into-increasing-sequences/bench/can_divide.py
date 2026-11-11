# LeetCode #1121: Divide Array Into Increasing Sequences -- the bench's
# Python mirror: the ★ arm over 4 sorted arrays of 100000 values, each
# round copying one value over its neighbour and answering for a new `k`.

seed = 1121


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def can_divide_into_subsequences(nums, k):
    longest = run = 0
    for i in range(len(nums)):
        if i > 0 and nums[i] == nums[i - 1]:
            run += 1
        else:
            run = 1
        if run > longest:
            longest = run
    return longest * k <= len(nums)


def main():
    n = 100000
    arrays = []
    for top in [2000, 1000, 500, 200]:
        arrays.append(sorted(next_random() % top + 1 for _ in range(n)))
    yes = check = 0
    for rnd in range(250):
        for j, nums in enumerate(arrays):
            at = (rnd * 7919 + j * 104729) % (n - 2) + 1
            nums[at] = nums[at + 1] if rnd % 2 == 0 else nums[at - 1]
            k = (rnd * 13 + j * 7) % 2000 + 1
            r = can_divide_into_subsequences(nums, k)
            yes += r
            check = (check * 31 + (1 if r else 2) + k) % 1000000007
    print(f"250 rounds over 4 arrays of 100000 values: {yes} can be divided, checksum {check}")


main()
