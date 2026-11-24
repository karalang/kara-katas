# LeetCode #1296 bench: the ★ arm over 20 arrays of 16666 runs of 6
# consecutive numbers, shuffled, built once; then 10 passes, each swapping two
# numbers of every array and choosing k from the checksum so far. Python has
# no sorted map; the counts' keys are sorted once per call, as the ★ arm's
# walk visits them.


def is_possible_divide(nums, k):
    if len(nums) % k != 0:
        return False
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    for x in sorted(count):
        sets = count[x]
        if sets == 0:
            continue
        for y in range(x, x + k):
            have = count.get(y, 0)
            if have < sets:
                return False
            count[y] = have - sets
    return True


def main():
    seed = 1296

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide_random():
        a = next_random()
        return a * 32768 + next_random()

    arrays = []
    for a in range(20):
        spread = 10000 if a % 2 == 0 else 1000000000
        nums = []
        for _ in range(16666):
            start = 1 + wide_random() % spread
            nums.extend(start + d for d in range(6))
        n = len(nums)
        for i in range(n):
            j = i + wide_random() % (n - i)
            nums[i], nums[j] = nums[j], nums[i]
        arrays.append(nums)
    check = 0
    for p in range(10):
        for a in range(len(arrays)):
            n = len(arrays[a])
            i = check % n
            j = (check // n) % n
            arrays[a][i], arrays[a][j] = arrays[a][j], arrays[a][i]
            k = 1 + check % 6
            possible = is_possible_divide(arrays[a], k)
            check = (check * 31 + (2 if possible else 1) + p) % 1000000007
    print(f"10 passes over 20 arrays of 99996: checksum {check}")


main()
